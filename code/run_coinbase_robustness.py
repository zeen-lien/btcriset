"""Phase B (Robustness) — Coinbase BTC-USD daily.

Frozen methodology inherited UNCHANGED from the Binance primary experiment.
Outputs are separate Coinbase artifacts; Binance artifacts are never touched.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from xgboost import XGBRegressor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from experiment_config import (  # noqa: E402
    FEATURE_COLUMNS, K, TRAIN_DAYS, VALID_DAYS, OOS_DAYS, STEP_DAYS,
    XGB_PARAMS, SELECTOR_IMPORTANCE, SEED, BOOTSTRAP_B, CONFIDENCE_LEVEL, REPORTS_DIR,
)
from bootstrap_analysis import automatic_block_length, stationary_bootstrap_pairs  # noqa: E402
from prepare_features import jaccard, kuncheva  # noqa: E402

PROCESSED = ROOT / "data/processed/coinbase_btcusd_daily_features_v1.parquet"
RAW = ROOT / "data/raw/coinbase_btc_usd_86400.parquet"
META = ROOT / "data/snapshots/coinbase_btcusd_daily_features_v1_metadata.json"


def _selector():
    return XGBRegressor(importance_type=SELECTOR_IMPORTANCE, **XGB_PARAMS)


def _forecaster():
    return XGBRegressor(**XGB_PARAMS)


def build_windows(n_rows: int) -> list[tuple[int, int, int, int]]:
    windows = []
    start = 0
    while start + TRAIN_DAYS + VALID_DAYS + OOS_DAYS <= n_rows:
        a = start
        b = a + TRAIN_DAYS
        c = b + VALID_DAYS
        d = c + OOS_DAYS
        windows.append((a, b, c, d))
        start += STEP_DAYS
    return windows


def main() -> None:
    data = pd.read_parquet(PROCESSED).sort_values("date").reset_index(drop=True)
    assert data["date"].is_monotonic_increasing and data["date"].is_unique
    x = data[FEATURE_COLUMNS].astype(float)
    y = data["target"].astype(float)
    assert np.isfinite(x.to_numpy()).all() and np.isfinite(y.to_numpy()).all()

    windows = build_windows(len(data))
    rows = []
    prev_selected = None

    for wid, (a, b, c, d) in enumerate(windows, start=1):
        # Selector: TRAIN only
        sel = _selector()
        sel.fit(x.iloc[a:b], y.iloc[a:b])
        gains = sel.get_booster().get_score(importance_type="gain")
        ranked = sorted(FEATURE_COLUMNS, key=lambda f: (-gains.get(f, 0.0), FEATURE_COLUMNS.index(f)))
        selected = ranked[:K]

        # Forecaster: TRAIN+VALIDATION -> score OOS only
        fc = _forecaster()
        fc.fit(x.iloc[a:c][selected], y.iloc[a:c])
        pred = fc.predict(x.iloc[c:d][selected])
        actual = y.iloc[c:d].to_numpy()
        err = actual - pred
        mae = float(np.mean(np.abs(err)))
        rmse = float(np.sqrt(np.mean(err ** 2)))
        naive_mae = float(np.mean(np.abs(actual)))
        naive_rmse = float(np.sqrt(np.mean(actual ** 2)))

        if prev_selected is None:
            jac = np.nan
            kun = np.nan
        else:
            jac = jaccard(prev_selected, selected)
            kun = kuncheva(prev_selected, selected, len(FEATURE_COLUMNS))
        prev_selected = selected

        rows.append({
            "window_id": wid,
            "train_start": data.date.iloc[a].date().isoformat(),
            "train_end": data.date.iloc[b - 1].date().isoformat(),
            "validation_start": data.date.iloc[b].date().isoformat(),
            "validation_end": data.date.iloc[c - 1].date().isoformat(),
            "oos_start": data.date.iloc[c].date().isoformat(),
            "oos_end": data.date.iloc[d - 1].date().isoformat(),
            "n_train": b - a, "n_validation": c - b, "n_oos": d - c, "k": K,
            "selected_features": json.dumps(selected),
            "jaccard_to_next": jac, "kuncheva_to_next": kun,
            "xgboost_mae": mae, "xgboost_rmse": rmse,
            "naive_mae": naive_mae, "naive_rmse": naive_rmse,
            "mae_improvement_vs_naive": naive_mae - mae,
        })

    result = pd.DataFrame(rows)
    reports = Path(REPORTS_DIR)
    reports.mkdir(parents=True, exist_ok=True)
    out_csv = reports / "coinbase_experiment_results.csv"
    result.to_csv(out_csv, index=False)

    # Frozen pairing: J_t -> MAE_(t+1)
    aligned = result.copy()
    aligned["paired_mae_next"] = aligned["xgboost_mae"].shift(-1)
    aligned["paired_rmse_next"] = aligned["xgboost_rmse"].shift(-1)
    paired = aligned.dropna(subset=["jaccard_to_next", "paired_mae_next"])
    jx = paired["jaccard_to_next"].to_numpy()
    my = paired["paired_mae_next"].to_numpy()

    rho, pval = spearmanr(jx, my)

    # §15: automatic block length from BOTH series; b = ceil(max(b_stab, b_err))
    b_stab = automatic_block_length(jx, random_state=SEED)
    b_err = automatic_block_length(my, random_state=SEED)
    b_opt = float(np.ceil(max(b_stab, b_err)))
    boot = stationary_bootstrap_pairs(jx, my, b=b_opt, B=BOOTSTRAP_B, seed=SEED,
                                      ci_level=CONFIDENCE_LEVEL)

    # Secondary descriptive associations (labelled secondary)
    sec = {}
    for name, xcol, ycol in [
        ("jaccard_rmse_next", "jaccard_to_next", "paired_rmse_next"),
        ("kuncheva_mae_next", "kuncheva_to_next", "paired_mae_next"),
        ("kuncheva_rmse_next", "kuncheva_to_next", "paired_rmse_next"),
    ]:
        sub = aligned.dropna(subset=[xcol, ycol])
        r, p = spearmanr(sub[xcol].to_numpy(), sub[ycol].to_numpy())
        sec[name] = {"spearman_rho": float(r), "iid_pvalue_reference_only": float(p),
                     "n": int(len(sub))}

    raw_sha = hashlib.sha256(RAW.read_bytes()).hexdigest()
    proc_sha = hashlib.sha256(PROCESSED.read_bytes()).hexdigest()
    meta_sha = hashlib.sha256(META.read_bytes()).hexdigest()
    csv_sha = hashlib.sha256(out_csv.read_bytes()).hexdigest()

    ci_includes_zero = boot["ci_lower"] <= 0 <= boot["ci_upper"]
    primary_conclusion = (
        "No convincing association detected in this sample (95% bootstrap CI includes zero)."
        if ci_includes_zero else
        "Evidence of association detected in this sample (95% bootstrap CI excludes zero)."
    )

    summary = {
        "dataset": "Coinbase BTC-USD daily",
        "period": [data.date.iloc[0].date().isoformat(), data.date.iloc[-1].date().isoformat()],
        "raw_rows": 3818,
        "processed_rows": int(len(data)),
        "feature_count": len(FEATURE_COLUMNS),
        "K": K,
        "train_days": TRAIN_DAYS, "validation_days": VALID_DAYS,
        "oos_days": OOS_DAYS, "step_days": STEP_DAYS,
        "number_of_windows": int(len(result)),
        "number_of_pairs": int(len(paired)),
        "mean_jaccard": float(result["jaccard_to_next"].mean()),
        "median_jaccard": float(result["jaccard_to_next"].median()),
        "min_jaccard": float(result["jaccard_to_next"].min()),
        "max_jaccard": float(result["jaccard_to_next"].max()),
        "mean_xgboost_mae": float(result["xgboost_mae"].mean()),
        "mean_naive_mae": float(result["naive_mae"].mean()),
        "mean_xgboost_rmse": float(result["xgboost_rmse"].mean()),
        "mean_naive_rmse": float(result["naive_rmse"].mean()),
        "primary_spearman_rho": float(rho),
        "iid_reference_pvalue": float(pval),
        "bootstrap_ci_lower": boot["ci_lower"],
        "bootstrap_ci_upper": boot["ci_upper"],
        "bootstrap_B": BOOTSTRAP_B,
        "bootstrap_seed": SEED,
        "block_length": b_opt,
        "block_length_stability": b_stab,
        "block_length_error": b_err,
        "block_length_rule": "ceil(max(b_stability, b_error)) per frozen prompt §15",
        "confidence_level": CONFIDENCE_LEVEL,
        "pairing": "J_t -> MAE_(t+1)",
        "primary_conclusion": primary_conclusion,
        "secondary_associations": sec,
        "sha256": {
            "raw": raw_sha, "processed": proc_sha, "metadata": meta_sha, "result_csv": csv_sha,
        },
    }
    out_json = reports / "coinbase_experiment_summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"\nCSV={out_csv}\nJSON={out_json}")


if __name__ == "__main__":
    main()
