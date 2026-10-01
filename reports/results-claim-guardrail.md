# Results Claim Guardrail

> Each statement is classified ONLY as SUPPORTED, NOT SUPPORTED, or
> REQUIRES CAREFUL WORDING, with the evidence file, supporting numbers, and
> limitations. No conclusion beyond the evidence.

Primary association source: `reports/final-association-c1-corrected.json`.
Stability/error sources: `reports/stability-summary.csv`,
`reports/forecast-error-summary.csv`.

---

**1. Feature subsets berubah antar temporal windows.**
- Status: **SUPPORTED**
- Evidence: `reports/stability-summary.csv`; `reports/final-pairing-evidence.csv`.
- Numbers: Binance mean Jaccard = 0.368 (range 0.111–0.667, 21 pairs); Coinbase
  mean Jaccard = 0.390 (range 0.176–0.538, 30 pairs). Subsets are not identical
  across windows (max Jaccard < 1).
- Limitations: overlap magnitude is descriptive; no threshold defines "change".

**2. Feature subsets stabil sepenuhnya sepanjang periode.**
- Status: **NOT SUPPORTED**
- Evidence: same as (1).
- Numbers: max Jaccard < 1 on both datasets (0.667 Binance, 0.538 Coinbase);
  mean well below 1.
- Limitations: none needed — directly contradicted.

**3. Terdapat hubungan positif antara feature stability dan forecasting error.**
- Status: **NOT SUPPORTED**
- Evidence: `reports/final-association-c1-corrected.json`.
- Numbers: Binance rho = −0.205 (negative, not positive); Coinbase rho = +0.239
  but 95% CI [−0.051, +0.507] includes zero. No positive association is
  established in either dataset.
- Limitations: low power (n=21/30), wide CIs.

**4. Terdapat hubungan negatif antara feature stability dan forecasting error.**
- Status: **NOT SUPPORTED**
- Evidence: same as (3).
- Numbers: Binance rho = −0.205 with 95% CI [−0.389, +0.115] includes zero;
  Coinbase rho is positive. Neither CI excludes zero.
- Limitations: low power, wide CIs.

**5. Tidak ditemukan bukti kuat hubungan stability-error pada dataset ini.**
- Status: **SUPPORTED**
- Evidence: `reports/final-association-c1-corrected.json`.
- Numbers: both bootstrap 95% CIs include zero (Binance [−0.389, +0.115];
  Coinbase [−0.051, +0.507]).
- Limitations: this is absence of detected association in this sample, NOT proof
  of no relationship; n is small and CIs are wide.

**6. XGBoost mengungguli naive baseline.**
- Status: **NOT SUPPORTED**
- Evidence: `reports/forecast-error-summary.csv`.
- Numbers: XGBoost MAE < naive MAE in 0/22 windows (Binance) and 2/31 windows
  (Coinbase); mean XGBoost MAE > mean naive MAE on both (Binance 0.0334 vs 0.0212;
  Coinbase 0.0254 vs 0.0224).
- Limitations: none needed — directly contradicted at the aggregate level.

**7. XGBoost tidak mengungguli naive baseline secara konsisten.**
- Status: **SUPPORTED**
- Evidence: same as (6).
- Numbers: XGBoost loses to naive on MAE in 22/22 (Binance) and 29/31 (Coinbase)
  windows; wins in 0 and 2 windows respectively.
- Limitations: describes error comparison only; no model ranking claim.

**8. Hasil Binance dan Coinbase menunjukkan pola association yang sama.**
- Status: **REQUIRES CAREFUL WORDING**
- Evidence: `reports/final-association-c1-corrected.json`.
- Numbers: both CIs include zero (same non-detection), but point estimates have
  opposite sign (Binance −0.205, Coinbase +0.239).
- Limitations: "same" only in the sense of non-detection; direction differs. State
  the direction difference explicitly.

**9. Hasil Binance dan Coinbase menunjukkan arah association yang berbeda.**
- Status: **SUPPORTED**
- Evidence: same as (8).
- Numbers: Binance rho = −0.205; Coinbase rho = +0.239 (opposite signs).
- Limitations: both estimates are uncertain (CIs include zero); do not over-read
  the sign difference as a real divergence.

**10. Hasil membuktikan hubungan kausal antara stability dan error.**
- Status: **NOT SUPPORTED**
- Evidence: design is observational/correlational (Spearman + bootstrap CI).
- Numbers: n/a — no causal identification.
- Limitations: correlation is not causation; no intervention/controls.

**11. Hasil dapat digeneralisasikan ke seluruh Bitcoin forecasting.**
- Status: **NOT SUPPORTED**
- Evidence: two exchanges (Binance BTC/USDT, Coinbase BTC-USD), one feature pool,
  one model, one window config.
- Numbers: 22 and 31 windows only.
- Limitations: no multi-asset, multi-model, multi-period generalisation tested.

**12. Hasil hanya mendukung kesimpulan pada experimental setting penelitian ini.**
- Status: **SUPPORTED**
- Evidence: frozen config (`code/experiment_config.py`), C1 association,
  reproducibility manifest.
- Numbers: K=10, 30 features, XGBoost fixed params, 730/180/90/90 windows, B=5000,
  seed=42.
- Limitations: conclusions are bounded by these choices.
