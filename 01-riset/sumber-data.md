# Sumber Data: Harga Pangan Harian Kota Semarang

Topik kelompok: **Belanja Hemat Bergizi Semarang**

Pengambilan data: **Shaula Putri** (Issue #4, `scripts/ambil_data_pihps.py`). Penulisan ulang berkas ini,
pemeriksaan angka, dan pembersihan data: **Kaila Adnani** (Issue #5).

## Inventaris (ringkas)

Data yang dibutuhkan dari empat pertanyaan: harga harian bahan pangan pokok di Kota Semarang dalam rentang waktu
panjang, untuk melihat tren dan pola, memperkirakan harga ke depan, dan menyusun rekomendasi belanja.

| # | Sumber | Cara mengambil | Lisensi atau izin | Frekuensi | Perkiraan baris | Data pribadi | Dibuka manusia? |
|---|---|---|---|---|---|---|---|
| 1 | [PIHPS Nasional — Bank Indonesia](https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah) (Jawa Tengah → Kota Semarang, pasar tradisional, laporan harian) | Script `scripts/ambil_data_pihps.py`, per tahun 2018–2026 (lihat bagian 2) | Hak cipta PIHPS Nasional, dipakai untuk keperluan akademik dengan menyebut sumber (lihat bagian 3) | Harian, hari kerja | 48.825 baris (21 komoditas × 2.325 tanggal) | Tidak ada | ✅ Dibuka Kaila (bukti `00-admin/bukti/pihps-halaman.png`) |


## 1. Sumber

**PIHPS Nasional (Pusat Informasi Harga Pangan Strategis), Bank Indonesia.**
Halaman: https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah

Cakupan data: harga harian di pasar tradisional, Kota Semarang, Provinsi Jawa Tengah, 1 Januari 2018 s.d. 27 November 2026, untuk 21 komoditas dalam 10 kategori (beras, daging ayam, daging sapi, telur ayam, bawang merah, bawang putih, cabai merah, cabai rawit, minyak goreng, gula pasir).

## 2. Cara mengambil data

Data diambil langsung dari halaman tabel harga PIHPS di tautan pada bagian 1, pada 27 November 2026 (sekitar pukul 14.15 WIB). Pengambilan memakai alamat data yang dipakai halaman tersebut (`https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataDaerah`) dengan parameter jenis pasar tradisional, Provinsi Jawa Tengah, Kota Semarang, dan tipe laporan harian. Pengambilan dilakukan per tahun (2018 sampai 2026) agar ukuran data tidak terlalu besar. Respons disimpan apa adanya, tanpa diubah, dalam format CSV dan JSON per tahun di `data/mentah/`, bersama berkas `metadata_pengambilan.json` yang mencatat alamat, parameter, dan waktu pengambilan.

Berkas mentah tidak di-commit. Yang di-commit hanya sampel bersih di `data/sampel/`.

## 3. Lisensi dan izin pemakaian

Halaman tabel harga PIHPS mencantumkan pernyataan hak cipta milik PIHPS Nasional (seluruh hak dilindungi) dan tidak mencantumkan lisensi terbuka. Karena itu, data diperlakukan sebagai data milik PIHPS Nasional yang dipakai hanya untuk keperluan akademik (tugas perkuliahan), dengan selalu mencantumkan sumbernya. Data mentah tidak disebarluaskan: berkas mentah dan data bersih lengkap tidak diunggah ke repositori, dan yang dibagikan hanya sampel kecil (300 baris) sebagai contoh struktur data.

## 4. Frekuensi data

Harian, pada hari kerja (Senin sampai Jumat). Tidak ada data untuk akhir pekan. Data terakhir yang diambil bertanggal 27 November 2026.

## 5. Perkiraan jumlah baris

Data mentah berupa 9 berkas tahunan, masing-masing 31 baris (10 baris kategori dan 21 baris komoditas) dengan satu kolom per hari kerja. Setelah diubah ke format panjang (hanya baris komoditas), tabel bersih berisi **48.825 baris** (21 komoditas x 2.325 tanggal).

## 6. Data pribadi

Tidak ada. Data berupa harga komoditas (rata-rata) per tanggal, tanpa identitas pedagang, pembeli, atau individu lain.

## 7. Keterbatasan

1. **Hari libur tidak ada data.** Pada hari libur, nilai harga berupa tanda "-" dan diperlakukan sebagai kosong. Ada 113 tanggal tanpa data sama sekali dan 1 tanggal kosong sebagian (17 Maret 2022). Kecocokan tanggal kosong dengan kalender libur resmi belum diperiksa.
2. **Tanda "-" berarti kosong.** Total 2.376 sel (4,9%). Nilai kosong tidak diisi dengan perkiraan.
3. **Satuan harga per kg atau liter**, dalam Rupiah, sesuai komoditas.
4. **Harga adalah rata-rata** dari pasar tradisional yang disurvei PIHPS di Kota Semarang, sehingga tidak mewakili harga di setiap pasar atau pedagang.
5. **Ada lonjakan harga tidak wajar** (lebih dari 50% antar-pengamatan) sebanyak 22 kejadian, sebagian besar pada cabai. Angkanya dibiarkan sesuai sumber dan dicatat di temuan kualitas.
6. **Data 2026 belum penuh**, hanya sampai 27 November 2026.

## 8. Catatan template

- **Sumber utama:** nomor 1. **Memenuhi** syarat ~500 baris dan minimal 24 periode: 48.825 baris; 2.325 periode
  harian atau 107 periode bulanan (Januari 2018 – November 2026).
- **Usulan AI yang tidak dipakai** (rincian di `LOG-AI.md`, entri Shaula 3): 5 dari 6 kandidat sumber yang diperiksa
  tidak dipakai (83%):
  1. Portal Satu Data Kota Semarang — hanya indikator tahunan, bukan harga harian.
  2. Satu Data Jawa Tengah "Harga Kepokmas di Kota Semarang" — hanya satu tanggal (14 April 2023).
  3. BPS "Indeks Harga Konsumen dan Inflasi Kota Semarang" — bulanan, tetapi berupa indeks, bukan harga.
  4. Panel Harga Badan Pangan Nasional — cara ekspor data per kabupaten/kota tidak bisa dipastikan.
  5. Data penumpang Trans Semarang (topik yang sempat dipertimbangkan) — hanya total tahunan 2017–2025.
- **Batas yang perlu diketahui untuk 4 pertanyaan:** PIHPS untuk Kota Semarang hanya memberi **satu** harga rata-rata
  kota (bukan per pasar), **tidak** memuat sayuran, **tidak** ada data akhir pekan, dan **tidak** memuat kandungan gizi.
  Pertanyaan yang membutuhkan hal-hal tersebut memerlukan sumber tambahan atau perlu disesuaikan.

Setiap sumber di tabel ini sudah dibuka sendiri oleh anggota kelompok.
