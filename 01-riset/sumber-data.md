# Inventaris Sumber Data

Topik: **Status gizi ibu hamil (KEK dan Anemia) di Kota Semarang** — dikerjakan Shaula Putri, lihat folder
[`dashboard-gizi-bumil/`](../dashboard-gizi-bumil/).

Data yang dibutuhkan dari empat pertanyaan: jumlah dan persentase ibu hamil KEK (LiLA < 23,5 cm),
jumlah dan prevalensi ibu hamil Anemia (Hb < 11 g/dl), jumlah ibu hamil (sasaran / K1) per tahun dan per
wilayah (kecamatan, Puskesmas), serta batas wilayah kecamatan untuk peta.

| # | Sumber | Cara mengambil | Lisensi atau izin | Frekuensi | Perkiraan baris | Data pribadi | Dibuka manusia? |
|---|---|---|---|---|---|---|---|
| 1 | [Portal Satu Data Kota Semarang](https://data.semarangkota.go.id/opendata?cari=hamil) — Dinas Kesehatan, elemen 11707 (KEK/LiLA), 13476 (% KEK), 11709 (Anemia), 12282 (prevalensi Anemia), 13493 (jumlah bumil), 11703 (K1), 11704 (K4) | Unduh CSV per elemen: `data.semarangkota.go.id/datasektoral/csv/{id}/2010/2026` | Portal data terbuka pemerintah; beberapa elemen berlabel "Klasifikasi: Tertutup" di metadata tetapi CSV-nya bisa diunduh publik | Tahunan | 7 elemen × 2016–2025 (±60 sel), level **kota** saja | Tidak ada (agregat) | ⚠ _(Shaula: centang setelah membuka tautan sendiri)_ |
| 2 | [Lampiran Profil Kesehatan Kota Semarang 2022](https://profil-kesehatan.dinkes.semarangkota.go.id/upload/dataset/LAMPIRAN%20PROFIL%20KES%202022%20KOTA%20SEMARANG.pdf), Tabel 32 — Dinas Kesehatan | Unduh PDF, ekstrak teks halaman 48 dengan Python (`pypdf`), urutan kolom dicek dari gambar halaman | Dokumen publik Dinkes | Tahunan (hanya 2022 yang memuat KEK & Anemia per Puskesmas) | 37 Puskesmas × 18 kolom | Tidak ada (agregat per Puskesmas) | ⚠ _(centang)_ |
| 3 | [Geoportal Kota Semarang](https://geoportal.semarangkota.go.id/) — layer WFS `ADMINISTRASI_AR_KECAMATAN_25K` (Distaru) | Unduh GeoJSON lewat WFS GeoServer | Geoportal publik Pemkot | Tidak berkala | 16 poligon kecamatan | Tidak ada | ⚠ _(centang)_ |
| 4 | [Lampiran Profil Kesehatan 2021](https://dinkes.semarangkota.go.id/asset/upload/Profil/Profil%202021/Lampiran%202021.pdf) — Dinas Kesehatan | Unduh PDF | Dokumen publik Dinkes | Tahunan | 37 Puskesmas | Tidak ada | ⚠ _(centang)_ |

## Catatan
- **Sumber utama:** nomor 2 (per Puskesmas) untuk perbandingan wilayah, nomor 1 untuk tren kota.
  **Belum memenuhi** syarat ~500 baris atau minimal 24 periode: per Puskesmas hanya 37 baris untuk satu tahun (2022),
  dan tren kota hanya 8 periode tahunan (2017–2024).
- **Keterbatasan sumber:**
  - Data KEK/Anemia per Puskesmas hanya tersedia untuk 2022; tahun 2021 (sumber 4) hanya memuat jumlah ibu hamil dan TTD.
  - Satu Data berisi beberapa nilai tidak valid: "% KEK" 2021–2022 berisi jumlah kasus, jumlah Anemia 2023 sama
    dengan jumlah K1, nilai 2016 bernilai 0. Rincian di `dashboard-gizi-bumil/reports/tahap2_validasi.md`.
  - Angka 2022 Tabel 32 (KEK 1.922, Anemia 3.163) berbeda dari Satu Data 2022 (KEK 1.790, Anemia 2.971) karena
    definisi pencatatan berbeda; keduanya tidak digabung.
  - Data KEK/Anemia 2025 belum tersedia.
  - Atribut `WADMKC` pada layer Geoportal tidak cocok dengan geometrinya; dipakai `NAMOBJ` + kode `KDCPUM`.
- **Usulan AI yang ternyata salah atau tidak dipakai** (juga dicatat di `LOG-AI.md`):
  1. Publikasi "Profil Kesehatan Kota Semarang 2023" dari BPS — ternyata berbasis Susenas, tidak memuat KEK/Anemia.
  2. Batas wilayah dari geoBoundaries — layer kecamatan (ADM3) Indonesia tidak tersedia.
  3. Angka KEK/Anemia dari jurnal (mis. "KEK 8,16% tahun 2021") — ditolak karena bukan sumber resmi primer.
  4. Portal Satu Data Jawa Tengah — tidak bisa diakses (koneksi ditolak) sehingga tidak dipakai.
  Total: 4 dari 8 kandidat sumber yang diperiksa tidak dipakai (50%).

⚠ Aturan kelompok: setiap sumber di tabel ini harus sudah dibuka sendiri oleh anggota kelompok. Kolom
"Dibuka manusia?" diisi oleh anggota yang membukanya.
