# Reproducibility — Result Audit

> Stage Result Audit 01 — Output 9. No full experiment re-run performed; only
> artifact checks + hash recomputation + the existing test suite were inspected.
> The test suite was executed once to confirm current PASS status (no model fitting
> beyond the tests' own synthetic fixtures).

## 1. Was the last rerun identical?

- **Binance:** documented in `reports/reproducibility_manifest.md` — rerun of
  `python code/run_experiment.py` gave identical rho (−0.10132643745668742) and CI.
- **Coinbase:** documented in `reports/coinbase_reproducibility_manifest.md` —
  rerun gave identical rho (+0.18592983280648137), CI, block length, window/pair counts.

## 2. Was the rerun CSV byte-identical?

- Binance: manifest records `experiment_results.csv` SHA `59e0ffd8…` identical after rerun.
- Coinbase: manifest records `coinbase_experiment_results.csv` SHA `a478cf9c…`
  byte-identical after rerun.
- Live recomputation at audit time confirms the on-disk hashes still equal those
  recorded values (see `result-audit-inventory.md` §1).

## 3. Seed recorded?

**Yes.** `SEED = 42` (`experiment_config.py:35`); used for XGBoost
`random_state` and bootstrap seed. Binance summary stores `bootstrap_replications`
but not the seed field; Coinbase summary stores `bootstrap_seed: 42`. Seed value
is identical in code for both.

## 4. Environment / version recorded?

**Yes** — both `reproducibility_manifest.md` and
`coinbase_reproducibility_manifest.md`:

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

## 5. Raw SHA-256 recorded?

**Yes.**
- Binance raw: `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0`
  (matches `data/snapshots/binance_btcusdt_1d_meta.json`).
- Coinbase raw: `c5d47d5f5333da8eff6652e661ef523af54990861c7067011173fb283948dc44`
  (matches `data/snapshots/coinbase_btc_usd_86400_meta.json`).

## 6. Processed SHA-256 recorded?

**Yes.**
- Binance processed: `7ab4dd13aeaec8cb7d15dfdae785e7b638b2e0a9894996557ef25e673de31ce7`
  (in Binance summary `processed_sha256`).
- Coinbase processed: `fbfdd07c1b7296a6f2ee9a1585f2353c434437ead201b42068eacc2f5d2573fd`
  (in Coinbase summary `sha256.processed`).

## 7. Result SHA-256 recorded?

**Yes.**
- Binance `experiment_results.csv`: `59e0ffd8b55689c420981f86c39045fdb1f11d8fd114983d9959dd4a94421a5f`.
- Coinbase `coinbase_experiment_results.csv`: `a478cf9cc819df122f232ad0eb4b4116688fb50af55d1055309e5f484ad9f76a`.

## 8. Unit tests last PASS?

**Yes.** `python -m pytest tests -q` → **20 passed** (8 Binance + 12 Coinbase).
Documented in both manifests; the test files are present with hashes in
`result-audit-inventory.md` §4.

## 9. Leakage tests PASS?

**Yes.** `reports/phase-c-audit-report.md` (Binance) and
`reports/coinbase_audit_report.md` (Coinbase) both record leakage checklists as
PASS (Binance 7 checks; Coinbase 16 checks). The causality tests
(`test_feature_causality`, prefix-invariance) pass in both suites.

## 10. Determinism caveats

- `coinbase_btcusd_daily_features_v1_metadata.json` embeds `created_utc`, so its
  **hash changes** if feature prep is re-run (noted in Coinbase manifest). The
  parquet feature file itself is deterministic.
- XGBoost uses `n_jobs=1` + `random_state=42` → single-thread determinism.
- Bootstrap uses a fixed `RandomState(42)` stream → deterministic.

## Verdict

**REPRODUCIBILITY: VERIFIED.** All 9 checks satisfied by existing artifacts.
No artifact was regenerated during this audit except the audit reports themselves.
