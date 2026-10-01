# Figure Data Inventory

> Documents the data source for each figure. No new figure design is introduced.
> All figures live in `reports/figures/`.

## A. Jaccard per transition

- Source data: `reports/result-table-{binance,coinbase}-full.csv` column `jaccard`
  (= `jaccard_to_next`), or `reports/final-pairing-evidence.csv` column `jaccard_t`.
- Existing figures: `reports/figures/jaccard_stability.png` (Binance),
  `reports/figures/coinbase_jaccard_stability.png` (Coinbase).
- Generator: `code/generate_figures.py`, `code/generate_coinbase_figures.py`.

## B. Kuncheva per transition

- Source data: `reports/result-table-*-full.csv` column `kuncheva`
  (= `kuncheva_to_next`), or `reports/final-pairing-evidence.csv` column `kuncheva_t`.
- No dedicated standalone figure exists; data available for plotting.

## C. XGBoost MAE per OOS window

- Source data: `reports/result-table-*-full.csv` column `mae_xgb`
  (= `xgboost_mae`).
- Existing figures: `reports/figures/forecast_error_comparison.png` (Binance),
  `reports/figures/coinbase_forecast_error_comparison.png` (Coinbase) — these plot
  XGBoost vs naive error per window.

## D. Naive MAE per OOS window

- Source data: `reports/result-table-*-full.csv` column `mae_naive` (= `naive_mae`).
- Existing figures: same `forecast_error_comparison.png` figures as (C).

## E. Feature selection frequency

- Source data: `reports/feature-selection-frequency.csv`
  (also `reports/feature-selection-window-matrix.csv`).
- Summary table: `reports/feature-selection-frequency-summary.md`.
- No standalone figure; data available for plotting.

## F. Jaccard vs next-window MAE

- Source data: `reports/final-pairing-evidence.csv` columns `jaccard_t` and
  `mae_t_plus_1` (C1-corrected pairing).
- Existing figures: `reports/figures/stability_vs_error_scatter.png` (Binance),
  `reports/figures/coinbase_stability_vs_error_scatter.png` (Coinbase).
- **Caveat:** the existing scatter figures were generated BEFORE the C1 pairing
  correction and may use the offset pairing. For final analysis, regenerate from
  `final-pairing-evidence.csv` (do not reuse the old scatter for inference).

## G. Rolling / window timeline

- Source data: `reports/result-table-*-full.csv` columns `window`,
  `train_start`, `train_end`, `validation_start/end`, `oos_start/end`.
- No standalone figure; data available for a window-timeline plot.

## Figure files present (`reports/figures/`)

| File | Dataset | Panels |
|---|---|---|
| `jaccard_stability.png` | Binance | A |
| `forecast_error_comparison.png` | Binance | C, D |
| `stability_vs_error_scatter.png` | Binance | F (pre-C1 caveat) |
| `coinbase_jaccard_stability.png` | Coinbase | A |
| `coinbase_forecast_error_comparison.png` | Coinbase | C, D |
| `coinbase_stability_vs_error_scatter.png` | Coinbase | F (pre-C1 caveat) |
