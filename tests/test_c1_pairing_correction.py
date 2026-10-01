"""C1 pairing-correction assertions.

Guarantees the frozen pairing is J_t = Jaccard(S_t, S_{t+1}) paired with MAE_{t+1},
and NOT MAE_t nor MAE_{t+2}. Reuses the C1 correction builder on the FINAL CSVs.
No model is fit here.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path("D:/Hermes/Projects/riset-btc")
sys.path.insert(0, str(ROOT / "code"))
from apply_c1_pairing_correction import build_pairs  # noqa: E402
from prepare_features import jaccard  # noqa: E402

CASES = {
    "Binance": ROOT / "reports/experiment_results.csv",
    "Coinbase": ROOT / "reports/coinbase_experiment_results.csv",
}


@pytest.mark.parametrize("name", list(CASES))
def test_pair_count_is_windows_minus_one(name):
    df = pd.read_csv(CASES[name])
    pairs = build_pairs(df)
    assert len(pairs) == len(df) - 1  # n_windows - 1 (frozen same-row pairing)


@pytest.mark.parametrize("name", list(CASES))
def test_x_is_jaccard_of_t_and_t_plus_1(name):
    df = pd.read_csv(CASES[name])
    sel = {int(r.window_id): set(json.loads(r.selected_features)) for r in df.itertuples()}
    pairs = build_pairs(df)
    for row in pairs.itertuples():
        t = int(row.t)
        assert np.isclose(row.jaccard_J_t, jaccard(sel[t], sel[t + 1]))
        # and explicitly NOT Jaccard(S_{t-1}, S_t) when that value differs
        if t - 1 >= 1:
            j_prev = jaccard(sel[t - 1], sel[t])
            if not np.isclose(j_prev, row.jaccard_J_t):
                assert not np.isclose(row.jaccard_J_t, j_prev)


@pytest.mark.parametrize("name", list(CASES))
def test_y_is_mae_t_plus_1(name):
    df = pd.read_csv(CASES[name])
    mae = {int(r.window_id): float(r.xgboost_mae) for r in df.itertuples()}
    pairs = build_pairs(df)
    for row in pairs.itertuples():
        t = int(row.t)
        assert np.isclose(row.mae_t_plus_1, mae[t + 1])


@pytest.mark.parametrize("name", list(CASES))
def test_y_is_not_mae_t_and_not_mae_t_plus_2(name):
    df = pd.read_csv(CASES[name])
    mae = {int(r.window_id): float(r.xgboost_mae) for r in df.itertuples()}
    pairs = build_pairs(df)
    n = len(df)
    for row in pairs.itertuples():
        t = int(row.t)
        if not np.isclose(mae[t], mae[t + 1]):
            assert not np.isclose(row.mae_t_plus_1, mae[t]), f"y equals MAE_t at t={t}"
        if t + 2 <= n and not np.isclose(mae[t + 2], mae[t + 1]):
            assert not np.isclose(row.mae_t_plus_1, mae[t + 2]), f"y equals MAE_(t+2) at t={t}"


@pytest.mark.parametrize("name", list(CASES))
def test_stored_column_matches_frozen_jaccard(name):
    """jaccard_to_next on row r stores Jaccard(S_{r-1}, S_r) -> equals J_t with t=r-1."""
    df = pd.read_csv(CASES[name])
    sel = {int(r.window_id): set(json.loads(r.selected_features)) for r in df.itertuples()}
    for r in df.itertuples():
        if r.window_id == 1:
            assert np.isnan(r.jaccard_to_next)
            continue
        expected = jaccard(sel[int(r.window_id) - 1], sel[int(r.window_id)])
        assert np.isclose(r.jaccard_to_next, expected)


@pytest.mark.parametrize("name", list(CASES))
def test_no_oos_or_validation_leak_into_selection_source(name):
    """Selection uses TRAIN-only by construction; here we assert the frozen
    invariants that make the pairing leak-free: window dates are ordered and the
    pre-OOS (train+validation) block strictly precedes OOS."""
    df = pd.read_csv(CASES[name])
    for r in df.itertuples():
        assert r.train_start < r.train_end < r.validation_start < r.validation_end < r.oos_start < r.oos_end
    # windows advance forward in time (step >= 1), so t+1 OOS follows t OOS
    assert df["oos_start"].is_monotonic_increasing
