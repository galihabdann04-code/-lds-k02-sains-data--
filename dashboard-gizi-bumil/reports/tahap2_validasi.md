# Laporan Validasi Tahap 2

Dihasilkan otomatis oleh `scripts/tahap2_cleaning.py`.

## A. Data level kota (Satu Data Kota Semarang)

| Status | Jumlah sel |
|---|--:|
| valid | 45 |
| perlu_perhatian | 9 |
| tidak_tersedia | 5 |
| tidak_valid | 3 |

### Sel yang tidak valid / perlu perhatian

| Tahun | Indikator | Nilai asli | Status | Catatan |
|---|---|--:|---|---|
| 2023 | ANEMIA_JUMLAH | 21375 | tidak_valid | Nilai (21,375) identik dengan jumlah K1 tahun 2023; tidak konsisten dengan prevalensi resmi 8.8% |
| 2017 | ANEMIA_PREVALENSI | 18.34 | perlu_perhatian | Tidak konsisten: jumlah anemia/K1 = 13.93% vs resmi 18.34% |
| 2018 | ANEMIA_PREVALENSI | 17.24 | perlu_perhatian | Tidak konsisten: jumlah anemia/K1 = 18.06% vs resmi 17.24% |
| 2019 | ANEMIA_PREVALENSI | 15.05 | perlu_perhatian | Tidak konsisten: jumlah anemia/K1 = 15.69% vs resmi 15.05%; Nilai sama persis dengan tahun 2020 (15.05%) |
| 2020 | ANEMIA_PREVALENSI | 15.05 | perlu_perhatian | Nilai sama persis dengan tahun 2019 (15.05%) |
| 2022 | BUMIL_JUMLAH | 22872 | perlu_perhatian | Jumlah ibu hamil identik dengan K4 pada 2022 (22,872); kemungkinan disalin antar-seri |
| 2023 | BUMIL_JUMLAH | 20698 | perlu_perhatian | Jumlah ibu hamil identik dengan K4 pada 2023 (20,698); kemungkinan disalin antar-seri |
| 2018 | BUMIL_K4 | 26131 | perlu_perhatian | K4 identik dengan K1 (retensi 100%) pada 2018 (26,131); kemungkinan disalin antar-seri |
| 2019 | BUMIL_K4 | 25655 | perlu_perhatian | K4 identik dengan K1 (retensi 100%) pada 2019 (25,655); kemungkinan disalin antar-seri |
| 2020 | BUMIL_K4 | 25981 | perlu_perhatian | K4 identik dengan K1 (retensi 100%) pada 2020 (25,981); kemungkinan disalin antar-seri |
| 2021 | KEK_PERSEN | 1721 | tidak_valid | Satuan % tetapi nilainya > 100 (berisi jumlah kasus, sama dengan elemen 11707) |
| 2022 | KEK_PERSEN | 1790 | tidak_valid | Satuan % tetapi nilainya > 100 (berisi jumlah kasus, sama dengan elemen 11707) |

### Tabel bersih (nilai yang dipakai dashboard)

| Indikator | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ANEMIA_JUMLAH | 4,006 | 4,718 | 4,026 | 4,030 | 2,962 | 2,971 |  | 755 |  |
| ANEMIA_PREVALENSI | 18.34 | 17.24 | 15.05 | 15.05 | 12.84 | 12.60 | 8.80 | 4.11 |  |
| BUMIL_JUMLAH |  |  |  |  | 23,885 | 22,872 | 20,698 | 18,338 | 17,636 |
| BUMIL_K1 | 28,758 | 26,131 | 25,655 | 25,981 | 23,075 | 23,503 | 21,375 | 18,338 | 17,636 |
| BUMIL_K4 | 28,060 | 26,131 | 25,655 | 25,981 | 22,040 | 22,872 | 20,698 | 18,104 |  |
| KEK_JUMLAH | 1,979 | 1,493 | 1,331 | 881 | 1,721 | 1,790 | 1,237 | 1,224 |  |
| KEK_PERSEN |  |  |  |  |  |  |  | 6.67 |  |
| KEK_PERSEN_TURUNAN | 6.88 | 5.71 | 5.19 | 3.39 | 7.46 | 7.62 | 5.79 | 6.67 |  |

_Sel kosong = tidak tersedia atau tidak valid (lihat catatan)._

## B. Data per Puskesmas 2022 (Lampiran Profil Kesehatan, Tabel 32)

- Halaman PDF terdeteksi: 48
- Jumlah Puskesmas: 37 | Jumlah Kecamatan: 16

| Kolom | Jumlah baris | Baris JUMLAH di PDF | Cocok |
|---|--:|--:|---|
| jumlah_bumil | 23,503 | 23,503 | ✅ |
| kek | 1,922 | 1,922 | ✅ |
| anemia | 3,163 | 3,163 | ✅ |

- Catatan sumber: baris JUMLAH kolom '% ditangani' tertulis 2,727 (seharusnya 73.8%). Kolom ini tidak dipakai dashboard.
- Judul tabel di PDF tertulis 'TAHUN 0.00' (galat template); tahun 2022 dipastikan dari nama berkas dan jumlah ibu hamil (23.503) = K1 2022 di Satu Data.

### Penyeragaman nama wilayah

| Nama di sumber | Nama baku |
|---|---|
| Smg Tengah / Poncol | Semarang Tengah / Poncol |
| Smg Tengah / Miroto | Semarang Tengah / Miroto |
| Smg Utara / Bandarharjo | Semarang Utara / Bandarharjo |
| Smg Utara / Bulu Lor | Semarang Utara / Bulu Lor |
| Smg Timur / Halmahera | Semarang Timur / Halmahera |
| Smg Timur / Bugangan | Semarang Timur / Bugangan |
| Smg Timur / Karangdoro | Semarang Timur / Karangdoro |
| Smg Selatan / Pandanaran | Semarang Selatan / Pandanaran |
| Smg Selatan / Lamper Tengah | Semarang Selatan / Lamper Tengah |
| Smg Barat / Karangayu | Semarang Barat / Karangayu |
| Smg Barat / Lebdosari | Semarang Barat / Lebdosari |
| Smg Barat / Manyaran | Semarang Barat / Manyaran |
| Smg Barat / Krobokan | Semarang Barat / Krobokan |
| Smg Barat / Ngemplak S | Semarang Barat / Ngemplak Simongan |

## C. Perbandingan antar-sumber tahun 2022

| Indikator | Satu Data (kota) | Tabel 32 (Σ Puskesmas) | Selisih |
|---|--:|--:|--:|
| KEK (jumlah) | 1,790 | 1,922 | +132 |
| Anemia (jumlah) | 2,971 | 3,163 | +192 |
| Ibu hamil / K1 | 23,503 | 23,503 | +0 |

Kedua sumber **tidak digabung**: Tabel 32 mencatat KEK/Anemia sebagai *komplikasi kebidanan*, sedangkan Satu Data memakai definisi LiLA < 23,5 cm / Hb < 11 g/dl. Dashboard menampilkan masing-masing dengan label sumbernya.
