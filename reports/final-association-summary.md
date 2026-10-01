# Final Association Summary — C1 Corrected (FINAL SOURCE)

> This is the ONLY association result to use for final analysis. It uses the
> C1-corrected pairing. The older association results (offset pairing) are
> **DO NOT USE** (see `reports/master-results-evidence-manifest.md`).
> Source: `reports/final-association-c1-corrected.json` and
> `reports/final-association-c1-corrected.csv`.

## Frozen pairing definition

```
J_t = Jaccard(S_t, S_{t+1})        paired with        MAE_{t+1}
```

i.e. the Jaccard overlap between the selected feature subset of window `t` and
window `t+1` is paired with the OOS MAE of window `t+1`. Implemented as the
same-row pair `(jaccard_to_next[r], xgboost_mae[r])` for `r = 2..N`, because
`jaccard_to_next[r] = Jaccard(S_{r-1}, S_r)` (= `J_t`, `t = r-1`) and
`xgboost_mae[r] = MAE_{t+1}`.

## Binance

| Field | Value |
|---|---|
| n (pairs) | 21 |
| Spearman rho | −0.20467616041525366 |
| Bootstrap 95% CI | [−0.38902802319377583, 0.11510760123127348] |
| CI includes zero | yes |
| Block length | 6.643900265687148 |
| Block-length rule | single-series `automatic_block_length(jaccard)` |
| B | 5000 |
| Seed | 42 |
| iid reference p (reference only) | 0.3734735602643581 |

## Coinbase

| Field | Value |
|---|---|
| n (pairs) | 30 |
| Spearman rho | 0.23851041407750545 |
| Bootstrap 95% CI | [−0.05082809846734598, 0.5070390505626119] |
| CI includes zero | yes |
| Block length | 6.0 = ceil(max(5.024005054490707, 2.8874134966896827)) |
| Block-length rule | `ceil(max(b_stability, b_error))` per frozen §15 |
| B | 5000 |
| Seed | 42 |
| iid reference p (reference only) | 0.20434181449570635 |

## Notes

- Primary inference is the stationary-bootstrap 95% CI; the iid Spearman p-value
  is reference only (residual autocorrelation is not modeled by it).
- Per-pair table with `t`, `jaccard_t`, `kuncheva_t`, `mae_t_plus_1`,
  `rmse_t_plus_1`, `oos_start/end_{t+1}`: `reports/final-pairing-evidence.csv`.
- No new interpretation is added here beyond reporting the corrected numbers.
