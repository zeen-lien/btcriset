# Log Keputusan Metodologi
> [!tldr] Tidak ada metodologi final dibekukan. Keputusan yang diturunkan di sini provisional sampai full-source review dan human review.

## D-METH-001 — Primary dataset tetap Binance snapshot
**Decision:** Pertahankan Binance BTC/USDT daily snapshot Phase 2 sebagai kandidat primary.
**Evidence:** Audit Phase 2 project mencatat SHA-256 `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0`, 3.059 rows, 2017-08-17–2025-12-31.
**Reason:** Source penelitian sudah ditetapkan, tersedia dan hash-verified.
**Alternative considered:** Coinbase BTC/USD; tidak dipilih untuk main karena beda exchange/quote currency dan perlu analisis terpisah.
**Confidence:** High untuk snapshot provenance; bukan klaim dataset terbaik.
**Status:** LOCKED source-of-truth.

## D-METH-002 — Target next-day log return
**Decision:** `r(t+1)=ln(Close[t+1]/Close[t])` tetap target provisional.
**Evidence:** Youssefi et al. (2025) menyatakan log returns sebagai target di crypto price forecasting, tetapi tidak membandingkan target alternatif.[1]
**Reason:** Selaras dengan continuous forecast-error association dan tidak menguji level nonstationary.
**Alternative considered:** Price level, simple return, direction.
**Why not selected:** Mismatch estimand atau classification; tidak ada head-to-head evidence yang memaksa pilihan.
**Confidence:** Medium-low.
**Status:** PROVISIONAL.

## D-METH-003 — Feature registry dan indicator formulas
**Decision:** Jangan menganggap current 30-feature list final. Buat formula table termasuk smoothing/`ddof`/warm-up.
**Evidence:** BTC daily feature selection paper memakai >130 indikator dan beberapa selector, namun exact list/periods berbeda.[1]
**Reason:** Keluarga fitur relevan; lookbacks exact belum didukung, dan implementasi RSI/ATR current memakai arithmetic rolling mean, bukan Wilder.
**Alternative considered:** Pandas-TA default formulas; simpler OHLCV/return-only registry.
**Why alternative not selected:** Belum dibandingkan; library name saja tidak menetapkan semantics.
**Confidence:** High bahwa formula mesti eksplisit; rendah soal feature set terbaik.
**Status:** REQUIRES DECISION.

## D-METH-004 — Window design
**Decision:** 730/90/30/30 tetap hanya kandidat; jangan freeze dulu.
**Evidence:** Youssefi memakai 2y train/6mo validation/month step; Bysik BTC hourly memakai 12mo train/3mo validation/3mo test/quarterly step.[1][3]
**Reason:** Dua tahun punya precedent, tetapi validation dan OOS berbeda; literature tidak menguji paket desain ini.
**Alternative considered:** 365 train; expanding; 180d validation; 90d OOS.
**Why alternative not selected:** Perlu dikaitkan ke estimand/power, bukan hasil pilot.
**Confidence:** Low-medium.
**Status:** REQUIRES DECISION.

## D-METH-005 — Selector dan feature importance
**Decision:** XGBoost Gain belum terkunci.
**Evidence:** XGBoost Gain merupakan split loss improvement; studi crypto terdekat memakai MI/RFE/Random-Forest importance, bukan XGB Gain.[1][10]
**Reason:** Dapat dipakai sebagai operational selector tetapi importance model-specific dan rentan substitution antarfitur berkorelasi.
**Alternative considered:** MI, RFE, permutation importance, SHAP, rank-based/group selector.
**Why alternative not selected:** Belum ada bukti comparative fit untuk pertanyaan stability↔error.
**Confidence:** Low.
**Status:** REQUIRES DECISION.

## D-METH-006 — Top-K
**Decision:** Jangan freeze K=10. Pilot-selected K tidak menjadi methodology evidence.
**Evidence:** Youssefi memilih 20 pada pool >130 setelah empirical tradeoff studi itu; bukan dukungan K=10 pada pool ini.[1]
**Reason:** K menentukan stability values dan Kuncheva membutuhkan equal K.
**Alternative considered:** Fixed K prespecified independently; nested validation per fold; variable-size set metric.
**Why alternative not selected:** Harus pilih setelah source review dan decision on inference.
**Confidence:** High bahwa pilot rule tidak cukup; low untuk rule pengganti.
**Status:** REQUIRES DECISION.

