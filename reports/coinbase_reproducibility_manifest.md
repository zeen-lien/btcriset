# Coinbase Robustness — Reproducibility Manifest

## Environment

| Component | Version |
|---|---|
| Python | 3.14.7 |
| xgboost | 3.4.1 |
| scikit-learn | 1.9.1 |
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| matplotlib | 3.11.2 |
| pyarrow | 25.0.1 |

## SHA-256 hashes

| Artifact | SHA-256 |
|---|---|
| `data/raw/coinbase_btc_usd_86400.parquet` | `c5d47d5f5333da8eff6652e661ef523af54990861c7067011173fb283948dc44` |
| `data/processed/coinbase_btcusd_daily_features_v1.parquet` | `fbfdd07c1b7296a6f2ee9a1585f2353c434437ead201b42068eacc2f5d2573fd` |
| `data/snapshots/coinbase_btcusd_daily_features_v1_metadata.json` | `c35960463f9b0e3471853041a9c28d25dd987857a320b0d39b5fa2fcb027b4cd` |
| `reports/coinbase_experiment_results.csv` | `a478cf9cc819df122f232ad0eb4b4116688fb50af55d1055309e5f484ad9f76a` |
| `reports/coinbase_experiment_summary.json` | `1e9d03b87f2d1146579dc4d65412d264a3631151c544fa827452d73f20167bb9` |

## Reproducibility verification (rerun from same snapshot)

`python code/run_coinbase_robustness.py` was run twice on the identical frozen
snapshot. Results:

| Quantity | Run 1 | Run 2 | Identical |
|---|---|---|---|
| window count | 31 | 31 | ✅ |
| pair count | 29 | 29 | ✅ |
| selected feature subsets | — | — | ✅ |
| Jaccard values | — | — | ✅ |
| MAE / RMSE | — | — | ✅ |
| Spearman rho | 0.18592983280648137 | 0.18592983280648137 | ✅ |
| bootstrap CI lower | -0.1691804895496767 | -0.1691804895496767 | ✅ |
| bootstrap CI upper | 0.437469352072282 | 0.437469352072282 | ✅ |
| block length | 5.0 | 5.0 | ✅ |
| `coinbase_experiment_results.csv` SHA-256 | `a478cf9c…` | `a478cf9c…` | ✅ (byte-identical) |

**Reproducibility: VERIFIED.** Deterministic given fixed `random_state=42` and `seed=42`.

## Determinism note

- All experiment outputs (CSV, summary statistics) are deterministic and byte-stable.
- `coinbase_btcusd_daily_features_v1_metadata.json` embeds a `created_utc`
  timestamp, so its hash changes if feature preparation is re-run. The parquet
  feature file itself is deterministic (SHA stable).
- No network access was used. The raw snapshot was never re-downloaded or replaced.

## Unit tests

`python -m pytest tests -q` → **20 passed** (8 Binance + 12 Coinbase), including:
target definition, causality, exactly-30-features, K=10, Jaccard/Kuncheva known
sets, window boundaries, OOS non-overlap, `J_t → MAE_(t+1)` pairing, paired
bootstrap resampling, automatic block length ≥ 1, and reproducibility.
