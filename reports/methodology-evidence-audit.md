# Audit Evidence Metodologi
> [!tldr] Audit adversarial: konfigurasi pilot **belum siap dibekukan**. Literatur terdekat Youssefi et al. (2025) sudah menanyakan temporal stability fitur dan dampaknya pada performa lintas horizon; gap perlu dipersempit ke hubungan yang secara eksplisit dipasangkan antara perubahan subset successive walk-forward windows dan error OOS yang bersesuaian. Full experiment tidak dijalankan.

## Executive Summary

Audit menilai 31 keputusan metodologis. Bukti terkuat adalah bahwa beberapa **keluarga** metode punya preseden; bukti belum membuktikan konfigurasi pilot sebagai satu paket unggul atau optimal. Temuan adversarial paling penting: Youssefi et al. (2025) bukan sekadar paper feature-selection crypto. Paper ini menyatakan RQ tentang temporal stability indikator lintas horizon dan dampaknya terhadap kinerja, memakai BTC/USDT, data Binance per menit yang diagregasi harian, 130+ technical indicators, tiga metode seleksi, dan 20 fitur terpilih. Desain mereka dua tahun training awal, validation enam bulan, step satu bulan, horizon 1–20 hari.[1] Ini mempersempit novelty awal, walau unit stabilitas mereka tampak per-horizon, bukan perubahan subset antarfold berturutan yang dipasangkan dengan error OOS pada periode sama.

**Kesimpulan sementara:** gap luas “stabilitas temporal fitur dan performa Bitcoin belum diteliti” tidak aman. Gap lebih sempit mungkin masih ada: mengukur stabilitas subset dari successive walk-forward training windows, mengaitkannya dengan forecast error pada blok OOS berikutnya, dengan inferensi yang mengakomodasi dependensi. Ini **belum lolos knockout search** dan bukan klaim first-ever. Butuh full text/appendix review Barak & Parvini, Bysik, serta Youssefi untuk memastikan perbedaan unit analisis dan prosedur OOS.

Dari 31 komponen: ada 3 fakta/konstraint terkunci bersyarat (snapshot, overlap windows sebagai fakta desain, hitungan windows bila dimensi lama dipakai); mayoritas provisional; banyak keputusan inti memerlukan keputusan sebelum freeze. Status rinci ada di [[methodology-rule-matrix]].

## Current Methodology dan Source Code

- Snapshot Binance BTC/USDT daily: 3.059 baris, 2017-08-17–2025-12-31, SHA-256 `6b05bd5bdb3127ec4d2be42936f6d75ab4a226ac5b0334677e70afe9925a2da0` (mengacu audit Phase 2).
- Fitur diproses: 2.969 baris; timestamp 2017-11-14–2025-12-30 UTC; 30 predictors + `target`.
- Implementasi target: `np.log(close.shift(-1)/close)`. Lag return: `log_close.diff(lag)`. Rolling SD pada log daily return. Tidak ada forward-fill/back-fill/imputation.
- Feature formulas terlihat kausal/trailing pada kode; target dikeluarkan dari `FEATURE_COLUMNS`. Tetapi indikator tidak identik dengan default textbook yang kerap diasumsikan: RSI dihitung dari rolling arithmetic mean gains/losses (bukan Wilder smoothing), ATR juga rolling mean TR (bukan Wilder), MACD memakai EMA `adjust=False`, stochastic D simple mean, Bollinger SD `ddof=0`. Formula harus disamakan dengan literatur/ditetapkan eksplisit; report feature audit wajib cocok.
- `prepare_features.py` menyatakan `indicator_parameters` terdokumentasi di report, belum memverifikasi kesesuaian report di pemeriksaan ini. Return formula benar log pada source; pastikan tidak ada dokumentasi lama yang bilang simple return.
- Pilot memakai Train 730 / validation 90 / OOS 30 / step 30, lima fold; K dari {10,15,20} dipilih dari RMSE validation window pertama lalu K=10. Ini keputusan pilot, bukan literatur.
- Candidate utama di prompt adalah PatchTST; pilot berisi XGBoost selector/forecaster dan zero-return baseline. Belum ada PatchTST run, dan tidak ada dasar menjadikan model tersebut final.

## Evidence Audit by Decision

