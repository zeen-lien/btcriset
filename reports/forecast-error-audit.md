# Forecasting Error Audit

> Stage Result Audit 01 — Output 6.
> Computed from the FINAL result CSVs only. No model re-run, no ranking as a
> research conclusion. Values are unrounded (full float precision in the CSVs).

Source files:
- Binance: `reports/experiment_results.csv` (SHA `59e0ffd8…`)
- Coinbase: `reports/coinbase_experiment_results.csv` (SHA `a478cf9c…`)

## Binance (22 windows)

| Metric | Mean | Median |
|---|---|---|
| MAE XGBoost (`xgboost_mae`) | 0.03344450115955859 | 0.0234052147… |
| MAE Naive zero-return (`naive_mae`) | 0.021160566910711116 | 0.0191014467… |
| RMSE XGBoost (`xgboost_rmse`) | 0.0442872110… | 0.0312403713… |
| RMSE Naive zero-return (`naive_rmse`) | 0.0296473078… | 0.0278440519… |

| Win/loss (MAE) | Count |
|---|---|
| XGBoost wins (MAE_xgb < MAE_naive) | **0** |
| XGBoost loses (MAE_xgb > MAE_naive) | **22** |
| Ties | 0 |

## Coinbase (31 windows)

| Metric | Mean | Median |
|---|---|---|
| MAE XGBoost | 0.025444939048928958 | 0.0234520438… |
| MAE Naive zero-return | 0.022426800349613408 | 0.0217534696… |
| RMSE XGBoost | 0.03597381036239864 | 0.0332588713… |
| RMSE Naive zero-return | 0.03231068659431041 | 0.0299988506… |

| Win/loss (MAE) | Count |
|---|---|
| XGBoost wins (MAE_xgb < MAE_naive) | **2** |
| XGBoost loses (MAE_xgb > MAE_naive) | **29** |
| Ties | 0 |

Coinbase windows where XGBoost beats naive (from the raw table):
window 4 (2019-01-09→2019-04-08) and window 20 (2022-12-19→2023-03-18).

## Notes

- Naive baseline = zero log-return forecast (`actual - 0.0`), same OOS block.
  Source: `code/run_experiment.py:83-85`, `code/run_coinbase_robustness.py:81-82`.
- **No model ranking is offered as a research conclusion.** The table only
  records which mean is numerically lower on these samples.
- The Binance summary JSON does not store RMSE means/medians; those are computed
  from the CSV columns `xgboost_rmse` / `naive_rmse` here.
