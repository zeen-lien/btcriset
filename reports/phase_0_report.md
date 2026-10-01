# PHASE 0 — RESEARCH VALIDATION REPORT
> **Date:** 2026-09-29 | **Status:** PASSED (Proceed to Phase 1)

## A. Previous Assumptions
| Assumption | Status | Reason |
|---|---|---|
| Domain is Bitcoin forecasting | **LOCKED** | Protocol v2.0 direction |
| Target is next-day direction | **REJECTED** | Must be evaluated vs returns |
| Features are OHLCV + TIs | **PROVISIONAL** | Causal rule required |
| Walk-forward evaluation | **LOCKED** | Required for temporal safety |
| Model is PatchTST/iTransformer | **PROVISIONAL** | Depends on complexity needs vs XGBoost |
| Contribution is WF+cost+naive | **REJECTED** | Bysika 2026 explicitly killed this |

## B. New Evidence
| Reference | Finding | Impact |
|---|---|---|
| Bysika 2026 (Full-text deep audit) | Jaccard used as Appendix B.2 diagnostic (mean 0.673). NEVER correlated with OOS error. Hourly, Binance only. | **Secures our core gap.** |
| Barak 2023 | Dynamic transfer-entropy feature selection on BTC. | Kills dynamic-FS novelty; preserves stability↔error gap. |
| Youssefi 2025 | Walk-forward feature selection on crypto (1-20 days). | Kills FS+WF novelty; preserves stability↔error gap. |
| Elmakias 2026 | Feature stability vs predictive performance (resampling). | Methodological foundation; kills "no one ever connected stability to performance" claim outside our domain. |

## C. Gap Status
**SURVIVES.** The specific analytical evaluation of temporal feature-subset stability and its explicit relationship to OOS forecasting error across chronological windows in Bitcoin forecasting has adversarially survived 12 targeted literature searches. Existing literature uses stability as a side-diagnostic (Bysika) or in non-temporal/non-financial contexts (Elmakias).

## D. Closest Prior Work
- **Bysik & Ślepaczuk (2026):** Identical structure (BTC, walk-forward, training-only feature selection, OOS evaluation) but evaluates executed trading profitability and uses Jaccard solely to report that features change across folds. It does not answer if those changes correspond to worse/better forecasting performance.

## E. Dataset Status
- **Binance BTC/USDT Daily:** PROVISIONALLY LOCKED (Primary). 3330+ obs, 12-field, reproducible.
- **Coinbase BTC/USD Daily:** PROVISIONALLY LOCKED (Robustness).
- *Both require raw JSON snapshotting and strict closed-candle rules.*

## F. Target Status
- PROVISIONALLY LOCKED: Next-period log return $r(t+1) = \ln(Close_{t+1}/Close_t)$.

## G. Timeframe Status
- PROVISIONALLY LOCKED: Daily. Supported by dataset volume and computationally feasible for repeated training.

## H. Feature Status
- PROVISIONAL: Raw OHLCV + causality-safe lagging technical indicators (SMA, EMA, RSI, MACD, Bollinger, ATR, OBV). Exact number TBD.

## I. Model Status
- PROVISIONAL: XGBoost (baseline/selector) + PatchTST (primary). Baseline Naive (persistence) required.

## J. Leakage Risks
- **HIGH:** Rolling calculations of indicators must strictly use `t` and backwards. Target definition must be strictly $t+1$. Scaler must fit only on train.

## K. Statistical Risks
- **HIGH:** Window overlap causes serial correlation in OOS error. Standard Pearson may be invalid without correction. Non-parametric rank correlation (Spearman) + block-bootstrap required.

## L. Required Decisions
- [ ] Determine K for top-K feature selection (requires sensitivity pilot).
- [ ] Determine window length (train/val/OOS) based on ~3300 data points.
- [ ] Finalize stability metric formula (Jaccard + Kuncheva).

## M. Recommended Research Design
1. Retrieve and snapshot Binance BTC/USDT daily data.
2. Generate causal features -> `dataset_v1.parquet`.
3. Configure expanding or rolling windows.
4. Per window: Fit XGBoost selector -> Record $S_t$ -> Calculate Jaccard vs $S_{t-1}$.
5. Fit Forecaster -> Predict OOS -> Record MAE/RMSE.
6. Analyze trajectory of Stability vs Error using Spearman rank correlation.
7. Re-run on Coinbase for robustness.

## N. Confidence
**HIGH.** The research is tightly scoped, data is available, and the gap has withstood direct adversarial scrutiny. We are clear to proceed to Phase 1 (Research Design).
