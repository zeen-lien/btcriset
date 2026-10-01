# Research Master — Temporal Feature-Subset Stability ↔ OOS Forecasting Error (Bitcoin)
> Protocol v2.0 | PHASE 0 — Research Validation | 2026-09-29
>
> **HISTORICAL SNAPSHOT (Phase 0).** This document records the *candidate/exploratory*
> state before the methodology was frozen. Everything below marked "candidates",
> "NOT locked", or "OPEN" was **superseded** by the final experiment. In particular,
> the final forecasting model is **XGBoost** (NOT PatchTST); see
> `docs/research/research-design.md` §7 and `reports/frozen_methodology_manifest.md`
> for the frozen protocol, and `README.md` for final results. Keep this file for the
> research history only.

## 1. Current Research Problem
[EVIDENCE-SYNTHESIS] Literatur BTC forecasting menunjukkan feature selection sudah banyak dilakukan (Barak 2023, Youssefi 2025, Hafid 2024, Bysika 2026), termasuk dynamic/temporal feature selection. Namun, belum teridentifikasi secara memadai dalam literatur yang diaudit penelitian yang menjadikan **perubahan temporal feature-subset stability** sebagai variabel analitis dan secara eksplisit menguji hubungannya dengan variasi OOS forecasting error.

## 2. Current Research Questions
**RQ Utama:** Apakah terdapat hubungan antara temporal feature-subset stability dan forecasting error pada periode out-of-sample Bitcoin?

**RQ1:** Bagaimana kestabilan subset fitur hasil feature selection berubah pada successive temporal windows dalam forecasting Bitcoin?

**RQ2:** Apakah perubahan temporal feature-subset stability berhubungan dengan variasi forecasting error pada periode out-of-sample yang bersesuaian?

**RQ3 (opsional):** Apakah hubungan tersebut tetap terlihat ketika digunakan baseline/model alternatif?

## 3. Current Hypothesis
[HYPOTHESIS] H1: Terdapat hubungan antara temporal feature-subset stability dan forecasting error pada periode out-of-sample Bitcoin.

Semua hasil valid: stability↑+error↓, stability↑+error↑, tidak ada hubungan signifikan, hubungan hanya pada kondisi tertentu, hubungan tidak konsisten antar-window.

## 4. Current Gap Status
**STATUS:** PROVISIONALLY LOCKED — menunggu kill-test segar (Phase 0 Step 6)

**Wording:** "Belum teridentifikasi secara memadai dalam literatur yang telah diaudit penelitian pada Bitcoin forecasting yang menjadikan perubahan temporal feature-subset stability antar-window sebagai variabel analitis dan secara eksplisit menguji hubungannya dengan variasi forecasting error pada periode out-of-sample yang bersesuaian."

**REJECTED claims:**
- "Dynamic FS pada Bitcoin belum pernah dilakukan" → KILLED (Barak 2023)
- "FS + WF pada crypto belum ada" → KILLED (Youssefi 2025)
- "Jaccard pada BTC belum pernah" → KILLED (Bysika 2026)
- "Feature stability belum dihubungkan dengan predictive performance" → KILLED secara umum (Elmakias 2026) tapi belum di domain BTC temporal forecasting

## 5. Literature Status
### 5.1 Papers FULL-TEXT DIBACA + DIANALISIS (dari fase sebelumnya)
| # | Paper | Tahun | Status | Relevansi baru |
|---|---|---|---|---|
| P1 | Aygün & Kabakçı | 2021 | FULL-TEXT | Baseline lemah; no FS; no stability |
| P2 | Chen (JRFM) | 2023 | FULL-TEXT (MIXED) | RF importance tapi mixed input; no stability |
| P3 | Zhao et al | 2019 | FULL-TEXT (MIXED) | Rolling monthly; no stability metric |
| P4 | Mubarak | 2026 | FULL-TEXT | BO indikator; no stability; satu split |
| P5 | Islas & García-Medina | 2025 | FULL-TEXT | BTC-only; no FS stability; no WF |
| P6 | Hafid et al | 2024 | FULL-TEXT | chi2 top-8; POTENTIAL RISK leakage; no stability |
| P7 | Samson et al | 2025 | FULL-TEXT | RFE; no stability |
| P8 | Vikas et al | 2025 | FULL-TEXT (LEMAH) | Bukti terlalu tipis |
| P9 | Bysika & Ślepaczuk | 2026 | FULL-TEXT | **NEAREST PRIOR WORK** — Jaccard diagnostic, TIDAK korelasi dgn error |
| P10 | Baquero (survei) | 2026 | FULL-TEXT | Standar baseline/WF; Puoti abstract-only |
| P11 | Deprez & Frömmel | 2024 | FULL-TEXT | Rules + OOS + cost; bukan ML FS |
| P12 | Huang et al | 2019 | BATCH RECORD | 124 TI; butuh verifikasi ulang |

