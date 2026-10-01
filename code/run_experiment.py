"""Phase B — full primary experiment.

Frozen: train 730d, validation 180d, OOS 90d, step 90d, K=10 (fixed),
selector = XGBoost Gain, pairing J_t -> MAE_(t+1), stationary bootstrap B=5000 seed=42.
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

ROOT = Path("D:/Hermes/Projects/riset-btc")
sys.path.insert(0, str(ROOT / "code"))

from experiment_config import (  # noqa: E402
    FEATURE_COLUMNS, K, TRAIN_DAYS, VALID_DAYS, OOS_DAYS, STEP_DAYS,
    XGB_PARAMS, SELECTOR_IMPORTANCE, SEED, BOOTSTRAP_B, CONFIDENCE_LEVEL,
    PROCESSED_SNAPSHOT, REPORTS_DIR,
)
from bootstrap_analysis import automatic_block_length, stationary_bootstrap_pairs  # noqa: E402
from prepare_features import jaccard, kuncheva  # noqa: E402


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
    data = pd.read_parquet(PROCESSED_SNAPSHOT).sort_values("date").reset_index(drop=True)
    assert data["date"].is_monotonic_increasing and data["date"].is_unique
    x = data[FEATURE_COLUMNS].astype(float)
    y = data["target"].astype(float)
    assert np.isfinite(x.to_numpy()).all() and np.isfinite(y.to_numpy()).all()

    windows = build_windows(len(data))
    rows = []
    prev_selected = None
    prev_jaccard = np.nan

    for wid, (a, b, c, d) in enumerate(windows, start=1):
        # --- Selector trained on TRAIN only (never sees validation or OOS) ---
        sel = _selector()
        sel.fit(x.iloc[a:b], y.iloc[a:b])
        gains = sel.get_booster().get_score(importance_type="gain")
        ranked = sorted(
            FEATURE_COLUMNS,
            key=lambda f: (-gains.get(f, 0.0), FEATURE_COLUMNS.index(f)),
        )
        selected = ranked[:K]

        # --- Forecaster fit on TRAIN+VALIDATION, scored on OOS only ---
        fc = _forecaster()
        fc.fit(x.iloc[a:c][selected], y.iloc[a:c])
        pred = fc.predict(x.iloc[c:d][selected])
        actual = y.iloc[c:d].to_numpy()
        err = actual - pred
        mae = float(np.mean(np.abs(err)))
        rmse = float(np.sqrt(np.mean(err ** 2)))
        # Naive (zero-return) baseline on the same OOS block
        naive_err = actual - 0.0
        naive_mae = float(np.mean(np.abs(naive_err)))
        naive_rmse = float(np.sqrt(np.mean(naive_err ** 2)))

        # --- Stability vs previous window's subset ---
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
            "n_train": b - a, "n_validation": c - b, "n_oos": d - c,
            "k": K,
            "selected_features": json.dumps(selected),
            # J_t = Jaccard(S_t, S_{t+1}); pairing frozen to MAE_(t+1)
            "jaccard_to_next": jac,
            "kuncheva_to_next": kun,
            "xgboost_mae": mae, "xgboost_rmse": rmse,
            "naive_mae": naive_mae, "naive_rmse": naive_rmse,
            "mae_improvement_vs_naive": naive_mae - mae,
        })

    result = pd.DataFrame(rows)
    REPORTS_DIR_PATH = Path(REPORTS_DIR)
    REPORTS_DIR_PATH.mkdir(parents=True, exist_ok=True)
    out_csv = REPORTS_DIR_PATH / "experiment_results.csv"
    result.to_csv(out_csv, index=False)

    # --- Frozen pairing: J_t paired with MAE_(t+1) ---
    # J_t lives on row t (jaccard_to_next). MAE_(t+1) lives on row t+1 (xgboost_mae).
    # Build aligned series: jaccard_to_next[t] with xgboost_mae[t+1].
    aligned = result.copy()
    aligned["paired_mae_next"] = aligned["xgboost_mae"].shift(-1)
    paired = aligned.dropna(subset=["jaccard_to_next", "paired_mae_next"])
    jx = paired["jaccard_to_next"].to_numpy()
    my = paired["paired_mae_next"].to_numpy()

    rho, pval = spearmanr(jx, my)
    # Stationary bootstrap on the paired series
    b_opt = automatic_block_length(jx, random_state=SEED)
    boot = stationary_bootstrap_pairs(jx, my, b=b_opt, B=BOOTSTRAP_B, seed=SEED,
                                      ci_level=CONFIDENCE_LEVEL)

    summary = {
        "n_windows": int(len(result)),
        "n_pairs": int(len(paired)),
        "pairing": "J_t -> MAE_(t+1)",
        "spearman_rho": float(rho),
        "spearman_p": float(pval),
        "bootstrap_block_length": float(b_opt),
        "bootstrap_replications": BOOTSTRAP_B,
        "bootstrap_mean_corr": boot["bootstrap_mean"],
        "bootstrap_ci_lower": boot["ci_lower"],
        "bootstrap_ci_upper": boot["ci_upper"],
        "confidence_level": CONFIDENCE_LEVEL,
        "mean_xgboost_mae": float(result["xgboost_mae"].mean()),
        "mean_naive_mae": float(result["naive_mae"].mean()),
        "mean_jaccard": float(result["jaccard_to_next"].mean()),
        "min_jaccard": float(result["jaccard_to_next"].min()),
        "max_jaccard": float(result["jaccard_to_next"].max()),
        "processed_rows": int(len(data)),
        "processed_sha256": hashlib.sha256(Path(PROCESSED_SNAPSHOT).read_bytes()).hexdigest(),
    }
    out_json = REPORTS_DIR_PATH / "experiment_summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print("\nWindows (J_t -> MAE_(t+1)):")
    print(paired[["window_id", "jaccard_to_next", "paired_mae_next"]].to_string(index=False))
    print(f"\nCSV={out_csv}\nJSON={out_json}")


if __name__ == "__main__":
    main()
