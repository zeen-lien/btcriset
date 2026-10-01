# PHASE 1 — RESEARCH DESIGN & EXPERIMENT PROTOCOL
> **Date:** 2026-09-29
> **Status:** Updated 2026-10-01 to describe the FINAL implemented (frozen) methodology.
> Settings that were provisional during development are retained below and explicitly
> labelled **provisional / superseded**; the frozen values are stated alongside them.
> Frozen manifest: `reports/frozen_methodology_manifest.md`. Final results: `README.md`
> and `reports/`.

## 1. Research Identification
- **Domain:** Multivariate Time-Series Forecasting (Bitcoin)
- **Research Problem:** Lack of empirical understanding regarding how the temporal stability of selected feature subsets relates to corresponding out-of-sample (OOS) forecasting error in Bitcoin price prediction.
- **RQ:** Is the temporal variation in feature-subset stability associated with the variation in OOS forecasting error across successive windows?
- **Hypothesis (H1):** There is a statistically significant association between feature-subset stability and OOS forecasting error.

## 2. Dataset Configuration
- **Primary Dataset:** Binance BTC/USDT Spot Klines (daily).
- **Robustness Dataset:** Coinbase BTC-USD Candles (daily).
- **Granularity:** Daily (1D).
- **Period:** Binance 2017-08-17 → 2025-12-31 (3,059 raw / 2,969 processed rows); Coinbase 2015-07-20 → 2025-12-31 (3,818 raw / 3,728 processed rows).
- **Retrieval Protocol:**
  - Save raw responses using strict closed-candle logic (drop the most recent active candle).
  - Produce unalterable raw snapshots with retrieval metadata.
- **Canonical dataset files (final):**
  - `data/raw/binance_btcusdt_1d.parquet`
  - `data/raw/coinbase_btc_usd_86400.parquet`
  - `data/processed/binance_btcusdt_daily_features_v1.parquet`
  - `data/processed/coinbase_btcusd_daily_features_v1.parquet`
  - *(Superseded planned names: `dataset_v1_binance_raw.parquet`, `dataset_v1_coinbase_raw.parquet`.)*

## 3. Variable Engineering
- **Target ($Y_t$):** Next-day log return: $r_{t+1} = \ln(C_{t+1} / C_t)$
- **Base Features:** Open, High, Low, Close, Volume. **The final implementation uses RAW volume** — no `StandardScaler` and no log transformation are applied anywhere in the pipeline (XGBoost is scale-invariant). *(Superseded plan: "Volume requires log-transformation or scaling due to wide distributions".)*
- **Candidate Feature Pool ($X_t$):** exactly **30 deterministic causal price/volume-derived features** (final):
  - Log Returns: 1D, 3D, 7D, 14D
  - Momentum: RSI (14), MACD (12,26,9), Stochastic Oscillator (K=14, D=3)
  - Trend: SMA (7, 14, 30, 90), EMA (7, 14, 30)
  - Volatility: ATR (14), Bollinger Bands (width, %B), Rolling StdDev (14, 30)
  - Volume: OBV, Volume SMA (14), Volume Change
  - *(Superseded plan: "~30-40 deterministic causal features".)*
- **Leakage Constraint:** All rolling calculations must only use data $\le t$. No `center=True` parameters. No future-informed imputation.

## 4. Temporal Window Design
- **Structure:** Anchored Walk-Forward (Expanding Window) OR Rolling Window.
  - *Recommendation:* **Rolling Window** to allow the model to forget stale regimes, which maximizes potential subset variation (stability variation) compared to an expanding window that anchors to 2017.
- **Frozen parameters (final implemented):**
  - **Train Window:** 730 days (2 years) to capture varied conditions.
  - **Validation Window:** 180 days (temporal separation layer only; K is NOT selected on validation — see §5).
  - **OOS Window:** 90 days.
  - **Step Size:** 90 days (= OOS window length).
