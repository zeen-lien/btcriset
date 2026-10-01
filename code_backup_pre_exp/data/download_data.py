import os
import time
import json
import requests
import pandas as pd
from datetime import datetime, timezone

RAW_DIR = "D:/Hermes/Projects/riset-btc/data/raw"
SNAPSHOT_DIR = "D:/Hermes/Projects/riset-btc/data/snapshots"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def download_binance(symbol="BTCUSDT", interval="1d"):
    print(f"Downloading Binance {symbol} {interval}...")
    limit = 1000
    start_ts = int(datetime(2017, 8, 1, tzinfo=timezone.utc).timestamp() * 1000)
    end_ts = int(datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp() * 1000)
    
    all_data = []
    current_start = start_ts
    
    while current_start < end_ts:
        params = {"symbol": symbol, "interval": interval, "limit": limit, "startTime": current_start, "endTime": end_ts}
        res = requests.get("https://api.binance.com/api/v3/klines", params=params)
        res.raise_for_status()
        data = res.json()
        if not data: break
        
        all_data.extend(data)
        current_start = data[-1][0] + 1
        time.sleep(0.2)
        
    cols = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
            'quote_volume', 'trades', 'taker_base', 'taker_quote', 'ignore']
    df = pd.DataFrame(all_data, columns=cols)
    for c in cols: df[c] = pd.to_numeric(df[c])
    
    # Closed-candle rule: drop current running candle
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    df = df[df['close_time'] < now_ms].copy()
    
    df.drop_duplicates(subset=['open_time'], inplace=True)
    df.sort_values('open_time', inplace=True)
    df['date'] = pd.to_datetime(df['open_time'], unit='ms')
    
    # Save
    out_path = os.path.join(RAW_DIR, f"binance_{symbol.lower()}_{interval}.parquet")
    df.to_parquet(out_path, index=False)
    
    meta = {
        "source": "Binance REST API",
        "endpoint": "/api/v3/klines",
        "symbol": symbol,
        "interval": interval,
        "retrieval_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "start_date": str(df['date'].min()),
        "end_date": str(df['date'].max()),
        "total_rows": len(df)
    }
    with open(os.path.join(SNAPSHOT_DIR, f"binance_{symbol.lower()}_{interval}_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
        
    print(f"Binance done: {len(df)} rows. Saved to {out_path}")
    return df

def download_coinbase(product="BTC-USD", granularity=86400):
    print(f"Downloading Coinbase {product} {granularity}...")
    end_date = datetime(2025, 12, 31, tzinfo=timezone.utc)
    current_start = datetime(2015, 1, 1, tzinfo=timezone.utc)
    
    all_data = []
    
    while current_start < end_date:
        # max 300 points. 300 days for daily. We'll do 200 days per chunk.
        current_end = current_start + pd.Timedelta(days=200)
        if current_end > end_date:
            current_end = end_date
            
        params = {
            "granularity": granularity,
            "start": current_start.isoformat()[:-6] + "Z", # strict ISO8601
            "end": current_end.isoformat()[:-6] + "Z"
        }
        res = requests.get(f"https://api.exchange.coinbase.com/products/{product}/candles", params=params, headers={'User-Agent': 'Mozilla/5.0'})
        if res.status_code == 200:
            data = res.json()
            if data:
                all_data.extend(data)
        elif res.status_code == 429:
            time.sleep(2)
            continue
        
        current_start = current_end
        time.sleep(0.3)
        
    cols = ['time', 'low', 'high', 'open', 'close', 'volume']
    df = pd.DataFrame(all_data, columns=cols)
    for c in cols: df[c] = pd.to_numeric(df[c])
    
    # Closed-candle rule
    now_s = int(datetime.now(timezone.utc).timestamp())
    # Coinbase bucket time is start of bucket. A daily candle closes at time + 86400.
    df = df[(df['time'] + granularity) < now_s].copy()
    
    df.drop_duplicates(subset=['time'], inplace=True)
    df.sort_values('time', inplace=True)
    df['date'] = pd.to_datetime(df['time'], unit='s')
    
    out_path = os.path.join(RAW_DIR, f"coinbase_{product.replace('-','_').lower()}_{granularity}.parquet")
    df.to_parquet(out_path, index=False)
    
    meta = {
        "source": "Coinbase Exchange API",
        "endpoint": "/products/{product}/candles",
        "product": product,
        "granularity": granularity,
        "retrieval_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "start_date": str(df['date'].min()),
        "end_date": str(df['date'].max()),
        "total_rows": len(df)
    }
    with open(os.path.join(SNAPSHOT_DIR, f"coinbase_{product.replace('-','_').lower()}_{granularity}_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
        
    print(f"Coinbase done: {len(df)} rows. Saved to {out_path}")
    return df

if __name__ == "__main__":
    download_binance()
    download_coinbase()
