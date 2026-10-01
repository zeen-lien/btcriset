"""MASTER RESULTS EVIDENCE PACKAGE — data generators.

Reads ONLY existing source-of-truth artifacts. No experiment re-run, no model fit,
no selection change. Produces summary CSVs for the evidence package.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("D:/Hermes/Projects/riset-btc")
REP = ROOT / "reports"
sys.path.insert(0, str(ROOT / "code"))
from prepare_features import jaccard, kuncheva  # noqa: E402

SRC = {"Binance": REP / "experiment_results.csv", "Coinbase": REP / "coinbase_experiment_results.csv"}
N_FEATURES = 30
K = 10


def load():
    out = {}
    for name, p in SRC.items():
        d = pd.read_csv(p)
        d["sel"] = d["selected_features"].apply(lambda s: set(json.loads(s)))
        out[name] = d
    return out


def transitions(d):
    """Return per-transition J_t = Jaccard(S_t, S_{t+1}), Kuncheva_t, and MAE_{t+1}."""
    rows = []
    N = int(d.window_id.max())
    for t in range(1, N):
        st, st1 = d.loc[d.window_id == t, "sel"].iloc[0], d.loc[d.window_id == t + 1, "sel"].iloc[0]
        J = jaccard(st, st1)
        Kun = kuncheva(st, st1, N_FEATURES)
        mae_next = float(d.loc[d.window_id == t + 1, "xgboost_mae"].iloc[0])
        rmse_next = float(d.loc[d.window_id == t + 1, "xgboost_rmse"].iloc[0])
        rows.append(dict(t=t, jaccard_t=J, kuncheva_t=Kun, mae_t_plus_1=mae_next, rmse_t_plus_1=rmse_next))
    return pd.DataFrame(rows)


def main():
    data = load()

    # ---------- 5. stability-summary.csv ----------
    srows = []
    for name, d in data.items():
        tr = transitions(d)
        J, Kk = tr.jaccard_t, tr.kuncheva_t
        srows.append(dict(dataset=name, n_windows=int(len(d)), n_jaccard_pairs=int(len(tr)),
            mean_jaccard=J.mean(), median_jaccard=J.median(), std_jaccard=J.std(ddof=1),
            min_jaccard=J.min(), max_jaccard=J.max(), q1_jaccard=J.quantile(.25), q3_jaccard=J.quantile(.75),
            mean_kuncheva=Kk.mean(), median_kuncheva=Kk.median(), std_kuncheva=Kk.std(ddof=1),
            min_kuncheva=Kk.min(), max_kuncheva=Kk.max(), q1_kuncheva=Kk.quantile(.25), q3_kuncheva=Kk.quantile(.75)))
    pd.DataFrame(srows).to_csv(REP / "stability-summary.csv", index=False)

    # ---------- 6. forecast-error-summary.csv ----------
    frows = []
    for name, d in data.items():
        xm, xr, nm, nr = d.xgboost_mae, d.xgboost_rmse, d.naive_mae, d.naive_rmse
        frows.append(dict(dataset=name,
            mean_xgb_mae=xm.mean(), median_xgb_mae=xm.median(), std_xgb_mae=xm.std(ddof=1), min_xgb_mae=xm.min(), max_xgb_mae=xm.max(),
            mean_xgb_rmse=xr.mean(), median_xgb_rmse=xr.median(),
            mean_naive_mae=nm.mean(), median_naive_mae=nm.median(),
            mean_naive_rmse=nr.mean(), median_naive_rmse=nr.median(),
            n_windows_xgb_mae_lt_naive=int((xm < nm).sum()),
            n_windows_xgb_mae_gt_naive=int((xm > nm).sum()),
            n_windows_xgb_mae_eq_naive=int((xm == nm).sum())))
    pd.DataFrame(frows).to_csv(REP / "forecast-error-summary.csv", index=False)

    # ---------- 3. feature-selection-window-matrix.csv ----------
    from experiment_config import FEATURE_COLUMNS
    frames = []
    for name, d in data.items():
        m = pd.DataFrame(0, index=d.window_id.astype(int), columns=FEATURE_COLUMNS, dtype=int)
        for r in d.itertuples():
            for f in r.sel:
                m.loc[int(r.window_id), f] = 1
        m.insert(0, "dataset", name)
        m.insert(1, "window_id", m.index)
        m = m.reset_index(drop=True)
        frames.append(m)
    pd.concat(frames, ignore_index=True).to_csv(REP / "feature-selection-window-matrix.csv", index=False)

    # ---------- 8. final-pairing-evidence.csv ----------
    prows = []
    for name, d in data.items():
        N = int(d.window_id.max())
        for t in range(1, N):
            rt = d.loc[d.window_id == t].iloc[0]
            rt1 = d.loc[d.window_id == t + 1].iloc[0]
            prows.append(dict(dataset=name, t=t,
                window_t=int(rt.window_id), window_t_plus_1=int(rt1.window_id),
                jaccard_t=jaccard(rt.sel, rt1.sel), kuncheva_t=kuncheva(rt.sel, rt1.sel, N_FEATURES),
                mae_t_plus_1=float(rt1.xgboost_mae), rmse_t_plus_1=float(rt1.xgboost_rmse),
                oos_start_t_plus_1=rt1.oos_start, oos_end_t_plus_1=rt1.oos_end))
    pd.DataFrame(prows).to_csv(REP / "final-pairing-evidence.csv", index=False)

    # ---------- 10. cross-dataset-results-table.csv ----------
    c1 = {r["dataset"]: r for r in json.loads((REP / "final-association-c1-corrected.json").read_text())}
    crows = []
    for name, d in data.items():
        tr = transitions(d)
        crows.append(dict(dataset=name,
            raw_rows=int(json.loads((ROOT / f"data/snapshots/{'binance_btcusdt_1d' if name=='Binance' else 'coinbase_btc_usd_86400'}_meta.json").read_text())["total_rows"]),
            processed_rows=int(json.loads((ROOT / f"data/snapshots/{'binance_btcusdt_daily_features_v1' if name=='Binance' else 'coinbase_btcusd_daily_features_v1'}_metadata.json").read_text())["row_count"]),
            windows=int(len(d)), pairs=int(len(tr)), feature_count=N_FEATURES, K=K,
            mean_jaccard=tr.jaccard_t.mean(), median_jaccard=tr.jaccard_t.median(),
            mean_kuncheva=tr.kuncheva_t.mean(),
            mean_xgb_mae=d.xgboost_mae.mean(), mean_naive_mae=d.naive_mae.mean(),
            mean_xgb_rmse=d.xgboost_rmse.mean(), mean_naive_rmse=d.naive_rmse.mean(),
            association_rho=c1[name]["spearman_rho"],
            association_ci_lower=c1[name]["bootstrap_ci_lower"],
            association_ci_upper=c1[name]["bootstrap_ci_upper"]))
    pd.DataFrame(crows).to_csv(REP / "cross-dataset-results-table.csv", index=False)

    print("generated: stability-summary.csv, forecast-error-summary.csv,")
    print("           feature-selection-window-matrix.csv, final-pairing-evidence.csv,")
    print("           cross-dataset-results-table.csv")
    for name, d in data.items():
        tr = transitions(d)
        print(f"  {name}: windows={len(d)} pairs(C1)={len(tr)} meanJ={tr.jaccard_t.mean():.6f}")


if __name__ == "__main__":
    main()
