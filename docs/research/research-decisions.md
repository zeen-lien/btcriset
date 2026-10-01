# Research Decisions Log

## D001 — Research Direction Shift
- **DATE:** 2026-09-29
- **DECISION:** Arah penelitian bergeser dari "leakage-aware pipeline evaluation" ke "temporal feature-subset stability ↔ OOS forecasting error"
- **QUESTION:** Apa fokus kontribusi penelitian?
- **EVIDENCE:** Protocol v2.0 dari user; Phase 2 problem candidates; Bysika 2026 sudah tutup gap luas WF/cost
- **ALTERNATIVES:** (1) Audit leakage pipeline — risiko: kontribusi menyusut jadi konfirmasi. (2) Cost-aware evaluation — risiko: Bysika sudah lakukan. (3) Stability↔error — gap belum teridentifikasi di literatur yang diaudit
- **WHY REJECTED:** Alt 1 & 2 overlap terlalu besar dengan Bysika 2026
- **CONFIDENCE:** MEDIUM — menunggu kill-test
- **IMPACT:** Mengubah seluruh research question, target analisis, dan kontribusi
- **SOURCE:** Master Research Control Prompt (user), Protocol v2.0 (user)

## D002 — Trading/Profit OUT OF SCOPE
- **DATE:** 2026-09-29
- **DECISION:** Penelitian ini forecasting research, BUKAN trading research. Tidak ada klaim profit/strategi.
- **QUESTION:** Apakah cost-aware trading evaluation diperlukan?
- **EVIDENCE:** Protocol v2.0 §16 LOCKED OUT OF SCOPE; Bysika 2026 sudah lakukan cost-aware trading evaluation
- **ALTERNATIVES:** Sertakan evaluasi trading sebagai robustness — REJECTED karena bukan RQ
- **CONFIDENCE:** HIGH
- **IMPACT:** Menghilangkan PC#2 (forecast→biaya) dari research master lama
- **SOURCE:** Protocol v2.0 §16

## D003 — Target Variable Candidate
- **DATE:** 2026-09-29
- **DECISION:** Target PROVISIONALLY LOCKED = next-period log return r(t+1) = ln(Close(t+1)/Close(t))
- **QUESTION:** Target apa yang paling sesuai untuk RQ stability↔error?
- **EVIDENCE:** Protocol v2.0 §14-15; return lebih informatif dari level harga untuk evaluasi perubahan relatif; avoid non-stationarity
- **ALTERNATIVES:** Price level — rejected (non-stationary, skala dominasi); direction — rejected (binary loss info kurang untuk korelasi kontinu stability↔error)
- **CONFIDENCE:** MEDIUM — perlu validasi setelah data audit
- **IMPACT:** Menentukan metrik error (MAE/RMSE on returns, bukan level)
- **SOURCE:** Protocol v2.0 §14

## D004 — Dataset Primary Candidate
- **DATE:** 2026-09-29
- **DECISION:** Binance BTC/USDT daily PROVISIONALLY LOCKED sebagai primary; Coinbase BTC/USD daily sebagai robustness
- **QUESTION:** Dataset mana yang memenuhi data requirements?
- **EVIDENCE:** Phase 2 screening: Binance 9 PASS/4 UNCLEAR/0 FAIL; 12-field kline; ~3330 daily; API publik; Yahoo ditolak karena agregat CCC tidak transparan
- **ALTERNATIVES:** Yahoo — rejected (agregasi tidak transparan, reproducibility UNCLEAR)
- **CONFIDENCE:** MEDIUM — perlu verifikasi final
- **IMPACT:** Menentukan endpoint, snapshot, dan robustness design
- **SOURCE:** Phase 2 screening §0.8, Protocol v2.0 §11-12

## D005 — Feature Selection Method Candidate
- **DATE:** 2026-09-29
- **DECISION:** XGBoost-based feature importance PROVISIONALLY LOCKED
- **QUESTION:** Metode apa untuk memilih fitur per temporal window?
- **EVIDENCE:** Protocol v2.0 §19; nonlinear; cocok tabular; importance tersedia; computational feasible; umum di financial ML
- **ALTERNATIVES:** MI, RFE, permutation — tidak ditolak tapi bukan primary
- **CONFIDENCE:** MEDIUM — perlu sensitivity analysis terhadap K
- **SOURCE:** Protocol v2.0 §19-20

## D006 — Stability Metrics Candidate
- **DATE:** 2026-09-29
- **DECISION:** Jaccard + Kuncheva PROVISIONALLY LOCKED
- **QUESTION:** Metrik apa untuk mengukur feature-subset stability antar window?
- **EVIDENCE:** Protocol v2.0 §25; Jaccard = overlap sederhana; Kuncheva = chance-corrected; Lazebnik 2024 tunjukkan limitasi metrik klasik
- **CONFIDENCE:** MEDIUM
- **SOURCE:** Protocol v2.0 §25-26

## D007 — Forecasting Model Candidate  ⟶  **SUPERSEDED**
- **DATE:** 2026-09-29
- **DECISION (historical):** PatchTST PROVISIONALLY LOCKED; baseline = Naive + XGBoost
- **QUESTION:** Model apa untuk forecasting?
- **EVIDENCE:** Protocol v2.0 §21-23; PatchTST = temporal DL; XGBoost = tabular ML baseline; Naive = simplest baseline
- **CONFIDENCE:** LOW — perlu evaluasi apakah PatchTST justified vs XGBoost saja
- **SOURCE:** Protocol v2.0 §21-23
- **STATUS: SUPERSEDED.** The final experiment did **NOT** implement PatchTST. The final forecasting model is **XGBoost** (`XGBRegressor`), as frozen in `reports/frozen_methodology_manifest.md` (Forecast = XGBoost, "Can change? No") and recommended in `reports/methodology-resolution.md` §17 (do not select PatchTST/iTransformer; keep XGBoost as the tabular forecaster). PatchTST was evaluated as a candidate and deliberately not used (small sample ≈2,969 daily rows; no directly verified BTC daily next-day evidence). This record is preserved as historical evidence only — it does **not** describe the implemented pipeline.
