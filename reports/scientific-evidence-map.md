# Scientific Evidence Map (evidence-only)

> Stage Result Audit 01 — Output 10. No new interpretation. Each candidate claim
> is marked SUPPORTED / NOT SUPPORTED by an existing artifact, with the exact value
> and file. Words like "significant", "causes", "affects", "better", "no
> relationship" are deliberately avoided unless literally defined by the artifact.

| # | Claim candidate | Supported by artifact? | Evidence file | Exact value |
|---|---|---|---|---|
| 1 | Feature subset changes between windows | **SUPPORTED** | `reports/experiment_results.csv`, `reports/coinbase_experiment_results.csv` | Jaccard < 1 in all transitions (max 0.6667 Binance, 0.5385 Coinbase) |
| 2 | Binance Jaccard mean = 0.368 | **SUPPORTED** | `reports/experiment_summary.json` (`mean_jaccard`); recomputed from CSV | 0.3680207125585277 |
| 3 | Binance Spearman = −0.1013 | **SUPPORTED** | `reports/experiment_summary.json` (`spearman_rho`) | −0.10132643745668742 |
| 4 | Binance bootstrap CI includes zero | **SUPPORTED** | `reports/experiment_summary.json` (`bootstrap_ci_lower/upper`) | [−0.5193248203679854, 0.3745795999026185] |
| 5 | Coinbase Spearman = +0.1859 | **SUPPORTED** | `reports/coinbase_experiment_summary.json` (`primary_spearman_rho`) | 0.18592983280648137 |
| 6 | Coinbase bootstrap CI includes zero | **SUPPORTED** | `reports/coinbase_experiment_summary.json` (`bootstrap_ci_lower/upper`) | [−0.1691804895496767, 0.437469352072282] |
| 7 | Point estimate changes sign across datasets | **SUPPORTED** | both summary JSONs | Binance −0.1013 vs Coinbase +0.1859 |
| 8 | XGB mean MAE higher than naive on Binance | **SUPPORTED** | `reports/experiment_summary.json`; CSV columns | XGB 0.03344450115955859 > naive 0.021160566910711116 |
| 9 | XGB mean MAE higher than naive on Coinbase | **SUPPORTED** | `reports/coinbase_experiment_summary.json`; CSV columns | XGB 0.025444939048928958 > naive 0.022426800349613408 |
| 10 | XGB wins only 2 of 31 Coinbase windows (MAE) | **SUPPORTED** | `reports/coinbase_experiment_results.csv` (per-window `xgboost_mae` < `naive_mae`) | wins = 2 (windows 4 and 20), losses = 29, ties = 0 |

## Claims that are NOT directly supported as stated (flag for ChatGPT)

| Candidate phrasing | Status | Reason |
|---|---|---|
| "No relationship between stability and error" | **NOT SUPPORTED as stated** | Artifacts support only "95% bootstrap CI includes zero in these samples" (non-detection). The phrase asserts absence. |
| "Feature stability does not affect error" | **NOT SUPPORTED** | No causal/effect estimate; correlation CI includes zero only. |
| "XGBoost is better/worse" | **NOT a research conclusion** | Table only records which mean is numerically lower; no test of forecast superiority is defined in the frozen design. |
| "Binance result is significant / H0 proven" | **NOT SUPPORTED** | p_iid is reference-only; CI includes zero. |

## Exact values verified by recomputation during this audit

- Binance n_pairs = 20; Coinbase n_pairs = 29.
- Binance rho recomputed from CSV = −0.101326437456687 (matches summary).
- Coinbase rho recomputed from CSV = 0.185929832806481 (matches summary).
- Binance "same-row" pairing variant would give rho −0.2047 (n=21); Coinbase
  +0.2385 (n=30). **The reported values use the code's `shift(-1)` pairing.**
  See `result-audit-conflicts.md` C1.

## Provenance rule applied

Every SUPPORTED value above is read from a FINAL artifact (CSV or summary JSON)
or recomputed from the FINAL CSV. No value comes from a narrative-only report.
