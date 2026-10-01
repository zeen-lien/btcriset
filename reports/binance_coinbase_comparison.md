# Binance vs Coinbase — Robustness Comparison

Descriptive cross-exchange comparison. Binance = primary experiment;
Coinbase = robustness validation. **No pooling into a single statistical test.**

## 1. Design (identical, frozen)

| Item | Binance (primary) | Coinbase (robustness) |
|---|---|---|
| Dataset | Binance BTC/USDT daily | Coinbase BTC-USD daily |
| Raw period | 2017-08-17 → 2025-12-31 | 2015-07-20 → 2025-12-31 |
| Raw rows | 3,059 | 3,818 |
| Processed rows | 2,969 | 3,728 |
| Features | 30 | 30 |
| Target | next-day log return | next-day log return |
| K | 10 | 10 |
| Train / Valid / OOS / Step | 730 / 180 / 90 / 90 | 730 / 180 / 90 / 90 |
| Selector | XGBoost Gain | XGBoost Gain |
| Forecaster | XGBoost | XGBoost |
| Stability | Jaccard (prim.), Kuncheva (sec.) | same |
| Error | MAE (prim.), RMSE (sec.) | same |
| Pairing | `J_t → MAE_(t+1)` | `J_t → MAE_(t+1)` |
| Inference | stationary bootstrap B=5000, seed 42 | same |

## 2. Sample size

| Quantity | Binance | Coinbase |
|---|---|---|
| Number of windows | 22 | 31 |
| Number of pairs | 20 | 29 |

Coinbase has a longer history (starts 2015) → more windows and pairs.

## 3. Feature stability (Jaccard)

| Statistic | Binance | Coinbase |
|---|---|---|
| mean Jaccard | 0.368 | 0.390 |
| median Jaccard | — | 0.429 |
| min Jaccard | 0.111 | 0.176 |
| max Jaccard | 0.667 | 0.538 |

Both exchanges show **moderate, comparable** subset stability (mean ≈ 0.37–0.39),
well above the contextual random reference of ≈ 0.20.

## 4. Forecasting error

| Statistic | Binance | Coinbase |
|---|---|---|
| mean XGBoost MAE | 0.0334 | 0.0254 |
| mean naive MAE | 0.0212 | 0.0224 |
| mean XGBoost RMSE | — | 0.0360 |
| mean naive RMSE | — | 0.0323 |

In **both** exchanges XGBoost fails to beat the zero-return naive baseline
(Coinbase: XGBoost better in only 2 of 31 windows). This is a consistent,
reproducible pattern.

## 5. Primary association — `Spearman rho(J_t, MAE_(t+1))`

| Statistic | Binance | Coinbase |
|---|---|---|
| Spearman rho | -0.101 | +0.186 |
| iid reference p (reference only) | 0.671 | 0.334 |
| bootstrap 95% CI | [-0.519, +0.375] | [-0.169, +0.437] |
| CI includes zero? | **Yes** | **Yes** |
| block length | 6.588 | 5.0 |
| B | 5000 | 5000 |
| n pairs | 20 | 29 |

## 6. Qualitative consistency

| Aspect | Finding |
|---|---|
| Primary non-detection | **Consistent** — both CIs include zero |
| Sign of point estimate | Differs (Binance negative, Coinbase positive) |
| Magnitude | Both small (|rho| < 0.2) |
| Effect on significance claim | None — both non-detections |

**Interpretation (prompt §26, outcome A):**
"The primary finding was qualitatively consistent across the two exchange datasets."
Both datasets show **no convincing association** between feature-subset stability
and subsequent OOS error. This does **not** prove universal absence of association.

## 7. Important differences (descriptive only)

- **Sign flip** of the point estimate (small negative → small positive), both
  within the noise band of a wide CI; not evidence of a real effect either way.
- **Coinbase CI is narrower** (n=29 vs n=20) — greater precision, but still
  spans zero.
- **Longer Coinbase history** includes 2015–2017 (pre-Binance period), which the
  Binance sample cannot cover.
- **Error levels** slightly lower on Coinbase (mean MAE 0.025 vs 0.033).

## 8. Prohibited operations (honored)

- No pooling of Binance + Coinbase into one test.
- Coinbase NOT treated as extra independent observations for the Binance test.
- No methodology change made to reconcile the two results.
- Binance primary artifacts left untouched.

## 9. Conclusion

Robustness verdict: **QUALITATIVELY CONSISTENT.** The absence of a detected
association between feature-subset stability and next-window OOS error holds
across both exchange datasets, under an identical frozen methodology.
Language remains conservative: *no association detected in these samples*, not
*proven absence of association*.
