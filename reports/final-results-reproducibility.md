# Final Results Reproducibility

> Hashes and versions for the final results package. No full experiment was re-run
> except where needed to verify artifact hashes (none needed here — hashes taken
> from on-disk artifacts).

## Dataset hashes (SHA-256)

| Artifact | SHA-256 |
|---|---|
| Raw Binance `data/raw/binance_btcusdt_1d.parquet` | `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0` |
| Raw Coinbase `data/raw/coinbase_btc_usd_86400.parquet` | `c5d47d5f5333da8eff6652e661ef523af54990861c7067011173fb283948dc44` |
| Processed Binance `data/processed/binance_btcusdt_daily_features_v1.parquet` | `7ab4dd13aeaec8cb7d15dfdae785e7b638b2e0a9894996557ef25e673de31ce7` |
| Processed Coinbase `data/processed/coinbase_btcusd_daily_features_v1.parquet` | `fbfdd07c1b7296a6f2ee9a1585f2353c434437ead201b42068eacc2f5d2573fd` |

## Config hash

| Artifact | SHA-256 |
|---|---|
| `code/experiment_config.py` | `91d630ce70d71f575a77def5129e391efe5a1c7973928e49fcd61af320d06322` |

## Result hashes

| Artifact | SHA-256 |
|---|---|
| Binance results `reports/experiment_results.csv` | `59e0ffd8b55689c420981f86c39045fdb1f11d8fd114983d9959dd4a94421a5f` |
| Coinbase results `reports/coinbase_experiment_results.csv` | `a478cf9cc819df122f232ad0eb4b4116688fb50af55d1055309e5f484ad9f76a` |

## Corrected association hashes

| Artifact | SHA-256 |
|---|---|
| `reports/final-association-c1-corrected.json` | `d945b079120909d040c08b0b94826d8b0858474ca35bf22317447baae7cd0697` |
| `reports/final-association-c1-corrected.csv` | `fafcf0eae4c6df008401d14dd434085404ebd8d373b53c8a427bc38779e232f0` |
| `code/apply_c1_pairing_correction.py` | `78fe5a258500ddaffe21f4ee1864f9d4b8fe475af05e3ee996de6e521f86724c` |
| `code/build_evidence_package.py` | `d983a9ad884db2bef2ec13c0fd01222544317cb23c3a86b8774aca0e2eba1154` |

## Software versions

| Package | Version |
|---|---|
| Python | 3.14.7 |
| Platform | Windows-11 (10.0.26200) |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| pandas | 3.0.6 |
| scikit-learn | 1.9.1 |
| xgboost | 3.4.1 |
| matplotlib | 3.11.2 |
| pyarrow | 25.0.1 |

## Random seeds / bootstrap config

| Item | Value |
|---|---|
| Global seed | 42 |
| Bootstrap B | 5000 |
| Bootstrap seed | 42 |
| Binance block length | 6.643900265687148 (single-series auto) |
| Coinbase block length | 6.0 = ceil(max(5.024005054490707, 2.8874134966896827)) [§15] |

## Tests

| File | Tests |
|---|---|
| `tests/test_prepare_features.py` | 3 |
| `tests/test_experiment.py` | 5 |
| `tests/test_coinbase_robustness.py` | 12 |
| `tests/test_c1_pairing_correction.py` | 12 |
| `tests/test_evidence_package.py` | 12 |
| **Total** | **44** |

Command: `python -m pytest tests -q` → **44 passed in 2.80s** (status: PASS).

## Notes

- Old result artifacts (`experiment_results.csv`, `coinbase_experiment_results.csv`,
  both summary JSONs) are byte-unchanged and preserved for the audit trail.
- The Binance summary JSON does not store seed/median-Jaccard/RMSE means; these are
  recomputable from the CSV and are included in the evidence CSVs.
- Coinbase feature-metadata JSON contains a `created_utc` field that makes it
  non-byte-stable on re-preparation; the processed parquet is stable.
