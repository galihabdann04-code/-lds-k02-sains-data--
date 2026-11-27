# AGENTS.md

> Ganti nama berkas sesuai harness yang dipilih: AGENTS.md, CLAUDE.md, atau GEMINI.md.

## Tujuan
Sistem database dan analisis data untuk membantu **warga Kota Semarang (ibu rumah tangga dan anak kos)** memutuskan **bahan pangan apa yang dibeli dan kapan membelinya supaya hemat dan tetap bergizi, setiap minggu** berdasarkan data **harga pangan harian Kota Semarang ("Belanja Hemat Bergizi Semarang")**.

## Aturan
- Jangan menulis kunci, token, atau sandi ke berkas apa pun. Simpan di `.env`.
- Data pribadi (nama, nomor HP, email, alamat, NIK orang sungguhan) tidak masuk repo. Buang kolomnya sebelum data disimpan.
- Data mitra atau pengguna tidak ditempel ke layanan AI yang melatih model.
- Jangan mengubah isi `data/mentah/`.
- Kutipan ulasan selalu dicocokkan dengan tangkapan layarnya.
- Sumber data atau tautan yang belum dibuka manusia tidak boleh masuk tabel riset.

## Struktur
- `01-riset/`: keputusan, pertanyaan, sumber data, riset kreatif
- `data/sampel/`: sampel data bersih
- `kamus-data.md`: kamus data sampel
- `00-admin/`: anggota, izin data, bukti
- `dashboard-gizi-bumil/`: dashboard Streamlit gizi ibu hamil (pipeline data, aplikasi, laporan)

## Log AI
Setiap pekerjaan penting dicatat di `LOG-AI.md`: perintah, hasil, dan yang dicek manusia.