### Target

El Youssefi et al. menyatakan memakai logarithmic returns sebagai target dan memberi alasan time-additivity/symmetry, tetapi paper framing/hasilnya juga disebut price forecasting. Mereka tidak melakukan eksperimen terkontrol price level vs simple return vs log return.[1] Target next-day log return konsisten dengan pertanyaan error return, mudah diinterpretasi, dan menghindari level nonstationary; tetapi bukti bahwa ia target paling baik tidak ada. Target provisional. Return bukan direction; jangan mengubahnya menjadi klasifikasi tanpa perubahan RQ.

### Dataset dan frequency

Binance BTC/USDT daily tetap source kandidat utama sebab sudah dipilih dan snapshot diaudit; bukan karena literature membuktikan Binance/daily terbaik. Youssefi mengagregasi Binance minute OHLCV ke daily; ini direct domain/frequency precedent, tetapi period, target framing, dan observasi berbeda.[1] Bysik & Ślepaczuk memakai Bitcoin/USDT hourly dan 27 walk-forward folds; berguna sebagai BTC-specific tapi frequency berbeda.[3] Tidak ada dasar membandingkan akurasi antar-paper lintas sampel/horizon.

### Feature pool, formula, indicator parameters

Youssefi memakai >130 indikator momentum/volatility/volume/trend dan menguji MI, RFE, RFI; hasil seleksi dan error berubah حسب aset, horizon, model.[1] Ini mendukung relevansi keluarga indikator, bukan 30 fitur kita atau parameter lookback tertentu. Mereka menyebut memilih 20 setelah menimbang kompleksitas/akurasi, namun itu konteks paper tersebut, bukan alasan K=20/10 di proyek kita. Indicator formulas harus ditetapkan, termasuk smoothing, `ddof`, warm-up, dan apakah level OHLC mentah dicampur dengan moving averages. Semua transformasi OHLC/TA saling deterministik/berkorelasi; importance dapat berpindah antarproksi. Exact RSI14, MACD12/26/9, stochastic14/3, SMA/EMA lookback, ATR14, BB20±2, std14/30 belum punya evidence tepat dan langsung untuk kumpulan ini. Status exact settings: unsupported as jointly justified, bukan salah secara teknis.

### Return representation

Kode kini konsisten memakai log returns (target dan lagged returns). Return log berbeda dari simple return `P_t/P_(t-k)-1`, khususnya pada horizon panjang/volatilitas besar; log return additive lintas waktu namun bukan persentase simple return. Audit report dan metadata perlu mengunci definisi, formula, dan istilah. Source code sudah jelas log; tidak ditemukan klaim simple return di file yang diperiksa di sini.

### Window design

Ada preseden Bitcoin/crypto walk-forward. Youssefi: initial train 2 tahun, validation 6 bulan, step 1 bulan, horizon 1–20 hari; mereka menyatakan model dilatih ulang tiap step.[1] Bysik: hourly BTC, 27 folds dan konfigurasi 12 bulan training, 3 bulan validation/test, step 3 bulan (lihat paper/appendix).[3] Ini menunjukkan berbagai pilihan yang dipakai, bukan pembandingan yang menentukan 730/90/30/30. Train 730 mendapat dukungan parsial desain dua tahun Youssefi; validation 90 bertentangan dengan 6 bulan Youssefi dan 3 bulan Bysik; OOS 30/step 30 tidak identik dengan kedua desain. Rolling vs expanding tetap trade-off adaptasi vs sample size. Belum ada dasar menyatakan 730/90/30/30 terbaik. OOS panjang mempengaruhi noise pada error per-window dan identifikasi asosiasi.

### Selector, importance, Top-K

XGBoost Gain adalah skor model-specific berdasarkan penurunan loss pada split; API XGBoost memisahkan Gain, Weight dan Cover sebagai definisi importance berbeda.[10][31] Itu bukan ukuran kontribusi kausal atau relevansi universal. Permutation importance dan SHAP mengestimasi aspek berbeda; fitur berkorelasi dapat saling menggantikan. Dalam evidence yang diperiksa, Youssefi menggunakan MI/RFE/Random Forest Importance, bukan XGBoost Gain.[1] Bysik menggunakan grouped selector berbasis ranking dengan 10 grup indikator dalam diagnostik kestabilan; ini bukan top-10 fitur dari pool 30 kita.[3]

