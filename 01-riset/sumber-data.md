# Sumber Data: Harga Pangan Harian Kota Semarang

Topik kelompok: **Belanja Hemat Bergizi Semarang**

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
