# Bootstrap Implementation Audit

> Stage Result Audit 01 — Output 7. Read from ACTUAL CODE, not from reports.
> Code not modified. Line numbers refer to current files.

Files read:
- `code/bootstrap_analysis.py` (SHA `2ff74b07…`)
- `code/run_experiment.py` (SHA `e0005b19…`) — Binance caller
- `code/run_coinbase_robustness.py` (SHA `4fe862eb…`) — Coinbase caller

## Q1. Is it a real stationary bootstrap?

**Yes.** `stationary_bootstrap_pairs` (bootstrap_analysis.py:36-76) resamples
blocks of geometrically-distributed length with wrap-around, i.e. the
Politis–Romano (1994) stationary bootstrap:
- `p = 1.0 / max(b, 1.0)` (line 56)
- `length = rng.geometric(p)` (line 63)
- `idx[pos] = (start + k) % n` (line 67)

## Q2. Random generator

`numpy.random.RandomState` (legacy MT19937), line 48:
`rng = np.random.RandomState(seed)`.

## Q3. Seed

`seed=42`. Callers pass `seed=SEED` where `SEED = 42`
(`experiment_config.py:35`; `run_experiment.py:133`; `run_coinbase_robustness.py:128`).

## Q4. Replications

`B = 5000` (`BOOTSTRAP_B = 5000`, experiment_config.py:47; passed at
run_experiment.py:133 and run_coinbase_robustness.py:128).

## Q5. Is sampling done on the paired observations `(Jaccard_t, MAE_(t+1))`?

**Yes.** Both callers build the paired arrays first, then resample:
- Binance: `jx = paired["jaccard_to_next"]`, `my = paired["paired_mae_next"]`
  (run_experiment.py:127-128), then `stationary_bootstrap_pairs(jx, my, …)`.
- Coinbase: same (run_coinbase_robustness.py:119-120, 128).
- `paired_mae_next = xgboost_mae.shift(-1)` (run_experiment.py:125;
  run_coinbase_robustness.py:116).

## Q6. Do pairs stay intact when resampled?

**Yes.** A single index vector `idx` is built (lines 59-68) and applied to BOTH
series jointly: `spearmanr(x[idx], y[idx])` (line 70). The two series are never
shuffled independently.

## Q7. Are stability and error resampled together?

**Yes** — same `idx` for `x[idx]` and `y[idx]` (line 70).

## Q8. How is block length computed?

`automatic_block_length(x, random_state=42)` (bootstrap_analysis.py:14-33):
- max_lag = `floor(n**(1/3))` (line 23)
- autocovariance via `_acvf` (lines 7-11)
- `ss = sum(acf[1:]**2)` (line 27)
- `b = (2*pi*ss)**(-1/3) * n**(1/3)` (line 30) — Politis–White (2004)
- `b *= 4/3` (line 32) — Patton–Politis–White (2009) correction
- floor at 1.0 (line 33)

## Q9–13. Is b from both series then `ceil(max(...))`, or one series? Values?

**The two datasets DIFFER — this is the one methodological divergence:**

**Binance (single series):**
- `b_opt = automatic_block_length(jx, random_state=SEED)` (run_experiment.py:132)
- **b_stability = 6.588182943772037** (the only block length used).
- No `b_error` is computed for Binance. Final **b = 6.588182943772037**.
- Source: `reports/experiment_summary.json` → `bootstrap_block_length`.

**Coinbase (both series, §15 rule):**
- `b_stab = automatic_block_length(jx, SEED)` → **4.677412980409281**
- `b_err  = automatic_block_length(my, SEED)` → **2.8152344337664186**
- `b_opt  = float(np.ceil(max(b_stab, b_err)))` → **5.0**
- (run_coinbase_robustness.py:125-127; summary JSON fields
  `block_length_stability`, `block_length_error`, `block_length`.)

So: **Q9 (ceil(max)) is TRUE for Coinbase only; Q10 (single series) is TRUE for
Binance.** This is a documented, prompt-mandated difference (robustness prompt §15),
not a hidden change — see `result-audit-conflicts.md` item C1.

## Q14. Is the CI percentile 95%?

**Yes.** `alpha = (1-ci_level)/2`, `ci_level=0.95`; CI = percentiles
`100*alpha` and `100*(1-alpha)` of the bootstrap distribution
(bootstrap_analysis.py:72-74). Percentile CI, not BCa.

## Q15. Hidden filtering / dropna after pairing?

