# Methodology Resolution
> [!tldr] Methodology belum siap eksperimen. Youssefi et al. (2025) explicitly menempatkan temporal stability seleksi fitur lintas horizon dan dampaknya pada model performance sebagai RQ/contribution; ini critical gap risk. Beberapa rules dapat direkomendasikan sementara, tetapi K, validitas gap, dan inferensi tetap perlu keputusan/review. Tidak ada eksperimen dijalankan.

## 1. Research Question

**RQ sementara, butuh persetujuan ulang:** Apakah stabilitas subset fitur yang dipilih pada successive rolling training windows berasosiasi dengan error forecasting pada blok OOS setelah window seleksi tersebut, untuk next-day BTC return?

Ini berbeda dari pertanyaan Youssefi hanya jika unit stabilitas benar-benar successive training windows dan pairing outcome `stability_t` dengan `error_(t+1)` secara eksplisit serta evaluasinya strictly OOS. Jangan mengklaim novelty. Keterangan dan evidence di Gap Risk Assessment.

## 2. Gap Risk Assessment

Youssefi et al. (2025) full text Sections 2–5 diperiksa. Paper:
- RQ2: “What is the temporal stability of selected technical indicators across different prediction horizons, and how does this impact model performance?”
- Mencantumkan sebagai kontribusi insights into temporal stability across cryptocurrencies and prediction horizons.
- Memproses Binance minute OHLCV menjadi daily; BTC/USDT, ETH/USDT, BNB/USDT.
- Membuat >130 indikator; MI, RFE, Random Forest Importance memilih 20 fitur; regresi Huber, SVR, KNN; horizon 1–20 hari; walk-forward; R²/RMSLE.[1]
- Metodologi menjelaskan initial train 2 tahun, validation 6 bulan, step satu bulan, retrain tiap step.
- Sections/method text yang diperiksa **tidak mengoperasionalkan stability** sebagai definisi/rumus overlap antar-feature-subsets successive training windows dan tidak menunjukkan paired test/regression `stability_t` vs error OOS window berikutnya. Mereka menyebut stabilitas lintas horizon, membandingkan kinerja subset berdasarkan horizon. Tidak cukup bukti bahwa stability itu dihitung sebagai Jaccard/metric formal. Terbatas pada teks yang tersedia dan inspectable figures; absence claim dibatasi ke bagian yang diperiksa.[1]

| Aspect | Youssefi 2025 | Our Proposed Study | Same/Different | Evidence |
|---|---|---|---|---|
| Pertanyaan stabilitas | Stabilitas technical indicators terpilih pada prediction horizons dan impact pada model performance | Stabilitas selected subsets antar-successive walk-forward training windows berhubungan dengan error OOS berikutnya | **Overlap kuat pada concept/RQ umbrella; temporal unit berbeda** | Youssefi RQ2 dan contribution, Sections 1–2.[1] |
| Definisi stability | Tidak menemukan definisi matematis atau metrik overlap formal dalam metode/hasil text yang diperiksa; pembahasan berupa stability lintas horizon/feature categories | Jaccard/Kuncheva antara selected sets window t dan t+1 | Berbeda/unclear | Youssefi Sections 2–5, seleksi 20 fitur dan hasil lintas horizon.[1] |
| Unit temporal | Forecast horizons 1–20 hari; walk-forward retraining bulanan juga digunakan untuk forecasting. Tidak dibuktikan subset stability dihitung antar-fold | Successive rolling training windows; pair `stability_t`, `error_(t+1)` | Berbeda menurut unit terukur; bukti detail Youssefi terbatas | Youssefi Sections 3.5; RQ2.[1] |
| Feature selection | MI, RFE, Random Forest Importance; top-20 dari >130 TA features | Selector final belum disetujui; pilot XGBoost Gain, pool 30 | Berbeda | Youssefi Sections 3.2–3.3 dan 4.1.[1] |
| Performance | Per model, asset, forecast horizon; R²/RMSLE | MAE/RMSE untuk tiap OOS block; error jadi observation terkait stability | Tumpang tindih umum; berbeda outcome protocol | Youssefi Sections 3.5–3.6, results.[1] |
| Pairing `stability_t` → next OOS error | Tidak ditemukan eksplisit di reviewed protocol | Core estimand | Berbeda pada desain analisis yang terlihat; absence terbatas | Tidak ada pairing/formula di sections yang diperiksa.[1] |
| OOS alignment | Walk-forward validation dan horizon forecasts, tapi apakah subset stability di satu origin dipasangkan dengan strictly next OOS block tidak dinyatakan | Prediksi held-out 30-hari berikutnya, setelah feature subset diambil | Belum dapat ditentukan untuk paper; proposed design lebih eksplisit | Sections 3.5–3.6.[1] |

