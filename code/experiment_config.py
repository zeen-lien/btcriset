"""FROZEN experiment configuration — do not modify without a freeze exception."""
from __future__ import annotations

ROOT = "D:/Hermes/Projects/riset-btc"

# --- Frozen decisions (master execution prompt) ---
PRIMARY_DATASET = "Binance BTC/USDT daily"
ROBUSTNESS_DATASET = "Coinbase BTC-USD daily"
RAW_SNAPSHOT = f"{ROOT}/data/raw/binance_btcusdt_1d.parquet"
PROCESSED_SNAPSHOT = f"{ROOT}/data/processed/binance_btcusdt_daily_features_v1.parquet"
SNAPSHOT_SHA = "6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0"

TARGET_DEF = "ln(Close[t+1]/Close[t])"
FEATURE_COLUMNS = [
    "open","high","low","close","volume",
    "return_1d","return_3d","return_7d","return_14d",
    "rsi_14",
    "macd_12_26","macd_signal_9","macd_hist",
    "stochastic_k_14","stochastic_d_3",
    "sma_7","sma_14","sma_30","sma_90",
    "ema_7","ema_14","ema_30",
    "atr_14",
    "bb_width_20","bb_percent_b_20",
    "rolling_std_14","rolling_std_30",
    "obv","volume_sma_14","volume_change",
]
assert len(FEATURE_COLUMNS) == 30, f"feature count {len(FEATURE_COLUMNS)}"

K = 10  # fixed; NOT selected from OOS
TRAIN_DAYS = 730
VALID_DAYS = 180
OOS_DAYS = 90
STEP_DAYS = 90

SEED = 42
RANDOM_STATE = SEED

# XGBoost feature-selector + forecaster (pilot-derived fixed reproducibility config)
XGB_PARAMS = dict(
    n_estimators=120, max_depth=3, learning_rate=0.05,
    subsample=1, colsample_bytree=1, reg_lambda=1,
    objective="reg:squarederror", random_state=RANDOM_STATE, n_jobs=1,
)
SELECTOR_IMPORTANCE = "gain"  # XGBoost Gain

# Bootstrap
BOOTSTRAP_B = 5000
CONFIDENCE_LEVEL = 0.95

# Pairing rule (frozen): J_t = Jaccard(S_t, S_{t+1}) paired with MAE_{t+1}
PAIRING = "J_t -> MAE_{t+1}"

# Outputs
REPORTS_DIR = f"{ROOT}/reports"
FIGURES_DIR = f"{REPORTS_DIR}/figures"
