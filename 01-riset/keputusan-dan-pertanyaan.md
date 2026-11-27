# Keputusan dan Pertanyaan Analitik

> **Status: DRAF** — disusun ulang untuk proyek **Belanja Hemat Bergizi Semarang** (harga pangan harian Kota Semarang). Pengguna, keputusan, dan pertanyaan perlu disepakati kelompok.

## Pengguna
Warga Kota Semarang khususnya **ibu rumah tangga dan anak kos** yang mengelola anggaran belanja harian/mingguan untuk memenuhi kebutuhan pangan bergizi secara mandiri.

## Keputusan
Warga Kota Semarang (ibu rumah tangga, anak kos) memutuskan **bahan pangan apa yang dibeli dan kapan membelinya supaya hemat dan tetap bergizi, setiap minggu**.

## Empat pertanyaan analitik

| Jenis | Pertanyaan | Progres |
|---|---|---|
| Deskriptif | Komoditas pangan pokok dan sumber gizi (beras, telur, ayam, cabai, sayuran, minyak goreng) apa saja yang memiliki fluktuasi harga harian/mingguan tertinggi di pasar-pasar Kota Semarang, serta bagaimana perbandingannya antar pasar? | 🟡 Sebagian: daftar komoditas utama sudah ditentukan, menunggu pengambilan data harga harian pasar Kota Semarang (Kaila) |
| Diagnostik | Apakah lonjakan harga harian/mingguan pada komoditas tertentu dipicu oleh pola musiman (seperti menjelang hari besar keagamaan atau akhir pekan), atau karena gangguan pasokan lokal di Kota Semarang? | ❌ Belum: memerlukan data historis harga harian lintas musim/bulan untuk analisis korelasi dan pola musiman |
| Prediktif | Berapa perkiraan harga per kilogram/liter untuk komoditas sumber protein dan bahan pokok utama (telur, ayam, beras, cabai) pada minggu depan di Kota Semarang? | ❌ Belum: membutuhkan deret waktu (*time-series*) harga harian yang cukup sebelum pemodelan prediksi |
| Preskriptif | Kapan hari terbaik dalam seminggu untuk berbelanja dan kombinasi paket bahan pangan bergizi apa yang paling murah untuk batas anggaran mingguan tertentu (misalnya Rp100.000–Rp150.000/minggu)? | ❌ Belum: memerlukan data harga harian yang bersih beserta informasi kandungan gizi dasar per komoditas |

Satuan yang dipakai bersama oleh keempat pertanyaan: **harga per komoditas (Rp/kg atau Rp/liter) per pasar di Kota Semarang per hari/minggu**.

## Hasil uji dengan AI
Saat keempat pertanyaan diuji menggunakan AI untuk mengevaluasi keterkaitannya langsung dengan keputusan belanja mingguan pengguna:
1. **Pertanyaan yang ditandai kurang langsung membantu keputusan:** Pertanyaan **Diagnostik** (*mengapa* harga naik karena faktor cuaca/distribusi makro) dinilai paling tidak langsung membantu keputusan praktis konsumen harian, karena ibu rumah tangga atau anak kos tidak bisa mengendalikan rantai pasok—mereka lebih membutuhkan sinyal *kapan* pola kenaikan biasanya terjadi agar bisa menyetok lebih awal.
2. **Perbaikan yang dilakukan:** Pertanyaan Diagnostik dipersempit fokusnya dari sekadar mencari penyebab makro menjadi identifikasi **pola berulang (hari dalam seminggu atau menjelang periode tertentu)** yang memicu kenaikan harga, sehingga hasilnya tetap bisa dipakai pengguna untuk mengatur jadwal belanja mingguan.
