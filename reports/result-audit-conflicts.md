# Result Audit — Conflicts & Anomalies

> Stage Result Audit 01 — Output 11. This report searches for discrepancies
> between code and reports, between reports, and between datasets.
> Rule applied: report the conflict, do NOT silently fix it.

## C1 — MATERIAL: `jaccard_to_next` indexing vs the frozen pairing definition

**What the frozen definition says:** pairing is `Jaccard_t → MAE_(t+1)`, where
`Jaccard_t` is the stability of the subset at window `t` against the next window.

**What the code actually computes** (`run_experiment.py:87-94, 106-108`;
`run_coinbase_robustness.py:84-90, 101-102`):

```python
if prev_selected is None:
    jac = np.nan
else:
    jac = jaccard(prev_selected, selected)   # Jaccard(S_{t-1}, S_t)
prev_selected = selected
rows.append({ ..., "jaccard_to_next": jac, ... })
```

The value stored in row `t` under `jaccard_to_next` is
`Jaccard(S_{t-1}, S_t)` — i.e. the transition **into** window `t`, despite the
column name "to_next". Verified by recomputation: 0 mismatches for both datasets
(stored row-`w` value = Jaccard(S_{w-1}, S_w)).

Then the pairing step (`run_experiment.py:124-128`) does:

```python
aligned["paired_mae_next"] = aligned["xgboost_mae"].shift(-1)
paired = aligned.dropna(subset=["jaccard_to_next", "paired_mae_next"])
```

So the realized pair is **`(Jaccard(S_{w-1}, S_w), MAE_{w+1})`**, not
`(Jaccard(S_w, S_{w+1}), MAE_{w+1})`.

**Consequences (quantified, recomputation only — no model refit):**

| Dataset | Code pairing `J_(w-1,w) → MAE_(w+1)` (reported) | Literal frozen `J_(t,t+1) → MAE_(t+1)` |
|---|---|---|
| Binance | n=20, rho = **−0.101326437456687** | n=21, rho = −0.204676160415254 |
| Coinbase | n=29, rho = **+0.185929832806481** | n=30, rho = +0.238510414077505 |

**Interpretation impact:** both variants keep the CI spanning zero (Binance
literal CI [−0.383, +0.113]; Coinbase literal CI [−0.047, +0.518]) — the
qualitative non-detection is unchanged. But the **reported point estimates and the
n_pairs (20/29)** correspond to the code's index, which is offset by one window
relative to the literal `J_t = Jaccard(S_t, S_{t+1})` reading.

**Status:** REPORTED, not fixed. This is an implementation-vs-specification
ambiguity. ChatGPT/user must decide whether:
(a) the frozen definition intended `J_{t-1,t} → MAE_{t+1}` (then the code is
correct and only the column name/summary `pairing` string is loose), or
(b) the literal `J_{t,t+1} → MAE_{t+1}` was intended (then code is off by one
window and the numbers would be n=21 / n=30).
Per the hard rules, code is authoritative for the *implementation* audit, but the
difference from the *frozen definition* is flagged here. Do not silently fix.

## C2 — NOT A CONFLICT: block-length rule differs between datasets

- Binance: single-series `b = 6.588182943772037` (`run_experiment.py:132`).
- Coinbase: `b = ceil(max(4.677412980409281, 2.8152344337664186)) = 5.0`
  (`run_coinbase_robustness.py:125-127`).

This is **explicitly mandated** by the robustness prompt §15 and documented in
`coinbase_methodology_check.md` ("Deliberate deviation (transparent, per frozen
prompt §15)"). Not a hidden conflict. Recorded for completeness.

## C3 — NOT A CONFLICT: pilot vs experiment window config

- `reports/pilot_results.csv` uses Train 730 / Valid 90 / OOS 30 / Step 30 (5 windows).
- `reports/experiment_results.csv` uses Train 730 / Valid 180 / OOS 90 / Step 90 (22 windows).

Different stages (pilot = pipeline validation; experiment = final). Explicitly
labelled in `pilot_report.md`. No conflict.

## C4 — NOT A CONFLICT: methodology docs vs executed methodology

`methodology-resolution.md`, `methodology-freeze-checklist.md`,
`methodology-evidence-audit.md`, `pre_experiment_approval.md` all say
"METHODOLOGY NOT READY FOR EXPERIMENT" and propose OOS=30/step=30 with K unset.
The executed experiment uses OOS=90/step=90 and K=10. These docs are **earlier
Stage-0B gate documents** that were superseded by the user's frozen master prompt
(the freeze-exception check recorded condition 7 not triggered). Not a conflict in
the final results; noted so ChatGPT does not mistake the earlier docs for the
frozen config. The authoritative frozen config is `experiment_config.py` +
`frozen_methodology_manifest.md`.

## C5 — Minor: summary JSON field coverage differs

- Binance `experiment_summary.json` stores `bootstrap_replications` but not the
  bootstrap seed, and does not store `median_jaccard` / RMSE means.
- Coinbase summary stores seed, median Jaccard, RMSE means, block-length parts.

Not a numeric conflict — all values are recomputable from the CSVs. Reported so
the evidence package is complete.

## Numeric cross-check (reports vs CSV) — no discrepancy found

| Quantity | Report value | CSV/summary recomputation | Match |
|---|---|---|---|
| Binance windows | 22 | 22 | ✅ |
| Binance pairs | 20 | 20 | ✅ |
| Coinbase windows | 31 | 31 | ✅ |
| Coinbase pairs | 29 | 29 | ✅ |
| Binance rho | −0.10132643745668742 | −0.101326437456687 | ✅ |
| Coinbase rho | +0.18592983280648137 | 0.185929832806481 | ✅ |
| Binance mean Jaccard | 0.368 | 0.3680207125585277 | ✅ |
| Coinbase mean Jaccard | 0.390 | 0.3897651368239604 | ✅ |
| Coinbase XGB-wins | 2/31 | 2/31 | ✅ |

## Verdict

**ONE MATERIAL CONFLICT FOUND: C1** (pairing-index vs frozen definition; reported,
not fixed). C2–C5 are transparency notes, not conflicts.

No conflicting duplicate result files. No contradictory statistic values between
the reports and the final CSVs.
