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
- **Yang dicek:** (a) AI membandingkan 12 sel acak hasil bersih dengan data mentah dan semuanya cocok. (b) Saya menjalankan ulang skripnya di komputer sendiri dan hasilnya 48.825 baris, 21 komoditas, dan 300 baris sampel. (c) Saya membuka sampel dan mencocokkan beberapa baris dengan data mentah. (d) Saya membaca isi skrip sampai paham cara kerjanya.

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
