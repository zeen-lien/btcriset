# Feature Selection Frequency — Summary

> Feature-selection result of XGBoost Gain (K=10), counted across experiment
> windows. This is NOT a claim of universal importance — the only meaning is
> **"paling sering terpilih dalam window eksperimen"** (most frequently selected
> across the experiment windows). Source: `reports/feature-selection-frequency.csv`,
> derived from `selected_features` in the source result CSVs.

## Binance (22 windows)

| Rank | Feature | Windows selected | Proportion |
|---|---|---|---|
| 1 | bb_percent_b_20 | 13 | 59.09% |
| 2 | stochastic_d_3 | 11 | 50.00% |
| 3 | bb_width_20 | 10 | 45.45% |
| 3 | ema_30 | 10 | 45.45% |
| 3 | obv | 10 | 45.45% |
| 3 | return_3d | 10 | 45.45% |
| 3 | rolling_std_14 | 10 | 45.45% |
| 3 | stochastic_k_14 | 10 | 45.45% |
| 9 | return_14d | 9 | 40.91% |
| 9 | rsi_14 | 9 | 40.91% |
| 9 | sma_30 | 9 | 40.91% |
| 9 | sma_7 | 9 | 40.91% |
| 9 | sma_90 | 9 | 40.91% |
| 9 | volume | 9 | 40.91% |
| 15 | return_1d | 8 | 36.36% |
| 15 | sma_14 | 8 | 36.36% |
| 17 | macd_12_26 | 7 | 31.82% |
| 17 | macd_signal_9 | 7 | 31.82% |
| 17 | rolling_std_30 | 7 | 31.82% |
| 17 | volume_sma_14 | 7 | 31.82% |
| 21 | atr_14 | 6 | 27.27% |
| 22 | close | 5 | 22.73% |
| 22 | ema_14 | 5 | 22.73% |
| 22 | ema_7 | 5 | 22.73% |
| 22 | macd_hist | 5 | 22.73% |
| 22 | return_7d | 5 | 22.73% |
| 27 | high | 2 | 9.09% |
| 27 | low | 2 | 9.09% |
| 27 | open | 2 | 9.09% |
| 30 | volume_change | 1 | 4.55% |

## Coinbase (31 windows)

| Rank | Feature | Windows selected | Proportion |
|---|---|---|---|
| 1 | bb_percent_b_20 | 23 | 74.19% |
| 2 | ema_14 | 19 | 61.29% |
| 3 | rsi_14 | 18 | 58.06% |
| 4 | obv | 16 | 51.61% |
| 4 | return_14d | 16 | 51.61% |
| 4 | return_3d | 16 | 51.61% |
| 4 | sma_30 | 16 | 51.61% |
| 8 | sma_7 | 12 | 38.71% |
| 8 | sma_90 | 12 | 38.71% |
| 10 | close | 11 | 35.48% |
| 10 | ema_30 | 11 | 35.48% |
| 10 | rolling_std_14 | 11 | 35.48% |
| 13 | atr_14 | 10 | 32.26% |
| 13 | macd_12_26 | 10 | 32.26% |
| 13 | macd_signal_9 | 10 | 32.26% |
| 13 | rolling_std_30 | 10 | 32.26% |
| 13 | sma_14 | 10 | 32.26% |
| 13 | stochastic_k_14 | 10 | 32.26% |
| 13 | volume_sma_14 | 10 | 32.26% |
| 20 | macd_hist | 9 | 29.03% |
| 21 | bb_width_20 | 8 | 25.81% |
| 21 | return_7d | 8 | 25.81% |
| 21 | stochastic_d_3 | 8 | 25.81% |
| 24 | volume | 6 | 19.35% |
| 25 | open | 5 | 16.13% |
| 25 | return_1d | 5 | 16.13% |
| 27 | ema_7 | 4 | 12.90% |
| 28 | volume_change | 3 | 9.68% |
| 29 | low | 2 | 6.45% |
| 30 | high | 1 | 3.23% |

## Notes

- Feature universe = 30 features (`code/experiment_config.py`), identical for both
  datasets. Each window selects exactly K=10.
- Ties in count are shown with the same rank; ranks are by count descending.
- `open`, `high`, `low`, `close`, `volume` are the raw OHLCV features from the
  30-feature pool (the pool is fixed, not curated per dataset).
