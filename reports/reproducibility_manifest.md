# Reproducibility Manifest — Phase A–C

> [!tldr] Semua hasil dapat direproduksi bit-for-bit. SHA-256 input & output terverifikasi; rerun menghasilkan nilai identik.

## Environment
| Komponen | Versi |
|---|---|
| Python | 3.14.7 |
| xgboost | 3.4.1 |
| scikit-learn | 1.9.1 |
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| matplotlib | 3.11.2 |
| pyarrow | 25.0.1 |

## Input snapshots (SHA-256)
| File | SHA-256 |
|---|---|
| `data/raw/binance_btcusdt_1d.parquet` | `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0` |
| `data/processed/binance_btcusdt_daily_features_v1.parquet` | `7ab4dd13aeaec8cb7d15dfdae785e7b638b2e0a9894996557ef25e673de31ce7` |
| `data/snapshots/binance_btcusdt_daily_features_v1_metadata.json` | `29a432d7278e4ca52d5761e84075b7739ad29b7433924f48801f18d5e6bb626f` |

## Output artifacts
| File | SHA-256 |
|---|---|
| `reports/experiment_results.csv` | `59e0ffd8b55689c420981f86c39045fdb1f11d8fd114983d9959dd4a94421a5f` |

## Reproducibility checks
- [x] Rerun `python code/run_experiment.py` → Spearman $\rho = -0.10132643745668742$ (identik).
- [x] Bootstrap CI identik: `[-0.5193248203679854, 0.3745795999026185]`.
- [x] CSV SHA-256 identik setelah rerun.
- [x] `random_state=42` di XGBoost + `seed=42` di bootstrap → deterministik.
- [x] Tidak ada unduhan data baru; snapshot input tidak diubah.

## Cara menjalankan ulang
```
cd D:/Hermes/Projects/riset-btc
python code/run_experiment.py
python code/generate_figures.py
python -m pytest tests
```

## Determinism notes
- Selector XGBoost: `n_jobs=1`, `random_state=42` → single-thread determinism.
- Stationary bootstrap: `np.random.RandomState(42)` → fixed RNG stream.
- Block length otomatis: Politis–White (2004) + koreksi Patton et al. (2009), $b \approx 6.588$.
