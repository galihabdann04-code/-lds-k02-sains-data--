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