## D-METH-007 — Stability scores
**Decision:** Jaccard candidate primary descriptive; Kuncheva secondary only if fixed K and fixed N.
**Evidence:** Bysik uses adjacent-fold Jaccard diagnostically; Kuncheva chance correction has fixed-cardinality assumptions.[3][8]
**Reason:** Jaccard easy to interpret; Kuncheva controls expected chance overlap.
**Alternative considered:** Nogueira stability estimator, recurrence profiles, subset-size-aware stability.
**Why alternative not selected:** Needs direct full methods comparison.
**Confidence:** Medium for definitions; low-medium for this estimand.
**Status:** PROVISIONAL.

## D-METH-008 — Forecast model
**Decision:** PatchTST not locked as primary; XGBoost not locked as final forecaster.
**Evidence:** PatchTST evaluated on general long-term benchmarks; no verified direct BTC daily next-day log-return evidence in this audit.[6]
**Reason:** 2.969 daily observations is a small sample for deep architecture; channel-independence needs justification for multivariate engineered covariates.
**Alternative considered:** XGBoost, linear model, other non-neural baseline.
**Why alternative not selected:** Model choice is not research novelty; select for valid comparator and available evidence.
**Confidence:** Low.
**Status:** REQUIRES DECISION.

## D-METH-009 — Baselines and metrics
**Decision:** Keep zero-return, MAE, RMSE as candidates; designate primary error before experiment.
**Evidence:** MAE/RMSE measure different loss behavior and are established forecasting metrics.[11]
**Reason:** Appropriate units for continuous return; together expose tail sensitivity.
**Alternative considered:** Train-mean baseline; MAPE.
**Why alternative not selected:** MAPE ill-suited to negative/zero returns; train mean could be secondary if prespecified.
**Confidence:** Medium.
**Status:** PROVISIONAL.

## D-METH-010 — Association and inference
**Decision:** No inferential statistic frozen; pilot Spearman remains exploratory.
**Evidence:** Spearman is a rank association; block methods preserve some temporal dependence under assumptions, but current window-pair design needs explicit unit and block length.[13][14]
**Reason:** Fold observations are dependent and effective sample size is far below nominal n.
**Alternative considered:** Kendall, Pearson/HAC, block bootstrap, descriptive-only association.
**Why alternative not selected:** Need answer exact estimand/assumptions and assess power first.
**Confidence:** High that iid p-values are unsafe; low for method selection.
**Status:** REQUIRES DECISION.

## D-METH-011 — Leakage and preprocessing
**Decision:** Maintain chronological target/features, train-only selector/scaler, untouched OOS; rerun audit once final pipeline frozen.
**Evidence:** Source code target shift and causal rolling formulas; 3 unit tests reported passed by Phase 3.
**Reason:** Necessary for unbiased OOS measurement.
**Alternative considered:** Fit selector on train+validation; only allowed if prespecified and no target/test leakage after K lock.
**Why alternative not selected:** Pilot currently selects K on validation, then refits forecaster train+validation; final nesting semantics must be explicit.
**Confidence:** Medium-high.
**Status:** PROVISIONAL pending code/config audit.

## D-METH-012 — Narrow research gap
**Decision:** Retire broad “temporal feature stability vs model performance unexplored” claim. Use narrower candidate: successive walk-forward subset stability paired with corresponding future OOS forecast error under dependence-aware inference.
**Evidence:** Youssefi et al. RQ explicitly discusses temporal stability across horizons and impact on model performance; Bysik reports fold Jaccard diagnostic.[1][3]
**Reason:** Closest work reduces novelty; unit/outcome distinction still potentially meaningful but not yet knockout-tested.
**Alternative considered:** Claim first-ever / no prior work.
**Why alternative not selected:** Unsupported and directly contradicted by adjacent work.
**Confidence:** High for narrowing; low that narrow gap survives exhaustive screening.
**Status:** PROVISIONAL, literature knockout required.
