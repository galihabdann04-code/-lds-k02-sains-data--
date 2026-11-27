# Laporan Analisis Harga Pangan Kota Semarang

Data: PIHPS Nasional, pasar tradisional Kota Semarang, 2018-01-01 – 2026-11-27, 21 komoditas, 48,825 baris (2,376 kosong).

## 1. Deskriptif

Paling naik-turun dalam setahun (rata-rata koefisien variasi per tahun):

- **Cabai Rawit Merah**: CV 39.4%; rata-rata 2018 Rp35.308 → 2026 Rp60.068 (+70.1%)
- **Cabai Merah Keriting**: CV 36.0%; rata-rata 2018 Rp30.696 → 2026 Rp40.709 (+32.6%)
- **Cabai Merah Besar**: CV 33.3%; rata-rata 2018 Rp35.173 → 2026 Rp38.567 (+9.6%)
- **Cabai Rawit Hijau**: CV 26.9%; rata-rata 2018 Rp32.998 → 2026 Rp53.672 (+62.7%)
- **Bawang Merah Ukuran Sedang**: CV 21.7%; rata-rata 2018 Rp25.806 → 2026 Rp36.018 (+39.6%)

Paling stabil:

- **Beras Kualitas Medium II**: CV 1.9%
- **Beras Kualitas Super I**: CV 1.6%
- **Beras Kualitas Super II**: CV 1.6%

## 2. Diagnostik

Rata-rata perubahan harga 14 hari menjelang Idul Fitri (dibanding 45–31 hari sebelumnya), 2018–2025:

- **Bawang Merah Ukuran Sedang**: +12.3% (naik pada 5 dari 8 tahun)
- **Daging Ayam Ras Segar**: +6.6% (naik pada 8 dari 8 tahun)
- **Daging Sapi Kualitas 2**: +1.7% (naik pada 7 dari 8 tahun)
- **Minyak Goreng Curah**: +1.6% (naik pada 6 dari 8 tahun)
- **Daging Sapi Kualitas 1**: +1.6% (naik pada 7 dari 8 tahun)
- **Cabai Merah Besar**: +1.2% (naik pada 5 dari 8 tahun)

Perbedaan antar hari kerja sangat kecil (rata-rata selisih terbesar per komoditas):

- terbesar Cabai Merah Besar: 1.42 poin persen; median semua komoditas 0.11 poin persen

## 3. Prediktif

Uji mundur 26 minggu terakhir (MAPE rata-rata horizon 1–4 minggu). Model naif dipakai kecuali model lain >= 10% lebih akurat:

- Minyak Goreng Kemasan Bermerk 1: naif (MAPE 0.23%)
- Beras Kualitas Super I: musiman52 (MAPE 0.28%)
- Minyak Goreng Kemasan Bermerk 2: naif (MAPE 0.28%)
- Beras Kualitas Bawah I: naif (MAPE 0.35%)
- Beras Kualitas Super II: musiman52 (MAPE 0.35%)
- Gula Pasir Kualitas Premium: naif (MAPE 0.35%)
- Beras Kualitas Bawah II: musiman52 (MAPE 0.37%)
- Beras Kualitas Medium II: naif (MAPE 0.39%)
- Beras Kualitas Medium I: musiman52 (MAPE 0.45%)
- Minyak Goreng Curah: naif (MAPE 0.75%)
- Daging Sapi Kualitas 1: naif (MAPE 0.87%)
- Gula Pasir Lokal: naif (MAPE 0.96%)
- Daging Sapi Kualitas 2: naif (MAPE 0.97%)
- Bawang Putih Ukuran Sedang: naif (MAPE 2.7%)
- Telur Ayam Ras Segar: naif (MAPE 4.08%)
- Daging Ayam Ras Segar: naif (MAPE 5.11%)
- Bawang Merah Ukuran Sedang: naif (MAPE 7.53%)
- Cabai Rawit Hijau: naif (MAPE 9.54%)
- Cabai Rawit Merah: naif (MAPE 14.85%)
- Cabai Merah Besar: naif (MAPE 15.13%)
- Cabai Merah Keriting: naif (MAPE 16.67%)

## 4. Preskriptif

