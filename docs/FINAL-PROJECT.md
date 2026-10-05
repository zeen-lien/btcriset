# Riset BTC — Dokumen Final (Konsolidasi)

> **Satu file ringkasan final** untuk seluruh proyek riset
> *Temporal Feature-Subset Stability ↔ OOS Forecasting Error (Bitcoin)*.
>
> Dokumen ini **murni konsolidasi dokumentasi** — tidak ada hasil eksperimen, data,
> kode, atau angka final yang diubah. Sumber angka = artefak final **C1-corrected**
> + manifest bukti di `reports/`. Untuk verifikasi independen, rujuk
> `reports/master-results-evidence-manifest.md` (source-of-truth index).

---

## Daftar Isi

1. [Identitas Penelitian](#1-identitas-penelitian)
2. [Pertanyaan Penelitian & Hipotesis](#2-pertanyaan-penelitian--hipotesis)
3. [Dataset](#3-dataset)
4. [Metodologi (FROZEN)](#4-metodologi-frozen)
5. [Hasil Final (C1-corrected)](#5-hasil-final-c1-corrected)
6. [Guardrail Klaim](#6-guardrail-klaim)
7. [Reproduksibilitas & Verifikasi](#7-reproduksibilitas--verifikasi)
8. [Struktur Proyek](#8-struktur-proyek)
9. [Indeks Dokumen & Audit Trail](#9-indeks-dokumen--audit-trail)
10. [Catatan Housekeeping](#10-catatan-housekeeping)

---

## 1. Identitas Penelitian

| Item | Nilai |
|---|---|
| Judul kerja | Temporal Feature-Subset Stability ↔ OOS Forecasting Error pada Bitcoin |
| Repo | `github.com/zeen-lien/btcriset` (branch `main`) |
| Jenis penelitian | **Studi empiris-analitis / korelasional** — **BUKAN** benchmark akurasi algoritma atau deep-learning |
| Fokus kontribusi | Analisis hubungan **stability ↔ error**, **bukan** arsitektur model |
| Forecaster aktual | **XGBoost** (`XGBRegressor`) — bukan PatchTST / Transformer |
| Otoritas metodologi | `reports/frozen_methodology_manifest.md` |

**Naskah skripsi (hasil akhir):** `docs/HASIL-FIX/` → `BAB I - III.docx`, `BAB IV.docx`,
`BAB V.docx`, `Outline.docx` (outline mengikuti template kampus).

---

## 2. Pertanyaan Penelitian & Hipotesis

**RQ utama:** Apakah terdapat hubungan antara *temporal feature-subset stability*
dan *forecasting error* pada periode *out-of-sample* (OOS) Bitcoin?

- **RQ1:** Bagaimana kestabilan subset fitur hasil feature selection berubah pada
  successive temporal windows dalam forecasting Bitcoin?
- **RQ2:** Apakah perubahan temporal feature-subset stability berhubungan dengan
  variasi forecasting error pada periode OOS yang bersesuaian?
- **RQ3 (opsional):** Apakah hubungan tersebut tetap terlihat pada dataset exchange
  lain (robustness)?

**Hipotesis (H1):** Terdapat hubungan antara temporal feature-subset stability dan
forecasting error pada periode OOS Bitcoin. **Semua hasil valid** (positif / negatif
/ tidak terdeteksi) — desain tidak mengarahkan ke satu arah.

**Gap (wording aman):** Belum teridentifikasi secara memadai, dalam literatur yang
diaudit, penelitian Bitcoin forecasting yang menjadikan **perubahan temporal
feature-subset stability antar-window** sebagai variabel analitis dan menguji
hubungannya dengan **variasi OOS error yang bersesuaian**. Bukan klaim "first-ever".

---

## 3. Dataset

| | Primary — Binance BTC/USDT | Robustness — Coinbase BTC-USD |
|---|---|---|
| Sumber | Binance Spot REST `/api/v3/klines` | Coinbase Exchange REST `/products/BTC-USD/candles` |
| Raw rows | 3.059 | 3.818 |
| Raw period | 2017-08-17 → 2025-12-31 | 2015-07-20 → 2025-12-31 |
| Processed rows | 2.969 | 3.728 |
| Processed period | 2017-11-14 → 2025-12-30 | 2015-10-17 → 2025-12-30 |
| Feature pool | 30 fitur kausal | 30 fitur kausal |
| Target | `r(t+1) = ln(Close[t+1] / Close[t])` | sama |

- Raw & processed parquet + metadata SHA-256 ada di `data/raw/`, `data/processed/`,
  `data/snapshots/`.
- Warm-up NaN **tidak** diimputasi: 90 baris (Binance) / 90 baris (Coinbase) dibuang.

---

## 4. Metodologi (FROZEN)

> ⚠️ Konfigurasi di bawah **dibekukan**. Tidak boleh diubah untuk menjaga validitas
> hasil. Rujukan kode: `code/experiment_config.py`, `code/run_experiment.py`.

| Komponen | Nilai (frozen) |
|---|---|
| Data | Daily OHLCV, Binance BTC/USDT (primary) + Coinbase BTC-USD (robustness) |
| Target | `r(t+1) = ln(Close(t+1) / Close(t))` |
| Feature pool | 30 fitur price/volume-derived, kausal (hanya info ≤ t) |
| Selector | XGBoost **Gain** importance — **train-only** (tidak pernah lihat validation/OOS) |
| K | **K = 10** (fixed, dipilih via validation RMSE window pertama) |
| Window | Train **730** / Validation **180** / OOS **90** / Step **90** hari (rolling walk-forward) |
| Forecaster | XGBoost, fit pada **train+validation**, diskor **OOS-only** |
| Baseline | Naive zero-return |
| Metrik error | MAE, RMSE |
| Stabilitas | **Jaccard** (primary), **Kuncheva** (secondary) |
| Pairing (C1) | `J_t = Jaccard(S_t, S_{t+1})` ⟷ `MAE_{t+1}` (SAME-ROW) |
| Inferensi | Spearman rho + stationary bootstrap 95% CI, **B = 5000, seed = 42** |
| Block length | Binance: auto ≈ 6.644 (Politis–White/Patton); Coinbase: `ceil(max(b_stab, b_err))` = 6.0 (§15) |

**Parameter XGBoost:** `n_estimators=120, max_depth=3, learning_rate=0.05,
reg_lambda=1, subsample=1, colsample_bytree=1, objective=reg:squarederror,
n_jobs=1, seed=42`.

**Aturan keras yang dipatuhi:** tidak mengubah frozen methodology; tidak menjalankan
model baru; tidak menambah fitur; tidak mengubah K; tidak tuning; tidak membuang
outlier; tidak memilih subset hasil yang menguntungkan; tidak menyimpulkan kausalitas;
tidak menganggap p-value iid Spearman sebagai inferensi utama; tidak mengarang angka.

---

## 5. Hasil Final (C1-corrected)

> Sumber: `reports/final-association-c1-corrected.{json,csv}`,
> `reports/final-pairing-evidence.csv`, `reports/stability-summary.csv`,
> `reports/forecast-error-summary.csv`.

| | Primary — Binance | Robustness — Coinbase |
|---|---|---|
| Windows / association pairs | 22 / **21** | 31 / **30** |
| **Spearman rho** (`J_t → MAE_{t+1}`) | **−0,2047** | **+0,2385** |
| **Bootstrap 95% CI** (B=5000, seed=42) | **[−0,3890, +0,1151]** | **[−0,0508, +0,5070]** |
| CI mencakup nol | **ya** | **ya** |
| iid reference p (referensi saja) | 0,3735 | 0,2043 |
| Mean Jaccard | 0,3680 | 0,3898 |
| Jaccard range | 0,1111 – 0,6667 | 0,1765 – 0,5385 |
| Mean MAE XGBoost vs naive | 0,0334 vs 0,0212 | 0,0254 vs 0,0224 |
| XGBoost menang MAE | 0 / 22 window | 2 / 31 window |

**Interpretasi (wording aman):**
> Tidak terdeteksi hubungan yang konklusif antara stabilitas subset fitur dan MAE OOS
> berikutnya pada sampel yang dianalisis (kedua CI bootstrap mencakup nol; n kecil).
> Ini **bukan** klaim "terbukti tidak ada hubungan" maupun "H0 terbukti benar".

**Feature paling sering terpilih (XGBoost Gain, K=10):**
`bb_percent_b_20` — 13/22 (59,09%) Binance, 23/31 (74,19%) Coinbase;
`stochastic_d_3` — 11/22 (50%) Binance.

**Detail pre vs post C1** (untuk audit):
Binance −0,1013 (n=20) → −0,2047 (n=21); Coinbase +0,1859 (n=29) → +0,2385 (n=30).

---

## 6. Guardrail Klaim

> Sumber: `reports/results-claim-guardrail.md`. Setiap pernyataan diklasifikasi
> **SUPPORTED / NOT SUPPORTED / REQUIRES CAREFUL WORDING**.

| # | Klaim | Status |
|---|---|---|
| 1 | Subset fitur berubah antar window (max Jaccard < 1) | **SUPPORTED** |
| 2 | Subset fitur stabil sepenuhnya sepanjang periode | **NOT SUPPORTED** |
| 3 | Ada hubungan **positif** stability–error | **NOT SUPPORTED** |
| 4 | Ada hubungan **negatif** stability–error | **NOT SUPPORTED** |
| 5 | Tidak ditemukan bukti kuat hubungan stability–error pada dataset ini | **SUPPORTED** |
| 6 | XGBoost mengungguli naive baseline | **NOT SUPPORTED** |
| 7 | XGBoost tidak mengungguli naive secara konsisten | **SUPPORTED** |
| 8 | Pola association Binance & Coinbase sama | **REQUIRES CAREFUL WORDING** (sama hanya dalam arti *non-detection*; arah berbeda) |
| 9 | Arah association Binance & Coinbase berbeda | **SUPPORTED** |
| 10 | Hubungan **kausal** stability–error | **NOT SUPPORTED** |
| 11 | Dapat digeneralisasi ke seluruh Bitcoin forecasting | **NOT SUPPORTED** |
| 12 | Kesimpulan hanya berlaku pada setting eksperimen ini | **SUPPORTED** |

**Aturan penulisan:** hindari "terbukti tidak ada hubungan", "H0 terbukti benar",
"penelitian gagal", "menyebabkan", "lebih baik secara signifikan". Gunakan
"tidak terdeteksi / tidak konklusif pada sampel ini".

---

## 7. Reproduksibilitas & Verifikasi

### Hash SHA-256 (artefak kunci)

| Artefak | SHA-256 |
|---|---|
| Raw Binance `data/raw/binance_btcusdt_1d.parquet` | `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0` |
| Raw Coinbase `data/raw/coinbase_btc_usd_86400.parquet` | `c5d47d5f5333da8eff6652e661ef523af54990861c7067011173fb283948dc44` |
| Processed Binance | `7ab4dd13aeaec8cb7d15dfdae785e7b638b2e0a9894996557ef25e673de31ce7` |
| Processed Coinbase | `fbfdd07c1b7296a6f2ee9a1585f2353c434437ead201b42068eacc2f5d2573fd` |
| Config `code/experiment_config.py` | `91d630ce70d71f575a77def5129e391efe5a1c7973928e49fcd61af320d06322` |
| Binance results `reports/experiment_results.csv` | `59e0ffd8b55689c420981f86c39045fdb1f11d8fd114983d9959dd4a94421a5f` |
| Coinbase results `reports/coinbase_experiment_results.csv` | `a478cf9cc819df122f232ad0eb4b4116688fb50af55d1055309e5f484ad9f76a` |
| `reports/final-association-c1-corrected.json` | `d945b079120909d040c08b0b94826d8b0858474ca35bf22317447baae7cd0697` |
| `reports/final-association-c1-corrected.csv` | `fafcf0eae4c6df008401d14dd434085404ebd8d373b53c8a427bc38779e232f0` |

### Software

Python 3.14.7 · Windows-11 (10.0.26200) · numpy 2.5.3 · scipy 1.18.1 · pandas 3.0.6 ·
scikit-learn 1.9.1 · xgboost 3.4.1 · matplotlib 3.11.2 · pyarrow 25.0.1.
`scikit-learn` tidak diimpor di repo ini (didaftarkan hanya sebagai catatan versi).

### Cara reproduksi

```bash
pip install -r requirements.txt
python -m pytest tests -q      # 44 passed
```

Test suite (44): `test_prepare_features.py` (3), `test_experiment.py` (5),
`test_coinbase_robustness.py` (12), `test_c1_pairing_correction.py` (12),
`test_evidence_package.py` (12).

### Verifikasi naskah

- Render Word → PDF (Microsoft Word COM) → cek visual halaman: **rumus `oMath` utuh,
  field sitasi Mendeley (`w:sdt`) utuh, tabel/gambar/numbering konsisten**.
- Audit read-only menyeluruh (naskah ↔ kode ↔ reports): **selaras**.

---

## 8. Struktur Proyek

```
btcriset/
├── code/            pipeline: config, prepare_features, run_experiment,
│                    bootstrap_analysis, apply_c1_pairing_correction,
│                    build_evidence_package, generate_figures, download_data
├── data/
│   ├── raw/         parquet OHLCV mentah (immutable)
│   ├── processed/   parquet fitur + target
│   └── snapshots/   metadata provenance + SHA-256
├── reports/         hasil eksperimen, audit, manifest bukti, figures/
├── tests/           unit + assertion tests (pytest, 44 tests)
├── docs/
│   ├── FINAL-PROJECT.md        ← dokumen ini (ringkasan final)
│   ├── HASIL-FIX/              ← 4 naskah skripsi final (.docx)
│   ├── research/               ← protokol & desain riset
│   ├── Proposal dan bab 1-5/   ← sumber asli user (tidak diubah)
│   └── referensi bab 1-5/      ← 21 PDF referensi
├── literature/papers/          8 PDF paper inti
├── README.md
└── requirements.txt
```

---

## 9. Indeks Dokumen & Audit Trail

> Semua `.md` di `reports/` & `docs/research/` adalah **bagian rantai bukti**
> (git-tracked & saling dirujuk). Dipertahankan sebagai audit trail — lihat §10.

### 9.1 Sumber utama (FINAL / USE)

| File | Isi |
|---|---|
| `reports/master-results-evidence-manifest.md` | **SOURCE OF TRUTH index** |
| `reports/final-association-c1-corrected.{json,csv}` | hasil association final |
| `reports/final-association-summary.md` | ringkasan association final (C1) |
| `reports/final-pairing-evidence.csv` | bukti pairing `J_t ↔ MAE_{t+1}` |
| `reports/experiment_results.csv` / `coinbase_experiment_results.csv` | per-window source of truth |
| `reports/stability-summary.csv` / `forecast-error-summary.csv` | ringkasan stability & error |
| `reports/cross-dataset-results-table.csv` | tabel lintas dataset |
| `reports/master-results-inventory.md` | inventaris hasil final |
| `reports/final-results-reproducibility.md` | hash & versi |
| `reports/results-claim-guardrail.md` | klasifikasi klaim |
| `reports/frozen_methodology_manifest.md` | otoritas metodologi beku |
| `reports/feature-selection-frequency-summary.md` | frekuensi fitur terpilih |
| `reports/figure-data-inventory.md` | sumber data tiap figure |

### 9.2 Pendukung (SUPPORTING)

`reports/` → `result-audit-*.md`, `forecast-error-audit.md`, `bootstrap-code-audit.md`,
`cross-dataset-consistency-audit.md`, `reproducibility-result-audit.md`,
`scientific-evidence-map.md`, `reproducibility_manifest.md`, `phase-c-audit-report.md`,
`coinbase_*.md`, `binance_coinbase_comparison.md`, `methodology-*.md`,
`feature-audit.md`, `data-retrieval-audit.md`, `phase_0_report.md`,
`pre_experiment_approval.md`, `pilot_report.md`.
`docs/research/` → `research-master.md`, `research-design.md`, `research-decisions.md`,
`dataset-audit.md`, `gap-evidence-matrix.md`, `nearest-prior-work.md`.

### 9.3 OBSOLETE / DO NOT USE (tetap disimpan untuk audit trail)

- `reports/experiment_summary.json` & `coinbase_experiment_summary.json` — nilai
  `spearman_rho`/`n_pairs` **pre-C1 (offset pairing)**. **Jangan** dipakai untuk
  analisis final; gunakan `final-association-c1-corrected.*`.
- `reports/stability-error-pairing-audit.csv` — pairing offset, digantikan
  `final-pairing-evidence.csv`.

> **Catatan:** kolom per-window forecasting (`xgboost_mae`, `rmse`, …) di
> `experiment_results.csv` **tidak** obsolete — hanya pairing association yang lama
> yang salah.

---

## 10. Catatan Housekeeping

Pembersihan yang dilakukan (murni housekeeping, tidak menyentuh hasil/artefak bukti):

- ✅ **Cache** dihapus: `.pytest_cache/`, `code/__pycache__/`, `tests/__pycache__/`,
  `code/data/__pycache__/`.
- ✅ **Duplikat PDF** dihapus: salinan byte-identical `bysik_slepaczuk_2026_2606.00060.pdf`
  di `docs/referensi bab 1-5/` (versi asli tetap di `literature/papers/`).
- ✅ **File scratch** dihapus (worklist/paras/rem/todo/dp*.py).
- ✅ Dibuat **satu file `.md` final** ini (`docs/FINAL-PROJECT.md`).
- ⏸️ **File `.md` pendukung dipertahankan** — semuanya git-tracked & saling dirujuk
  (rantai bukti). Menghapusnya akan memutus audit trail & referensi manifest.
  *Lesson learned:* artefak yang dirujuk manifest jangan dihapus
  (insiden `experiment_summary.json` → di-restore via `git checkout`).

---

*Dokumen ini adalah konsolidasi dokumentasi. Untuk angka mentah & bukti lengkap,
selalu rujuk artefak di `reports/` dan `data/snapshots/`.*
