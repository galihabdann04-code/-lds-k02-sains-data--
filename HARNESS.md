# HARNESS

> Setiap anggota mengisi bagiannya sendiri: Shaula, Kaila, dan Galih.

## Harness Shaula Putri

Harness       : Claude Code (aplikasi desktop Claude, tab Code), dipasang di laptop Shaula (macOS)
Biaya         : ⚠ _(Shaula: isi paket langganan Claude yang dipakai; dicek tanggal ...)_
Agent Skills  : Didukung. Skill pribadi di `~/.claude/skills/`, skill proyek di `.claude/skills/` dalam repo.
                Skill yang dipakai dicatat di `SKILL-TERPASANG.md`.
File instruksi: Claude Code otomatis membaca `CLAUDE.md`; `AGENTS.md` repo ini dibaca bila diminta dalam perintah.
Bukti GitHub  : Commit `3b80c2c` dari akun shaulaputri-tech (`scripts/ambil_data_pihps.py`, `01-riset/sumber-data.md`),
                dikerjakan dengan bantuan AI. Baris `Co-authored-by` tidak dicantumkan atas permintaan Shaula;
                pemakaian AI dicatat di `LOG-AI.md` (bagian Shaula).

## Sambungan ke aplikasi lain (pengambilan data PIHPS)

Aplikasi : (1) PIHPS Nasional Bank Indonesia, (2) GitHub
Cara     : (1) `scripts/ambil_data_pihps.py` meminta tabel harga harian Kota Semarang per tahun (2018–2026) ke alamat
           data halaman PIHPS dan menyimpan respons apa adanya di `data/mentah/` (tidak di-commit), lalu dikirim ke
           Kaila untuk dibersihkan; (2) GitHub CLI `gh` (login lewat browser) untuk commit dan Issue.
Uji      : AI mengunduh 9 berkas tahunan (31 baris × 237–262 tanggal; 72.075 sel, 95,1% terisi).
Dicek    : 12 harga dari pengambilan uji cocok 12/12 dengan berkas akhir; 7 angka pada tangkapan layar halaman PIHPS
           (`00-admin/bukti/pihps-halaman.png`) cocok 7/7 dengan data unduhan.
           ⚠ _(Shaula: tambahkan apa yang kamu cek sendiri)_
Bukti    : `00-admin/bukti/pihps-halaman.png` ⚠ _(Shaula: tambahkan tangkapan layar milikmu sendiri bila ada)_

Catatan: harness yang sama dipakai untuk topik awal (dashboard gizi ibu hamil, lihat `LOG-AI.md` entri Shaula 1).

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

## Harness Galih Chandra Athallah

Harness       : Google Gemini (gemini.google.com versi web), diakses melalui browser Google Chrome di MacBook Galih (macOS)
Biaya         : Paket Google AI Plus (dicek 27 November 2026)
Agent Skills  : Didukung melalui fitur ekstensi/alat bawaan (Google Search, Workspace, analisis dokumen/gambar) serta
                instruksi terstruktur dalam percakapan; hasil pengujian skill dicatat di `SKILL-TERPASANG.md`.
File instruksi: Menggunakan `AGENTS.md` yang dirujuk langsung melalui prompt percakapan karena antarmuka web tidak
                membaca repositori lokal secara otomatis.
Bukti GitHub  : Commit langsung dari akun GitHub `galihabdann04-code`: `01-riset/riset-kreatif.md` (`6641009`),
                `KENAPA-KAMI.md`, `README.md` (`ec5eb65`), serta unggahan tangkapan layar bukti di `00-admin/bukti/` (`c702897`).

## Sambungan ke aplikasi lain (riset dasbor pembanding)

Aplikasi : (1) Portal Satu Data Kota Semarang (`data.semarangkota.go.id`), (2) Panel Harga Pangan Bapanas
           (`panelharga.badanpangan.go.id`), (3) SP2KP Kementerian Perdagangan RI (`sp2kp.kemendag.go.id`), (4) GitHub
Cara     : Membuka langsung ketiga portal data pemerintah melalui browser, memfilter wilayah Kota Semarang/Jawa Tengah
           dan kata kunci komoditas pangan, mengambil tangkapan layar bertanggal, lalu mengunggah dan me-commit ke GitHub.
Uji      : AI membantu memetakan fungsi deskriptif dan celah (prediktif & preskriptif) dari ketiga platform tersebut
           berdasarkan hasil eksplorasi dan tangkapan layar yang diunggah ke percakapan.
Dicek    : Galih membuka langsung ketiga tautan portal di browser, memverifikasi ketersediaan dataset tahunan serta
           harga komoditas harian Kota Semarang, dan mencocokkan setiap klaim tabel sebelum di-commit.
Bukti    : `00-admin/bukti/bukti-1-satu-data-semarang.png`, `00-admin/bukti/bukti-2-panel-harga-bapanas.png`,
           `00-admin/bukti/bukti-3-sp2kp-kemendag.png`