**K=10 wajib dibuka lagi.** Pemilihan K=10 dari validation fold pertama merupakan pilot-adaptasi. Youssefi memilih 20 dari >130 dalam eksperimen mereka, bukan mendukung 10 di pool ini. Fixed K membuat Kuncheva terdefinisi dan subset-size comparison lebih fair, tetapi rule K sendiri belum dipilih secara independen. Alternatif defensible: (i) satu K ditetapkan berdasarkan desain/kapasitas sebelum membuka OOS; atau (ii) nested validation per training window, lalu laporkan K variation dan gunakan stabilitas metric yang menangani ukuran subset variable. Jangan pilih berdasarkan error OOS.

### Stability: Jaccard dan Kuncheva

Jaccard `|A∩B|/|A∪B|` transparan, tidak chance-corrected; berubah dengan K dan N. Bysik melaporkan Jaccard adjacent-fold di Appendix sebagai diagnostik (mean 0.673, range 0.333–1), bukan menguji korelasi stability–OOS error.[3] Ini bukti langsung untuk temporal subset-overlap diagnostic BTC hourly, bukan untuk pertanyaan asosiasi kita.

Kuncheva `((r*N)-K²)/(K*(N-K))` mengoreksi expected overlap under random selections, dengan overlap `r`, universe size `N`, dan subset cardinality sama `K`. Harus ada feature universe tetap dan equal K; bila tidak, metric tak sesuai/tidak comparable.[8] Jadi ia cocok sebagai secondary jika cardinality dikunci. Jaccard dan Kuncheva mengukur overlap subset, bukan predictive utility/trust. Nogueira, Sechidis & Brown mengembangkan estimasi stability berbasis seleksi biner yang chance-corrected, dengan interval kepercayaan/uji; kandidat berguna jika melaporkan ketidakpastian atau membandingkan prosedur seleksi.[7] Tetapi resampling i.i.d. biasa tidak valid otomatis untuk seri finansial: perturbasi harus menghormati urutan/dependensi temporal, sehingga Nogueira tidak langsung menyelesaikan inference pada rolling windows.

### Forecasting models

PatchTST paper adalah long-term forecasting architecture dengan patching dan channel-independent design pada benchmark time-series; tidak ada direct evidence terverifikasi bahwa ia cocok untuk daily BTC next-day return dengan 2.969 observasi.[6] Bukan otomatis pilihan karena modern. Channel independence perlu dibahas terhadap 30 engineered covariates karena interaksi antarfitur tidak dimodelkan dengan cara multivariate channel-mixing biasa.

XGBoost plausible untuk tabular lag/features dan sudah dipakai pilot, tetapi hyperparameter di pilot (120 trees, depth 3, learning rate .05, lambda 1) tidak mendapat justifikasi empiris dari pilot. XGBoost sebagai selector sekaligus forecaster juga mengikat dua peran; harus dinyatakan bahwa stability mengukur selector behavior model-specific. Zero-return cocok jadi benchmark sederhana untuk target return, namun jangan namakan naive price persistence tanpa menjelaskan ekuivalensi.

### Metrics dan association

MAE memberi penalti linear dan satuan sama dengan log-return target; RMSE lebih menghukum error besar. Keduanya complementary. MAPE tidak cocok untuk target return yang bisa nol/negatif; tidak perlu ditambahkan. MAE/RMSE masing-masing dianalisis sebagai outcome terpisah atau satu harus dinyatakan primary.

Spearman menangkap asosiasi monotonic berbasis ranking, tetapi tidak mengatasi dependensi, ukuran sampel kecil, ties, atau multiple testing. Pilot `rho=.80, n=4, nominal p=.20` eksploratif saja. Elmakias et al. memosisikan stability profiles berdampingan dengan held-out AUC pada synthetic/binary data; tidak membuktikan asosiasi BTC temporal.[4] Dürre et al. membahas significance testing rank cross-correlations antara seri autokorelasi; ini lebih tepat sebagai kandidat dibanding p-value Spearman iid, tetapi window-level metrics kita tetap perlu validasi spesifik.[34] Pearson linear dan Kendall rank alternatives; pilih menurut estimand/distribution dan prespecify satu pasangan utama.

