# LAPORAN SINKRONISASI NASKAH ↔ PANDUAN UNISNU (No. 57/PR/UNISNU/V/2023)

Sumber aturan: `docs/HASIL-FIX/panduan-skripsi.docx`
(Peraturan Rektor Universitas Islam Nahdlatul Ulama Jepara Nomor 57/PR/UNISNU/V/2023
tentang Pedoman Penulisan Skripsi, Tugas Akhir, dan Tesis).

Prinsip kerja: **hanya menyelaraskan dokumentasi/format/reproduksibilitas**.
Tidak ada angka, hasil eksperimen, metode, dataset, K, window, atau kesimpulan yang diubah.

File kerja hasil perbaikan:
- `BAB I - III_FIXED.docx`
- `BAB IV_FIXED.docx`
- `BAB V_FIXED.docx`

---

## A. SUDAH DIUPDATE / DIPERBAIKI (terverifikasi di XML)

### A1. Heading & penomoran otomatis (via style, bukan ketik manual)
| Bab | Sebelum | Sesudah |
|---|---|---|
| BAB I | 5 H2 polos, tanpa nomor | 5 H2 → A–E ; 2 H3 → 1–2 |
| BAB II | **28 H2 flat** (H2 "sampai Z/AA") | **9 H2 (A–I)** + H3 + H4 |
| BAB III | **25 H2 flat** | **10 H2 (A–J)** + H3 + H4 |
| BAB IV | 12 H2 + nomor manual (4.1–4.13, lubang 4.9) | 12 H2 → A–L otomatis, lubang ditutup |
| BAB V | nomor manual 5.1–5.3 | 3 H2 → A–C otomatis |

- 14 override `numPr` liar (numId 21,22,25,27–36,38) **dihapus** → heading kini murni ikut style.
- Style `Heading1–Heading4` di-link ke numbering `numId 950 → abstractNum 950`:
  - ilvl0 = `none`  → nomor bab ditulis manual sebagai angka Romawi ("BAB I/II/III"), sesuai panduan.
  - ilvl1 = `upperLetter` "%2."  → subbab **A, B, C …** ✔ (panduan §543–544)
  - ilvl2 = `decimal` "%3."      → anak subbab **1, 2, 3 …** ✔ (panduan §545)
  - ilvl3 = `lowerLetter` "%4."  → **a, b, c …**
- Semua nomor manual yang tersisa di teks heading: **0** (dicek regex `^([A-Z]\.|\d+\.\d+)`).
- Tabel BAB II (9 H2, A–I): Konsep Dasar dan Data · Feature Engineering · Technical Indicators ·
  Feature Selection dan XGBoost · Kestabilan Fitur dan Ukurannya · Evaluasi Forecasting dan
  Analisis Asosiasi · Penelitian Terdahulu · Posisi Penelitian · Kerangka Pemikiran · Hipotesis
  Penelitian · Kesimpulan Tinjauan Pustaka.
- Tabel BAB III (10 H2, A–J): Jenis dan Rancangan Penelitian · Data Penelitian · Pengembangan
  Fitur dan Target · Pembagian Temporal Window · Feature Selection · Analisis Kestabilan Fitur ·
  Forecasting dan Evaluasi · Analisis Asosiasi dan Signifikansi · Validitas dan Pengendalian Data
  Leakage · Robustness dan Reproduksibilitas.

### A2. Margin & ukuran kertas (panduan §536–539, §522)
- Tepi: **atas 4 cm, bawah 3 cm, kiri 4 cm, kanan 3 cm** → **cocok 100%** di ketiga file.
- Kertas: 21,0 × 29,7 cm (A4) → sesuai.

### A3. Spasi & font (panduan §524, §547, §309)
- Style `Normal`: `line=480` = **spasi ganda 2,0** → sesuai isi bagian inti.
- `docDefaults` font: **diubah dari theme (minorHAnsi) → Times New Roman** (ascii/hAnsi/eastAsia/cs).
- Daftar Pustaka: `line=240` (satu spasi antar-baris dalam 1 pustaka) + `after=480`
  (dua spasi antar-pustaka) → **cocok** panduan §532–533.

### A4. Caption tabel & gambar (panduan §530, §578–594)
- `Tabel 2. 1` → **`Tabel 2.1`** ; `tabel 2. 2` → **`Tabel 2.2`** (spasi liar dibersihkan).
- Salah nomor bab: `Gambar 2.1 Tahapan Eksperimen` → **`Gambar 3.1 …`** ;
  `Tabel 2.2 Ringkasan Metodologi` → **`Tabel 3.2 …`** (keduanya ada di BAB III).
- Semua caption `Tabel x` / `Gambar x` kini ber-style **Caption** (rata tengah).
- `Tabel 3.1 Feature Universe Penelitian` dilepas dari Heading 2 → kini caption biasa.

