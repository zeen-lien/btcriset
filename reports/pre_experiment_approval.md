# PRE-EXPERIMENT APPROVAL REPORT
> [!tldr] **PRE-EXPERIMENT REVIEW REQUIRED.** This document is a proposed configuration and blocker report, not approval. Methodology is not ready to freeze; no full experiment was run.

## 1. Research Objective
Test whether temporal stability of selected predictor subsets across successive walk-forward windows is associated with corresponding out-of-sample forecasting error for Bitcoin.

## 2. Final Research Question
**Proposed, not frozen:** On Binance BTC/USDT daily next-period log-return forecasts, is feature-subset stability between successive training windows associated with the absolute forecasting error on the subsequent OOS blocks?

RQ wording must acknowledge Youssefi et al. (2025), whose RQ already asks temporal stability of selected indicators across horizons and its impact on performance. Our possible distinction is successive-window stability paired with the next OOS error and dependence-aware association, not “first ever.” This narrower gap still requires a one-paper knockout review of Youssefi, Barak & Parvini, and Bysik.[1][3]

## 3. Final Hypothesis
No directional alternative. H1: association differs from zero between prespecified feature-set stability and corresponding OOS error. Null/negative/positive/inconsistent findings remain valid. Hypothesis and inferential method **not locked** until effective sample/power and dependence are addressed.

## 4. Dataset
- Source: Phase 2 local Binance snapshot, `D:/Hermes/Projects/riset-btc/data/raw/binance_btcusdt_1d.parquet`
- Symbol/interval: BTC/USDT, daily
- Period: 2017-08-17 through 2025-12-31
- Raw observations: 3,059
- Processed observations: 2,969 after causal warm-up and target boundary
- Processed dates: 2017-11-14 through 2025-12-30 UTC
- SHA-256: `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0`
- Coinbase: excluded from proposed main run; robustness is separate study requiring approval.

## 5. Target
Candidate `r(t+1)=ln(Close[t+1]/Close[t])`. Youssefi et al. describes log returns, but does not establish target superiority over levels/simple return/direction.[1] Provisional only.

## 6. Feature Pool
Candidate 30 variables in `code/prepare_features.py`: 5 OHLCV, 4 lagged log returns, 21 technical/volume transforms. Exact registry not yet approved; indicators are deterministic correlated transforms.

## 7. Feature Engineering Rules
Trailing calculations, no center/future values, no interpolation or imputation, target `shift(-1)`, drop warm-up/final boundary. Source hash assertion. Formula caveat: current RSI/ATR use simple rolling means rather than Wilder smoothing; MACD uses `ewm(adjust=False)`, Bollinger SD `ddof=0`. Document, verify, then freeze.

## 8. Feature Selection
Candidate selector: XGBoost gain, fitted on training portion only. Not locked. Direct BTC daily study Youssefi uses MI, RFE, Random-Forest importance, not XGBoost Gain.[1] Gain is split-loss statistic, not universal relevance.[10]

## 9. Stability Metric
Jaccard candidate descriptive primary. Kuncheva candidate secondary only if fixed feature universe N and equal subset K. Neither final pending K and estimand decision.[3][8]

## 10. Temporal Window Design
**Candidate only:** rolling 730 training + 90 validation + 30 OOS, step 30 days. Youssefi uses 2-year train/6-month validation/1-month step; Bysik uses 12-month train/3-month validation/test/quarter step at hourly frequency.[1][3] These are precedents, not optimality claims. Final design not locked.

## 11. Forecasting Models
PatchTST candidate in original prompt, not piloted and not justified for 2,969 daily return rows. XGBoost used for pilot and candidate forecast model. Neither is locked. PatchTST evidence is general long-horizon time-series benchmarks, not direct BTC daily return.[6]

## 12. Baselines
Candidate zero-return forecast. Alternative train-only historical-mean return must be considered once and then fixed. No price-persistence mislabeling.

## 13. Evaluation Metrics
MAE and RMSE; one primary outcome must be named. No MAPE for possibly negative/zero return target.[11]

## 14. Statistical Analysis
Candidate Spearman is descriptive/exploratory only. Inference not locked. Window pairs are serially dependent because training histories overlap, even if OOS blocks do not overlap. Block bootstrap/HAC require sampling unit, block length, assumptions, small-sample treatment, and multiplicity procedure.[13][14][16]

## 15. Leakage Prevention
Features available by t only; label t+1. Selector fit on training only. Validation may tune only predeclared choices. OOS never used for model/K/hyperparameter selection. Neural scaler train-only. Re-audit final implementation after configuration freeze.

## 16. Hyperparameters
Pilot XGBoost candidate: 120 trees, depth 3, learning rate .05, `reg_lambda=1`, seed 42, one thread. Not evidence-based or final. PatchTST hyperparameters absent. Final values not frozen.

## 17. Random Seeds
Pilot seed 42. Final seed/count not frozen. Need seed policy before run.

## 18. Number of Experiments
Under old 730/90/30/30 candidate, conditional window count is **71** on 2,969 rows. Not 73. Recompute after design freeze.

## 19. Expected Number of Model Trainings
If retaining exact current pilot algorithm and applying it across 71 windows: 71 selector fits + 3 validation candidate fits once in first window + 71 forecast fits = **145 XGBoost model fits**. This excludes any PatchTST repetitions/tuning, robustness dataset, selector sensitivity, or inference bootstrap. It is an arithmetic count from `run_pilot.py`, not final workload.

