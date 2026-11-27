## Kaila Adnani

Alat AI: Claude Sonnet 5.5 (Anthropic), lewat claude.ai. Semua entri bertanggal 27 November 2026.

### Entri 1: Memahami tugas dan menyusun langkah kerja

- **Tanggal:** 2026-11-27
- **Nama:** Kaila
- **Perintah:** Mengunggah tangkapan layar tiga issue GitHub (pengambilan data, #5 pembersihan data, #8 berkas pribadi) dan meminta langkah pengerjaan dari awal.
- **Hasil:** Pemetaan tugas, aturan bersama, dan urutan langkah pengerjaan.
- **Yang dicek:** Isi pemetaan saya cocokkan dengan teks issue di GitHub. AI sempat mengira issue pengambilan data dipegang orang lain; saya koreksi karena data itu saya sendiri yang mengambil.

### Entri 2: Skrip pembersihan data (issue #5)

- **Tanggal:** 2026-11-27
- **Nama:** Kaila
- **Perintah:** Mengunggah zip data mentah PIHPS Kota Semarang 2018 sampai 2026 dan meminta pembersihan sesuai checklist issue #5.
- **Hasil:** Skrip `bersihkan_pihps.py` yang menggabungkan file tahunan menjadi tabel format panjang (`tanggal`, `komoditas`, `kategori`, `harga`), mengubah "16,100" menjadi 16100, mengubah "-" menjadi kosong tanpa diisi tebakan, dan merapikan nama komoditas. Keluarannya: data bersih lengkap (48.825 baris), sampel 300 baris, dan catatan temuan kualitas (113 tanggal tanpa data, 1 tanggal kosong sebagian, 22 lonjakan harga lebih dari 50%, tidak ada duplikat).
- **Yang dicek:** (a) AI membandingkan 12 sel acak hasil bersih dengan data mentah dan semuanya cocok. (b) Saya menjalankan ulang skripnya di Google Colab dan hasilnya 48.825 baris, 21 komoditas, dan 300 baris sampel. (c) Saya membuka sampel dan mencocokkan beberapa baris dengan data mentah. (d) Saya membaca isi skrip sampai paham cara kerjanya.

### Entri 3: Kamus data

- **Tanggal:** 2026-11-27
- **Nama:** Kaila
- **Perintah:** Meminta `kamus-data.md` untuk berkas sampel.
- **Hasil:** Kamus berisi kolom, tipe, arti, contoh, catatan pembersihan, dan daftar 21 komoditas dengan 10 kategori.
- **Yang dicek:** AI semula menulis bahwa data kosong "sebagian besar hari libur" tanpa mencocokkan dengan kalender libur; kalimat itu diganti dengan pernyataan yang lebih hati-hati. Saya juga mencocokkan daftar komoditas dan kategori dengan sampel.

### Entri 4: Sumber data (issue pengambilan data)

- **Tanggal:** 2026-11-27
- **Nama:** Kaila
- **Perintah:** Meminta draf `sumber-data.md` untuk topik harga pangan.
- **Hasil:** Berkas berisi sumber, cara mengambil, lisensi dan izin, frekuensi, perkiraan baris, data pribadi, dan keterbatasan.
- **Yang dicek:** Angka dalam berkas (48.825 baris, 113 hari kosong, 2.376 sel kosong, 22 lonjakan) saya cocokkan dengan hasil skrip. Tautan sumber dan keterangan cara pengambilan saya cocokkan dengan `metadata_pengambilan.json` dan dengan halaman situs PIHPS yang saya buka sendiri.

---

## Galih Chandra Athallah

Alat AI: Google Gemini (`gemini.google.com` versi web), diakses lewat Google Chrome di macOS. Semua entri bertanggal 27 November 2026.

### Entri 1: Riset kreatif dan verifikasi bukti 3 dasbor pembanding (Issue #3)

- **Tanggal:** 2026-11-27
- **Nama:** Galih
- **Perintah:** Meminta penyusunan tabel perbandingan 3 dasbor/portal harga pangan untuk `01-riset/riset-kreatif.md` dan mengunggah tangkapan layar bertanggal dari tiga situs resmi (Portal Satu Data Kota Semarang, Panel Harga Pangan Bapanas, dan SP2KP Kementerian Perdagangan RI) untuk diverifikasi kesesuaian filter dan bukti fisiknya.
- **Hasil:** Tabel riset kreatif berisi 3 temuan pembanding lengkap dengan pembuat, tautan, pertanyaan yang dijawab (deskriptif), celah (prediktif & preskriptif), serta rujukan ke tiga berkas tangkapan layar di `00-admin/bukti/` (`bukti-1-satu-data-semarang.png`, `bukti-2-panel-harga-bapanas.png`, `bukti-3-sp2kp-kemendag.png`).
- **Yang dicek:** Saya membuka langsung ketiga situs pemerintah tersebut di browser, memfilter wilayah Kota Semarang/Jawa Tengah dan komoditas pangan, memastikan tanggal dan jam pada tangkapan layar Mac terlihat jelas, serta mencocokkan seluruh nama berkas dan tautan sebelum di-commit.

### Entri 2: Penulisan ulang `KENAPA-KAMI.md` (v1) dan pembersihan Papan Status `README.md` (Issue #3)

- **Tanggal:** 2026-11-27
- **Nama:** Galih
- **Perintah:** Meminta penulisan ulang `KENAPA-KAMI.md` v1 agar selaras dengan topik baru kelompok ("Belanja Hemat Bergizi Semarang") serta pembaruan Papan Status di `README.md` agar mencerminkan pembagian tugas dan progres anggota terkini.
- **Hasil:** Draf lengkap `KENAPA-KAMI.md` v1 (tabel perbandingan alternatif gratis beserta tanggal cek, alasan sistem dibuat, dan batasan kapan alternatif lebih baik) serta `README.md` yang sudah diperbarui dan dibersihkan dari sisa kerangka topik awal (gizi ibu hamil).
- **Yang dicek:** Saya memeriksa ulang kesesuaian isi `KENAPA-KAMI.md` dengan ketiga bukti tangkapan layar di `00-admin/bukti/` dan menghapus direktori `dashboard-gizi-bumil/` agar struktur repositori sepenuhnya selaras dengan topik harga pangan.

### Entri 3: Dokumentasi harness, pengujian skill, dan pencatatan log AI (Issue #8)

- **Tanggal:** 2026-11-27
- **Nama:** Galih
- **Perintah:** Memberikan instruksi Issue #8 serta isi mentah `HARNESS.md`, `SKILL-TERPASANG.md`, dan `LOG-AI.md` untuk melengkapi bagian milik Galih tanpa menimpa catatan Shaula dan Kaila.
- **Hasil:** Penambahan subbagian `Harness Galih Chandra Athallah` dan `Sambungan ke aplikasi lain (riset dasbor pembanding)` di `HARNESS.md`, penambahan hasil uji perbandingan skill serta kandidat skill yang ditolak di `SKILL-TERPASANG.md`, dan pencatatan riwayat kerja AI di `LOG-AI.md`.
- **Yang dicek:** Saya memastikan catatan milik Shaula dan Kaila tetap utuh, nomor commit dan nama berkas bukti cocok dengan riwayat repositori GitHub, dan seluruh entri di-commit langsung menggunakan akun GitHub saya (`galihabdann04-code`).

---

## Shaula Putri

Alat AI: Claude (Claude Code, aplikasi desktop Claude) di laptop Shaula. Entri 1–3 dipulihkan dari commit `3b80c2c`
karena sempat tertimpa saat `LOG-AI.md` diperbarui; isinya tidak diubah selain penyesuaian format.

### Entri 1: Dashboard topik awal — status gizi ibu hamil (sebelum topik diganti)

- **Tanggal:** 2026-11-26
- **Nama:** Shaula
- **Perintah:** Mengerjakan "Dashboard Monitoring dan Analisis Status Gizi Ibu Hamil di Kota Semarang" secara bertahap (Tahap 1–5), hanya dari data resmi, tanpa data dummy, dengan KEK dan Anemia dianalisis terpisah. Setiap tahap disetujui dulu sebelum lanjut.
- **Hasil:** Folder `dashboard-gizi-bumil/` (sumber resmi Satu Data Kota Semarang, Lampiran Profil Kesehatan 2022 Tabel 32, Geoportal Kota Semarang; validasi data; EDA; dashboard Streamlit live di https://gizi-bumil-semarang.streamlit.app). Folder ini kemudian dihapus dari `main` oleh Galih (`74115b4`) karena topik kelompok diganti ke harga pangan; isinya tetap ada di riwayat git.
- **Yang dicek:** Oleh AI: total Tabel 32 cocok dengan baris JUMLAH di PDF; 90 kombinasi filter dashboard lolos tanpa error; pipeline diulang dari repo bersih menghasilkan file identik. Oleh Shaula: menyetujui setiap tahap dan pengaturan deploy.

### Entri 2: Pengisian awal berkas template TK1 (topik awal)

- **Tanggal:** 2026-11-27
- **Nama:** Shaula
- **Perintah:** Mengisi berkas template TK1 berdasarkan pekerjaan dashboard gizi ibu hamil.
- **Hasil:** Draf awal `sumber-data.md`, `keputusan-dan-pertanyaan.md`, `kamus-data.md`, `data/sampel/`, `KENAPA-KAMI.md`, bagian Shaula di `HARNESS.md` dan `SKILL-TERPASANG.md`. Berkas-berkas ini kemudian ditulis ulang anggota lain untuk topik harga pangan.
- **Yang dicek:** Oleh AI: setiap angka diambil dari berkas hasil di `dashboard-gizi-bumil/`.

### Entri 3: Pengambilan data harga pangan PIHPS (Issue #4)

- **Tanggal:** 2026-11-27
- **Nama:** Shaula
- **Perintah:** Mencari sumber harga pangan harian Kota Semarang, lalu mengambil data mentahnya.
- **Hasil:** Sumber terpilih PIHPS Nasional (Bank Indonesia). Script `scripts/ambil_data_pihps.py` mengunduh data harian Kota Semarang, pasar tradisional, 1 Jan 2018 – 27 Nov 2026: 2.325 tanggal × 31 baris (21 komoditas + 10 kategori), 95,1% sel terisi. Data mentah disimpan di `data/mentah/` (tidak di-commit) dan dikirim ke Kaila dalam bentuk zip untuk Issue #5. Kandidat sumber yang ditolak: Satu Data Kota Semarang (tahunan), Satu Data Jateng (1 tanggal), BPS IHK (indeks), Panel Harga Bapanas (ekspor tidak pasti), data penumpang Trans Semarang (tahunan).
- **Yang dicek:** Oleh AI: jumlah tanggal dan sel terisi per tahun dihitung dari berkas yang diunduh; 12 harga dari pengambilan uji (Jan 2018, Jan 2020, Nov 2026) cocok 12/12 dengan berkas akhir.

### Entri 4: Pemeriksaan hasil kerja kelompok dan pelengkapan bagian Shaula

- **Tanggal:** 2026-11-27
- **Nama:** Shaula
- **Perintah:** Memeriksa progres Galih dan Kaila di GitHub, lalu melengkapi bagian Shaula yang kurang.
- **Hasil:** Entri 1–3 dipulihkan; `01-riset/sumber-data.md` dilengkapi tabel inventaris dan catatan sesuai template (isi tulisan Kaila dipertahankan); sampel topik awal (`puskesmas_2022.csv`, `kota_tahunan.csv`) dihapus dari `data/sampel/`; bagian Shaula di `HARNESS.md` dan `SKILL-TERPASANG.md` diperbarui untuk topik harga pangan.
- **Yang dicek:** Oleh AI: angka pada `sumber-data.md` dan `kamus-data.md` buatan Kaila dihitung ulang dari data mentah dan semuanya cocok (48.825 baris, 2.325 tanggal, 2.376 sel kosong = 4,9%, 113 tanggal kosong, 1 tanggal kosong sebagian pada 17 Maret 2022, 22 lonjakan >50%); 300 dari 300 baris `harga_pangan_semarang_sampel.csv` cocok dengan data mentah. Tujuh angka yang terlihat pada tangkapan layar halaman PIHPS (`00-admin/bukti/pihps-halaman.png`, 1–2 Januari 2018) cocok 7/7 dengan data unduhan.

### Entri 5: Dashboard "Belanja Hemat Bergizi Semarang" (Issue #7)

- **Tanggal:** 2026-11-27
- **Nama:** Shaula
- **Perintah:** Membuat dashboard Streamlit untuk topik harga pangan dengan memakai ulang tampilan dashboard topik awal, hanya memakai data ringkasan.
- **Hasil:** Folder `dashboard/`: `siapkan_data.py` (ringkasan bulanan 2.247 baris, mingguan 26 minggu 546 baris, harian 20 hari kerja 420 baris), `app.py` (5 tab: Harga Terbaru, Tren & Pola, Prediksi, Rekomendasi Belanja, Data & Metodologi), `requirements.txt`, `README.md`. Tab Pola, Prediksi, dan Rekomendasi membaca `hasil_analisis/` dari Issue #6; selama belum ada, dashboard menampilkan pemberitahuan.
- **Yang dicek:** Oleh AI: 20 kombinasi filter diuji otomatis tanpa error (dengan dan tanpa hasil analisis); tampilan tiap tab diperiksa di browser; perbaikan format Rupiah di tabel dan kalimat kesimpulan menjelang Idul Fitri (menyebut komoditas paling konsisten, bukan hanya kenaikan terbesar). ⚠ _(Shaula: coba dashboard-nya dan tulis apa yang kamu cek)_

### Entri 6: Menyelesaikan sisa tugas kelompok (Issue #2, #3, #6, #8)

- **Tanggal:** 2026-11-27
- **Nama:** Shaula
- **Perintah:** Mengerjakan sisa tugas yang belum selesai: revisi 4 pertanyaan, perapian `AGENTS.md`/`README.md`, analisis 4 jenis, dan uji skill dataviz. Draf revisi pertanyaan dan analisis sebelumnya sudah dikirim ke Galih dan Kaila (komentar Issue #2 dan #6); karena belum ada perubahan dari mereka, Shaula yang meng-commit, dan mereka tetap bisa meninjau.
- **Hasil:** `01-riset/keputusan-dan-pertanyaan.md` v2 (hasil uji AI dari Galih dipertahankan); struktur folder di `AGENTS.md` dan `README.md`; `scripts/analisis_harga_pangan.py` + `hasil_analisis/` (9 CSV + laporan); `scripts/uji_skill_dataviz.py` + hasil uji di `SKILL-TERPASANG.md`.
- **Yang dicek:** Oleh AI: tanggal Idul Fitri 2018–2025 dicocokkan dengan pengumuman sidang isbat pemerintah (Setkab/Kemenag); model prediksi musiman satu tahun ditolak karena sempat memberi perkiraan cabai turun 31%, bertentangan dengan pola 8 tahun, sehingga dipakai aturan "naif kecuali model lain ≥10% lebih akurat"; hasil analisis identik saat script dijalankan ulang dari root repo; hasil uji dataviz ditulis apa adanya (skill menaikkan kontras, tetapi jarak warna palet bawaan Plotly lebih besar). ⚠ _(Shaula: tambahkan apa yang kamu cek sendiri)_
