import importlib.util
from pathlib import Path

MODULE = Path(__file__).parents[1] / 'code' / 'prepare_features.py'
spec = importlib.util.spec_from_file_location('prepare_features', MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_target_is_next_close_log_return_and_not_feature():
    frame = mod.build_features(mod.synthetic_ohlcv())
    expected = (frame['close'].shift(-1) / frame['close']).map(__import__('math').log)
    assert frame['target'].iloc[:-1].equals(expected.iloc[:-1])
    assert frame['target'].iloc[-1] != frame['target'].iloc[-1]
    assert 'target' not in mod.FEATURE_COLUMNS


def test_features_are_causal_and_numeric():
    data = mod.synthetic_ohlcv(160)
    full = mod.build_features(data)
    prefix = mod.build_features(data.iloc[:120])
    cols = [c for c in mod.FEATURE_COLUMNS if c in prefix.columns]
    assert full.loc[prefix.index[100], cols].equals(prefix.loc[prefix.index[100], cols])
    assert all(str(full[c].dtype).startswith(('float','int')) for c in cols)


def test_jaccard_and_kuncheva_known_sets():
    assert mod.jaccard({'a','b'}, {'b','c'}) == 1/3
    assert mod.kuncheva({'a','b'}, {'b','c'}, 4) == 0.0