### Dependence, inference, multiple testing

Rolling windows share training/validation observations; even with non-overlapping 30-day OOS blocks, adjacent window metrics may be dependent due to overlapping histories and market serial dependence. Moving/stationary block bootstrap and HAC address dependence under assumptions, not by magic.[13][14][16] Must define sampling unit (daily returns vs window-pair rows), statistic, block-length choice, and whether pairs are stationary; 71-ish window pairs remain a small effective sample. No inference method locked yet. Multiple stability scores × MAE/RMSE × model variants inflate testing; pre-register primary outcome and correct/label secondary tests.

### Leakage, scaling, tuning

Current feature builders use trailing windows and target shift -1; unit tests cover formula/causality/metric cases per Phase 3 record. Selector must be fit only in training data; validation used for hyperparameters/K only, OOS never used for choice. Any scaler for PatchTST fit on train only and applied forward. No scaling required by current tree pipeline in pilot, but neural model requires explicit preprocessing. Full walk-forward leakage audit must inspect exact selector refit cadence, training vs validation fit, model training data inclusion after tuning, and feature dates/OOS target alignment. Avoid validation leakage from using validation to select K then report model fitted with same validation without clear nested procedure.

## Existing Required Literature: Audit status

- **El Youssefi et al. (2025), DOI 10.32604/cmc.2025.063218:** full text read, Sections 2–5 inspected. Important overlap: RQ asks temporal stability across horizons and effect on model performance; 3 cryptoassets, BTC/USDT, daily aggregated data, 20 selected indicators, MI/RFE/RFI, walk-forward. Result directions differ by model/horizon; not direct successive-window stability versus paired OOS error. Closest verified work.[1]
- **Bysik & Ślepaczuk (2026), arXiv:2606.00060:** full HTML retrieved, methods and appendices partly read. BTC/USDT hourly, walk-forward 27 folds, Jaccard appendix diagnostic; no reported association/regression of stability against OOS error found in reviewed sections. Preprint and trading-oriented target differ.[3]
- **Barak & Parvini (2023), DOI 10.1002/fut.22453:** metadata/title/abstract-level prior verification only; full publisher full text not verified in this pass. Dynamic Bitcoin feature selection is clearly adjacent; exact data/configuration and whether subset stability is associated with paired OOS forecast error remain UNCLEAR. Do not claim absence.[18]
- **Elmakias, Kolsky & Vilenchik (2026), DOI 10.3390/math14132372:** publisher record/full text partially retrieved; stability as trust layer and resampling recurrence profiles beyond predictive performance. Not BTC forecasting temporal-window evidence.[4]
- **Lazebnik & Rosenfeld (2024), DOI 10.1007/s10472-024-09936-8:** publisher abstract/record reviewed; definitional stability analysis. Not direct temporal BTC forecasting.[5]
- **WinnowML (Bel et al., 2021), DOI 10.1109/BigData52589.2021.9671602:** official PNNL/Datahub metadata confirms authors and conference paper. Full methods not read. Time-based system modeling is different domain/task; do not quote reported gains absent full-text check.[9][35]
- **Tripathi & Sharma (2023), DOI 10.1007/s10614-022-10325-8:** primary abstract/record says Bitcoin price forecasts at 1, 3, 5, 7 days and hybrid feature-selection procedure; exact data/windows/stability results remain unverified.[19]
- **Peng et al. (2021), DOI 10.1016/j.mlwa.2021.100060:** article is stock price-direction forecast, not Bitcoin; publisher page describes 124 technical indicators and selection methods including SFFS, TS, LASSO. Different market/target; indirect evidence only.[20][37]
- **Nie et al. (2023), PatchTST, arXiv:2211.14730:** architecture paper; patching and channel-independent Transformer for long-horizon TS, not feature-subset stability and no direct BTC evidence.[6]
- **Liu et al. (2024), iTransformer, arXiv:2310.06625:** official ICLR record; inverts dimensions so variates are tokens, reports general TS forecasting experiments; no feature-selection stability or direct BTC daily return evidence.[33][38]

## Pilot Rules That Are NOT Yet Justified