### A5. Sitasi stationary bootstrap (temuan kritis)
- Di file FIXED sudah benar: **"Politis & Romano (1994)"** (2 titik teks) +
  entri Daftar Pustaka: *Politis, D. N., & Romano, J. P. (1994). The Stationary Bootstrap.
  JASA, 89(428), 1303.* → **sudah sinkron** dengan `code/bootstrap_analysis.py`.
- Sisa "de Jesús" = **0**.

### A6. Istilah
- "Daftar Referensi" → diseragamkan menjadi **"Daftar Pustaka"** (sesuai panduan §506).

---

## B. PERLU DITAMBAH (belum ada di naskah)

1. **Bagian awal (front matter)** — belum ada sama sekali di file FIXED:
   Sampul Dalam, **Abstrak (ID) + Abstract (EN)**, Surat Pernyataan, Lembar Persetujuan
   Pembimbing, Lembar Pengesahan, Halaman Persembahan, Moto, Kata Pengantar,
   **Daftar Isi, Daftar Tabel, Daftar Gambar, Daftar Lampiran**. (panduan §310–376)
   → Buat 1 file "BAGIAN AWAL" terpisah.
2. **Abstrak**: 1 halaman, spasi tunggal, **250–500 kata**, diakhiri **maksimal 5 kata kunci** (§317).
3. **Bagian akhir**: **Lampiran** + Daftar Lampiran (§509–513).
4. **Nomor halaman Romawi kecil (i, ii, iii…)** untuk bagian awal; **angka Arab** mulai BAB I
   (§550). Footer saat ini hanya field `PAGE` (Arab) — perlu section break Romawi di depan.
5. **Field TOC** untuk Daftar Isi (belum ada `instrText` TOC di file mana pun).
6. **Nomor persamaan matematik** di tepi kanan dalam tanda kurung, angka Arab (§551–552) —
   perlu dipastikan semua rumus punya `(1)`, `(2)`, …

---

## C. PERLU DIKURANGI / DIHAPUS

1. **BAB V punya 3 subbab (Kesimpulan, Saran, Penutup)** — panduan §444 menyebut
   **cukup 2 subbab: Simpulan dan Saran**. → hapus/lebur "Penutup".
2. **"Daftar Pustaka" muncul di 2 file** (BAB I–III_FIXED *dan* BAB IV_FIXED) →
   saat digabung jadi 1 dokumen, sisakan **satu** saja.
3. **File ganda** `BAB I - III.docx`, `BAB IV.docx`, `BAB V.docx` (versi lama) — sudah
   digantikan `*_FIXED.docx`; jangan dipakai lagi agar tidak salah pakai.

---

## D. KEPUTUSAN USER & TINDAK LANJUT (sudah diterapkan)

1. **Judul skripsi** → **TETAP 17 kata** (keputusan user: dibiarkan apa adanya).
   *"Analisis Kestabilan Temporal Subset Fitur XGBoost Berbasis Jaccard dan Hubungannya
   dengan Error Prediksi Out-of-Sample pada Return Bitcoin"*.
   Catatan: panduan menyebut maks 14 kata untuk judul artikel e-jurnal (§896);
   user memutuskan tetap memakai 17 kata.
2. **Penomoran tabel/gambar → DISESUAIKAN KE PANDUAN (global, §582/§593).**
   Sudah di-renumber berurutan dari bab pertama ke terakhir:
   | Lama | Baru |
   |---|---|
   | Tabel 2.1 Penelitian Terdahulu | **Tabel 1** |
   | Gambar 2.1 Kerangka Konseptual | **Gambar 1** |
   | Tabel 3.1 Feature Universe | **Tabel 2** |
   | Gambar 3.1 Tahapan Eksperimen | **Gambar 2** |
   | Tabel 3.2 Ringkasan Metodologi | **Tabel 3** |
   | Tabel 4.1–4.5 (Karakteristik s.d. Ringkasan Forecasting) | **Tabel 4–8** |
   Referensi di dalam teks ikut diperbarui ("pada Gambar 1", "pada Tabel 3").
3. **Nama BAB II → SUDAH DIUBAH menjadi "LANDASAN TEORI"** (ikut panduan §389 + template
   Daftar Isi §1187). Dua titik diubah di `BAB I - III_FIXED.docx`:
   - Heading1: `BAB II TINJAUAN PUSTAKA` → **`BAB II LANDASAN TEORI`**
   - Heading2: `Kesimpulan Tinjauan Pustaka` → **`Kesimpulan Landasan Teori`**
4. **Ukuran font Heading → SUDAH DISAMAKAN** di ketiga file:
   Heading1 = 14 pt bold, Heading2 = 14 pt bold, Heading3 = **12 pt bold**,
   Heading4 = 12 pt (tanpa bold); semua rFonts = Times New Roman.

---

## E0. PERBAIKAN BUG "Word found unreadable content" (BAB I - III_FIXED.docx)

