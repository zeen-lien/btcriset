# HASIL FIX — Naskah BAB 1–3 (oleh asisten)

> ⚠️ **File asli kamu TIDAK disentuh.** Semua hasil ada di folder ini.
> Sumber: `docs/Proposal dan bab 1-5/bab 1-3.docx` (tetap utuh, tidak diubah).

## 📄 File hasil

| File | Isi |
|---|---|
| **`bab 1-3_FIXED.docx`** | Naskah BAB 1–3 dengan **rumus sudah jadi equation Word**, heading ber-style, referensi betul |
| `README.md` | Dokumen ini |

## ✅ Yang sudah diperbaiki

| # | Perbaikan | Jumlah | Detail |
|---|---|---|---|
| 1 | **Rumus LaTeX → equation Word** | **127 rumus** | `\frac...`, `[ ]`, `\rho`, `\sigma`, dll → pecahan & simbol beneran |
| 2 | **Heading diberi style H1/H2/H3** | 11 heading | BAB II: 2.9.2, 2.12, 2.21, 2.23, 2.27, 2.28 · BAB III: 3.6.8, 3.10.2, 3.13.2, 3.22, 3.23 |
| 3 | **Referensi Barak** | 1 entri + 6 sitasi | `Barak S, P. N. (2023)` → `Barak, S., & Parvini, N. (2023)`; sitasi `(Barak S, 2023)` → `(Barak & Parvini, 2023)` |
| 4 | **Hyperlink nyasar "MDPI"** | 1 | dihapus dari akhir paragraf 2.27 |

## 📊 Sebelum vs Sesudah

| Metrik | ASLI | FIXED |
|---|---|---|
| `\frac` mentah | 22 | **0** ✅ |
| Kurung `[ ]` nyasar | 125 | **0** ✅ |
| Pecahan beneran (`m:f`) | 5 | **35** ✅ |
| Hyperlink "MDPI" | 1 | **0** ✅ |
| Total equation | 212 | 212 |
| Jumlah paragraf | 997 | 997 (**nol konten hilang**) |

## 🔍 Cara cek hasilnya

1. Buka `bab 1-3_FIXED.docx` di Word
2. Lihat rumus Jaccard (§2.14) → harus jadi **pecahan beneran** `|St ∩ St+1| / |St ∪ St+1|`
3. Lihat MAE (§2.19) & RMSE (§2.20) → pecahan beneran
4. Buka **References → Table of Contents → Update** → heading yang baru udah kebaca
5. Bandingkan dengan file asli — teks, gambar, tabel semua utuh

## ⚠️ BELUM diperbaiki (butuh keputusan kamu)

### 1. 🔴 Entri daftar pustaka DUPLIKAT (9 pasang)
Ini **artefak library Mendeley**, bukan salahmu di Word:
```
Huang (2024a & 2024b) — judul SAMA
Youssefi (2025a, 2025b, 2025c) — judul SAMA
Lazebnik (2024a & 2024b) — judul SAMA
Mudassir (2025a & 2025b) — judul SAMA
Nogueira (2018a & 2018b) — judul SAMA
Chen (2016a & 2016b) — judul SAMA
Bysik (2026a & 2026b) — judul SAMA
Elmakias (2026a & 2026b) — judul SAMA
de Jesús-Gutiérrez (2020a & 2020b) — judul SAMA
```
**Fix terbaik (bukan di Word):**
1. Buka **Mendeley Desktop / Mendeley Reference Manager**
2. Cari tiap judul → **hapus entri duplikat** (sisakan 1)
3. Di Word: **References → Refresh** (Mendeley toolbar)
→ Entri dobel otomatis hilang, dan suffix `a/b/c` di teks menyesuaikan sendiri.

**Kenapa jangan gw edit di Word?** Karena sitasi dalam teks = **field Mendeley**. Kalau gw hapus entri di Word manual, field-nya bisa rusak / nggak sinkron lagi. Lebih aman dari sisi Mendeley.

### 2. 🟡 Kalimat >45 kata
BAB III paling banyak. Ini **nulis ulang** — gw nggak mau ubah gaya bahasa kamu tanpa izin. Kalau mau, kasih tau.

### 3. 🟡 Daftar Isi otomatis
File ini belum ada field TOC. Setelah heading rapi, kamu bisa tambah: **References → Table of Contents → Insert Table of Contents**.

---

## 🔧 Cara regenerate

```bash
cd docs/_fix
python fix_docx.py
```

- `latex_map.py` = kamus 126 rumus (LaTeX bener)
- `fix_docx.py` = skrip perbaikan
- Output selalu ke `docs/HASIL-FIX/`, file asli nggak pernah ditulis

## 📌 Backup
Backup file asli: `docs/_backup_<timestamp>/Proposal dan bab 1-5/`
