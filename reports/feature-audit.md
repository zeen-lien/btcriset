# Feature Engineering Audit — Phase 3
> Feature pipeline uses pinned Phase 2 Binance snapshot; 30 causal predictors and next-day log-return target.

## Source snapshot
- File: `data/raw/binance_btcusdt_1d.parquet`
- SHA-256: `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0` (matches Phase 2 metadata)
- Schema: `open_time, open, high, low, close, volume, close_time, quote_volume, trades, taker_base, taker_quote, ignore, date`; 3,059 rows; first `2017-08-17T00:00:00Z`, last `2025-12-31T00:00:00Z`.
- Raw input columns passed to feature calculation: date, open, high, low, close, volume. No network access.

## Target
`target[t] = ln(Close[t+1] / Close[t])`. Implemented with `np.log(close.shift(-1)/close)`. Automated assertion compares implementation with independent expected formula to `rtol=1e-12, atol=1e-12`. Final target NaN dropped; no filling. Target excluded from `FEATURE_COLUMNS`.

## Feature registry (30 columns)
| Group | Features | Formula / parameters |
|---|---|---|
| Base | open, high, low, close, volume | Raw OHLCV at t |
| Lagged returns | return_1d/3d/7d/14d | `ln(Close[t]/Close[t-k])` |
| RSI | rsi_14 | Wilder-style not claimed: simple rolling mean gains/losses over 14; 100 - 100/(1+RS) |
| MACD | macd_12_26, macd_signal_9, macd_hist | EMA spans 12,26; signal EMA span 9; adjust=False |
| Stochastic | stochastic_k_14, stochastic_d_3 | 14-day rolling low/high; %K and 3-period rolling mean %D |
| Trend | sma_7/14/30/90, ema_7/14/30 | Trailing SMA; recursive EMA, adjust=False |
| Volatility | atr_14 | True range max(H-L, abs(H-prevClose), abs(L-prevClose)); 14-row simple mean |
| Bollinger | bb_width_20, bb_percent_b_20 | 20-row close mean ±2 population SD; width / mean and %B |
| Return volatility | rolling_std_14/30 | Population SD of close pct-change over trailing rows |
| Volume | obv, volume_sma_14, volume_change | Cumulative sign(close change)*volume; trailing mean 14; pct change |

All `rolling()` calls use default `center=False` and explicit trailing `min_periods`; EWM uses `adjust=False`. No indicator library is used. Deterministic tests compare full-series feature values against truncated-prefix values at a shared time to test causality.

## Warm-up / preprocessing
No imputation, fill, or interpolation. Warm-up NaN counts logged per feature by `prepare_features.py`; longest warm-up is SMA(90), 89 rows. The target boundary creates 1 NaN at final row. Rows with any NaN among 30 input features or target are dropped. Rows before: 3,059; after: 2,969; removed: 90 (warm-up + target boundary). The code records per-column NaN counts in output metadata.

## Assertions and results
- Source SHA-256 + row count match Phase 2 metadata: PASS.
- Timestamp ascending/unique in retained result: PASS.
- Target formula assertion: PASS.
- Target excluded from feature matrix: PASS.
- Prefix/truncation causal comparison: PASS (automated test).
- All final features numeric; all retained numeric values finite: PASS.
- Registry count = output features = 30: PASS.
- Duplicate feature names: none.
- Automated tests: `3 passed`.

**FEATURE ENGINEERING STATUS: PASS.** Feature output: `data/processed/binance_btcusdt_daily_features_v1.parquet`; metadata: `data/snapshots/binance_btcusdt_daily_features_v1_metadata.json`.
