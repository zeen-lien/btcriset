# Methodology Freeze Checklist
> [!tldr] **METHODOLOGY NOT READY FOR EXPERIMENT.** Critical research-gap overlap and multiple unresolved/unsupported decisions remain. No experiment performed.

| Check | Status | Evidence / action required |
|---|---|---|
| [ ] Research question aman | REQUIRES USER REVIEW | Youssefi 2025 already asks temporal feature stability across horizons and impact on model performance. Review distinction in `methodology-resolution.md`. |
| [ ] Gap risk selesai | REQUIRES USER REVIEW | Critical overlap risk; no novelty claim. Decide whether to retain/reframe/drop RQ after full near-paper knockout. |
| [x] Target | PROVISIONAL | Next-period log return formula clear; target choice not comparative-literature proven. |
| [ ] Feature pool | PROVISIONAL | Existing 30 are candidates; exact set not justified as a package. |
| [ ] Feature definitions | REQUIRES USER REVIEW | Current RSI/ATR are rolling-mean variants, not Wilder; document and accept or later request change. |
| [ ] Selector | REQUIRES USER REVIEW | XGBoost Gain candidate; no evidence of superiority to MI/RFE/RF/permutation/SHAP. |
| [ ] K | REQUIRES USER REVIEW | Recommend fixed K chosen independently of pilot/OOS; numeric K has no evidence, remains unset. |
| [ ] Window | REQUIRES USER REVIEW | 730/180/30/30 is only adaptation candidate; not optimum; folds depend on final selection. |
| [ ] Stability metric | PROVISIONAL | Jaccard primary descriptive candidate; Kuncheva only equal K and fixed universe; K unresolved. |
| [ ] Forecasting model | REQUIRES USER REVIEW | XGBoost pragmatic candidate; PatchTST/iTransformer not justified directly for this small BTC daily task. |
| [ ] Baseline | PROVISIONAL | Zero-return matches target; decide if train-mean also needed before freeze. |
| [ ] Error metric | PROVISIONAL | MAE primary/RMSE secondary recommended; one primary to freeze. |
| [ ] Association method | UNSUPPORTED | No defensible inferential procedure for exact paired window design. No SciPy default p-value. |
| [ ] Dependence handling | UNSUPPORTED | No resampling object/block length/stationarity rule; block bootstrap not default. |
| [x] Leakage | PROVISIONAL | Code inspection supports trailing features and t+1 label; final end-to-end audit required after config freeze. |
| [ ] Reproducibility | PROVISIONAL | Source hash exists; final config hash, environment, seeds, exact boundaries/log schema not frozen. |

## Decision

At least one item is **REQUIRES USER REVIEW** and two inference items are **UNSUPPORTED**.

**METHODOLOGY NOT READY FOR EXPERIMENT.** Do not request full-experiment approval yet. No full walk-forward, PatchTST training, statistical test, bootstrap, or runtime benchmark was run. Main code unchanged.

See `reports/methodology-resolution.md` for evidence, comparison table, rules, and unresolved decisions.