1. K=10 selected from one validation window.
2. 730/90/30/30 as a package; only partial precedent and conflicting alternatives.
3. XGBoost Gain uniquely appropriate selector; no direct evidence versus MI/RFE/permutation/SHAP.
4. Exact 30 feature registry and exact periods as forecast-optimal.
5. PatchTST as primary for small BTC daily return sample.
6. 120/3/.05 XGBoost forecasting settings.
7. Spearman p-values or block-bootstrap inference without dependence-specific design.
8. Pilot rho as evidence; n=4 invalid for substantive conclusion.

## Literature-Supported Rules

- Causal chronology is mandatory; walk-forward evaluation used in BTC/crypto forecasting.[1][3]
- Daily BTC technical-indicator feature selection has direct precedent, including multiple selectors and multi-horizon comparisons.[1]
- Jaccard is usable as an adjacent-fold overlap diagnostic; Kuncheva needs equal K and fixed universe.[3][8]
- MAE/RMSE quantify different error penalties; keep both if hypothesis plan identifies primary.[11]
- Overlapping windows require dependence-aware inference; block resampling/HAC have methodological precedent but need assumptions/design.[13][14][16]

## Conflicting Evidence

- Train/validation/test block lengths vary: 2y/6mo/1mo-step in Youssefi versus 12mo/3mo/3mo-step in Bysik; neither establishes optimality.[1][3]
- Feature count varies by source: Youssefi chooses 20 after an empirical check; Bysik's 10 indicator groups are not equivalent to top-10 individual features.[1][3]
- Feature importance is method-dependent; Youssefi compares MI, RFE, RFI and observes horizon/model variation, weakening a universal selector claim.[1]
- Objective differs: literature often price forecasting or profitable trading, while this study is return-error association, not profit.

## Recommended Methodology (preliminary, not freeze)

1. Keep Binance snapshot/hash and provisional next-day log-return estimand.
2. Keep causally computed candidate pool only after formula audit; document rolling-vs-Wilder deviations explicitly.
3. Compare candidate selector designs during methodology review, not on OOS. If XGBoost Gain remains, name it model-specific gain-ranked selector, fit on train only.
4. Do not carry K=10 automatically. Pick a fixed K by prespecified independent rule or adopt a stability score supporting variable K; justify universe and chance correction.
5. Treat Jaccard descriptive primary only provisionally; Kuncheva secondary only under equal K.
6. Do not lock PatchTST absent BTC/daily/small-sample justification. XGBoost/zero-return are candidates, not final model commitments.
7. Use one primary error and one primary stability-error association; freeze multiple-testing plan and serial-dependence inference before computation.
8. Recompute exact final window count from final method and data after all decisions. Current conditional count is 71, not ~73.

## FINAL PRE-FREEZE METHODOLOGY

| Component | Rule | Evidence | Confidence | Status |
|---|---|---|---|---|
| Dataset | Phase 2 Binance BTC/USDT daily snapshot/hash | Exact audited project record | High | LOCKED source only |
| Target | next-day log return | Direct crypto precedent but no target comparison [1] | Medium | PROVISIONAL |
| Features/formulas | 30 candidate predictors; explicit formulas still audit | Indicator families in BTC daily work [1] | Low–medium | NOT YET LOCKED |
| Train/validation/OOS/step | NOT YET LOCKED | Distinct prior designs, no optimum evidence [1][3] | Low | REQUIRES DECISION |
| Selector/importance | NOT YET LOCKED; Gain candidate only | XGBoost algorithm source not comparative support [10] | Low | REQUIRES DECISION |
| K | NOT YET LOCKED; do not inherit K=10 | Prior K rules are context-specific [1][3] | Low | REQUIRES DECISION |
| Stability metrics | Jaccard candidate; Kuncheva conditional on equal K/N | Adjacent BTC diagnostic and theoretical definitions [3][8] | Medium | PROVISIONAL |
| Forecast model | NOT YET LOCKED; PatchTST not justified yet | General benchmark evidence [6] | Low | REQUIRES DECISION |
| Error metrics | MAE + RMSE candidates; designate primary | General forecasting metric definitions [11] | Medium | PROVISIONAL |
| Association/inference | NOT YET LOCKED; no pilot p-value inference | Rank/bootstrapping sources not tailored to this panel [13][14] | Low | REQUIRES DECISION |
| Leakage | causal t features, shifted t+1, train-only selector/scaler | Code/test audit | Medium-high | PROVISIONAL pending full configuration |

