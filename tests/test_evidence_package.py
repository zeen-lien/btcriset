"""Evidence-package consistency tests (MASTER RESULTS EVIDENCE PACKAGE, item 14).

Assertions only over EXISTING artifacts. No model fit, no re-run.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
REP = ROOT / "reports"
sys.path.insert(0, str(ROOT / "code"))
from prepare_features import jaccard  # noqa: E402
from apply_c1_pairing_correction import build_pairs  # noqa: E402

CASES = {"Binance": REP / "experiment_results.csv", "Coinbase": REP / "coinbase_experiment_results.csv"}
EXPECTED = {"Binance": {"windows": 22, "pairs": 21}, "Coinbase": {"windows": 31, "pairs": 30}}


def _sel(d):
    return {int(r.window_id): set(json.loads(r.selected_features)) for r in d.itertuples()}


@pytest.mark.parametrize("name", list(CASES))
def test_window_count_matches_result_csv(name):
    d = pd.read_csv(CASES[name])
    assert len(d) == EXPECTED[name]["windows"]
    assert d.window_id.is_unique
    assert list(d.window_id) == list(range(1, len(d) + 1))


@pytest.mark.parametrize("name", list(CASES))
def test_pairs_equal_windows_minus_one(name):
    d = pd.read_csv(CASES[name])
    assert len(build_pairs(d)) == len(d) - 1 == EXPECTED[name]["pairs"]


@pytest.mark.parametrize("name", list(CASES))
def test_c1_pairing_jaccard_and_mae(name):
    d = pd.read_csv(CASES[name])
    sel = _sel(d)
    mae = {int(r.window_id): float(r.xgboost_mae) for r in d.itertuples()}
    pairs = build_pairs(d)
    for row in pairs.itertuples():
        t = int(row.t)
        assert np.isclose(row.jaccard_J_t, jaccard(sel[t], sel[t + 1]))
        assert np.isclose(row.mae_t_plus_1, mae[t + 1])


@pytest.mark.parametrize("name", list(CASES))
def test_no_missing_pairing(name):
    d = pd.read_csv(CASES[name])
    pairs = build_pairs(d)
    assert not pairs[["jaccard_J_t", "mae_t_plus_1"]].isna().any().any()
    assert list(pairs.t) == list(range(1, len(d)))


def test_binance_final_association_n_is_21():
    j = json.loads((REP / "final-association-c1-corrected.json").read_text())
    b = next(r for r in j if r["dataset"] == "Binance")
    assert b["n_pairs"] == 21


def test_coinbase_final_association_n_is_30():
    j = json.loads((REP / "final-association-c1-corrected.json").read_text())
    c = next(r for r in j if r["dataset"] == "Coinbase")
    assert c["n_pairs"] == 30


def test_corrected_json_csv_consistent():
    j = {r["dataset"]: r for r in json.loads((REP / "final-association-c1-corrected.json").read_text())}
    csv = pd.read_csv(REP / "final-association-c1-corrected.csv")
    assert set(csv.dataset) == {"Binance", "Coinbase"}
    for name, r in j.items():
        sub = csv[csv.dataset == name]
        assert len(sub) == r["n_pairs"]
        rho = sub.jaccard_J_t.corr(sub.mae_t_plus_1, method="spearman")
        assert np.isclose(rho, r["spearman_rho"])


def test_pairing_evidence_file_matches_corrected_csv():
    ev = pd.read_csv(REP / "final-pairing-evidence.csv")
    csv = pd.read_csv(REP / "final-association-c1-corrected.csv")
    for name in ["Binance", "Coinbase"]:
        a = ev[ev.dataset == name].sort_values("t").reset_index(drop=True)
        b = csv[csv.dataset == name].sort_values("t").reset_index(drop=True)
        assert np.allclose(a.jaccard_t.values, b.jaccard_J_t.values)
        assert np.allclose(a.mae_t_plus_1.values, b.mae_t_plus_1.values)