## 20. Expected Runtime
**Not reliably estimated yet.** No verified measured end-to-end pilot runtime was retained, and a shell timing attempt failed due bash-vs-PowerShell syntax before running code. Do not extrapolate invented numbers. After model/design choices, benchmark one representative fold and report measured wall time × actual fit count with overhead caveat. No full experiment run.

## 21. CPU/GPU/RAM Requirement
XGBoost code specifies `n_jobs=1`, CPU-capable, and no GPU needed for that path. RAM/disk use not benchmarked. PatchTST needs separate hardware/model benchmark and could use GPU; requirement unknown. Do not promise resource sufficiency.

## 22. Disk Requirement
Not measured. Expected outputs include per-window selected subsets/predictions/errors/logs and configuration; actual size unknown until format and model decision freeze.

## 23. Expected Output Files
Proposed: frozen config JSON+hash; source metadata; per-window feature subsets, validation selection logs, predictions, error metrics, stability series; run manifest, stdout/stderr, timing/environment; analysis/bootstrap outputs; approval/change logs. Names/schema not yet frozen.

## 24. Reproducibility Information
Record snapshot hash, code hash/commit, Python and package versions, OS/CPU/GPU, random seeds, exact window boundaries, selected K and validation scores, model params, start/end timestamps, command/logs. Dataset snapshot remains unchanged.

## 25. Methodology Evidence Summary
| Rule | Evidence | Reason | Confidence |
|---|---|---|---|
| Binance daily snapshot | Phase 2 audit | reproducible source and project decision | High provenance |
| Log-return target | Youssefi 2025 also describes log returns | target matches continuous return-error question | Medium-low |
| Two-year training | Youssefi 2y train; Bysik 1y hourly | precedent only, no optimum comparison | Medium-low |
| 90d validation / 30d OOS | other papers use 3–6mo validation / 1–3mo test | chosen pilot config not directly supported | Low |
| Jaccard | Bysik adjacent-fold diagnostic | direct temporal subset overlap precedent, no error association | Medium |
| Kuncheva | theoretical equal-K index | chance correction if equal subset cardinality | Medium for definition |
| XGBoost Gain/K10 | no direct supporting comparison; K10 pilot-selected | operational option only | Low/insufficient |
| PatchTST | general TS benchmark paper | no verified direct BTC daily returns | Low |
| MAE/RMSE | general forecast metric source | interpretable complementary errors | Medium |
| Block bootstrap/Spearman | general dependent-data/rank methods | correct direction but design unresolved | Low |

## 26. Remaining Risks
1. Closest work (Youssefi 2025) may narrow/defeat broader gap.
2. Small number of temporal windows and dependence may leave no reliable inferential power.
3. Selector/pool changes can mechanically alter stability values.
4. Indicator semantics mismatch textbook defaults unless specified.
5. PatchTST may overfit/poorly fit modest single-asset daily data.
6. Multiple comparisons among metrics/models/features inflate false positives.

## 27. Remaining Uncertainties
Need full source reads: Barak & Parvini, exact Youssefi stability definitions/tables/appendices, Bysik details, WinnowML, Tripathi & Sharma, Peng, iTransformer. Decide exact target, indicators, windows, selector/Gain, K, model, tuning/scaling, primary endpoint, dependence inference, block length, multiplicity, seeds, exact count and runtime.

## 28. Changes From Pilot
| Pilot | Proposed status before final |
|---|---|
| K=10 based on first validation fold | Not carried forward; must be independently justified/prespecified |
| 730/90/30/30 | Candidate only; not locked |
| XGBoost Gain selector | Candidate only; compare rationale with MI/RFE/RFI/permutation methods |
| XGBoost forecaster | Candidate baseline only |
| PatchTST | Not run; not yet approved |
| Spearman p-value with n=4 | Exploratory pilot only; no inferential claim |
| 5 windows | Pilot validation only; not final sample size |
| Approx. 73 windows | Corrected to 71 conditional on old design |
| Coinbase robustness | Excluded from main proposal; separate approval needed |
| Feature formulas | current code uses rolling-mean RSI/ATR and population SD; disclose/decide |

## 29. FINAL PROPOSED CONFIGURATION
**No complete final configuration is approved or defensible yet.** Human-readable provisional candidate: Binance daily snapshot; next-day log return; current 30 causal predictors after formula audit; selector and K not selected; Jaccard candidate / Kuncheva only fixed K; PatchTST not locked; XGBoost/zero-return candidate; MAE+RMSE with one primary; dependence-aware analysis not specified; 730/90/30/30 only candidate. This is intentionally **NOT READY FOR EXPERIMENT**. Resolving outstanding decisions is prerequisite to an approval request, not an invitation to auto-run.

## PRE-EXPERIMENT REVIEW REQUIRED
Methodology audit still has blocking decisions and primary-source review gaps. No full experiment, 71-window run, PatchTST training, final statistical test, or bootstrap was executed. Review reports:
- `reports/methodology-evidence-audit.md`
- `reports/methodology-rule-matrix.md` / `.csv`
- `reports/methodology-evidence-bibliography.md`
- `reports/methodology-decision-log.md`

**Approval gate:** no experiments until blockers closed, configuration frozen and hash recorded, resource/runtime benchmark honestly measured, and user explicitly approves. `oke/lanjut` without clear approval must not start expensive computation.
