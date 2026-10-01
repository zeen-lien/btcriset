"""Comprehensive test suite for Bitcoin feature stability & forecasting experiment."""
import numpy as np
import pandas as pd
import pytest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

import prepare_features as pf
import bootstrap_analysis as ba


def test_target_definition():
    df = pf.synthetic_ohlcv(50)
    res = pf.build_features(df)
    expected = np.log(df['close'].shift(-1) / df['close'])
    np.testing.assert_allclose(res['target'].iloc[:-1], expected.iloc[:-1], rtol=1e-12)
    assert 'target' not in pf.FEATURE_COLUMNS


def test_feature_causality():
    df = pf.synthetic_ohlcv(100)
    full = pf.build_features(df)
    partial = pf.build_features(df.iloc[:70])
    idx = partial.index[50]
    for c in pf.FEATURE_COLUMNS:
        if c in partial.columns:
            v1 = full.loc[idx, c]
            v2 = partial.loc[idx, c]
            if np.isnan(v1) and np.isnan(v2):
                continue
            assert np.isclose(v1, v2)


def test_jaccard_and_kuncheva():
    s1 = {'a', 'b', 'c', 'd'}
    s2 = {'c', 'd', 'e', 'f'}
    assert pf.jaccard(s1, s2) == 2 / 6
    # Kuncheva index for k=4, n=10, overlap=2
    # (2*10 - 4*4) / (4*(10-4)) = (20 - 16) / (4*6) = 4 / 24 = 1/6
    assert np.isclose(pf.kuncheva(s1, s2, 10), 4 / 24)


def test_automatic_block_length():
    np.random.seed(42)
    x = np.random.randn(200)
    b = ba.automatic_block_length(x)
    assert b >= 1.0


def test_stationary_bootstrap_pairs():
    np.random.seed(42)
    x = np.random.randn(100)
    y = x + 0.1 * np.random.randn(100)
    res = ba.stationary_bootstrap_pairs(x, y, b=5.0, B=100, seed=42)
    assert 'bootstrap_mean' in res
    assert 'ci_lower' in res
    assert 'ci_upper' in res
    assert res['ci_lower'] <= res['bootstrap_mean'] <= res['ci_upper']
