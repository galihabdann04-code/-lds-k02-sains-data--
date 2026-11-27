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
