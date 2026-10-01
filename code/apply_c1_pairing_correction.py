"""C1 CORRECTION — pairing index only.

Frozen definition:
    J_t = Jaccard(S_t, S_{t+1})   paired with   MAE_{t+1}

Source-of-truth rows store `jaccard_to_next` on row r as
    jaccard_to_next[r] = Jaccard(S_{r-1}, S_r)      (verified, 0 mismatches)
which equals J_t for t = r-1. The paired MAE_{t+1} is therefore xgboost_mae[r].

=> Correct frozen pairing is SAME-ROW:  (jaccard_to_next[r], xgboost_mae[r]), r = 2..N.

This script does NOT refit any model and does NOT modify any experiment artifact.
It only re-pairs existing per-window values, recomputes Spearman + stationary
bootstrap CI (B=5000, seed=42, frozen block-length rule per dataset), writes new
files, and asserts the pairing is (t -> t+1) and not (t -> t) or (t -> t+2).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path("D:/Hermes/Projects/riset-btc")
sys.path.insert(0, str(ROOT / "code"))
from bootstrap_analysis import automatic_block_length, stationary_bootstrap_pairs  # noqa: E402
from prepare_features import jaccard  # noqa: E402  (frozen Jaccard definition, reused)

SEED = 42
B = 5000
CI = 0.95

DATASETS = {
    "Binance": ROOT / "reports/experiment_results.csv",
    "Coinbase": ROOT / "reports/coinbase_experiment_results.csv",
}


def build_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows with frozen pairing J_t -> MAE_{t+1} (same-row index)."""
    sel = {int(r.window_id): set(json.loads(r.selected_features)) for r in df.itertuples()}
    mae = {int(r.window_id): float(r.xgboost_mae) for r in df.itertuples()}
    rmse = {int(r.window_id): float(r.xgboost_rmse) for r in df.itertuples()}
    stored_jac = {int(r.window_id): float(r.jaccard_to_next) for r in df.itertuples()}
    kun = {int(r.window_id): float(r.kuncheva_to_next) for r in df.itertuples()}

    N = int(df.window_id.max())
    out = []
    for t in range(1, N):                       # J_t exists for t = 1..N-1
        J_t = jaccard(sel[t], sel[t + 1])       # Jaccard(S_t, S_{t+1})  <-- frozen definition
        r = t + 1                               # row that stores Jaccard(S_{t}, S_{t+1})
        assert np.isclose(J_t, stored_jac[r]), (t, J_t, stored_jac[r])
        out.append({
            "t": t,
            "jaccard_J_t": J_t,                 # J_t = Jaccard(S_t, S_{t+1})
            "jaccard_stored_row": r,
            "kuncheva_J_t": kun[r],
            "mae_t_plus_1": mae[t + 1],         # MAE_{t+1}
            "rmse_t_plus_1": rmse[t + 1],
            "mae_t_used_for_negative_test": mae[t],          # NOT used; guard
            "mae_t_plus_2_used_for_negative_test": mae.get(t + 2, np.nan),  # NOT used; guard
        })
    return pd.DataFrame(out)


def association(pairs: pd.DataFrame, dataset: str) -> dict:
    x = pairs["jaccard_J_t"].to_numpy()
    y = pairs["mae_t_plus_1"].to_numpy()
    rho, pval = spearmanr(x, y)

    # Frozen block-length rule per dataset (unchanged):
    if dataset == "Binance":
        # Binance frozen rule = single-series automatic block length on stability series
        b_stab = automatic_block_length(x, random_state=SEED)
        b_err = None
        b_opt = b_stab
        rule = "single-series automatic_block_length(jaccard)"
    else:
        # Coinbase frozen prompt §15: b = ceil(max(b_stability, b_error))
        b_stab = automatic_block_length(x, random_state=SEED)
        b_err = automatic_block_length(y, random_state=SEED)
        b_opt = float(np.ceil(max(b_stab, b_err)))
        rule = "ceil(max(b_stability, b_error)) [§15]"

    boot = stationary_bootstrap_pairs(x, y, b=b_opt, B=B, seed=SEED, ci_level=CI)
    return {
        "dataset": dataset,
        "n_pairs": int(len(pairs)),
        "spearman_rho": float(rho),
        "iid_reference_pvalue": float(pval),
        "bootstrap_ci_lower": boot["ci_lower"],
        "bootstrap_ci_upper": boot["ci_upper"],
        "ci_includes_zero": bool(boot["ci_lower"] <= 0.0 <= boot["ci_upper"]),
        "block_length": float(b_opt),
        "block_length_rule": rule,
        "block_length_stability": float(b_stab),
        "block_length_error": (None if b_err is None else float(b_err)),
        "B": B,
        "seed": SEED,
        "ci_level": CI,
    }


def main() -> None:
    summary_rows = []
    all_pairs = []
    for name, path in DATASETS.items():
        df = pd.read_csv(path)
        pairs = build_pairs(df)

        # ---- HARD ASSERTIONS: pairing must be (t -> t+1), never (t -> t) or (t -> t+2) ----
        sel = {int(r.window_id): set(json.loads(r.selected_features)) for r in df.itertuples()}
        mae = {int(r.window_id): float(r.xgboost_mae) for r in df.itertuples()}
        for row in pairs.itertuples():
            t = int(row.t)
            # y must equal MAE_{t+1}
            assert np.isclose(row.mae_t_plus_1, mae[t + 1]), f"{name} y != MAE_(t+1) at t={t}"
            # x must equal Jaccard(S_t, S_{t+1})
            assert np.isclose(row.jaccard_J_t, jaccard(sel[t], sel[t + 1])), f"{name} x != Jaccard(S_t,S_t+1) at t={t}"
            # explicitly NOT MAE_t and NOT MAE_{t+2}
            if not np.isclose(mae[t], mae[t + 1]):
                assert not np.isclose(row.mae_t_plus_1, mae[t]), f"{name} y == MAE_t at t={t}"
            if t + 2 <= len(df):
                if not np.isclose(mae[t + 2], mae[t + 1]):
                    assert not np.isclose(row.mae_t_plus_1, mae[t + 2]), f"{name} y == MAE_(t+2) at t={t}"

        res = association(pairs, name)
        summary_rows.append(res)

        pairs_out = pairs.copy()
        pairs_out.insert(0, "dataset", name)
        all_pairs.append(pairs_out)
        print(f"[{name}] n_pairs={res['n_pairs']} rho={res['spearman_rho']:.15f} "
              f"CI=[{res['bootstrap_ci_lower']:.6f}, {res['bootstrap_ci_upper']:.6f}] "
              f"b={res['block_length']} B={B} seed={SEED}")

    # ---- Write CSV (per-pair, both datasets) ----
    out_csv = ROOT / "reports/final-association-c1-corrected.csv"
    pd.concat(all_pairs, ignore_index=True).to_csv(out_csv, index=False)

    # ---- Write summary JSON (side artifact, audit trail) ----
    (ROOT / "reports/final-association-c1-corrected.json").write_text(
        json.dumps(summary_rows, indent=2))

    print("WROTE", out_csv)
    return summary_rows


if __name__ == "__main__":
    main()
