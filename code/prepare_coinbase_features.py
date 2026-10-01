"""Coinbase BTC-USD daily feature construction — REUSES frozen Binance build_features.

No network access. Identical feature universe and formulas as primary Binance experiment.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("D:/Hermes/Projects/riset-btc")
sys.path.insert(0, str(ROOT / "code"))

# Reuse the EXACT frozen feature builder from the Binance primary experiment.
from prepare_features import build_features, FEATURE_COLUMNS  # noqa: E402

RAW = ROOT / "data/raw/coinbase_btc_usd_86400.parquet"
META_IN = ROOT / "data/snapshots/coinbase_btc_usd_86400_meta.json"
OUT = ROOT / "data/processed/coinbase_btcusd_daily_features_v1.parquet"
META_OUT = ROOT / "data/snapshots/coinbase_btcusd_daily_features_v1_metadata.json"


def main() -> None:
    if not RAW.exists():
        raise FileNotFoundError(RAW)
    src = pd.read_parquet(RAW)
    raw_hash = hashlib.sha256(RAW.read_bytes()).hexdigest()
    source_meta = json.loads(META_IN.read_text())
    assert raw_hash == source_meta["sha256"], "Raw source hash differs from audit metadata"
    assert len(src) == source_meta["number_of_rows"], "Row count differs from audit metadata"

    # Normalize to the frozen schema: date, open, high, low, close, volume
    src = src.copy()
    src["date"] = pd.to_datetime(src["date"], utc=True).dt.tz_localize(None)
    frame = src[["date", "open", "high", "low", "close", "volume"]]

    out = build_features(frame)
    nan_by = out[FEATURE_COLUMNS + ["target"]].isna().sum().to_dict()
    clean = out.dropna(subset=FEATURE_COLUMNS + ["target"]).copy()

    assert clean[FEATURE_COLUMNS].select_dtypes(exclude="number").empty
    assert np.isfinite(clean[FEATURE_COLUMNS + ["target"]].to_numpy()).all()
    assert clean["date"].is_monotonic_increasing and clean["date"].is_unique
    assert not set(FEATURE_COLUMNS) & {"target"}
    assert len(FEATURE_COLUMNS) == 30

    OUT.parent.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(OUT, index=False)
    meta = {
        "source_raw_snapshot": str(RAW),
        "source_sha256": raw_hash,
        "feature_version": "v1",
        "feature_count": len(FEATURE_COLUMNS),
        "feature_columns": FEATURE_COLUMNS,
        "row_count": len(clean),
        "rows_before": len(src),
        "target_definition": "ln(Close[t+1]/Close[t])",
        "indicator_parameters": "identical to Binance primary (reused build_features)",
        "preprocessing": "causal trailing windows; no imputation; drop warm-up and final target-boundary rows",
        "warmup_nan_by_column": nan_by,
        "created_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    META_OUT.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({
        "rows_before": len(src),
        "rows_after": len(clean),
        "feature_count": len(FEATURE_COLUMNS),
        "period": [clean["date"].min().date().isoformat(), clean["date"].max().date().isoformat()],
        "raw_sha256": raw_hash,
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
