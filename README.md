# btcriset — Temporal Feature-Subset Stability ↔ OOS Forecasting Error (Bitcoin)

Penelitian tentang **hubungan antara temporal feature-subset stability dan
out-of-sample (OOS) forecasting error** pada Bitcoin, menggunakan rolling
walk-forward windows.

**RQ utama:** Apakah terdapat hubungan antara temporal feature-subset stability
dan forecasting error pada periode OOS Bitcoin?

> Catatan status: penelitian ini menggunakan **XGBoost** sebagai forecaster.
> Fokus kontribusi adalah analisis **stability ↔ error**, bukan arsitektur deep
> learning/Transformer.

## Ringkasan hasil (final, C1-corrected pairing)

| | Primary — Binance BTC/USDT | Robustness — Coinbase BTC-USD |
|---|---|---|
| Raw / processed rows | 3,059 / 2,969 | 3,818 / 3,728 |
| Windows / association pairs | 22 / **21** | 31 / **30** |
| Feature pool / K | 30 / 10 | 30 / 10 |
| Spearman rho (J_t → MAE_{t+1}) | **−0.2047** | **+0.2385** |
| Bootstrap 95% CI (B=5000, seed=42) | [−0.3890, +0.1151] | [−0.0508, +0.5070] |
| CI includes zero | ya | ya |
| Mean Jaccard | 0.368 | 0.390 |
| Mean XGBoost MAE vs naive MAE | 0.0334 vs 0.0212 | 0.0254 vs 0.0224 |

**Pairing final (frozen):** `J_t = Jaccard(S_t, S_{t+1})` dipasangkan dengan
`MAE_{t+1}`. Hasil association final ada di
`reports/final-association-c1-corrected.{json,csv}`.

**Kesimpulan kualitatif:** tidak terdeteksi hubungan yang konklusif antara
feature-subset stability dan OOS MAE berikutnya pada sampel yang dianalisis
(kedua CI bootstrap mencakup nol; n kecil). Ini **bukan** klaim "terbukti tidak
ada hubungan".

## Struktur proyek

```
code/            pipeline (config, prepare_features, run_experiment, bootstrap,
                 C1 correction, figure generators, evidence builder)
data/            raw + processed parquet + snapshots (metadata & SHA-256)
reports/         hasil eksperimen, audit, ringkasan, figure
tests/           unit + assertion tests (pytest)
docs/            proposal & dokumen skripsi
literature/      paper referensi (PDF)
notes/, thesis/  catatan & draf
```

## Metodologi (frozen)

- **Data:** daily OHLCV, Binance BTC/USDT (primary) + Coinbase BTC-USD (robustness).
- **Target:** `r(t+1) = ln(Close(t+1) / Close(t))`.
- **Feature pool:** 30 price/volume-derived features; selector XGBoost Gain, **K=10** (train-only).
- **Window:** Train 730d / Validation 180d / OOS 90d / Step 90d (rolling walk-forward).
- **Forecaster:** XGBoost (train+validation), scored OOS; baseline zero-return naive.
- **Metrics:** MAE, RMSE.
- **Stability:** Jaccard (primary), Kuncheva (secondary).
- **Inference:** Spearman rho + stationary bootstrap 95% CI, **B=5000, seed=42**;
  block length per dataset (Binance auto ≈6.64; Coinbase §15 `ceil(max(b_stab,b_err))`=6.0).

## Reproduksi

```bash
pip install numpy scipy pandas scikit-learn xgboost matplotlib pyarrow
python -m pytest tests -q          # 44 tests
```

Source-of-truth & hash lengkap: `reports/final-results-reproducibility.md`,
`reports/master-results-evidence-manifest.md`.

## Dokumentasi kunci

| File | Isi |
|---|---|
| `reports/master-results-inventory.md` | inventaris hasil final |
| `reports/final-association-summary.md` | association final (C1) |
| `reports/final-pairing-evidence.csv` | bukti pairing J_t → MAE_{t+1} |
| `reports/stability-summary.csv` / `forecast-error-summary.csv` | ringkasan stability & error |
| `reports/results-claim-guardrail.md` | klasifikasi klaim (SUPPORTED / NOT SUPPORTED) |
| `reports/master-results-evidence-manifest.md` | SOURCE OF TRUTH index |
| `research-master.md`, `research-design.md` | protokol & desain riset |
