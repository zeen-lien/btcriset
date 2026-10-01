# Master Results Inventory

> Phase: MASTER RESULTS EVIDENCE PACKAGE. All values read from ACTUAL artifacts
> (CSV/JSON/metadata), not from assumptions. No experiment re-run.

## 1. Datasets

| | Primary | Robustness |
|---|---|---|
| Dataset | Binance BTC/USDT daily | Coinbase BTC-USD daily |
| Source | Binance Spot REST `/api/v3/klines` | Coinbase Exchange REST `/products/BTC-USD/candles` |
| Raw rows | 3,059 | 3,818 |
| Raw period | 2017-08-17 → 2025-12-31 | 2015-07-20 → 2025-12-31 |
| Processed rows | 2,969 | 3,728 |
| Processed period | 2017-11-14 → 2025-12-30 | 2015-10-17 → 2025-12-30 |
| Feature count | 30 | 30 |
| Target | ln(Close[t+1]/Close[t]) | ln(Close[t+1]/Close[t]) |

Sources: `data/snapshots/binance_btcusdt_1d_meta.json`,
`data/snapshots/coinbase_btc_usd_86400_meta.json`,
`data/snapshots/binance_btcusdt_daily_features_v1_metadata.json`,
`data/snapshots/coinbase_btcusd_daily_features_v1_metadata.json`,
`reports/experiment_summary.json`, `reports/coinbase_experiment_summary.json`.

## 2. Experiment configuration (frozen)

| Item | Value | Source |
|---|---|---|
| K (selected features) | 10 | `code/experiment_config.py` |
| Train / Validation / OOS / Step | 730 / 180 / 90 / 90 days | `code/experiment_config.py` |
| Selector | XGBoost Gain importance (train-only) | `code/run_experiment.py:64-66` |
| Forecaster | XGBoost (train+validation, scored OOS) | `code/run_experiment.py:76-79` |
| XGBoost params | n_est=120, depth=3, lr=0.05, subsample=1, colsample=1, λ=1, objective=reg:squarederror, n_jobs=1 | `code/experiment_config.py:39-43` |
| Random seed | 42 | `code/experiment_config.py:35` |

## 3. Results scale

| | Binance | Coinbase |
|---|---|---|
| Windows | 22 | 31 |
| Association pairs (C1-corrected) | **21** | **30** |
| Evaluation metrics | MAE, RMSE (XGBoost vs naive zero-return) | MAE, RMSE (XGBoost vs naive zero-return) |
| Association method | Spearman rho + stationary bootstrap 95% CI | Spearman rho + stationary bootstrap 95% CI |
| Bootstrap B | 5000 | 5000 |
| Bootstrap seed | 42 | 42 |
| Block length | 6.643900265687148 | 6.0 = ceil(max(5.024005054490707, 2.8874134966896827)) |
| Block-length rule | single-series auto (Politis–White + Patton) | `ceil(max(b_stability,b_error))` per frozen §15 |

Source: `reports/final-association-c1-corrected.json`,
`reports/stability-summary.csv`, `reports/forecast-error-summary.csv`.

## 4. Artifact locations

**Result source-of-truth:**
- `reports/experiment_results.csv` — Binance per-window (SHA `59e0ffd8…`)
- `reports/experiment_summary.json` — Binance summary
- `reports/coinbase_experiment_results.csv` — Coinbase per-window (SHA `a478cf9c…`)
- `reports/coinbase_experiment_summary.json` — Coinbase summary
- `reports/final-association-c1-corrected.csv` + `.json` — **final association (use this)**

**Full window tables:** `reports/result-table-binance-full.csv`,
`reports/result-table-coinbase-full.csv`

**Feature selection:** `reports/feature-selection-frequency.csv`,
`reports/feature-selection-window-matrix.csv`

**Summaries:** `reports/stability-summary.csv`, `reports/forecast-error-summary.csv`,
`reports/cross-dataset-results-table.csv`

**Pairing evidence:** `reports/final-pairing-evidence.csv`

**Code:** `code/experiment_config.py`, `code/prepare_features.py`,
`code/prepare_coinbase_features.py`, `code/run_experiment.py`,
`code/run_coinbase_robustness.py`, `code/bootstrap_analysis.py`,
`code/apply_c1_pairing_correction.py`, `code/build_evidence_package.py`

**Tests:** `tests/test_prepare_features.py`, `tests/test_experiment.py`,
`tests/test_coinbase_robustness.py`, `tests/test_c1_pairing_correction.py`

**Input data:** `data/raw/*.parquet`, `data/processed/*.parquet`,
`data/snapshots/*.json`

## 5. Column mapping (full tables vs source CSV)

`result-table-*-full.csv` renames source columns; mapping is explicit and lossless:

| Full table column | Source column |
|---|---|
| `window` | `window_id` |
| `pre_oos_start` / `pre_oos_end` | `validation_start` / `validation_end` |
| `jaccard` | `jaccard_to_next` |
| `kuncheva` | `kuncheva_to_next` |
| `mae_xgb` / `rmse_xgb` | `xgboost_mae` / `xgboost_rmse` |
| `mae_naive` / `rmse_naive` | `naive_mae` / `naive_rmse` |

Source-of-truth columns are NOT modified; the mapping is documentation only.
