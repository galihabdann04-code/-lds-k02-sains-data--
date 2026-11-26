# LOG AI

Format setiap entri: tanggal dan nama anggota, perintah, hasil, dan apa yang dicek atau diperbaiki manusia.

## <tanggal>, <nama>
Perintah: _(isi)_
Hasil   : _(isi)_
Dicek   : _(isi)_

## 26 November 2026, Shaula Putri
Perintah: Meminta AI (Claude, lewat Claude Code) mengerjakan proyek "Dashboard Monitoring dan Analisis
          Status Gizi Ibu Hamil di Kota Semarang" secara bertahap (Tahap 1–5), hanya dari data resmi,
          tanpa data dummy, dengan KEK dan Anemia dianalisis terpisah. Setiap tahap disetujui dulu sebelum lanjut.
Hasil   : Folder `dashboard-gizi-bumil/` berisi:
          - Tahap 1: sumber resmi — Satu Data Kota Semarang (7 elemen data), Lampiran Profil Kesehatan
            Dinkes 2022 Tabel 32 (37 Puskesmas), Geoportal Kota Semarang (batas 16 kecamatan).
          - Tahap 2: validasi & cleaning (`scripts/tahap2_cleaning.py`); 3 sel tidak valid dikosongkan,
            9 sel ditandai "perlu perhatian" (`reports/tahap2_validasi.md`).
          - Tahap 3: EDA deskriptif (`reports/tahap3_eda.md`, `reports/tahap3_eda.html`).
          - Tahap 4: dashboard Streamlit (`app.py`, `src/`).
          - Tahap 5: `requirements.txt`, `DEPLOY.md`; live di https://gizi-bumil-semarang.streamlit.app
Dicek   : Oleh AI (otomatis): total Tabel 32 cocok dengan baris JUMLAH di PDF; 90 kombinasi filter
          dashboard lolos tanpa error; pipeline diulang dari repo bersih menghasilkan file identik;
          angka kartu 2024 di link publik dicek (K1 18.338, % KEK 6,67%, Anemia 4,11%).
          Oleh Shaula: menyetujui setiap tahap, memilih repo & pengaturan deploy.
          _(Shaula: tambahkan di sini bagian yang kamu cek/cocokkan sendiri dengan sumber aslinya.)_
Catatan : Masalah di data sumber yang ditemukan & ditangani: atribut `WADMKC` di layer Geoportal tidak cocok
          dengan geometri (dipakai `NAMOBJ`); CSV Satu Data rusak karena koma tanpa kutip ("23,5 Cm").