- **Window counts (final implemented):**
  - Binance = **22 windows** → **21 association pairs** (after the frozen C1 pairing).
  - Coinbase = **31 windows** → **30 association pairs** (after the frozen C1 pairing).
- *(Superseded provisional plan: Train 730 / Validation 90 / Test 30 / Step 30, "approximately 73 windows". The label "Test" was renamed "OOS"; the implemented configuration is 730 / 180 / 90 / 90. Earlier arithmetic corrections to 71 windows applied to the old provisional design only.)*

## 5. Feature Selection Protocol
- **Method:** XGBoost Feature Importance (Gain).
- **Timing:** Fit ONLY on the `Train Window` of the current temporal fold.
- **K Selection (Top-K):** **$K = 10$, fixed** across all folds (frozen a priori; NOT selected from OOS).
  - *Pilot Task (superseded): Run sensitivity analysis for $K \in \{10, 15, 20\}$ on the first 5 windows. The pilot's K choice did not become final methodology evidence; $K=10$ was frozen for the final experiment.*
- **Output:** Set $S_t$ containing exactly $K$ features.

## 6. Stability Measurement
- **Primary Metric:** Jaccard Similarity
  - $J(S_t, S_{t-1}) = \frac{|S_t \cap S_{t-1}|}{|S_t \cup S_{t-1}|}$
- **Secondary Metric:** Kuncheva Index (chance-corrected)
  - Evaluates if overlap exceeds random chance given pool size $N$ and selection size $K$.
- **Timing:** Computed before forecasting phase.

## 7. Forecasting Models
- **Baseline:** Naive Persistence (zero-return baseline, $Y_{t+1} = 0$).
- **Primary Forecaster (final implemented):** **XGBoost Regressor** (`XGBRegressor`).
- **PatchTST — NOT used:** PatchTST (Transformer-based time-series model) was an **earlier candidate architecture considered during Phase 0/1** but was **NOT implemented and NOT used** in the final experiment. The final forecasting model is XGBoost. *(Superseded plan: "Primary Forecaster: PatchTST (Transformer-based time-series model)".)*
- **Scaling:** No `StandardScaler` is applied (XGBoost is scale-invariant). *(Superseded plan: "StandardScaler fit ONLY on Train Window".)*

## 8. Evaluation Metrics
- **Performance:** RMSE, MAE.
- **Directional (Optional tracking):** Directional Accuracy (Accuracy of $sgn(Y_{t+1}) == sgn(\hat{Y}_{t+1})$).

## 9. Statistical Analysis Plan
- **Variables:** Pair $(J_t, MAE_{t+1})$ where $J_t = \text{Jaccard}(S_t, S_{t+1})$ (frozen C1 pairing, SAME-ROW index).
- **Final counts:** Binance 21 pairs; Coinbase 30 pairs.
  - *(Superseded plan: $t \in \{2, 3, ..., 73\}$ under the old provisional window design.)*
- **Method:** Spearman Rank Correlation.
- **Dependency Control:** Stationary block bootstrap (dependence-aware), $B = 5000$, seed $= 42$, 95% confidence interval.
- **Hypothesis Test:** $H_0: \rho_s = 0$ vs $H_1: \rho_s \neq 0$. Interpreted cautiously (small n, wide CI); the iid Spearman p-value is a reference only, not the primary inference.

## 10. Next Step: Phase 3 (Pipeline Validation / Pilot)
*(Historical — retained for the research record.)*
Do NOT run the full test immediately.
1. Build `download_data.py` to get Binance data and save snapshot.
2. Build `prepare_features.py` to generate the causal features.
3. Build `run_pilot.py` to execute the pipeline on the FIRST 5 WINDOWS only.
4. Output Pilot Table: Window, Train bounds, OOS bounds, Selected Features, Jaccard, RMSE.
5. Check for code failure, leakage issues, and ensure Jaccard actually varies.
