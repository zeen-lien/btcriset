# Frozen Methodology Manifest

| Item | Frozen value | Evidence type | Can change? |
|---|---|---|---|
| Dataset | Binance BTC/USDT daily | Dataset audit | No |
| Target | Next-day log return | Research design | No |
| Features | 30 | Study design | No |
| K | 10 | Literature-supported adaptation | No |
| Train | 730d | Literature-supported adaptation | No |
| Validation | 180d | Literature-supported adaptation | No |
| OOS | 90d | Study-specific adaptation | No |
| Step | 90d | Study-specific adaptation | No |
| Selector | XGBoost Gain | Method design | No |
| Stability | Jaccard | Literature | No |
| Secondary stability | Kuncheva | Literature | No |
| Forecast | XGBoost | Study design | No |
| Primary error | MAE | Metric design | No |
| Secondary error | RMSE | Metric design | No |
| Association | Spearman | Statistical design | No |
| Inference | Stationary bootstrap | Dependence-aware method | No |
| Bootstrap B | 5000 | Reproducibility | No |
| Seed | 42 | Reproducibility | No |
| Pairing | `Jaccard_t → MAE_(t+1)` | Research design | No |

## Execution details
- **Validation Role:** The 180-day validation period is a temporal separation layer and must never contain OOS information. K=10 is NOT selected via validation. Validation is NOT an unrestricted hyperparameter search. The pre-specified early stopping configuration must be documented; otherwise validation is merely a methodological separation layer.
- **XGBoost parameters:** The parameter set (`n_estimators=120`, `max_depth=3`, `learning_rate=0.05`, `subsample=1`, `colsample_bytree=1`, `reg_lambda=1`, `random_state=42`, `n_jobs=1`) is a **pilot-derived fixed reproducibility configuration**, NOT a literature-derived rule. They are not tuned on OOS.
