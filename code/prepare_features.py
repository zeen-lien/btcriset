"""Causal daily BTC feature construction. No network access."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'data/raw/binance_btcusdt_1d.parquet'
OUT = ROOT/'data/processed/binance_btcusdt_daily_features_v1.parquet'
META = ROOT/'data/snapshots/binance_btcusdt_daily_features_v1_metadata.json'
FEATURE_COLUMNS = ['open','high','low','close','volume','return_1d','return_3d','return_7d','return_14d','rsi_14','macd_12_26','macd_signal_9','macd_hist','stochastic_k_14','stochastic_d_3','sma_7','sma_14','sma_30','sma_90','ema_7','ema_14','ema_30','atr_14','bb_width_20','bb_percent_b_20','rolling_std_14','rolling_std_30','obv','volume_sma_14','volume_change']


def synthetic_ohlcv(n=180):
    i=np.arange(n, dtype=float); close=100+i*.2+np.sin(i/5)
    return pd.DataFrame({'open':close-.1,'high':close+1,'low':close-1,'close':close,'volume':100+i}, index=pd.date_range('2020-01-01',periods=n,tz='UTC'))


def build_features(source):
    d=source.copy().reset_index(drop=True)
    close=d['close'].astype(float); high=d['high'].astype(float); low=d['low'].astype(float); vol=d['volume'].astype(float)
    out=d.copy()
    log_close=np.log(close)
    for lag in (1,3,7,14): out[f'return_{lag}d']=log_close.diff(lag)
    delta=close.diff(); gain=delta.clip(lower=0).rolling(14,min_periods=14).mean(); loss=(-delta.clip(upper=0)).rolling(14,min_periods=14).mean()
    rs=gain/loss.replace(0,np.nan); out['rsi_14']=100-100/(1+rs)
    ema12=close.ewm(span=12,adjust=False,min_periods=12).mean(); ema26=close.ewm(span=26,adjust=False,min_periods=26).mean()
    macd=ema12-ema26; out['macd_12_26']=macd; out['macd_signal_9']=macd.ewm(span=9,adjust=False,min_periods=9).mean(); out['macd_hist']=macd-out['macd_signal_9']
    ll=low.rolling(14,min_periods=14).min(); hh=high.rolling(14,min_periods=14).max(); out['stochastic_k_14']=100*(close-ll)/(hh-ll).replace(0,np.nan); out['stochastic_d_3']=out['stochastic_k_14'].rolling(3,min_periods=3).mean()
    for w in (7,14,30,90): out[f'sma_{w}']=close.rolling(w,min_periods=w).mean()
    for w in (7,14,30): out[f'ema_{w}']=close.ewm(span=w,adjust=False,min_periods=w).mean()
    prev=close.shift(); tr=pd.concat([high-low,(high-prev).abs(),(low-prev).abs()],axis=1).max(axis=1); out['atr_14']=tr.rolling(14,min_periods=14).mean()
    mid=close.rolling(20,min_periods=20).mean(); sd=close.rolling(20,min_periods=20).std(ddof=0); upper=mid+2*sd; lower=mid-2*sd
    out['bb_width_20']=(upper-lower)/mid; out['bb_percent_b_20']=(close-lower)/(upper-lower).replace(0,np.nan)
    daily_log_return=log_close.diff()
    for w in (14,30): out[f'rolling_std_{w}']=daily_log_return.rolling(w,min_periods=w).std(ddof=0)
    out['obv']=(np.sign(close.diff()).fillna(0)*vol).cumsum(); out['volume_sma_14']=vol.rolling(14,min_periods=14).mean(); out['volume_change']=vol.pct_change()
    out['target']=np.log(close.shift(-1)/close)
    assert 'target' not in FEATURE_COLUMNS
    expected=np.log(close.shift(-1)/close)
    np.testing.assert_allclose(out['target'].iloc[:-1],expected.iloc[:-1],rtol=1e-12,atol=1e-12)
    return out


def jaccard(a,b):
    u=set(a)|set(b); return len(set(a)&set(b))/len(u) if u else 1.0


def kuncheva(a,b,n_features):
    a,b=set(a),set(b); k=len(a)
    if len(b)!=k or n_features<=k: raise ValueError('Kuncheva requires equal subset sizes and N>K')
    return (len(a&b)*n_features-k*k)/(k*(n_features-k))


def main():
    if not RAW.exists(): raise FileNotFoundError(RAW)
    src=pd.read_parquet(RAW)
    raw_hash=hashlib.sha256(RAW.read_bytes()).hexdigest()
    source_meta=json.loads((ROOT/'data/snapshots/binance_btcusdt_1d_meta.json').read_text())
    assert raw_hash==source_meta['sha256'], 'Raw source hash differs from Phase 2 metadata'
    assert len(src)==source_meta['number_of_rows']
    src['date']=pd.to_datetime(src['open_time'],unit='ms',utc=True)
    out=build_features(src[['date','open','high','low','close','volume']])
    nan_by=out[FEATURE_COLUMNS+['target']].isna().sum().to_dict()
    clean=out.dropna(subset=FEATURE_COLUMNS+['target']).copy()
    assert clean[FEATURE_COLUMNS].select_dtypes(exclude='number').empty
    assert np.isfinite(clean[FEATURE_COLUMNS+['target']].to_numpy()).all()
    assert clean['date'].is_monotonic_increasing and clean['date'].is_unique
    assert not set(FEATURE_COLUMNS)&{'target'}
    OUT.parent.mkdir(parents=True,exist_ok=True); META.parent.mkdir(parents=True,exist_ok=True)
    clean.to_parquet(OUT,index=False)
    meta={'source_raw_snapshot':str(RAW),'source_sha256':raw_hash,'feature_version':'v1','feature_count':len(FEATURE_COLUMNS),'feature_columns':FEATURE_COLUMNS,'row_count':len(clean),'rows_before':len(src),'target_definition':'ln(Close[t+1]/Close[t])','indicator_parameters':'documented in reports/feature-audit.md','preprocessing':'causal trailing windows; no imputation; drop warm-up and final target-boundary rows','warmup_nan_by_column':nan_by,'created_utc':pd.Timestamp.now(tz='UTC').isoformat(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    META.write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps({'rows_before':len(src),'rows_after':len(clean),'feature_count':len(FEATURE_COLUMNS),'nan_by_column':nan_by,'raw_sha256':raw_hash,'output':str(OUT)},indent=2))

if __name__=='__main__': main()
