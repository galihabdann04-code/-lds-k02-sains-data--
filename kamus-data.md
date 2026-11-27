# Kamus Data

Berkas: `data/sampel/harga_pangan_semarang_sampel.csv` (300 baris, sampel acak dari data bersih lengkap)

Sumber: PIHPS Nasional, Bank Indonesia. Pasar tradisional, Kota Semarang, Provinsi Jawa Tengah, laporan harian, 1 Januari 2018 s.d. 27 November 2026. Sumber data mentah: https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah (hak cipta PIHPS Nasional). Cara pengambilan data dicatat di `sumber-data.md`.

## Kolom

| Kolom | Tipe | Arti | Contoh |
|---|---|---|---|
| `tanggal` | tanggal (YYYY-MM-DD) | Tanggal pencatatan harga (hanya hari kerja, Senin sampai Jumat) | `2023-07-26` |
| `komoditas` | teks | Nama komoditas (level 2 di PIHPS), 21 komoditas | `Gula Pasir Kualitas Premium` |
| `kategori` | teks | Kelompok komoditas (level 1 di PIHPS), 10 kategori | `Gula Pasir` |
| `harga` | bilangan bulat | Harga rata-rata di pasar tradisional dalam Rupiah per kg/liter. Kosong berarti tidak ada data | `14750` |

## Catatan penting

1. Harga kosong berasal dari tanda "-" di data asli dan **tidak diisi** dengan perkiraan. Banyak tanggal kosong bertepatan dengan hari libur, tetapi belum dicocokkan dengan kalender libur resmi. Berkas sampel ini hanya berisi baris yang ada harganya; harga kosong hanya ada di data lengkap.
2. Baris level 1 PIHPS (rata-rata per kategori) tidak dimasukkan agar tidak terjadi hitung ganda. Kolom `kategori` diambil dari baris level 1 tersebut.
3. Angka dengan pemisah ribuan koma (mis. "16,100") sudah diubah menjadi bilangan bulat (16100).
4. Nama komoditas sudah dirapikan (spasi berlebih dihapus).
5. Data lengkap tidak di-commit; hanya sampel ini yang ada di repositori.

## Daftar komoditas dan kategori

| Kategori | Komoditas |
|---|---|
| Beras | Beras Kualitas Bawah I, Beras Kualitas Bawah II, Beras Kualitas Medium I, Beras Kualitas Medium II, Beras Kualitas Super I, Beras Kualitas Super II |
| Daging Ayam | Daging Ayam Ras Segar |
| Daging Sapi | Daging Sapi Kualitas 1, Daging Sapi Kualitas 2 |
| Telur Ayam | Telur Ayam Ras Segar |
| Bawang Merah | Bawang Merah Ukuran Sedang |
| Bawang Putih | Bawang Putih Ukuran Sedang |
| Cabai Merah | Cabai Merah Besar, Cabai Merah Keriting |
| Cabai Rawit | Cabai Rawit Hijau, Cabai Rawit Merah |
| Minyak Goreng | Minyak Goreng Curah, Minyak Goreng Kemasan Bermerk 1, Minyak Goreng Kemasan Bermerk 2 |
| Gula Pasir | Gula Pasir Kualitas Premium, Gula Pasir Lokal |
