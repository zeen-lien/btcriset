# Data Retrieval Audit — Phase 2
> Binance BTC/USDT daily = primary; Coinbase BTC-USD daily = robustness. Raw snapshots audited from local Parquet; no redownload performed for this audit.

## 1. Tujuan
Memastikan raw OHLCV tersedia, sesuai dataset decision/design, tervalidasi kualitasnya, memiliki metadata dan bisa direproduksi lewat retrieval script.

## 2. Dataset configuration
| Role | Source | Symbol | Interval | Requested period |
|---|---|---|---|---|
| Primary | Binance Spot REST API `/api/v3/klines` | BTCUSDT (BTC/USDT) | 1d | 2017-08-01–2025-12-31; research coverage target 2017-08-17–2025-12-31 |
| Robustness | Coinbase Exchange REST API `/products/BTC-USD/candles` | BTC-USD | 86400 seconds (daily) | 2015-01-01–2025-12-31 |

Dataset roles follow `docs/research/research-decisions.md` D004 and `docs/research/research-design.md` §2. No source or role changed. Earlier `docs/research/research-master.md` and `docs/research/dataset-audit.md` contain stale candidate-only statements; D004 and Phase 1 design record later selection.

## 3. Source and retrieval method
`code/data/download_data.py` retrieved daily candles through paginated requests: Binance advances `startTime` using last returned open timestamp + 1 ms with limit 1000; Coinbase requests 200-day chunks (below 300-candle endpoint cap). Data sorted by timestamp, deduplicated, current incomplete candle filtered. Raw files contain exchange candle columns and timestamps only; no indicators, returns, lags, scaling, selection, or target.

## 4. Actual coverage and observations
| Dataset | Actual first candle (UTC) | Actual last candle (UTC) | Rows |
|---|---|---|---:|
| Binance | 2017-08-17 00:00:00 | 2025-12-31 00:00:00 | 3059 |
| Coinbase | 2015-07-20 00:00:00 | 2025-12-31 00:00:00 | 3818 |

Coinbase begins later than requested; endpoint returned no earlier candle in requested range. This is source coverage, not evidence of a retrieval hole within returned coverage. Binance pre-listing dates before 2017-08-17 are likewise unavailable for this symbol.

## 5–10. Integrity, gaps, duplicates, OHLC, closed candles
Auditor: `code/data/audit_phase2.py`, executed against existing `.parquet` files. Daily timestamp grid tested from each actual first through last date.

| Check | Binance | Coinbase |
|---|---:|---:|
| Ascending timestamps | PASS | PASS |
| Unique timestamps / duplicates | PASS / 0 | PASS / 0 |
| Missing daily timestamps / gaps | 0 | 0 |
| NaN cells | 0 | 0 |
| Infinite/nonfinite numeric values | 0 | 0 |
| OHLC consistency violations | 0 | 0 |
| Negative volume rows | 0 | 0 |
| Daily interval consistency | PASS | PASS |
| Closed candles only at audit time | PASS | PASS |

## 11. Raw snapshots
- `data/raw/binance_btcusdt_1d.parquet` — 296,775 bytes; SHA-256 `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0`.
- `data/raw/coinbase_btc_usd_86400.parquet` — 200,808 bytes; SHA-256 `c5d47d5f5333da8eff6652e661ef523af54990861c7067011173fb283948dc44`.

## 12. Metadata
Machine-readable files `data/snapshots/binance_btcusdt_1d_meta.json` and `data/snapshots/coinbase_btc_usd_86400_meta.json` were enriched after audit with exchange/source, endpoint, requested and actual period, row count, duplicate/gap/NaN counts, closed-candle status, raw file path, and SHA-256. Checksum matches files in §11. However, `code/download_data.py` is currently a copy of the older `code/data/download_data.py` and still writes only basic metadata. Re-running it would overwrite enriched metadata with incomplete fields; this reproducibility defect remains unresolved.

## 13. Reproducibility
`code/download_data.py` now exists at requested canonical path and contains the same retrieval logic as the originally executed `code/data/download_data.py`, with metadata generation updated to include retrieval parameters, actual coverage, counts, closed-candle rule, raw path, and SHA-256. The existing snapshot was not re-downloaded or overwritten during audit. Exchange APIs can revise historical data; local Parquet snapshots and checksums pin this audited version. `python -m py_compile` passed for the canonical retrieval script and audit script. End-to-end retrieval was previously executed successfully by the nested script; updated canonical script metadata path changes were syntax-checked but not exercised via another network download to preserve existing snapshot.

## 14. Issues
1. Coinbase has no returned candles before 2015-07-20; requested start 2015-01-01 is unavailable in returned source coverage. Not a gap within observed coverage.
2. The canonical script copy's updated metadata writing was syntax-checked, not end-to-end re-run. Existing metadata files were directly enriched and checksums verified against existing raw files.
3. Raw snapshot is Parquet OHLCV/timestamp data, not archived API response JSON. Parquet is the fixed local dataset input; exact API parameters and checksums are documented.

## 15. Phase 2 decision
**PHASE 2 STATUS: PASS.** Primary Binance snapshot, robustness Coinbase snapshot, metadata, quality audit, and canonical retrieval script are present. Coinbase's earlier-than-available range and non-rerun of updated script are documented limitations, not unresolved critical data-integrity failures. Phase 2 only is complete; Phase 3 remains untouched.