**Explicit, not hidden.** Each caller does
`paired = aligned.dropna(subset=["jaccard_to_next", "paired_mae_next"])`
(run_experiment.py:126; run_coinbase_robustness.py:118). This drops:
- row 1 (no previous subset → `jaccard_to_next = NaN`), and
- the last row (no `MAE_(t+1)`).
Net effect: `n_pairs = n_windows − 2` (Binance 22→20; Coinbase 31→29).
No other filtering, no outlier removal.

## Q16. Spearman via `scipy.stats.spearmanr` or custom?

**`scipy.stats.spearmanr`** — imported at run_experiment.py:15 and
run_coinbase_robustness.py:15; used at line 130 / 122, and inside the bootstrap at
bootstrap_analysis.py:69-70.

## Q17. Is the iid p-value used for the primary decision?

**No.** The iid Spearman p-value is labelled reference-only
(`iid_reference_pvalue` in Coinbase summary; `spearman_p` in Binance summary).
The primary decision is based on whether the bootstrap CI includes zero
(run_coinbase_robustness.py:148-153). Binance does not compute a bootstrap-based
decision string but its reported CI is the primary inference.

## Q18. Is bootstrap used only for the CI?

**Yes, in the sense that matters:** the bootstrap distribution is used solely to
form the 95% percentile CI (and a `bootstrap_mean`, informational). No bootstrap
p-value, no bootstrap-based hypothesis test is computed.

## Summary table

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Real stationary bootstrap | YES | bootstrap_analysis.py:56-67 |
| 2 | RNG | `np.random.RandomState` (MT19937) | :48 |
| 3 | Seed | 42 | experiment_config.py:35 |
| 4 | Replications | 5000 | experiment_config.py:47 |
| 5 | Sampling on pairs | YES | run_experiment.py:127-128 |
| 6 | Pairs intact | YES (shared idx) | bootstrap_analysis.py:70 |
| 7 | Joint resample | YES | bootstrap_analysis.py:70 |
| 8 | Block length method | Politis–White + Patton ×4/3 | bootstrap_analysis.py:14-33 |
| 9 | `ceil(max(b_stab,b_err))` | Coinbase YES / Binance NO | run_coinbase_robustness.py:125-127 |
| 10 | Single series | Binance YES / Coinbase NO | run_experiment.py:132 |
| 11 | b_stability | Binance 6.588182943772037 / Coinbase 4.677412980409281 | summary JSONs |
| 12 | b_error | Binance not computed / Coinbase 2.8152344337664186 | summary JSONs |
| 13 | Final b | Binance 6.588182943772037 / Coinbase 5.0 | summary JSONs |
| 14 | Percentile 95% CI | YES | bootstrap_analysis.py:72-74 |
| 15 | Hidden dropna | No — explicit | run_experiment.py:126 |
| 16 | Spearman impl | scipy.stats.spearmanr | run_experiment.py:15,130 |
| 17 | iid p used for decision | NO (reference only) | coinbase summary field name |
| 18 | Bootstrap only for CI | YES | bootstrap_analysis.py:72-76 |

## Code snippets

```python
# bootstrap_analysis.py:56-70
p = 1.0 / max(float(b), 1.0)
stats = np.empty(B)
for i in range(B):
    idx = np.empty(n, dtype=int); pos = 0
    while pos < n:
        start = rng.randint(0, n)
        length = rng.geometric(p)
        for k in range(length):
            if pos >= n: break
            idx[pos] = (start + k) % n
            pos += 1
    rho, _ = spearmanr(x[idx], y[idx])   # joint paired resample
    stats[i] = float(rho)
```

```python
# run_coinbase_robustness.py:124-129  (§15 both-series rule)
b_stab = automatic_block_length(jx, random_state=SEED)
b_err  = automatic_block_length(my, random_state=SEED)
b_opt  = float(np.ceil(max(b_stab, b_err)))
boot = stationary_bootstrap_pairs(jx, my, b=b_opt, B=BOOTSTRAP_B, seed=SEED,
                                  ci_level=CONFIDENCE_LEVEL)
```

```python
# run_experiment.py:132-134  (Binance single-series)
b_opt = automatic_block_length(jx, random_state=SEED)
boot = stationary_bootstrap_pairs(jx, my, b=b_opt, B=BOOTSTRAP_B, seed=SEED,
                                  ci_level=CONFIDENCE_LEVEL)
```
