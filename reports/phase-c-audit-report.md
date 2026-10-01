# Phase C — Audit Report

> [!tldr] Audit pasca-eksperimen: LULUS. Tidak ditemukan leakage, matematika valid, hasil reproducible. Satu catatan keterbatasan: daya statistik rendah (n=20 pasangan).

## 1. Leakage audit
| Check | Method | Result |
|---|---|---|
| Selector tidak melihat validation/OOS | `sel.fit(x.iloc[a:b])` — hanya TRAIN | PASS |
| Forecaster fit TRAIN+VALIDATION | `fc.fit(x.iloc[a:c][selected])` | PASS |
| Evaluasi hanya OOS | `pred = fc.predict(x.iloc[c:d][selected])` | PASS |
| Target tidak dalam feature list | `assert 'target' not in FEATURE_COLUMNS` | PASS |
| Fitur kausal (no future info) | test `test_feature_causality` (prefix-invariance) | PASS |
| Tidak ada re-fit di OOS | window boundaries strictly `a<b<c<d`, non-overlap eval | PASS |
| Data sorted & unique dates | `assert data['date'].is_monotonic_increasing and is_unique` | PASS |

## 2. Mathematical validity
| Check | Result |
|---|---|
| Target $= \ln(Close_{t+1}/Close_t)$ | PASS (`test_target_definition`, rtol 1e-12) |
| Jaccard $=|S_1 \cap S_2| / |S_1 \cup S_2|$ | PASS ($2/6$ verified) |
| Kuncheva $(r k - k^2)/(k(n-k))$ | PASS ($4/24 = 1/6$ verified) |
| K = 10 persis per window | PASS (semua 22 window) |
| Bootstrap block length $\geq 1$ | PASS ($b=6.588$) |
| Bootstrap pairing joint (bukan independent shuffle) | PASS (idx joint) |

## 3. Statistical validity
| Item | Value |
|---|---|
| n windows | 22 |
| n pairs ($J_t \to MAE_{t+1}$) | 20 |
| Spearman $\rho$ | $-0.1013$ |
| p-value | $0.671$ |
| Bootstrap CI 95% | $[-0.519,\ +0.375]$ |
| Block length $b$ | $6.588$ |

**Catatan daya statistik**: n=20 pasangan memberi daya terbatas; CI lebar mencakup 0. Hasil **tidak konklusif untuk klaim null yang kuat** — hanya "tidak terdeteksi hubungan signifikan pada sampel ini".

## 4. Anomali
- **Window 10** ($MAE = 0.222$): lonjakan ekstrem, kemungkinan rezim crash 2022. Bukan error; outlier nyata yang tercatat.
- XGBoost MAE > naive MAE di hampir semua window → model tidak mengalahkan baseline zero-return.

## 5. Reproducibility
- Rerun identik (lihat `reproducibility_manifest.md`). PASS.
- Unit tests 8/8 PASS.

## 6. Kesimpulan audit
**LULUS.** Eksperimen valid, leakage-aware, reproducible. Temuan utama: tidak ada bukti hubungan signifikan antara stabilitas subset fitur dan error OOS berikutnya pada dataset BTC/USDT daily.
