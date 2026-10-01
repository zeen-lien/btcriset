# Nearest Prior Work Analysis

## 1. Bysik & Ślepaczuk (2026) — arXiv:2606.00060v1
**What they did:**
Evaluated ML-based Bitcoin trading hourly using 70k obs in 2018–2026. 27-fold walk-forward framework using XGBoost, LSTM, iTransformer. Evaluated cost-aware trading filters (10bps cost). Diagnostic Jaccard subset similarity between adjacent folds (Appendix B.2, Table B.23) for selected TA feature sets.

**What we would do:**
Evaluate relationship between temporal feature-subset stability (Jaccard/Kuncheva) and out-of-sample (OOS) forecasting error (MAE/RMSE) across sequential temporal windows, focusing on prediction error instead of executed trading profitability. Use daily BTC.

**Overlap:**
Bitcoin, temporal windows (walk-forward), feature selection per window (training-only), OOS forecasting/evaluation, Jaccard measurement, use of PatchTST/iTransformer/XGBoost as candidates.

**Difference:**
Bysik evaluates *economic execution* constraints, using Jaccard merely as an appendix diagnostic showing sets are moderately stable. They do not correlate or regress stability against the resulting fold-level forecasting errors. Their horizon is hourly; we target daily. Their selection is rank-based (Spearman).

**Remaining gap:**
The explicit analytical relationship (correlation, association, mapping) between feature-subset stability and OOS forecasting error for Bitcoin across temporal windows.

**Risk of novelty overlap:**
**HIGH.** Conceptually very close. They possess the stability data and the error data; their objective was simply different.

## 2. Barak & Parvini (2023) — DOI 10.1002/fut.22453
**What they did:**
Transfer-entropy-based dynamic feature selection for evaluating Bitcoin price drivers. Shows information flow changes over time (e.g. COVID pandemic).

**What we would do:**
Analyze stability ↔ OOS error relationship.

**Overlap:**
Bitcoin forecasting, temporal/dynamic feature selection.

**Difference:**
They focus on identifying the drivers themselves (transfer entropy) and their relevance shifts; we focus on the relationship of subset *stability* to forecasting *error*.

**Remaining gap:**
Explicit analysis of how dynamic feature changes (stability) relate to OOS forecast error.

**Risk of novelty overlap:**
**MEDIUM.** They do dynamic selection; whether they relate it to OOS error is unknown pending full-text review.

## 3. Youssefi et al. (2025) — DOI 10.32604/cmc.2025.063218
**What they did:**
Optimize forecast accuracy in crypto markets; evaluate feature selection (MI, RFE, Random Forest Importance) on >130 technical indicators across multiple horizons (1-20 days) using walk-forward validation for BTC, ETH, BNB.

**What we would do:**
Measure feature subset stability over time and correlate to OOS forecasting error variation.

**Overlap:**
Crypto/BTC forecasting, feature selection on technical indicators, walk-forward validation.

**Difference:**
They focus on identifying the best subset and model (SVR, Huber, KNN) to improve accuracy across horizons; we focus on the *temporal stability* of the subset and its relationship to performance over time.

**Remaining gap:**
Measurement of temporal subset stability and its analytical link to OOS performance variation.

**Risk of novelty overlap:**
**MEDIUM-HIGH.** They combine FS, crypto, and WF. Kills broad claims but currently preserves narrow gap.

## 4. Elmakias, Kolsky & Vilenchik (2026) — DOI 10.3390/math14132372
**What they did:**
Feature stability as a trust layer for feature selection. Resampling-based recurrence profiles beyond predictive performance.

**What we would do:**
Feature subset stability vs OOS predictive performance on Bitcoin time-series forecasting.

**Overlap:**
Analyzing both feature stability and predictive performance; treating stability as distinct from performance.

**Difference:**
They use resampling methodology and focus on general ML problems; we apply temporal walk-forward evaluation specifically to financial time-series (Bitcoin forecasting).

**Remaining gap:**
Domain-specific application: the temporal relationship between stability and OOS error in cryptocurrency forecasting.

**Risk of novelty overlap:**
**HIGH conceptually.** They likely test the general claim we make for Bitcoin. Domain distinction is required.

## 5. Lazebnik & Rosenfeld (2024) — DOI 10.1007/s10472-024-09936-8
**What they did:**
New definition for feature selection stability analysis under data drift.

**What we would do:**
Use robust stability metrics to evaluate BTC forecasting.

**Overlap:**
Feature selection stability concepts under drift.

**Difference:**
Methodology paper vs applied financial forecasting.

**Remaining gap:**
Methodological foundation only; does not close our applied gap.

**Risk of novelty overlap:**
**LOW.** Will use as metric justification.

## 6. Lee & Cai (2026) & WinnowML (2021/2022)
**Status:** Incomplete audit pending verified source/text. WinnowML connects stable FS and accuracy in time-based modeling; Lee & Cai evaluate moving-window importance in financial forecasting. Must read before concluding gap impact.
