# Kamus Data

Topik: status gizi ibu hamil Kota Semarang (dikerjakan Shaula Putri). Kedua berkas adalah hasil bersih dari
`dashboard-gizi-bumil/scripts/tahap2_cleaning.py`; tidak ada data simulasi atau estimasi.

## 1. `data/sampel/puskesmas_2022.csv` (37 baris)
Sumber: Lampiran Profil Kesehatan Kota Semarang 2022, Tabel 32 (Dinas Kesehatan).

| kolom | tipe | arti | contoh |
|---|---|---|---|
| tahun | integer | Tahun data | 2022 |
| kecamatan | teks | Nama kecamatan baku (16 kecamatan; "Smg Tengah" di sumber → "Semarang Tengah") | Semarang Tengah |
| puskesmas | teks | Nama Puskesmas baku ("Ngemplak S" di sumber → "Ngemplak Simongan") | Poncol |
| jumlah_bumil | integer | Jumlah ibu hamil di wilayah Puskesmas | 226 |
| kek_jumlah | integer | Ibu hamil dengan Kurang Energi Kronis (dicatat sebagai komplikasi kebidanan) | 31 |
| anemia_jumlah | integer | Ibu hamil dengan Anemia (dicatat sebagai komplikasi kebidanan) | 60 |
| kek_persen | desimal | kek_jumlah ÷ jumlah_bumil × 100 (nilai turunan) | 13.72 |
| anemia_persen | desimal | anemia_jumlah ÷ jumlah_bumil × 100 (nilai turunan) | 26.55 |
| jenis_persen | teks | Penanda bahwa kolom persen adalah hasil hitung, bukan angka resmi | turunan (kasus / jumlah ibu hamil x 100) |
| sumber | teks | Dokumen, tabel, dan halaman sumber | Lampiran Profil Kesehatan Kota Semarang 2022, Tabel 32, hlm. 48 |
| sumber_url | teks | Tautan dokumen sumber | https://profil-kesehatan.dinkes.semarangkota.go.id/... |

## 2. `data/sampel/kota_tahunan.csv` (62 baris, format panjang)
Sumber: Portal Satu Data Kota Semarang (Dinas Kesehatan), 2016–2025, level kota.

| kolom | tipe | arti | contoh |
|---|---|---|---|
| tahun | integer | Tahun data | 2024 |
| kelompok | teks | KEK, Anemia, atau Sasaran (jumlah ibu hamil) | KEK |
| indikator | teks | Kode indikator: KEK_JUMLAH, KEK_PERSEN, KEK_PERSEN_TURUNAN, ANEMIA_JUMLAH, ANEMIA_PREVALENSI, BUMIL_JUMLAH, BUMIL_K1, BUMIL_K4 | KEK_JUMLAH |
| nilai | desimal / kosong | Nilai bersih yang dipakai analisis; **kosong** jika tidak tersedia atau tidak valid | 1224 |
| satuan | teks | orang atau % | orang |
| jenis_nilai | teks | resmi (dari sumber) atau turunan (dihitung dari dua angka resmi) | resmi |
| status | teks | valid / tidak_tersedia / tidak_valid / perlu_perhatian (hasil validasi) | valid |
| catatan | teks | Alasan status bila bukan valid | Satuan % tetapi nilainya > 100 ... |
| nilai_asli | desimal / kosong | Nilai persis seperti di sumber, sebelum dibersihkan | 1224.0 |
| definisi | teks | Definisi resmi indikator | Ibu hamil dengan LiLA < 23,5 cm |
| sumber | teks | Elemen Satu Data asal | Satu Data Kota Semarang (elemen 11707) |
| sumber_url | teks | Tautan elemen data | https://data.semarangkota.go.id/datasektoral/detail/11707 |

Kolom dibuang: tidak ada kolom data pribadi (semua data berupa agregat wilayah). Dari Tabel 32, kolom komplikasi
lain (perdarahan, TB, malaria, preeklampsia, dll.) tidak dibawa ke sampel karena di luar topik; versi lengkapnya ada
di `dashboard-gizi-bumil/data/interim/tabel32_2022_lengkap.csv`.