## Remaining Uncertainties

- Full methodological reading required for Barak & Parvini, Youssefi's cited appendices/split semantics, Bysik fold details, Elmakias full simulations, WinnowML, Tripathi & Sharma, Peng, iTransformer.
- Whether Youssefi's temporal stability is subset recurrence across forecast horizons vs temporal windows; their RQ and wording establishes close overlap but not exact paired-window analysis. Verify tables/appendix and definitions.
- Clarify target in Youssefi: section calls log returns target, while paper title/results call price forecasting and RMSLE; avoid oversimplified claim.
- Define exact final features (RSI/ATR smoothing, std ddof, volume change, OBV resets), K selection, selector family, forecast model, window design, primary error, association statistic and inference.
- Estimate runtime/resources only after model and fit count frozen. No trustworthy full-experiment benchmark available in this audit; do not invent runtime.

## Decisions that Must Be Frozen Before Full Experiment

Target date alignment; fixed input feature formulas; candidate pool; train/validation/OOS/step; selector and importance; K rule; stability score(s); forecaster and exact hyperparameters; tuning nesting; scaling; random seeds; primary error/association; dependence-aware inference and block length; multiplicity; exact fold enumeration; expected training count/resources; source hash.

## Research Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| Nearest prior directly asks temporal stability and performance | Critical | Narrow gap; do one-paper knockout on its exact stability unit/outcome and Barak/Bysik |
| Pilot-based K choice contaminates freeze | High | Discard as justification; choose before final OOS use |
| Small effective number of dependent windows | Critical | Power/precision assessment; report descriptive CI, avoid naive p-values |
| Correlated engineered predictors distort gain rankings | High | Fix pool, document instability interpretation; selector sensitivity only if prespecified |
| Indicator formula mismatch with literature/defaults | Medium-high | Formula/version table; unit tests on known hand examples |
| Neural model too data-hungry/architecture mismatch | High | Do not lock PatchTST without explicit input/task suitability and resource review |
| Post-hoc multiple metrics/models | High | One preregistered primary pair and adjustment for secondary tests |
| Snapshot/source mismatch | Low after hash assertion | Reverify SHA-256 before run |

## Search/read coverage

Sources were searched in parallel across publisher/arXiv and methodological works. Full text read: Youssefi 2025; Bysik 2026 partial; PatchTST paper partial; project source files. Abstract/record or partial: Barak & Parvini; Elmakias; Lazebnik & Rosenfeld; WinnowML; Tripathi & Sharma; Peng. iTransformer not sufficiently reviewed. This is an adversarial screening pass, **not exhaustive systematic review**. Search snippets were not treated as load-bearing support.

## Sources
[1] https://www.techscience.com/cmc/v83n2/60595/html
[3] https://arxiv.org/html/2606.00060v1
[4] https://www.mdpi.com/2227-7390/14/13/2372
[5] https://link.springer.com/article/10.1007/s10472-024-09936-8
[6] https://arxiv.org/abs/2211.14730
[7] https://jmlr.org/papers/v18/17-514.html
[8] https://lucykuncheva.co.uk/papers/lkAIA07.pdf
[9] https://www.pnnl.gov/publications/winnowml-stable-feature-selection-maximizing-prediction-accuracy-time-based-system
[10] https://doi.org/10.1145/2939672.2939785
[11] https://otexts.com/fpptr/accuracy.html
[13] https://doi.org/10.1214/aos/1176347265
[14] https://doi.org/10.1080/01621459.1994.10476870
[16] https://doi.org/10.1016/j.ijforecast.2019.04.014
[18] https://doi.org/10.1002/fut.22453
[19] https://doi.org/10.1007/s10614-022-10325-8
[20] https://doi.org/10.1016/j.mlwa.2021.100060
[31] https://xgboost.readthedocs.io/en/stable/python/python_api.html
[32] https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
[33] https://arxiv.org/abs/2310.06625
[34] https://doi.org/10.1080/02664763.2022.2137115
