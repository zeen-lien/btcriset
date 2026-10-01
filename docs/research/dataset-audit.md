# Dataset Audit — BTC/USDT and BTC/USD Daily

## 1. Provenance and Availability
- **Binance BTC/USDT Spot Klines:** REST public API `https://api.binance.com/api/v3/klines`. No API key required for public market data. Documentation explicitly defines 12 fields (Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore).
- **Coinbase BTC-USD Candles:** REST public API `https://api.exchange.coinbase.com/products/BTC-USD/candles`. No API key required for historical public candles. Documentation defines 6 fields (time, low, high, open, close, volume).

## 2. Historical Range and Missingness
- **Binance:** Earliest verified daily candle starts `2017-08-17 04:00:00 UTC` (1502928000000). Total daily candles to Dec 31, 2025: ~3050+. 1000-candle sample tested: strictly ascending, 0 gaps, 0 missing.
- **Coinbase:** Testing 2016-2018 monthly bounds yields 32 candles per month (daily aggregation includes boundary logic). Confirmed available back to at least `2015-01-01`.

## 3. Timestamp Integrity and Closed-Candle Validation
- **Binance:** `open_time` and `close_time` are explicit milliseconds since epoch. Current running candle is included in response (close_time > serverTime). *Rule:* Must drop the final candle if `close_time` is strictly greater than retrieval time to prevent forward-looking data.
- **Coinbase:** `time` is seconds since epoch for the bucket start. Current running bucket included. *Rule:* Same closed-candle logic required.

## 4. Derived-Feature Audit and Leakage Control
- **Raw fields:** OHLCV (Open, High, Low, Close, Volume). Causal rule: safe to use.
- **Log Returns:** Calculated as `ln(Close_t / Close_{t-1})`. Alignment must ensure `Close_t` is not used to predict `Target_t`. If predicting next-day return, `Target_{t+1}` is `ln(Close_{t+1} / Close_t)`.
- **Rolling Statistics (SMA, EMA, RSI, MACD, Bollinger, ATR):** Must be calculated using trailing windows (e.g., `rolling(window).mean()`). No `center=True` or forward-looking imputation is allowed.

## 5. Duplicates and Distribution Audit
- **Binance:** 1000-candle test: 0 duplicates on `open_time`. OHLC logic validated (High $\ge$ Open, Close, Low; Low $\le$ Open, Close, High); 0 violations in sample.
- **Coinbase:** Chunk-boundary overlap handling required to prevent duplicates when pulling full history via pagination.

## 6. Differences Between Sources
- **Quote currency:** Binance is USDT (Tether, stablecoin with own slight peg variances); Coinbase is pure USD fiat.
- **Volume definition:** Binance separates base asset volume, quote asset volume, and taker/maker volumes. Coinbase provides one base asset volume field.
- **Market structure:** Binance has zero-fee trading promotions periodically which can distort volume series artificially; Coinbase volume is generally fee-bearing retail/institutional.

## 7. Reproducibility Test
- **Binance:** Pagination `startTime` works predictably. However, historical data can theoretically be revised by exchange.
- **Coinbase:** Start/end parameter parsing requires ISO-8601 strings and max 300 data points per request.
- **Reproducibility measure:** Must save raw JSON/CSV locally alongside a `metadata.json` indicating retrieval date, exact endpoint, and parameters. The research must run off the saved local snapshot, not live pulls.

## 8. Dataset Verdict
- **Primary:** Binance BTC/USDT Daily. Fits temporal multi-variable prediction requirement, has volume, is reproducible via explicit script, and provides longest clean un-aggregated stream for USDT trading pair (industry dominant).
- **Robustness:** Coinbase BTC-USD Daily. Will be used to ensure the stability-error relationship is not an artifact of Binance's USDT market structure.
- **Gate Status:** PASS. Both datasets meet reproducibility and leakage-safety requirements given the closed-candle drop rule and local raw snapshot.
