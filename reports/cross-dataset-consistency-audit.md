# Cross-Dataset Consistency Audit

> Stage Result Audit 01 — Output 8. Binance (primary) vs Coinbase (robustness).
> Each row marked SAME or DIFFERENT. DIFFERENT rows explained from ACTUAL code.

Sources: `code/experiment_config.py`, `code/run_experiment.py`,
`code/run_coinbase_robustness.py`, the two result CSVs, the two summary JSONs.

| Item | Binance | Coinbase | SAME / DIFFERENT | Explanation (from code) |
|---|---|---|---|---|
| Raw rows | 3,059 | 3,818 | DIFFERENT | different raw snapshots |
| Raw period | 2017-08-17→2025-12-31 | 2015-07-20→2025-12-31 | DIFFERENT | Coinbase history starts earlier |
| Processed rows | 2,969 | 3,728 | DIFFERENT | follows raw length; same drop rule |
| Number of windows | 22 | 31 | DIFFERENT | `build_windows` from n_rows |
| Number of pairs | 20 | 29 | DIFFERENT | n_windows − 2 (dropna rule) |
| K | 10 | 10 | SAME | `experiment_config.K` imported by both |
| Feature universe | 30 | 30 | SAME | same `FEATURE_COLUMNS` list |
| Feature formulas | `build_features` | `build_features` (reused) | SAME | Coinbase imports the same function |
| Target | ln(C_{t+1}/C_t) | ln(C_{t+1}/C_t) | SAME | same `build_features` |
| Train / Valid / OOS / Step | 730/180/90/90 | 730/180/90/90 | SAME | `experiment_config` constants |
| Selector | XGBoost Gain | XGBoost Gain | SAME | `SELECTOR_IMPORTANCE="gain"` |
| Forecaster | XGBoost | XGBoost | SAME | same `XGB_PARAMS` |
| XGBoost parameters | pilot-derived fixed | same dict | SAME | both `XGB_PARAMS` (n_est=120, depth=3, lr=0.05, sub=1, col=1, λ=1, rs=42, n_jobs=1) |
| Random seed | 42 | 42 | SAME | `SEED=42` |
| Bootstrap B | 5000 | 5000 | SAME | `BOOTSTRAP_B` |
| Bootstrap RNG | RandomState(42) | RandomState(42) | SAME | same function |
| Block length | 6.588182943772037 (single series) | 5.0 = ceil(max(4.677, 2.815)) | **DIFFERENT** | Binance = single-series auto; Coinbase = §15 both-series ceil(max) rule |
| Spearman rho | −0.10132643745668742 | +0.18592983280648137 | DIFFERENT (data) | same statistic, different data |
| Bootstrap 95% CI | [−0.5193248203679854, 0.3745795999026185] | [−0.1691804895496767, 0.437469352072282] | DIFFERENT (data) | wider for Binance despite larger block |
| CI includes zero | Yes | Yes | SAME (qualitative) | both CIs span 0 |
| mean Jaccard | 0.3680207125585277 | 0.3897651368239604 | DIFFERENT (data) | — |
| median Jaccard | 0.3333333333333333 | 0.42857142857142855 | DIFFERENT (data) | — |
| min / max Jaccard | 0.1111 / 0.6667 | 0.1765 / 0.5385 | DIFFERENT (data) | — |
| mean XGB MAE | 0.03344450115955859 | 0.025444939048928958 | DIFFERENT (data) | — |
| mean naive MAE | 0.021160566910711116 | 0.022426800349613408 | DIFFERENT (data) | — |
| mean XGB RMSE | 0.0442872110… | 0.03597381036239864 | DIFFERENT (data) | Binance RMSE mean from CSV (not in JSON) |
| mean naive RMSE | 0.0296473078… | 0.03231068659431041 | DIFFERENT (data) | — |
| Baseline | zero-return | zero-return | SAME | `actual - 0.0` |
| Pairing rule | J_t→MAE_(t+1) | J_t→MAE_(t+1) | SAME (nominal) | see conflicts C1 for realized-index caveat |
| iid p-value role | reference only | reference only | SAME | not primary inference |

## Design-level verdict

**Methodology is SAME** on every frozen design axis (features, target, K,
window config, selector, forecaster, params, seed, B, pairing rule, baseline).
Two categories of DIFFERENT:

1. **Data-driven differences** (expected): rows, periods, window/pair counts,
   Jaccard/MAE values, rho, CI. These follow from the different exchange
   datasets, not from any design change.
2. **One methodological DIFFERENT**: the **block-length rule**
   (single-series for Binance vs `ceil(max(b_stab,b_err))` for Coinbase). This is
   mandated by the robustness prompt §15 and documented in
   `coinbase_methodology_check.md`. It is transparent, not silent. See
   `result-audit-conflicts.md` item C1.

## Note on Binance median Jaccard

The Binance summary JSON does not store `median_jaccard`; it is computed here
from `experiment_results.csv` (= 0.3333333333333333). No conflict — absence in
JSON, present in CSV.
