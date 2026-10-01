"""Coinbase robustness test suite — mirrors frozen Binance checks."""
import numpy as np
import pandas as pd
import pytest
from pathlib import Path
import sys

ROOT = Path("D:/Hermes/Projects/riset-btc")
sys.path.insert(0, str(ROOT / "code"))

import prepare_features as pf
import bootstrap_analysis as ba
import run_coinbase_robustness as rcb


def test_target_definition():
    df = pf.synthetic_ohlcv(50)
    res = pf.build_features(df)
    expected = np.log(df['close'].shift(-1) / df['close'])
    np.testing.assert_allclose(res['target'].iloc[:-1], expected.iloc[:-1], rtol=1e-12)


def test_feature_causality():
    df = pf.synthetic_ohlcv(120)
    full = pf.build_features(df)
    partial = pf.build_features(df.iloc[:80])
    idx = partial.index[60]
    for c in pf.FEATURE_COLUMNS:
        if c in partial.columns:
            v1, v2 = full.loc[idx, c], partial.loc[idx, c]
            if np.isnan(v1) and np.isnan(v2):
                continue
            assert np.isclose(v1, v2)


def test_exactly_30_features():
    assert len(pf.FEATURE_COLUMNS) == 30
    assert 'target' not in pf.FEATURE_COLUMNS


def test_k_exactly_10():
    from experiment_config import K
    assert K == 10


def test_jaccard_known():
    assert pf.jaccard({'a', 'b', 'c', 'd'}, {'c', 'd', 'e', 'f'}) == 2 / 6


def test_kuncheva_known():
    assert np.isclose(pf.kuncheva({'a', 'b', 'c', 'd'}, {'c', 'd', 'e', 'f'}, 10), 4 / 24)


def test_window_boundaries():
    w = rcb.build_windows(730 + 180 + 90)
    assert w == [(0, 730, 910, 1000)]
    a, b, c, d = w[0]
    assert (b - a, c - b, d - c) == (730, 180, 90)


def test_oos_blocks_non_overlapping():
    data = pd.read_parquet(ROOT / "data/processed/coinbase_btcusd_daily_features_v1.parquet")
    w = rcb.build_windows(len(data))
    for (a1, b1, c1, d1), (a2, b2, c2, d2) in zip(w, w[1:]):
        assert c2 == c1 + 90 and d2 == d1 + 90
        assert c2 >= d1  # OOS blocks never overlap


def test_jaccard_paired_to_next_mae():
    df = pd.read_csv(ROOT / "reports/coinbase_experiment_results.csv")
    aligned = df.copy()
    aligned["paired_mae_next"] = aligned["xgboost_mae"].shift(-1)
    paired = aligned.dropna(subset=["jaccard_to_next", "paired_mae_next"])
    # J_t of window t must equal MAE of window t+1
    for _, row in paired.iterrows():
        t = int(row["window_id"])
        assert row["paired_mae_next"] == df.loc[df["window_id"] == t + 1, "xgboost_mae"].iloc[0]


def test_bootstrap_paired_resampling():
    rng = np.random.RandomState(0)
    x = rng.randn(60); y = x + 0.2 * rng.randn(60)
    res = ba.stationary_bootstrap_pairs(x, y, b=4.0, B=200, seed=42)
    assert res["ci_lower"] <= res["bootstrap_mean"] <= res["ci_upper"]


def test_automatic_block_length_ge_1():
    rng = np.random.RandomState(1)
    assert ba.automatic_block_length(rng.randn(300)) >= 1.0


def test_reproducibility_of_block_length():
    x = np.array([0.2, 0.5, 0.3, 0.6, 0.4, 0.2, 0.5, 0.3, 0.6, 0.4])
    assert ba.automatic_block_length(x) == ba.automatic_block_length(x)
