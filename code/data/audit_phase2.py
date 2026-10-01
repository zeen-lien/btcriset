import hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SETS = [
    ('binance', ROOT/'data/raw/binance_btcusdt_1d.parquet', ROOT/'data/snapshots/binance_btcusdt_1d_meta.json', 'open_time', 86400000, 'ms'),
    ('coinbase', ROOT/'data/raw/coinbase_btc_usd_86400.parquet', ROOT/'data/snapshots/coinbase_btc_usd_86400_meta.json', 'time', 86400, 's'),
]

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

for name, path, meta_path, tscol, day, unit in SETS:
    df=pd.read_parquet(path)
    raw_meta=json.loads(meta_path.read_text(encoding='utf-8'))
    ts=pd.to_numeric(df[tscol], errors='coerce')
    expected=pd.Series(np.arange(int(ts.min()), int(ts.max())+day, day))
    actual=set(ts.dropna().astype('int64'))
    missing=sorted(set(expected.astype('int64'))-actual)
    dup=int(ts.duplicated().sum())
    numeric=df.select_dtypes(include='number')
    finite=bool(np.isfinite(numeric.to_numpy(dtype='float64')).all())
    nulls=int(df.isna().sum().sum())
    ohlc=(df['high'] >= df[['open','close','low']].max(axis=1)) & (df['low'] <= df[['open','close','high']].min(axis=1))
    nonneg=bool((df['volume']>=0).all())
    ascending=bool(ts.is_monotonic_increasing)
    interval=bool(ts.diff().dropna().eq(day).all())
    now=pd.Timestamp.now(tz='UTC').timestamp()
    closed=bool((ts.astype('float64')/1000 + day/1000 < now).all()) if unit=='ms' else bool((ts.astype('float64')+day<now).all())
    result={
      'dataset':name,'path':str(path),'source':raw_meta.get('source'),'symbol':raw_meta.get('symbol',raw_meta.get('product')),
      'interval':raw_meta.get('interval',raw_meta.get('granularity')),
      'requested_period':('2017-08-01 to 2025-12-31' if name=='binance' else '2015-01-01 to 2025-12-31'),
      'actual_start_utc':pd.to_datetime(ts.min(),unit=unit,utc=True).isoformat(),
      'actual_end_utc':pd.to_datetime(ts.max(),unit=unit,utc=True).isoformat(),'rows':len(df),
      'duplicate_count':dup,'missing_daily_timestamps':len(missing),'missing_timestamp_examples':missing[:10],
      'gap_count':len(missing),'nan_cells':nulls,'infinite_or_nonfinite_numeric':not finite,
      'ascending':ascending,'timestamp_unique':dup==0,'daily_interval_consistent':interval,
      'ohlc_violations':int((~ohlc).sum()),'volume_nonnegative':nonneg,'closed_candles_only':closed,
      'sha256':sha256(path),'file_size_bytes':path.stat().st_size,
      'metadata_file':str(meta_path),'metadata_recorded_rows':raw_meta.get('total_rows')
    }
    print(json.dumps(result,indent=2))
