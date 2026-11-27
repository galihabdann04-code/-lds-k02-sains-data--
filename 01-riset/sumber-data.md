# Inventaris Sumber Data

Topik kelompok: **"Belanja Hemat Bergizi Semarang"** — harga pangan harian Kota Semarang.
Penanggung jawab pengambilan data: **Shaula Putri** (Issue 4).

Data yang dibutuhkan dari empat pertanyaan: harga harian bahan pangan pokok di Kota Semarang (beras, daging ayam,
daging sapi, telur, bawang, cabai, minyak goreng, gula) dalam rentang waktu panjang, untuk melihat tren,
pola musiman, memperkirakan harga ke depan, dan menyusun rekomendasi belanja.

| # | Sumber | Cara mengambil | Lisensi atau izin | Frekuensi | Perkiraan baris | Data pribadi | Dibuka manusia? |
|---|---|---|---|---|---|---|---|
| 1 | [PIHPS Nasional — Bank Indonesia](https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah), Tabel Harga Berdasarkan Daerah: Jawa Tengah → **Kota Semarang**, Pasar Tradisional, Laporan Harian | Script [`scripts/ambil_data_pihps.py`](../scripts/ambil_data_pihps.py) (permintaan per tahun ke endpoint tabel situs PIHPS, jeda 3 detik). Bisa juga manual lewat tombol **Download** di situs | Situs mencantumkan "Hak Cipta © PIHPS Nasional". ⚠ _(Shaula: baca ketentuan pemakaian di situs dan tulis ringkasannya di sini)_ | Harian (hari kerja) | 2.325 hari (1 Jan 2018 – 27 Nov 2026) × 21 komoditas ≈ **48.800 baris** format panjang; 95,1% sel terisi | Tidak ada (harga rata-rata pasar) | ⚠ _(Shaula: centang setelah membuka situs sendiri)_ |
| 2 | Kalender hari libur nasional & cuti bersama (untuk analisis diagnostik: Ramadan, Lebaran, Natal/Tahun Baru) | ⚠ _(belum dipilih — sumber resmi SKB Menteri per tahun)_ | Dokumen publik pemerintah | Tahunan | ±20 tanggal per tahun | Tidak ada | ⚠ |

Data mentah disimpan di `data/mentah/` (tidak di-commit, tercantum di `.gitignore`):
9 berkas JSON respons asli + 9 berkas CSV per tahun + `metadata_pengambilan.json` (parameter dan waktu pengambilan).
Diambil pada 27 November 2026.

## Catatan
- **Sumber utama:** nomor 1. **Memenuhi** syarat ~500 baris dan minimal 24 periode
  (±48.800 baris; 2.325 periode harian atau 107 periode bulanan).
- **Isi data:** 31 baris per tanggal = 10 baris **kategori** (rata-rata, level 1) + 21 **komoditas** (level 2):
  beras (6 kualitas), daging ayam ras segar, daging sapi (2 kualitas), telur ayam ras segar, bawang merah,
  bawang putih, cabai merah besar, cabai merah keriting, cabai rawit hijau, cabai rawit merah, minyak goreng
  (curah, kemasan bermerk 1 & 2), gula pasir (premium, lokal).
- **Keterbatasan sumber:**
  - Hanya hari kerja; akhir pekan dan sebagian hari libur tidak ada data.
  - 4,9% sel berisi "-" (tidak ada data) — dibiarkan kosong, **tidak** diisi tebakan (ditangani di Issue 5).
  - Angka memakai koma ribuan ("16,100" = Rp16.100). ⚠ Satuan per komoditas (per kg / per liter) perlu dicek di situs.
  - "Kota Semarang" di PIHPS adalah rata-rata pasar yang dipantau, bukan harga satu pasar tertentu.
  - Respons "Laporan Bulanan" untuk rentang 2018–2026 sekaligus gagal dimuat; karena itu data diambil harian per tahun.
- **Usulan AI yang ternyata tidak dipakai** (juga dicatat di `LOG-AI.md`):
  1. Portal Satu Data Kota Semarang — hanya indikator tahunan (mis. IHK, koefisien variasi harga), bukan harga harian.
  2. Satu Data Jawa Tengah "Harga Kepokmas di Kota Semarang" — hanya satu tanggal (14 April 2023).
  3. BPS "Indeks Harga Konsumen dan Inflasi Kota Semarang" — bulanan tetapi berupa indeks, bukan harga.
  4. Panel Harga Badan Pangan Nasional — situs terbuka, tetapi cara ekspor data per kab/kota tidak bisa dipastikan.
  5. (Topik sebelumnya) Data penumpang Trans Semarang di Satu Data — hanya total tahunan 2017–2025, tidak cukup
     untuk prediksi, sehingga topik dialihkan ke harga pangan.
  Total: 5 dari 6 kandidat sumber tidak dipakai.
- Topik awal (gizi ibu hamil) dan sumber datanya tetap terdokumentasi di [`dashboard-gizi-bumil/`](../dashboard-gizi-bumil/).

⚠ Aturan kelompok: setiap sumber di tabel ini harus sudah dibuka sendiri oleh anggota kelompok.