**Kesimpulan:** **OVERLAP KUAT** secara konseptual, **berbeda secara metodologis** pada unit (horizon vs successive windows) dan estimand paired-next-window yang diaudit. Ini **CRITICAL RESEARCH RISK**, bukan bukti otomatis gap gugur, tapi RQ semula tidak aman dipertahankan tanpa framing lebih sempit dan full-paper/table/appendix knockout review. Tidak menyebut novelty/first-ever. Karena prior task meminta STOP bila overlap terlalu kuat, tahap eksperimen dihentikan; user review diperlukan untuk mempertahankan, reframing, atau membatalkan topik.

## 3. Target

**Rekomendasi:** next-period log return `ln(Close[t+1]/Close[t])`, provisional. Youssefi memakai/logically motivates log returns tetapi sekaligus menamai tugas price forecasting; bukan target comparative study.[1] Return cocok dengan estimand error atas perubahan harian dan tidak memerlukan level forecast. Beda dari simple return dan direction. Final target/date convention butuh user review setelah RQ risk diputuskan.

## 4. Dataset

**Rekomendasi:** tetap Binance BTC/USDT daily Phase 2 snapshot sebagai source-of-truth. Raw hash `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0`, rows 3,059, period 2017-08-17–2025-12-31. Processed rows 2,969, dates 2017-11-14–2025-12-30 UTC. Ini project decision/provenance, bukan bukti literature terbaik. Coinbase bukan main.

## 5. Feature Pool

30 predictors di `prepare_features.py` tetap candidate registry untuk menjaga pilot traceability, bukan feature pool terkunci. Pool memuat OHLCV levels dan banyak highly correlated deterministic transforms. Literature Youssefi mendukung family TA/selection di BTC daily, bukan daftar/lookback kita.[1] Pilihan pool wajib ditinjau bersama selector; jangan mengubah code source sekarang.

## 6. Feature Definitions

Semua formulas di kode causal trailing. Classification atas implementation sekarang:

| Fitur | Formula/kode kini | Klasifikasi / konsekuensi |
|---|---|---|
| Lagged return k | `ln(Close[t]/Close[t-k])` | Standard log-return definition; parameter k=1,3,7,14 merupakan study choice. |
| RSI(14) | Mean positive/negative close change pada trailing 14, ratio lalu 0–100 | Valid simple-moving-average RSI variant; **bukan Wilder RSI** (yang memakai Wilder smoothing/recursive average). Script tidak menyatakan “Wilder” secara eksplisit. |
| ATR(14) | True range rolling arithmetic mean 14 | Valid SMA-smoothed ATR variant; **bukan Wilder ATR**. |
| MACD | EMA12−EMA26; signal EMA9; `adjust=False`, min periods | Standard parameter family/EMA recursion variant. Initialization/warm-up wajib dinyatakan. |
| Stochastic | 14-bar high/low range; D=3-bar SMA K | Standard %K/%D form; formula/zero-range behavior explicit. |
| SMA/EMA | Trailing mean; pandas ewm span with `adjust=False` | Standard variants; all lookback periods are design constants, not optimal evidence. |
| Bollinger | SMA20 ±2 population SD (`ddof=0`); width/%B | Standard family, population SD explicit. |
| Rolling volatility | Population SD (`ddof=0`) trailing 14/30 of log one-day returns | Valid realized-volatility proxy variant; parameter/ddof explicit. |
| OBV | sign close change × volume, cumulative sum | Standard OBV-like recurrence; reset at dataset start; scale depends on cumulative start. |
| Volume SMA/change | trailing SMA14; simple pct_change 1d | Standard transforms; volume basis (base asset vs quote) from raw Binance schema. |
| Target | `ln(Close[t+1]/Close[t])` | Correct next-bar log-return alignment; not predictor. |

**Recommended definition policy:** retain the current simple-rolling RSI and ATR formulas as named variants for traceability, rather than silently rewrite to Wilder. Label as `RSI-SMA(14)` and `ATR-SMA(14)` in methodology, explicitly say not Wilder. This avoids undocumented convention substitution and needs no experiment/code change. Whether these variants are suitable for question remains **PROVISIONAL/USER REVIEW**. Rolling features create early warm-up NaNs; no imputation; rows dropped. No future interpolation/fill.

## 7. Feature Selector

