# Keputusan dan Pertanyaan Analitik

> **Status: v2** — disesuaikan dengan isi data PIHPS Kota Semarang (lihat `01-riset/sumber-data.md` bagian 7–8):
> satu harga rata-rata kota (bukan per pasar), 21 komoditas pokok (tanpa sayuran), hanya hari kerja, tanpa data gizi.

## Pengguna
Warga Kota Semarang khususnya **ibu rumah tangga dan anak kos** yang mengelola anggaran belanja harian/mingguan untuk
memenuhi kebutuhan pangan pokok secara mandiri.

## Keputusan
Warga Kota Semarang (ibu rumah tangga, anak kos) memutuskan **bahan pangan pokok apa yang dibeli dan kapan membelinya
supaya hemat, setiap minggu**.

## Empat pertanyaan analitik

| Jenis | Pertanyaan | Data yang dipakai |
|---|---|---|
| Deskriptif | Komoditas pangan pokok mana (beras, telur, daging ayam, daging sapi, bawang, cabai, minyak goreng, gula) yang harganya **paling naik-turun** dan bagaimana **tren harganya 2018–2026** di Kota Semarang? | Harga harian per komoditas; koefisien variasi dan perubahan harga |
| Diagnostik | Apakah kenaikan harga terjadi **berulang pada periode tertentu** — bulan tertentu, **menjelang Idul Fitri**, akhir tahun — atau pada **hari kerja tertentu** (Senin–Jumat)? | Harga harian dan rata-rata bulanan; tanggal Idul Fitri |
| Prediktif | Berapa **perkiraan harga** (Rp/kg atau Rp/liter) tiap komoditas pokok untuk **4 minggu ke depan**, beserta rentang ketidakpastiannya? | Rata-rata harga mingguan 2018–2026 |
| Preskriptif | **Kapan sebaiknya membeli atau menyetok** tiap komoditas (bulan dan hari kerja yang cenderung lebih murah, serta apakah harga diperkirakan naik), dan berapa **biaya paket bahan pokok mingguan** untuk anggaran Rp100.000–Rp150.000/minggu? | Hasil diagnostik dan prediktif; paket bahan pokok contoh |

Satuan yang dipakai bersama oleh keempat pertanyaan: **harga per komoditas (Rp/kg atau Rp/liter) di Kota Semarang
per hari kerja, dirangkum per minggu atau per bulan**.

## Yang tidak bisa dijawab dengan data ini
- Perbandingan **antar pasar** di Kota Semarang (PIHPS hanya memberi satu harga rata-rata kota).
- Harga **sayuran** dan harga **akhir pekan** (tidak ada di data).
- **Kandungan gizi** paket belanja (perlu sumber tambahan, mis. Tabel Komposisi Pangan Indonesia); karena itu paket
  preskriptif disebut "paket bahan pokok", bukan "paket bergizi" yang terukur.

## Hasil uji dengan AI
Saat keempat pertanyaan diuji menggunakan AI untuk mengevaluasi keterkaitannya langsung dengan keputusan belanja mingguan pengguna:
1. **Pertanyaan yang ditandai kurang langsung membantu keputusan:** Pertanyaan **Diagnostik** (*mengapa* harga naik karena faktor cuaca/distribusi makro) dinilai paling tidak langsung membantu keputusan praktis konsumen harian, karena ibu rumah tangga atau anak kos tidak bisa mengendalikan rantai pasok—mereka lebih membutuhkan sinyal *kapan* pola kenaikan biasanya terjadi agar bisa menyetok lebih awal.
2. **Perbaikan yang dilakukan:** Pertanyaan Diagnostik dipersempit fokusnya dari sekadar mencari penyebab makro menjadi identifikasi **pola berulang (hari dalam seminggu atau menjelang periode tertentu)** yang memicu kenaikan harga, sehingga hasilnya tetap bisa dipakai pengguna untuk mengatur jadwal belanja mingguan.
3. **Revisi v2 (pencocokan dengan data):** keempat pertanyaan dicocokkan dengan isi data PIHPS. Frasa "antar pasar", "sayuran", "akhir pekan", dan "kandungan gizi" dihapus karena datanya tidak tersedia; satuan bersama diubah menjadi harga per komoditas di Kota Semarang per hari kerja/minggu.
