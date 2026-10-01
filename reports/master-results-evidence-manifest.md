# Master Results Evidence Manifest

> SOURCE OF TRUTH index for the Results Analysis stage. Files are split into
> FINAL/USE, SUPPORTING, and OBSOLETE/DO NOT USE. Obsolete files are NOT deleted —
> they are preserved for the audit trail but must not be used for final analysis.

## A. FINAL / USE

**Association (C1-corrected — the only valid association result):**
- `reports/final-association-c1-corrected.json` — final association summary (both datasets)
- `reports/final-association-c1-corrected.csv` — final per-pair association table
- `reports/final-association-summary.md` — human-readable summary
- `reports/final-pairing-evidence.csv` — pairing audit table (J_t ↔ MAE_{t+1})

**Forecasting results (per-window, unchanged):**
- `reports/experiment_results.csv` — Binance per-window source of truth (SHA `59e0ffd8…`)
- `reports/coinbase_experiment_results.csv` — Coinbase per-window source of truth (SHA `a478cf9c…`)

**Full window tables (column-mapped views of the above):**
- `reports/result-table-binance-full.csv`
- `reports/result-table-coinbase-full.csv`

**Feature selection:**
- `reports/feature-selection-frequency.csv`
- `reports/feature-selection-window-matrix.csv`
- `reports/feature-selection-frequency-summary.md`

**Summaries:**
- `reports/stability-summary.csv`
- `reports/forecast-error-summary.csv`
- `reports/cross-dataset-results-table.csv`
- `reports/master-results-inventory.md`

**Metadata / reproducibility:**
- `data/snapshots/binance_btcusdt_1d_meta.json`
- `data/snapshots/coinbase_btc_usd_86400_meta.json`
- `data/snapshots/binance_btcusdt_daily_features_v1_metadata.json`
- `data/snapshots/coinbase_btcusd_daily_features_v1_metadata.json`
- `reports/experiment_summary.json` — Binance summary
- `reports/coinbase_experiment_summary.json` — Coinbase summary
- `reports/final-results-reproducibility.md`

**Guardrail:**
- `reports/results-claim-guardrail.md`

## B. SUPPORTING

- `reports/figure-data-inventory.md`; `reports/figures/*.png`
- `reports/result-audit-inventory.md`, `result-audit-conflicts.md`,
  `forecast-error-audit.md`, `bootstrap-code-audit.md`,
  `cross-dataset-consistency-audit.md`, `reproducibility-result-audit.md`,
  `scientific-evidence-map.md` — prior Result Audit 01 outputs
- `reports/frozen_methodology_manifest.md`, `reproducibility_manifest.md`,
  `phase-c-audit-report.md`, `coinbase_methodology_check.md`,
  `coinbase_audit_report.md`, `coinbase_reproducibility_manifest.md`,
  `binance_coinbase_comparison.md`
- `reports/methodology-*.md`, `feature-audit.md`, `data-retrieval-audit.md`,
  `phase_0_report.md`, `pre_experiment_approval.md`, `pilot_report.md`,
  `pilot_results.csv`
- Code: `code/experiment_config.py`, `code/prepare_features.py`,
  `code/prepare_coinbase_features.py`, `code/run_experiment.py`,
  `code/run_coinbase_robustness.py`, `code/bootstrap_analysis.py`,
  `code/apply_c1_pairing_correction.py`, `code/build_evidence_package.py`,
  `code/generate_figures.py`, `code/generate_coinbase_figures.py`
- Tests: `tests/*.py`

## C. OBSOLETE / DO NOT USE (preserved for audit trail)

**⚠ Association with the WRONG (offset) pairing — DO NOT USE for final analysis:**
- `reports/experiment_summary.json` field `spearman_rho` = −0.10132643745668742,
  `n_pairs` = 20 — computed with the offset pairing
  `(Jaccard(S_{w-1},S_w), MAE_{w+1})`. Use `final-association-c1-corrected.*`
  instead (Binance n=21, rho=−0.20467616041525366).
- `reports/coinbase_experiment_summary.json` field `primary_spearman_rho` =
  0.18592983280648137, `number_of_pairs` = 29 — same offset pairing. Use
  `final-association-c1-corrected.*` instead (Coinbase n=30, rho=0.23851041407750545).
- `reports/stability-error-pairing-audit.csv` — pairs `jaccard_t` with
  `next_window_mae` = MAE_{t+2} (offset). Superseded by `final-pairing-evidence.csv`.
- `reports/scientific-evidence-map.md`, `reports/binance_coinbase_comparison.md`,
  `reports/result-audit-conflicts.md` — may quote the pre-C1 association values;
  read them as history, not as the final numbers.

**Figures (regenerated from the C1-corrected pairing):**
- `reports/figures/stability_vs_error_scatter.png` (Binance, 21 points)
- `reports/figures/coinbase_stability_vs_error_scatter.png` (Coinbase, 30 points)
  Both were regenerated from `final-pairing-evidence.csv` (X = `jaccard_t`,
  Y = `mae_t_plus_1`) on 2026-09-30 01:05. No regression line / new inferential
  claim. Generator: `code/regenerate_c1_scatter.py`.

**Note:** The per-window forecasting columns themselves (`xgboost_mae`, `rmse`,
etc.) in `experiment_results.csv` / `coinbase_experiment_results.csv` are NOT
obsolete — only the association pairing computed from them was wrong. Those CSVs
remain the source of truth for forecasting results.