**RECOMMENDED SELECTOR (provisional):** XGBoost regression feature ranking by **mean Gain per split** (`importance_type='gain'`): sum of objective loss reduction attributed to splits using feature divided by number of splits using it (verify exact XGBoost API/version before final run). Do not confuse with `total_gain`. Fit selector separately within each training window only. Tie break must be deterministic.

Rationale: continuous return target, nonlinear interactions, already reproducible on tree pipeline. Tradeoffs:
- MI: filter, relatively cheap, nonlinear dependence estimator, univariate unless extended; not model-specific and estimates vary with discretization/estimator.
- RFE: wrapper, costly repeated fits and estimator-dependent, but directly optimizes model/metric.
- Random Forest importance: tree embedded selector, BTC/crypto precedent in Youssefi, but correlated-feature importance substitution and impurity bias concerns.
- Permutation: model-agnostic and loss-linked; correlation groups can dilute/redistribute importance; requires validation/permutation loops, more cost; should use training/inner validation in temporal-safe manner.
- SHAP: local additive attribution aggregated to ranking; expensive and attribution under feature dependence can be ambiguous; not feature selection test.
- XGBoost Gain: low additional cost after fit; intuitive split-loss contribution; strongly model/hyperparameter/sample-dependent, correlated transforms swap/split scores; cannot be read as causal/relevance truth.

Youssefi does not use XGBoost Gain; uses MI, RFE, RF importance on BTC daily aggregated features.[1] No verified direct comparison supports Gain as best. Selector choice remains **REQUIRES USER REVIEW**, while Gain stays an operational candidate, not an evidence-proven winner.

## 8. K Rule

**RECOMMENDED K RULE:** use one prespecified fixed K for all successive windows, chosen before examining OOS errors, and document selection budget/rationale independent of pilot results. Do **not** select K=10 from pilot or retune K separately in each fold. No literature/source reviewed supports a particular numeric K for the current 30-feature set. Therefore numeric K remains **NOT SET / REQUIRES USER REVIEW**; do not fabricate value.

Comparison:
1. **Fixed K:** equal-size sets, comparable Jaccard interpretation and required Kuncheva assumptions; introduces choice of K and can omit weak-but-real groups.
2. **Validation-selected K:** legitimate only nested chronologically in each training/validation window, but K may vary by window; can adapt selection to noise, complicate stability and any K=10-from-first-fold is pilot-derived. If K selected globally once from validation, that leaks design choice from one regime and understates uncertainty.
3. **Threshold-based:** variable cardinality determined by gain threshold; score scale changes by fold, so same threshold may not mean same selection strength. Kuncheva not applicable at varying K.
4. **Variable-size/top-p candidates:** can use Jaccard but values reflect both membership and size; use Nogueira/general stability with temporal-resampling adaptation or report cardinality and decomposed overlap. No direct BTC evidence determines rule.

## 9. Temporal Window

**Proposed methodological adaptation (not optimal):** rolling origin, train 730 daily rows, validation 180 rows (~6 months), OOS 30 rows, step 30. This draws training duration and validation duration/monthly step from Youssefi; their 1–20 day horizon does not directly establish a 30-day OOS block. Bysik uses hourly BTC, 27 folds and longer 12-month/3-month/3-month blocks, a different frequency/task.[1][3]

Why candidate: 730 rows retain two years for daily BTC; six-month validation provides more observations for selection than 90 days; 30-day OOS creates an interpretable monthly error series and step=OOS avoids reusing OOS rows as labels in adjacent windows. Successive train sets still overlap strongly; resulting window-level pairs are dependent. Daily dataset (~8.4 years, 2,969 engineered rows) yields about 68 complete windows conditional on exact boundaries (`floor((2969-(730+180+30))/30)+1=68`). Effective independent sample is lower than 68.

This is a **study-specific adaptation** to support monthly successive-window stability, not exact literature match or proven choice. Training duration 730 and OOS/step30 remain **REQUIRES USER REVIEW**; six-month validation has precedent but costs rows/fewer windows. Need decide whether objective is monthly association vs more windows before freeze.

## 10. Stability Metrics

**Primary proposed:** Jaccard on successive fixed-K selected feature sets. Estimand: fraction of unique features common to either of the two adjacent selectors that are in common, `|A∩B|/|A∪B|`. Directly interpretable overlap; not chance corrected; reports set size with each value.

**Secondary proposed:** Kuncheva index, only with same fixed K and same candidate universe N each window: `(r*N-K²)/(K*(N-K))`, r intersection size. Measures overlap above expected random overlap; values become degenerate if K=0 or K=N, must enforce `0<K<N`.

