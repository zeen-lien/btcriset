# Gap Evidence Matrix — Temporal Feature Stability ↔ OOS Error

**Gap tested:** Dalam literatur terverifikasi, adakah studi Bitcoin forecasting yang mengukur temporal feature-subset stability antar-window, memiliki OOS error per window, lalu secara eksplisit menguji hubungan stability dengan error yang bersesuaian?

| Paper | Domain | FS temporal? | Stability metric? | OOS error? | Explicit stability↔OOS error? | Bitcoin? | Impact | Evidence / confidence |
|---|---|---:|---:|---:|---:|---:|---|---|
| Bysik & Ślepaczuk 2026, arXiv:2606.00060v1 | BTC trading hourly | YES | YES, Jaccard diagnostic | YES (OOS trading outcomes; forecasting metrics in paper) | NOT FOUND in full-text; Jaccard in Appendix B.2 Table B.23 only | YES | Very close comparator; narrowly does not kill based on inspected full text | PDF extracted 135,326 chars, Appendix B.2; HIGH |
| Barak & Parvini 2023, DOI 10.1002/fut.22453 | BTC price drivers | Dynamic FS | UNKNOWN pending full text | UNKNOWN | UNKNOWN | YES | Kills dynamic-FS novelty; no evidence yet that it tests stability↔OOS error | Crossref metadata + prompt-supplied claim; MEDIUM metadata / LOW methods |
| Youssefi et al. 2025, DOI 10.32604/cmc.2025.063218 | Crypto forecasting | YES, FS + walk-forward | Not reported in extracted publisher text | YES | Not identified in available article extract | YES, BTC/USDT | Kills FS+crypto+WF novelty; narrow gap not killed on current evidence | Publisher text partial; MEDIUM |
| Elmakias et al. 2026, DOI 10.3390/math14132372 | General ML methodology | Resampling | Stability/recurrence profiles | Held-out predictive performance | General stability-performance comparison likely; exact method UNKNOWN pending full-text read | NO | Kills broad claim stability never linked to predictive performance; not BTC temporal study | DOI + publisher metadata; LOW methods |
| Lazebnik & Rosenfeld 2024, DOI 10.1007/s10472-024-09936-8 | Feature selection methodology | Data drift/stability definitions | New stability definition | N/A | N/A | NO | Requires careful metric justification; no direct BTC overlap known | Crossref metadata; LOW methods |
| WinnowML 2021/2022 | Time-based systems | Stable FS | Stability method | Prediction accuracy | Likely connected to accuracy; exact relationship UNKNOWN | NO | Potential conceptual overlap outside finance; full text needed | Citation/source pending; LOW |
| Lee & Cai 2026 | Financial ML | Moving-window importance claimed | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Must verify; potential dynamic relevance counter-evidence | Citation/source pending; LOW |

## Current gap verdict
**PARTIALLY SURVIVES / LOW–MEDIUM CONFIDENCE; NOT FINAL.** Bysika full text directly confirms Jaccard temporal stability measurement but located it as a diagnostic in Appendix B.2; scanned text has no explicit relationship test between Jaccard and corresponding OOS forecast error. This does not establish that no other study did it. Elmakias 2026 may already connect stability and predictive performance in general ML, so gap must stay domain-specific and must be revised after full-text review. Barak, Youssefi, WinnowML, and Lee & Cai remain incomplete audits.

## Exact distinction
- **Fact:** Bysika calculates adjacent-fold Jaccard for selected TA feature sets; mean 0.673, range 0.333–1.000 (Appendix B.2, Table B.23).
- **Fact about inspected text:** no explicit correlation/regression/association between this Jaccard series and corresponding OOS forecasting error was found by targeted full-text search; this is a bounded negative search result, not proof of absence everywhere.
- **Inference:** The narrow stability↔OOS-error question appears distinct from Bysika's trading-performance objective.
- **Gap claim:** provisional only until kill-test and full-text review of nearest methodological papers finish.

## Files
Machine-readable matrix: `gap-evidence-matrix.csv`.
Detailed paper audit: `nearest-prior-work.md`.