- **Gejala**: Word menolak membuka `BAB I - III_FIXED.docx`
  ("Word found unreadable content… Do you want to recover?").
- **Diagnosis bertahap**: semua part XML well-formed, rels & content-types lengkap,
  numId valid, re-zip file asli tetap OK → masalah bukan di ZIP tapi di **isi sebuah part**.
  Binary-search swap part dari file asli (yang bisa dibuka) menemukan pemicunya:
  **`word/_rels/document.xml.rels`**.
- **AKAR MASALAH (definitif)**: relasi footer di `document.xml.rels` salah tulis —
  nilai `Type` memakai **kurung kurawal `{...}`** (efek `str(QName)` Python), yaitu
  `Type="{http://...relationships}footer"`. Skema OOXML tidak mengizinkan kurung kurawal
  → Word menandai file korup. Hanya file yang punya footer (ketiga `_FIXED`) yang kena.
- **Perbaikan**: ganti `Type="{...}footer"` → `Type="http://...relationships/footer"`
  pada `word/_rels/document.xml.rels` di ketiga file (dan semua backup yang ikut rusak).
- **Hasil verifikasi (buka via Word COM, bukan cuma python-docx)**:
  ketiga file → **OPEN OK** (BAB I–III 1061 paragraf, BAB IV 335, BAB V 20).
  Isi utuh: heading BAB I (A–E), BAB II (A–K), BAB III (A–J); caption Tabel 1–8 & Gambar 1–2.
- Backup sebelum perbaikan: `_backup_panduan/*_PRERELSFIX.docx`.
- Catatan: perbaikan `styles.xml` (rFonts duplikat) sebelumnya tetap berguna, tetapi
  **bukan** penyebab utama file tidak bisa dibuka — biang keroknya adalah relasi footer ini.

## F. SINKRONISASI ISI (GAP / NOVELTY / RUMUSAN MASALAH)

Perbaikan **murni teks** — tidak menyentuh angka, hasil, atau konfigurasi eksperimen.
Backup: `_backup_panduan/*_PRETEXTSYNC.docx`.

1. **Judul di dalam naskah diseragamkan.** Di BAB I (Latar Belakang) masih tertulis
   judul lama *"Analisis Kestabilan Fitur XGBoost Menggunakan Jaccard pada Prediksi
   Bitcoin Berbasis Time Series"* — judul lama **tidak memuat** aspek "hubungan dengan
   error OOS" yang menjadi inti novelty. Diganti menjadi judul final (17 kata):
   *"Analisis Kestabilan Temporal Subset Fitur XGBoost Berbasis Jaccard dan Hubungannya
   dengan Error Prediksi Out-of-Sample pada Return Bitcoin"*.
   (Catatan: `Analisis Kestabilan Fitur` yang muncul di BAB III adalah **judul sub-bab
   metode**, bukan judul skripsi — dibiarkan.)

2. **Sitasi XGBoost diperbaiki.** Di BAB IV tertulis *"XGBoost diperkenalkan oleh
   Nogueira et al. (2018)"* — **keliru**. XGBoost diperkenalkan oleh **Chen & Guestrin
   (2016)**. Diperbaiki, dan entri Chen & Guestrin (2016) **ditambahkan ke Daftar Pustaka
   BAB IV** (urutan alfabet setelah Bysik, di dalam content control bibliografi).

3. **Redaksi 3 Rumusan Masalah diseragamkan.** BAB IV memakai redaksi berbeda dari
   BAB I (mis. "perubahan fitur penting" vs "perubahan subset fitur hasil feature
   selection XGBoost"; "hubungan antara kestabilan fitur" vs "temporal feature-subset
   stability"). Ketiga RM di BAB IV kini **identik** dengan BAB I (diverifikasi
   `BAB I RM == BAB IV RM` → True).

**Verifikasi**: ketiga file tetap **OPEN OK** di Word (BAB I–III 1061 paragraf,
BAB IV 336, BAB V 20). Nol perubahan pada angka/hasil eksperimen.

## E. STATUS FILE & BACKUP

- `zipfile.testzip()` = OK (tidak ada ZIP rusak) untuk ketiga `_FIXED`.
- Tidak ada file kunci Word (`~$*`), tidak ada `.tmp` sisa.
- Backup berlapis:
  - `_backup_headings/` — sebelum restruktur heading
  - `_backup_panduan/` — sebelum penerapan panduan (+ `*_PREPANDUAN2.docx`)
  - `_backup_panduan/BAB I - III_FIXED_PREHEAD.docx` — sebelum regrouping BAB II/III

---

## F. YANG TIDAK DISENTUH (frozen methodology)

Raw data, data terproses, snapshot, output eksperimen, CSV/JSON hasil, konfigurasi model,
logika feature engineering/selection/stability/forecasting/evaluasi, koreksi C1, dan
**seluruh angka final** — nol perubahan. Semua edit murni pada lapisan dokumen/format.
