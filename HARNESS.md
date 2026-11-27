# HARNESS

> Bagian Shaula Putri sudah diisi. Galih dan Kaila menambahkan harness masing-masing jika berbeda.

Harness       : Claude Code (aplikasi desktop Claude, tab Code), dipasang di laptop Shaula (macOS)
Biaya         : ⚠ _(Shaula: isi paket langganan Claude yang dipakai; dicek tanggal ...)_
Agent Skills  : Didukung. Skill pribadi di `~/.claude/skills/`, skill proyek di `.claude/skills/` dalam repo.
                Skill yang dipakai pada proyek ini dicatat di `SKILL-TERPASANG.md`.
File instruksi: AGENTS.md. Catatan: Claude Code membaca `CLAUDE.md`; template meminta nama berkas disesuaikan
                dengan harness ⚠ _(disepakati kelompok: ganti nama atau buat salinan CLAUDE.md)_
Bukti GitHub  : Commit dashboard `a215dc4` (folder `dashboard-gizi-bumil/`) dibuat oleh AI atas nama shaulaputri-tech.
                Baris `Co-authored-by` dihapus dari riwayat atas permintaan Shaula; pemakaian AI dicatat di `LOG-AI.md`.

## Sambungan ke aplikasi lain
Aplikasi : (1) Portal Satu Data Kota Semarang, (2) Geoportal Kota Semarang, (3) GitHub, (4) Streamlit Community Cloud
Cara     : (1) unduh CSV per elemen data; (2) WFS GeoServer → GeoJSON; (3) GitHub CLI `gh` (login lewat browser);
           (4) deploy dari repo GitHub, aplikasi live di https://gizi-bumil-semarang.streamlit.app
Uji      : AI membaca 7 berkas CSV Satu Data (1 baris × 9–10 kolom tahun tiap elemen), 16 poligon kecamatan dari
           Geoportal, dan Tabel 32 PDF Lampiran Profil 2022 (37 baris × 18 kolom; jumlah baris = baris JUMLAH di PDF).
Dicek    : ⚠ _(Shaula: siapa yang mencocokkan angka dengan sumber aslinya, dan hasilnya)_
Bukti    : ⚠ 00-admin/bukti/_(tambahkan tangkapan layar dashboard live / unduhan CSV, bertanggal)_.png

## Harness Kaila Adnani

Harness       : Claude (claude.ai versi web, model Claude Sonnet 5.5), dipakai lewat peramban di laptop Kaila sendiri
Biaya         : Paket yang dipakai: Free dicek 27 November 2026
Agent Skills  : Didukung di claude.ai (butuh fitur code execution aktif). Skill bawaan dipakai otomatis saat Claude
                memproses berkas yang diunggah. Skill yang diuji dicatat di `SKILL-TERPASANG.md`.
File instruksi: Tidak ada. claude.ai tidak membaca AGENTS.md/CLAUDE.md dari repo; instruksi diberikan lewat percakapan.
Bukti GitHub  : Commit dari akun GitHub Kaila sendiri: data/sampel/harga_pangan_semarang_sampel.csv, kamus-data.md,
                01-riset/sumber-data.md, LOG-AI.md. Tangkapan layar: 00-admin/bukti/commit-kaila.png

## Sambungan ke aplikasi lain (data PIHPS)

Aplikasi : (1) PIHPS Nasional Bank Indonesia, (2) GitHub
Cara     : (1) data diambil per tahun 2018-2026 dari halaman tabel harga pasar tradisional Kota Semarang,
           disimpan apa adanya di data/mentah/ (tidak di-commit); (2) skrip Python membersihkan data,
           sampel 300 baris di data/sampel/ di-commit, data lengkap dikirim ke Shaula.
Uji      : AI membaca 9 berkas tahunan (CSV dan JSON, 21 komoditas, 31 baris per berkas) dan menghasilkan
           tabel format panjang 48.825 baris.
Dicek    : Kaila menjalankan ulang skrip (hasil 48.825 baris, 300 baris sampel) dan mencocokkan beberapa baris
           sampel dengan data mentah.
Bukti    : 00-admin/bukti/pihps-halaman.png, data-mentah.png, hasil-skrip.png