### 5.2 Papers WAJIB BACA (dari Protocol v2.0)
| Paper | DOI | Status | Priority |
|---|---|---|---|
| Barak & Parvini 2023 | 10.1002/fut.22453 | DOI VERIFIED, full-text BELUM (Wiley paywall) | CRITICAL |
| Youssefi et al 2025 | 10.32604/cmc.2025.063218 | DOI VERIFIED, full-text BELUM | CRITICAL |
| Lazebnik & Rosenfeld 2024 | 10.1007/s10472-024-09936-8 | DOI VERIFIED, full-text BELUM | HIGH |
| Elmakias et al 2026 | 10.3390/math14132372 | DOI VERIFIED, full-text BELUM | HIGH |
| Peng et al 2021 | 10.1016/j.mlwa.2021.100060 | DOI VERIFIED, full-text BELUM | MEDIUM |
| PatchTST (Nie et al 2023) | arXiv:2211.14730 | VERIFIED | MODEL |
| iTransformer (Liu et al 2024) | arXiv:2310.06625 | VERIFIED | OPTIONAL MODEL |
| Lee & Cai 2026 | BELUM VERIFIKASI | BELUM | HIGH |
| WinnowML 2021/2022 | BELUM VERIFIKASI | BELUM | MEDIUM |
| Tripathi & Sharma 2023 | 10.1007/s10614-022-10325-8 | DOI VERIFIED | MEDIUM |

## 6. Dataset Status (Phase 0 baseline — NOT FINAL)
- Binance BTC/USDT: kandidat yang pernah disaring; source REST public, limit 1000/req, pagination teruji parsial, ~3330 daily pada audit lama. Candidate only; belum dipilih. Snapshot/versioning tak terjamin → pin retrieval + raw snapshot wajib.
- Coinbase BTC/USD: kandidat robustness; endpoint perlu chunking, full-history end-to-end belum diverifikasi. Candidate only; belum dipilih.
- Yahoo BTC-USD: candidate; audit sebelumnya 4395 daily namun agregasi CCC/adjclose belum terjelaskan. Tidak ditolak permanen; provenance perlu audit.
- Exact provider, exchange, interval, period, source-role (primary/robustness): UNKNOWN. Protokol v2.0 §7/§16 mengharuskan keputusan setelah gate.

## 7. Method Status (candidates, NOT locked)
| Component | Candidate(s) | Status | Novelty? |
|---|---|---|---|
| Domain | Bitcoin forecasting | CORE DIRECTION LOCKED, masih dapat direvisi bila evidence/data gagal | NO |
| Feature pool | OHLCV / price-derived pool | UNKNOWN | NO |
| Feature selection | XGBoost importance, MI, RFE, permutation | OPEN CANDIDATES | NO |
| Stability metric | Jaccard, Kuncheva, alternatives | OPEN CANDIDATES | NO |
| Forecasting model | PatchTST, XGBoost, alternatives | OPEN CANDIDATES | NO |
| Baseline | Naive/persistence, XGBoost | OPEN CANDIDATES | NO |
| Validation | Rolling/expanding walk-forward | PRINCIPLE: temporal/OOS LOCKED; exact design OPEN | NO |
| Target | next-period log return | UNKNOWN; candidate only | NO |
| **CONTRIBUTION** | **Stability↔corresponding OOS error analysis** | **PROVISIONAL GAP CANDIDATE; kill-test pending** | **Not claimed as novelty until audit** |

## 8. Experiment Status
BELUM DIMULAI. Menunggu Phase 0 validation + Phase 1 design.

## 9. Open Questions
1. Apakah kill-test menemukan paper yang sudah lakukan stability↔error di BTC? → MENUNGGU
2. Apakah Bysika sudah korelasikan Jaccard dengan OOS error? → MENUNGGU deep audit
3. Berapa jumlah temporal windows yang feasible dengan ~3000 daily obs? → BELUM HITUNG
4. Apakah PatchTST justified vs XGBoost saja sebagai forecaster? → BELUM EVALUASI
5. Berapa K optimal untuk top-K feature selection? → BELUM (sensitivity analysis)
6. Window overlap → efek pada independence asumsi statistik → BELUM AUDIT

## 10. Risks
| Risk | Severity | Mitigation |
|---|---|---|
| Gap sudah terjawab paper lain | CRITICAL | Kill-test + deep audit |
| Jumlah windows terlalu kecil untuk statistik | HIGH | Hitung sebelum design |
| Stability↔error tidak ada hubungan | MEDIUM | Negative result valid |
| PatchTST overkill untuk daily BTC | MEDIUM | Coba XGBoost dulu |
| Coinbase data insufficient untuk robustness | MEDIUM | Full audit sebelum commit |

## 11. Decisions
Lihat `research-decisions.md`

## 12. Results
BELUM ADA

## 13. Next Actions
1. ✅ Struktur proyek dibuat
2. ✅ Paper library disalin
3. ⏳ Kill-test segar (12 search) — DELEGATED
4. ⏳ Deep audit Bysika 8 pertanyaan — DELEGATED
5. ⬜ Baca full-text Elmakias 2026 (MDPI OA)
6. ⬜ Baca full-text Lazebnik 2024
7. ⬜ Baca full-text Youssefi 2025
8. ⬜ Cari + baca Lee & Cai 2026
9. ⬜ Cari + baca WinnowML
10. ⬜ Tulis gap-evidence-matrix.csv
11. ⬜ Tulis PHASE 0 REPORT
