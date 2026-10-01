import json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from xgboost import XGBRegressor
from prepare_features import FEATURE_COLUMNS, jaccard, kuncheva, OUT

ROOT=Path('D:/Hermes/Projects/riset-btc'); RESULTS=ROOT/'reports/pilot_results.csv'
TRAIN,VALID,TEST,STEP=730,90,30,30
K_CANDIDATES=(10,15,20)
K=10  # overwritten by train/validation-only sensitivity procedure; never use OOS for K choice
SEED=42

def main():
    data=pd.read_parquet(OUT).sort_values('date').reset_index(drop=True)
    assert data['date'].is_monotonic_increasing and data['date'].is_unique
    assert len(data)>=TRAIN+VALID+TEST
    x=data[FEATURE_COLUMNS].astype(float); y=data['target'].astype(float)
    windows=[]
    prevset=None
    fixed_k=None
    for wi in range(5):
        start=wi*STEP; a=start; b=a+TRAIN; c=b+VALID; d=c+TEST
        tr=slice(a,b); va=slice(b,c); te=slice(c,d)
        if d>len(data): raise ValueError('Insufficient data for exactly five windows')
        selector=XGBRegressor(n_estimators=120,max_depth=3,learning_rate=.05,subsample=1,colsample_bytree=1,reg_lambda=1,objective='reg:squarederror',importance_type='gain',random_state=SEED,n_jobs=1)
        selector.fit(x.iloc[tr],y.iloc[tr])
        gains=selector.get_booster().get_score(importance_type='gain')
        ranked=sorted(FEATURE_COLUMNS,key=lambda f:(-gains.get(f,0.0),FEATURE_COLUMNS.index(f)))
        # Choose K using validation only; OOS remains untouched until final scoring.
        val_scores={}
        if fixed_k is None:
            for candidate_k in K_CANDIDATES:
                candidate=ranked[:candidate_k]
                vm=XGBRegressor(n_estimators=120,max_depth=3,learning_rate=.05,subsample=1,colsample_bytree=1,reg_lambda=1,objective='reg:squarederror',random_state=SEED,n_jobs=1)
                vm.fit(x.iloc[tr][candidate],y.iloc[tr])
                vp=vm.predict(x.iloc[va][candidate]); vy=y.iloc[va].to_numpy()
                val_scores[candidate_k]=float(np.sqrt(np.mean((vy-vp)**2)))
            fixed_k=min(K_CANDIDATES,key=lambda k:(val_scores[k],k))
        chosen_k=fixed_k
        selected=ranked[:chosen_k]
        forecaster=XGBRegressor(n_estimators=120,max_depth=3,learning_rate=.05,subsample=1,colsample_bytree=1,reg_lambda=1,objective='reg:squarederror',random_state=SEED,n_jobs=1)
        # Fit final predictor using train+validation after K selection; selector remains trained on train only.
        trainval=slice(a,c)
        forecaster.fit(x.iloc[trainval][selected],y.iloc[trainval])
        pred=forecaster.predict(x.iloc[te][selected]); actual=y.iloc[te].to_numpy(); naive=np.zeros_like(actual) 
        def metrics(pred):
            e=actual-pred; return float(np.mean(np.abs(e))),float(np.sqrt(np.mean(e**2)))
        nmae,nrmse=metrics(naive); xmae,xrmse=metrics(pred)
        jac=np.nan if prevset is None else jaccard(prevset,selected)
        kun=np.nan if prevset is None else kuncheva(prevset,selected,len(FEATURE_COLUMNS))
        windows.append({'window_id':wi+1,'train_start':data.date.iloc[a].isoformat(),'train_end':data.date.iloc[b-1].isoformat(),'validation_start':data.date.iloc[b].isoformat(),'validation_end':data.date.iloc[c-1].isoformat(),'test_start':data.date.iloc[c].isoformat(),'test_end':data.date.iloc[d-1].isoformat(),'n_train':b-a,'n_validation':c-b,'n_oos':d-c,'chosen_k':chosen_k,'validation_rmse_by_k':json.dumps(val_scores),'selected_features':json.dumps(selected),'jaccard_from_previous':jac,'kuncheva_from_previous':kun,'naive_mae':nmae,'naive_rmse':nrmse,'xgboost_mae':xmae,'xgboost_rmse':xrmse})
        prevset=selected
    result=pd.DataFrame(windows); RESULTS.parent.mkdir(parents=True,exist_ok=True); result.to_csv(RESULTS,index=False)
    for col in ('jaccard_from_previous','kuncheva_from_previous'):
        mask=result[col].notna()
        for error in ('naive_mae','naive_rmse','xgboost_mae','xgboost_rmse'):
            rho,p=spearmanr(result.loc[mask,col],result.loc[mask,error]) if mask.sum()>=2 else (np.nan,np.nan)
            print(f'exploratory_spearman {col} vs {error}: rho={rho}, p={p}, n={int(mask.sum())}')
    print(result.to_string(index=False)); print(f'CSV={RESULTS}')

if __name__=='__main__': main()