**Nogueira et al. general stability estimator:** chance-corrected selection-frequency estimator with uncertainty/testing across perturbed samples; broader algorithm stability estimand, not identical to adjacent-window overlap. Standard iid resampling inappropriate for temporal market data; a valid time-series perturbation design would require separate methodology work. Do not add automatically.

Given present question about temporal drift rather than re-sampling noise, Jaccard is the closer descriptive estimand; Kuncheva adjusts chance overlap, not temporal dependence. Both require fixed selector universe and fixed K for clean comparison. **PROVISIONAL; user review needed because K unresolved.**

## 11. Forecasting Model

**Recommendation:** do not select PatchTST/iTransformer as primary now. Keep XGBoost as provisional tabular forecaster because 30 engineered OHLCV features and ~3k rows suit tree regression more naturally; this is a study-specific pragmatic recommendation, not direct evidence of superiority. PatchTST is patch-tokenized channel-independent transformer; iTransformer treats variates as tokens. Both have general forecasting benchmark papers, no directly verified evidence here for BTC daily next-day log return at this sample size.[6][33] Neural models add architecture choices and train-only scaling, increase cost/seed variance. Do not train now or change model automatically. User review needed before model lock.

## 12. Baselines

**Primary simple baseline:** zero log-return forecast. Directly aligned to a no-change daily return prediction; not trading strategy or price-persistence model.
**Optional comparator:** train-mean return estimated within each training set, if user wants a drift benchmark; must be selected before OOS and not added post hoc. For a minimal model, retain zero-return baseline only. **PROVISIONAL.**

## 13. Error Metrics

**Primary:** MAE of per-observation OOS next-day log-return errors; estimand is average absolute forecast miss per held-out day, robust-ish relative to square loss but still affected linearly by tails.
**Secondary:** RMSE; square-root mean squared error on same OOS returns, penalizes rare large misses more. Both defined for negative/zero returns. Do not use MAPE. **PROVISIONAL pending user review.**

## 14. Association Analysis

Object: paired series `S_t` (subset stability from selector sets at adjacent origins t-1,t) and `E_(t+1)` (error on OOS block after origin t). Define error block MAE as primary; RMSE secondary.

Pearson estimates linear co-movement, sensitive to tails/outliers and linearity. Spearman estimates monotone rank association, handles scale/nonlinearity but ordinary p-values assume independent pairs. Kendall tau-b is rank concordance, more interpretable for ties/small samples in some settings but still needs dependent-data inference. None imply causality. Predefine one statistic rather than selecting among correlations after looking at outcomes.

Dürre et al. test rank cross-correlations between autocorrelated time series with short-range dependence; it supports that naive Spearman significance is inadequate in principle, but assumptions concern autocorrelated series and do not automatically validate our generated rolling-window pairs, likely trend/regime change, small ~67 pairs, or association between generated stability and next block error. Evidence insufficient to specify null distribution/test and finite-sample calibration for exact design. **STATUS: UNSUPPORTED for inferential p-values at this time.** Descriptive rho + scatter/paired timeline is possible, but full statistical claim must wait.

## 15. Dependence Handling

No block bootstrap default. Do not resample 67 window pairs i.i.d. The exact sampling object could be paired window-level values `(S_t,E_(t+1))`, but overlapping train/validation histories create serial dependence and possible nonstationarity. Resampling raw daily returns and recomputing selector/model/stability/error is computationally a different estimand and costly; resampling window pairs loses dependence if blocks too short. No defensible block length selection rule has been established. Need choose block bootstrap only after define object, dependence diagnostic, block length rule, and stationarity assumptions. Current inference handling: **UNSUPPORTED**. Do not calculate final p-value or CI with default SciPy Spearman.

## 16. Leakage Control

- Feature for day t uses values through t only; all transforms trailing.
- Label is next close log return and never predictor.
- Selector fit on train only; K/forecast hyperparameters must be selected without OOS.
- Validation choices nested chronologically; if forecaster refits on train+validation after selector/K lock, spell out and ensure no validation target reused for final tuning.
- OOS predictions once per frozen configuration.
- Scaler (if neural chosen) fit on train only.
- Freeze snapshot hash/code/environment, test date boundaries, deterministic ties/seeds.
- Existing feature code shows shift(-1), trailing rolling functions, target excluded, raw hash assertion. Do not modify now. Reaudit after decisions.

## 17. Computational Design

No experiment, full walk-forward, PatchTST training, hypothesis test, bootstrap, or runtime benchmark performed. Previous pilot code fit one selector + one forecaster per window; for first window it also fit three K candidates. Counts depend on final model/K tuning. No reliable time/RAM/disk estimate. When a configuration is approved later, estimate from tiny resource benchmark only if separately authorized; no full run without explicit human approval. Source code remains unchanged.

