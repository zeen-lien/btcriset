# Coinbase Robustness — Methodology Check

Verifies the Coinbase run inherits the **frozen** Binance methodology with **no** changes.
This is an execution/verification artifact, not a design document.

## Frozen parameters (inherited unchanged)

| Item | Frozen value | Coinbase run | Match |
|---|---|---|---|
| Dataset | Coinbase BTC-USD daily (robustness) | Coinbase BTC-USD daily | ✅ |
| Raw period | 2015-07-20 → 2025-12-31 | 2015-07-20 → 2025-12-31 | ✅ |
| Raw rows | 3,818 | 3,818 | ✅ |
| Feature universe | 30 (frozen list) | 30 (identical `build_features`) | ✅ |
| Target | `ln(Close[t+1]/Close[t])` | same | ✅ |
| K | 10 (fixed) | 10 | ✅ |
| Train | 730 | 730 | ✅ |
| Validation | 180 | 180 | ✅ |
| OOS | 90 | 90 | ✅ |
| Step | 90 | 90 | ✅ |
| Selector | XGBoost Gain | XGBoost Gain | ✅ |
| Forecaster | XGBoost | XGBoost | ✅ |
| XGBoost params | pilot-derived fixed configuration | same `XGB_PARAMS` | ✅ |
| Stability | Jaccard (primary), Kuncheva (secondary) | same | ✅ |
| Error | MAE (primary), RMSE (secondary) | same | ✅ |
| Pairing | `J_t → MAE_(t+1)` | same | ✅ |
| Association | Spearman rho | same | ✅ |
| Inference | stationary bootstrap | same | ✅ |
| Bootstrap B | 5000 | 5000 | ✅ |
| Seed | 42 | 42 | ✅ |

## Parameter provenance

- XGBoost configuration is labelled **`pilot-derived fixed reproducibility configuration`**
  (NOT optimal, NOT literature-proven). No tuning was performed.
- Feature formulas reuse the exact `build_features` function from
  `code/prepare_features.py` — no reimplementation, no convention change
  (RSI/ATR remain simple rolling means, Bollinger uses population std, etc.).

## Deliberate deviation (transparent, per frozen prompt §15)

- The Binance primary used a single-series automatic block length.
- The robustness prompt **§15 explicitly requires**:
  `b = ceil(max(b_stability, b_error))` computed from BOTH series.
- Coinbase therefore uses `b = ceil(max(4.677, 2.815)) = 5.0`.
- This is a **rule specified by the frozen robustness prompt itself**, not a
  post-hoc change. It is documented here and in the summary
  (`block_length_rule`). Binance artifacts were NOT modified.

## Conclusion

Methodology inheritance: **VERIFIED — no silent changes.**