- **Bawang Merah Ukuran Sedang**: bulan termurah Sep, termahal Apr; perkiraan 4 minggu +0.0%, pola historis bulan depan +9.5% → Pertimbangkan stok (pola historis: bulan depan cenderung naik)
- **Bawang Putih Ukuran Sedang**: bulan termurah Okt, termahal Mar; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.8% → Beli seperti biasa (perkiraan stabil)
- **Beras Kualitas Bawah I**: bulan termurah Jul, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.4% → Beli seperti biasa (perkiraan stabil)
- **Beras Kualitas Bawah II**: bulan termurah Jul, termahal Feb; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.3% → Beli seperti biasa (perkiraan stabil)
- **Beras Kualitas Medium I**: bulan termurah Jan, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.7% → Beli seperti biasa (perkiraan stabil)
- **Beras Kualitas Medium II**: bulan termurah Jul, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.6% → Beli seperti biasa (perkiraan stabil)
- **Beras Kualitas Super I**: bulan termurah Jan, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.5% → Beli seperti biasa (perkiraan stabil)
- **Beras Kualitas Super II**: bulan termurah Jan, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.3% → Beli seperti biasa (perkiraan stabil)
- **Cabai Merah Besar**: bulan termurah Sep, termahal Feb; perkiraan 4 minggu +0.0%, pola historis bulan depan +14.8% → Pertimbangkan stok (pola historis: bulan depan cenderung naik)
- **Cabai Merah Keriting**: bulan termurah Mei, termahal Feb; perkiraan 4 minggu +0.0%, pola historis bulan depan +14.1% → Pertimbangkan stok (pola historis: bulan depan cenderung naik)
- **Cabai Rawit Hijau**: bulan termurah Mei, termahal Jan; perkiraan 4 minggu +0.0%, pola historis bulan depan +26.9% → Pertimbangkan stok (pola historis: bulan depan cenderung naik)
- **Cabai Rawit Merah**: bulan termurah Mei, termahal Jan; perkiraan 4 minggu +0.0%, pola historis bulan depan +35.3% → Pertimbangkan stok (pola historis: bulan depan cenderung naik)
- **Daging Ayam Ras Segar**: bulan termurah Sep, termahal Jun; perkiraan 4 minggu +0.0%, pola historis bulan depan +3.4% → Pertimbangkan stok (pola historis: bulan depan cenderung naik)
- **Daging Sapi Kualitas 1**: bulan termurah Feb, termahal Jun; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.4% → Beli seperti biasa (perkiraan stabil)
- **Daging Sapi Kualitas 2**: bulan termurah Jan, termahal Jun; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.5% → Beli seperti biasa (perkiraan stabil)
- **Gula Pasir Kualitas Premium**: bulan termurah Sep, termahal Mei; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.4% → Beli seperti biasa (perkiraan stabil)
- **Gula Pasir Lokal**: bulan termurah Jul, termahal Apr; perkiraan 4 minggu +0.0%, pola historis bulan depan +0.3% → Beli seperti biasa (perkiraan stabil)
- **Minyak Goreng Curah**: bulan termurah Jul, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +2.4% → Beli seperti biasa (perkiraan stabil)
- **Minyak Goreng Kemasan Bermerk 1**: bulan termurah Agu, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +1.5% → Beli seperti biasa (perkiraan stabil)
- **Minyak Goreng Kemasan Bermerk 2**: bulan termurah Agu, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +1.0% → Beli seperti biasa (perkiraan stabil)
- **Telur Ayam Ras Segar**: bulan termurah Okt, termahal Des; perkiraan 4 minggu +0.0%, pola historis bulan depan +9.7% → Pertimbangkan stok (pola historis: bulan depan cenderung naik)

Paket bahan pokok contoh (1 orang/minggu, asumsi): bulan terakhir Rp81.544; termurah Rp58.645 (2018-09); termahal Rp86.982 (2026-03).

## Catatan
- Tanggal Idul Fitri 2018–2025 sudah dicocokkan dengan penetapan sidang isbat pemerintah.
- Minggu tanpa data diisi nilai minggu sebelumnya hanya sebagai masukan model; nilai aktual tidak diubah.
- Paket bahan pokok adalah contoh dengan jumlah asumsi, bukan standar gizi.
- Semua hasil bersifat deskriptif/asosiatif; tidak menyimpulkan sebab-akibat.