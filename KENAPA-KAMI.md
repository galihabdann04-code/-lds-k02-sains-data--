# KENAPA KAMI (v1)

Pertanyaan v1: mengapa perlu sistem database kelompok, padahal sudah ada spreadsheet dan dasbor siap pakai?

> **Status: DRAF** dari pekerjaan dashboard gizi ibu hamil (Shaula Putri). Kolom "ulasan dengan tangkapan layar"
> belum ada; yang tertulis di bawah adalah temuan pemeriksaan data, bukan ulasan pengguna.

## Alternatif yang sudah ada

| Alternatif | Biaya (sumber, tanggal cek) | Kelebihan | Kelemahan dan celah |
|---|---|---|---|
| Tetap manual: membaca PDF Profil Kesehatan Dinkes satu per satu | Gratis (situs Dinkes Kota Semarang, dicek 26 Nov 2026) | Data resmi, sampai tingkat Puskesmas | Tabel KEK/Anemia per Puskesmas hanya ada di Lampiran 2022; angka terkunci di PDF dan harus disalin manual; judul Tabel 32 tertulis "TAHUN 0.00" dan total kolom % salah hitung (2.727) |
| Grafik bawaan Portal Satu Data Kota Semarang | Gratis (data.semarangkota.go.id, dicek 26 Nov 2026) | Bisa diunduh CSV, ada grafik per elemen | Hanya level kota; tiap indikator terpisah sehingga KEK dan jumlah ibu hamil tidak bisa dibandingkan langsung; nilai tidak valid ditampilkan apa adanya (mis. "% KEK" 2021 = 1.721, jumlah Anemia 2023 = 21.375) |
| _(alternatif 3)_ | ⚠ _(isi)_ | | ⚠ _(ulasan, dengan tangkapan layar)_ |

## Alasan sistem kami dibuat
Bukti dari pemeriksaan data (`dashboard-gizi-bumil/reports/tahap2_validasi.md`):
1. 12 sel data kota bermasalah (3 tidak valid, 9 perlu perhatian) yang tidak terlihat di portal; dashboard menandainya.
2. Menggabungkan sumber kota (Satu Data) dan per Puskesmas (PDF) dalam satu tampilan, tanpa mencampur definisinya.
3. Menunjukkan bahwa jumlah kasus bisa menyesatkan: kasus KEK turun 38% (2017–2024), tetapi jumlah ibu hamil
   juga turun 36%, sehingga persentase KEK hampir tetap (6,88% → 6,67%).
4. Membandingkan Puskesmas dengan selang kepercayaan 95% agar Puskesmas kecil tidak salah dicap "tertinggi".

## Kapan alternatif lebih baik
- Jika yang dibutuhkan hanya satu angka kota untuk satu tahun: cukup lihat Satu Data.
- Jika Dinkes kelak menerbitkan data KEK/Anemia per Puskesmas tiap tahun dalam bentuk tabel yang sudah divalidasi,
  dashboard ini hanya menjadi tampilan tambahan.
