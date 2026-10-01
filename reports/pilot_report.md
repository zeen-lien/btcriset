# Phase 3 Pilot — 5 Walk-Forward Windows
> Pilot pipeline passed engineering/runtime checks. Five windows only; no full experiment run.

## 1. Source dataset
Primary raw snapshot: `data/raw/binance_btcusdt_1d.parquet`, Binance BTC/USDT daily. SHA-256 `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0`, matches Phase 2 metadata. Schema read: 13 raw columns; 3,059 rows; `2017-08-17` through `2025-12-31` UTC. No network calls made. Coinbase excluded from this pilot.

## 2. Feature engineering and target
30 causal features; calculations/parameters documented in `reports/feature-audit.md`. Features use data available by t. Target is `ln(Close[t+1]/Close[t])`; independent formula assertion passed. Warm-up NaNs were not imputed; 90 rows dropped (89-row longest lookback plus one target-boundary row). Processed dataset has 2,969 rows. Raw snapshot unchanged.

## 3. Window configuration
| Setting | Value |
|---|---:|
| Train | 730 daily rows |
| Validation | 90 daily rows |
| OOS test | 30 daily rows |
| Step | 30 daily rows |
| Windows run | Exactly 5 |

All splits chronological. No shuffle/random split. Test windows are contiguous, non-overlapping; training ranges overlap. First available window starts after feature warm-up. No full ~73-window run.

## 4–5. Feature selection and K
XGBoost `gain` importance trained on TRAIN only. Candidate K `{10,15,20}` compared by validation RMSE on first window only; selected K=10, then fixed across all five windows to keep subset size and Kuncheva comparable. K choice uses no OOS scores. For forecasting, XGBoost is fit on train+validation with training-selected features, then evaluated once on OOS. Hyperparameters are fixed in script; no OOS tuning. This pilot rule is provisional, not a claim K is optimal.

## 6–8. Selected subsets, stability, errors
| Win | OOS | Selected features (ordered by training Gain) | Jaccard vs prior | Kuncheva vs prior | Naive MAE / RMSE | XGBoost MAE / RMSE |
|---:|---|---|---:|---:|---:|---:|
| 1 | 2020-02-12–2020-03-12 | volume_sma_14, return_14d, low, rolling_std_30, stochastic_k_14, rolling_std_14, ema_30, sma_14, return_7d, bb_width_20 | — | — | 0.043434 / 0.100825 | 0.041432 / 0.098110 |
| 2 | 2020-03-13–2020-04-11 | ema_30, stochastic_k_14, volume_sma_14, rolling_std_30, sma_14, sma_30, return_14d, rsi_14, low, return_1d | 0.5385 | 0.55 | 0.037836 / 0.050512 | 0.055989 / 0.066564 |
| 3 | 2020-04-12–2020-05-11 | ema_30, low, macd_12_26, rolling_std_30, rolling_std_14, ema_7, return_3d, stochastic_k_14, return_14d, sma_90 | 0.3333 | 0.25 | 0.028447 / 0.040741 | 0.028773 / 0.040899 |
| 4 | 2020-05-12–2020-06-10 | rolling_std_14, ema_7, close, rolling_std_30, ema_30, stochastic_d_3, return_1d, macd_12_26, sma_7, sma_90 | 0.4286 | 0.40 | 0.026743 / 0.034584 | 0.025859 / 0.033357 |
| 5 | 2020-06-11–2020-07-10 | rolling_std_30, return_14d, volume_sma_14, volume, sma_30, ema_7, sma_90, bb_percent_b_20, return_7d, macd_12_26 | 0.2500 | 0.10 | 0.012164 / 0.015247 | 0.011378 / 0.015822 |

First window has no preceding subset: metrics correctly undefined. Jaccard: intersection/union. Kuncheva: `(r*N-k*k)/(k*(N-k))`, with same K=10 and pool N=30. Baseline predicts zero return. Errors are unscaled log-return units.

## 9. Exploratory association only
Across four adjacent-window transitions, Spearman rho of Jaccard vs the corresponding next-window OOS errors was `0.80` for each error column (n=4; nominal p=0.20). Kuncheva has identical rank ordering here and same exploratory value. Do not interpret as evidence, final inference, or causality: n is tiny and training/validation windows overlap. Pilot shows a pattern only.

## 10–12. Checks and problems
- Feature unit tests: 3 passed, including target formula, prefix-causality, and known-set stability values.
- Source hash/row count: pass. Retained feature timestamps ascending/unique; finite numeric matrix; feature registry 30/30; no target among features.
- Window counts: each 730/90/30; chronological boundaries; exactly five windows.
- Feature selection fitting only TRAIN; validation only first-window K selection; OOS reserved for scoring.
- No assertion failures after pipeline run. No trading/profit/transaction-cost metrics used.
- Naive baseline is zero-return benchmark; no PatchTST included.

## 13. Unresolved methodological issues
1. Feature formulas (e.g., simple rolling-average RSI, simple-average ATR, OBV initialization) are explicit, but may differ from textbook/vendor variants; lock conventions before full run.
2. Selecting K on first window validation then fixing it is a pilot-only rule. Full experiment needs a prespecified K decision/sensitivity plan before examining broad OOS results.
3. Adjacent windows have overlapping train/validation histories. Statistical inference must account for dependence; five-window correlation is not inferential.
4. Forecast model/parameters are deliberately simple pilot configuration; they are not model-selection conclusions.
5. Window table stores timestamp endpoints for input/target rows; each target at t is realized from close at t+1.

## 14–15. Recommendation and status
**PHASE 3 PILOT STATUS: PASS (pipeline validation only).** Feature generation, target alignment, feature selection, stability metrics, and five-window OOS scoring executed. Recommendation: pipeline is ready for methodological review, not automatic expansion. Resolve the issues above and obtain user instruction before any full experiment. No full experiment started.
