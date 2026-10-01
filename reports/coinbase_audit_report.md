# Coinbase Robustness — Leakage & Validity Audit

Independent audit of the Coinbase BTC-USD robustness run.
Methodology is frozen; this audit verifies faithful execution only.

## 1. Leakage checklist (frozen prompt §21)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Target definition correct | **PASS** | `target = ln(Close[t+1]/Close[t])`; test_target_definition |
| 2 | Target excluded from features | **PASS** | `target` not in 30 FEATURE_COLUMNS; test_exactly_30_features |
| 3 | Features causal | **PASS** | trailing-only windows; test_feature_causality (append/remove future rows) |
| 4 | No future imputation | **PASS** | `build_features` uses no bfill/centered windows; warm-up rows dropped |
| 5 | Selector sees TRAIN only | **PASS** | `sel.fit(x.iloc[a:b], y.iloc[a:b])` |
| 6 | Validation not used for feature selection | **PASS** | selector fit range = `[a,b)` excludes validation `[b,c)` |
| 7 | OOS not used for selection | **PASS** | selector never sees `[c,d)` |
| 8 | Forecaster sees TRAIN+VALID only | **PASS** | `fc.fit(x.iloc[a:c], ...)` |
| 9 | OOS only used for final scoring | **PASS** | `fc.predict(x.iloc[c:d])` after fit; no refit on OOS |
| 10 | Jaccard only between adjacent subsets | **PASS** | `jaccard(prev_selected, selected)` adjacent windows only |
| 11 | Jaccard paired to NEXT window MAE | **PASS** | `paired_mae_next = xgboost_mae.shift(-1)`; test_jaccard_paired_to_next_mae |
| 12 | No OOS-based K selection | **PASS** | K=10 constant, never read from results |
| 13 | No OOS-based hyperparameter tuning | **PASS** | fixed `XGB_PARAMS`; no search |
| 14 | Bootstrap resamples paired observations | **PASS** | `stationary_bootstrap_pairs(jx, my)` joint resampling; test_bootstrap_paired_resampling |
| 15 | Bootstrap block length is automatic | **PASS** | Politis-White + Patton; `ceil(max(b_stab,b_err))=5.0` |
| 16 | No data replacement after seeing results | **PASS** | single frozen snapshot; raw SHA verified against audit metadata |

**All 16 checks: PASS.**

## 2. Mathematical validity

| Item | Check | Result |
|---|---|---|
| Target | `ln(C_{t+1}/C_t)`, finite, no NaN after warm-up | PASS |
| Jaccard known-set | `{a,b,c,d}` vs `{c,d,e,f}` = 2/6 | PASS |
| Kuncheva known-set | `{a,b,c,d}` vs `{c,d,e,f}`, n=10 → 4/24 | PASS |
| Window boundaries | b=a+730, c=b+180, d=c+90 | PASS |
| OOS non-overlap | `c2 = c1+90`, `c2 >= d1` | PASS |
| Block length ≥ 1 | guaranteed by floor | PASS |

## 3. Statistical validity

- **Primary inference** = stationary bootstrap (paired), B=5000, seed=42, 95% CI.
  The iid Spearman p-value is reported as **reference only** (prompt §14) and is
  NOT used as the significance claim.
- **Dependence** handled: paired stationary bootstrap with automatic block length
  accounts for serial dependence and overlapping training histories.
- **Low statistical power acknowledged**: n = 29 paired windows → wide CI.

## 4. Data audit (raw Coinbase snapshot)

| Check | Result |
|---|---|
| File present (`data/raw/coinbase_btc_usd_86400.parquet`) | PASS |
| Rows = 3,818 (matches audit metadata) | PASS |
| Period 2015-07-20 → 2025-12-31 | PASS |
| Timestamps monotonic & unique | PASS |
| Duplicates | 0 |
| Missing days / gaps > 1 day | 0 |
| NaN / non-finite | 0 |
| OHLC validity (high≥low, open/close within range) | PASS |
| Volume non-negative | PASS |
| SHA-256 vs metadata (`c5d47d5f…48dc44`) | **MATCH** |

## 5. Verdict

**AUDIT RESULT: PASS** — no leakage, no invalid math, no unreproducible step detected.
No `freeze_exception_report.md` required.