## 18. Final Proposed Configuration

| Component | Proposed Rule | Evidence | Applicability | Confidence | Status |
|---|---|---|---|---|---|
| Research question | Successive-window subset stability paired with next OOS-block error | Youssefi already asks stability across horizons and impact on model performance [1] | Narrower unit/outcome, but close concept overlap | Low | REQUIRES USER REVIEW |
| Gap | Do not claim novelty; narrower paired next-window estimand pending knockout/full review | Youssefi full text; Barak abstract-level; Bysik fold diagnostic [1][3] | Critical risk | Low | REQUIRES USER REVIEW |
| Target | Next-day log return | Crypto precedent [1] + estimand fit | Direct but no target comparison | Medium-low | PROVISIONAL |
| Dataset | Binance BTCUSDT daily Phase2 hash | Project audit | Exact | High provenance | LOCKED |
| Features | Existing 30 causal feature registry, candidate | Youssefi uses >130 TA, selectors [1] | Family-level, not exact pool | Medium-low | PROVISIONAL |
| Feature formulas | Explicit simple rolling RSI/ATR (not Wilder), MACD EMA recursion, Stoch/SMA/EMA/BB/std/OBV as described | Current code plus standard variants | Reproducible, exact choice not literature-optimal | Medium implementation; low rationale | REQUIRES USER REVIEW |
| Selector | XGBoost `gain` mean split loss improvement, train-only | XGBoost definition [10][31]; crypto precedent uses RF importance not XGB gain [1] | Practical but correlated-feature bias/model-specific | Low-medium | REQUIRES USER REVIEW |
| K | Fixed K, same all folds, picked a priori independent of pilot/OOS; numeric K not set | Kuncheva requires equal K; no evidence for exact integer [8] | Enables comparison, unresolved count | Low | REQUIRES USER REVIEW |
| Window | Candidate rolling 730/180/30/30; not optimal | Youssefi 730-ish/180/30-step; Bysik distinct hourly design [1][3] | Daily BTC adaptation, ~68 folds | Low | REQUIRES USER REVIEW |
| Primary stability | Jaccard adjacent selected sets | Definition/interpretability; BTC diagnostic precedent [3] | Chance-unadjusted; depends on K | Medium | PROVISIONAL |
| Secondary stability | Kuncheva fixed same K and universe; otherwise omit | Formal equal-K/N requirement [8] | Chance correction | Medium | PROVISIONAL |
| Forecast model | XGBoost provisional; no PatchTST/iTransformer lock | General transformer benchmarks [6][33] vs small tabular data | pragmatic adaptation, not validated winner | Low-medium | REQUIRES USER REVIEW |
| Baseline | Zero return, optional train mean only if predeclared | Target-matched method principle | Clear baseline | Medium | PROVISIONAL |
| Error primary | MAE | General metric interpretation [11] | Return-unit average miss | Medium | PROVISIONAL |
| Error secondary | RMSE | General metric interpretation [11] | tail-sensitive companion | Medium | PROVISIONAL |
| Association | descriptive Spearman only; no default p-value | Rank association and dependence literature [32][34] | inferential method unresolved | Low | UNSUPPORTED |
| Dependence | no block bootstrap until sampling unit/block rule justified | General stationary bootstrap [13][14], not exact design | Overlapping windows threaten iid inference | Low | UNSUPPORTED |
| Leakage | chronological features/labels, train-only selection/scaler; OOS untouched | Existing code + tests | directly applicable | High principle | PROVISIONAL |

## Stop Decision

**METHODOLOGY NOT READY FOR EXPERIMENT.** Reasons: critical RQ/gap overlap requires user review; numeric K unresolved; exact window rule requires user review; selector and forecast model are provisional; inference and dependence handling unsupported. No final experiment approval requested. No experiment was run.

## Sources
[1] https://www.techscience.com/cmc/v83n2/60595/html
[3] https://arxiv.org/html/2606.00060v1
[6] https://arxiv.org/abs/2211.14730
[8] https://lucykuncheva.co.uk/papers/lkAIA07.pdf
[10] https://doi.org/10.1145/2939672.2939785
[11] https://otexts.com/fpptr/accuracy.html
[13] https://doi.org/10.1214/aos/1176347265
[14] https://doi.org/10.1080/01621459.1994.10476870
[31] https://xgboost.readthedocs.io/en/stable/python/python_api.html
[32] https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
[33] https://arxiv.org/abs/2310.06625
[34] https://doi.org/10.1080/02664763.2022.2137115
