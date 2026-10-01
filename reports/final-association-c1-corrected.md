# Final Association — C1 Pairing Index Correction

> Scope: ONE methodological correction to the association analysis — the pairing
> index only. No dataset, raw data, feature engineering, 30-feature pool, target,
> K=10, XGBoost parameters, window config, step, predictions, MAE/RMSE, Jaccard
> definition, bootstrap method, B, seed, or block-length methodology was changed.
> No forecasting artifact was modified or overwritten.
> Status: **PASS**.

## 1. Problem (confirmed by source-of-truth audit)

`jaccard_to_next` on row `r` of the result CSV stores
`Jaccard(S_{r-1}, S_r)` (verified against `selected_features`: 0 mismatches), but
the old code paired it with `MAE_{r+1}` (via `xgboost_mae.shift(-1)`). The realized
pair was therefore `(Jaccard(S_{r-1},S_r), MAE_{r+1})` — offset one window from the
frozen definition.

Frozen definition (from `experiment_config.py:50-51`):
```
J_t = Jaccard(S_t, S_{t+1})     paired with     MAE_{t+1}
```

## 2. Correct pairing (implemented)

Since `jaccard_to_next[r] = Jaccard(S_{r-1}, S_r) = J_t` with `t = r-1`, the frozen
pair `(J_t, MAE_{t+1})` is exactly the **same row `r = t+1`**:

```
(jaccard_to_next[r], xgboost_mae[r])   for r = 2 .. N   →   n_pairs = N - 1
```

This is now the implemented pairing in `code/apply_c1_pairing_correction.py`.

## 3. Recomputed results (frozen bootstrap: B=5000, seed=42)

| Dataset | n pairs | Spearman rho | Bootstrap 95% CI | CI incl. 0 | block length | rule | B | seed |
|---|---|---|---|---|---|---|---|---|
| Binance | **21** | **−0.204676160415254** | **[−0.389028, 0.115108]** | Yes | 6.643900265687148 | single-series `automatic_block_length(jaccard)` | 5000 | 42 |
| Coinbase | **30** | **+0.238510414077505** | **[−0.050828, 0.507039]** | Yes | 6.0 | `ceil(max(b_stab=5.024005054490707, b_err=2.8874134966896827))` [§15] | 5000 | 42 |

iid reference p-values (reference only, NOT the primary inference):
Binance 0.3734735602643581; Coinbase 0.20434181449570635.

Source: `reports/final-association-c1-corrected.json`; per-pair table in
`reports/final-association-c1-corrected.csv`.

## 4. Comparison with the pre-correction (preserved) values

| Dataset | Pre-C1 (offset pairing) | C1-corrected (frozen) |
|---|---|---|
| Binance | n=20, rho=−0.10132643745668742, CI [−0.519325, 0.374580] | n=21, rho=−0.204676160415254, CI [−0.389028, 0.115108] |
| Coinbase | n=29, rho=+0.18592983280648137, CI [−0.169180, 0.437469] | n=30, rho=+0.238510414077505, CI [−0.050828, 0.507039] |

The old files (`experiment_results.csv`, `coinbase_experiment_results.csv`, both
summary JSONs) are **untouched** — SHA-256 verified unchanged
(`59e0ffd8…` and `a478cf9c…`). Both corrected CIs still include zero.

## 5. Leakage verification (PASS)

- Selector trained on **TRAIN only** (`run_experiment.py:64-66`); never sees
  validation or OOS.
- Forecaster trained on **TRAIN+VALIDATION**, scored on **OOS only**.
- Pairing uses only realized per-window values: `J_t` from subsets `S_t,S_{t+1}`
  (both are train-derived selections) and `MAE_{t+1}` from OOS block `t+1`.
  No future information enters the stability term or the error term.
- Date invariants asserted: `train_start < train_end < validation_start <
  validation_end < oos_start < oos_end`, and `oos_start` monotonic increasing.
- New leakage tests: `tests/test_c1_pairing_correction.py::test_no_oos_or_validation_leak_into_selection_source`.

## 6. Assertions added (item 9)

`tests/test_c1_pairing_correction.py` (12 tests) proves:
- `x == Jaccard(S_t, S_{t+1})` and explicitly `!= Jaccard(S_{t-1}, S_t)` when they differ;
- `y == MAE_{t+1}`;
- `y != MAE_t` and `y != MAE_{t+2}` (guards were non-trivial on every row:
  Binance 21/21 vs MAE_t and 20/20 vs MAE_{t+2}; Coinbase 30/30 and 29/29);
- `n_pairs == n_windows − 1`;
- stored `jaccard_to_next[r] == Jaccard(S_{r-1}, S_r)`.

Full suite: **32 passed** (20 existing + 12 new). No existing test modified.

## 7. Artifacts

Created (new; old preserved):
- `reports/final-association-c1-corrected.csv` (`fafcf0ea…`) — per-pair, both datasets
- `reports/final-association-c1-corrected.json` (`d945b079…`) — summary
- `code/apply_c1_pairing_correction.py` (`78fe5a25…`) — correction script
- `tests/test_c1_pairing_correction.py` (`f510a651…`) — assertions

## 8. Interpretation

No new interpretation. Reported only: under the frozen definition
`J_t = Jaccard(S_t,S_{t+1}) → MAE_{t+1}`, the corrected Spearman association is
ρ=−0.2047 (Binance, n=21) and ρ=+0.2385 (Coinbase, n=30); both bootstrap 95% CIs
include zero. Primary inference remains the bootstrap CI.

## 9. Status

**PASS** — pairing index corrected to match frozen methodology; forecasting
artifacts untouched; leakage verified; assertions added; old artifacts preserved.
