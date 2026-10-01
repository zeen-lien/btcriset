# PHASE 1 — RESEARCH DESIGN & EXPERIMENT PROTOCOL
> **Date:** 2026-09-29

## 1. Research Identification
- **Domain:** Multivariate Time-Series Forecasting (Bitcoin)
- **Research Problem:** Lack of empirical understanding regarding how the temporal stability of selected feature subsets relates to corresponding out-of-sample (OOS) forecasting error in Bitcoin price prediction.
- **RQ:** Is the temporal variation in feature-subset stability associated with the variation in OOS forecasting error across successive windows?
- **Hypothesis (H1):** There is a statistically significant association between feature-subset stability and OOS forecasting error.

## 2. Dataset Configuration
- **Primary Dataset:** Binance BTC/USDT Spot Klines
- **Robustness Dataset:** Coinbase BTC-USD Candles
- **Granularity:** Daily (1D)
- **Period:** 2017-08-17 to 2025-12-31 (Binance); ~3050 observations.
- **Retrieval Protocol:**
  - Save raw JSON responses using strict closed-candle logic (drop the most recent active candle).
  - Produce unalterable `dataset_v1_binance_raw.parquet` and `dataset_v1_coinbase_raw.parquet` with retrieval metadata.

## 3. Variable Engineering
- **Target ($Y_t$):** Next-day log return: $r_{t+1} = \ln(C_{t+1} / C_t)$
- **Base Features:** Open, High, Low, Close, Volume (Volume requires log-transformation or scaling due to wide distributions).
- **Candidate Feature Pool ($X_t$):** ~30-40 deterministic causal features:
  - Log Returns: 1D, 3D, 7D, 14D
  - Momentum: RSI (14), MACD (12,26,9), Stochastic Oscillator
  - Trend: SMA (7, 14, 30, 90), EMA (7, 14, 30)
  - Volatility: ATR (14), Bollinger Bands (width, %B), Rolling StdDev (14, 30)
  - Volume: OBV, Volume SMA (14), Volume Change
- **Leakage Constraint:** All rolling calculations must only use data $\le t$. No `center=True` parameters. No future-informed imputation.

## 4. Temporal Window Design
- **Structure:** Anchored Walk-Forward (Expanding Window) OR Rolling Window.
  - *Recommendation:* **Rolling Window** to allow the model to forget stale regimes, which maximizes potential subset variation (stability variation) compared to an expanding window that anchors to 2017.
- **Parameters (Provisional - subject to tuning on pilot):**
  - **Train Window:** 730 days (2 years) to capture varied conditions.
  - **Validation Window:** 90 days (3 months) for early stopping/hyperparameter tuning.
  - **Test (OOS) Window:** 30 days (1 month).
  - **Step Size:** 30 days (Test window length).
  - **Total Windows:** Approx. $\frac{3050 - 730 - 90 - 30}{30} \approx 73$ windows.

## 5. Feature Selection Protocol
- **Method:** XGBoost Feature Importance (Gain).
- **Timing:** Fit ONLY on the `Train Window` of the current temporal fold.
- **K Selection (Top-K):** $K$ will be fixed during the main experiment to ensure stability metrics are mathematically comparable.
  - *Pilot Task:* Run sensitivity analysis for $K \in \{10, 15, 20\}$ on the first 5 windows. Select the $K$ that balances model performance and subset variance.
- **Output:** Set $S_t$ containing exactly $K$ features.

## 6. Stability Measurement
- **Primary Metric:** Jaccard Similarity
  - $J(S_t, S_{t-1}) = \frac{|S_t \cap S_{t-1}|}{|S_t \cup S_{t-1}|}$
- **Secondary Metric:** Kuncheva Index (chance-corrected)
  - Evaluates if overlap exceeds random chance given pool size $N$ and selection size $K$.
- **Timing:** Computed before forecasting phase.

## 7. Forecasting Models
- **Baseline 1:** Naive Persistence ($Y_{t+1} = Y_t$, or 0 return).
- **Baseline 2:** XGBoost Regressor (cheap tabular ML baseline; same architecture as feature selector but tuned for forecasting).
- **Primary Forecaster:** PatchTST (Transformer-based time-series model).
- **Scaling constraint:** `StandardScaler` fit ONLY on `Train Window`, applied to Train, Val, and OOS.

## 8. Evaluation Metrics
- **Performance:** RMSE, MAE.
- **Directional (Optional tracking):** Directional Accuracy (Accuracy of $sgn(Y_{t+1}) == sgn(\hat{Y}_{t+1})$).

## 9. Statistical Analysis Plan
- **Variables:** Pair $(Stability_t, Error_t)$ for $t \in \{2, 3, ..., 73\}$.
- **Method:** Spearman Rank Correlation (due to likely non-normality of errors and stability scores).
- **Dependency Control:** Block-bootstrap resampling to control for autocorrelation between adjacent test windows.
- **Hypothesis Test:** $H_0: \rho_s = 0$ vs $H_1: \rho_s \neq 0$.

## 10. Next Step: Phase 3 (Pipeline Validation / Pilot)
Do NOT run the 73-window full test immediately.
1. Build `download_data.py` to get Binance data and save snapshot.
2. Build `prepare_features.py` to generate the 30-40 causal features.
3. Build `run_pilot.py` to execute the pipeline on the FIRST 5 WINDOWS only.
4. Output Pilot Table: Window, Train bounds, OOS bounds, Selected Features, Jaccard, RMSE.
5. Check for code failure, leakage issues, and ensure Jaccard actually varies.
