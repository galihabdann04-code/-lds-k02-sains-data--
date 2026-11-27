# Dashboard "Belanja Hemat Bergizi Semarang" (Issue #7 — Shaula)

Dashboard Streamlit harga pangan pokok harian di pasar tradisional Kota Semarang (PIHPS Bank Indonesia, 2018–2026).

| Tab | Isi | Jenis analisis |
|---|---|---|
| 🛒 Harga Terbaru | Kartu harga, grafik 20 hari kerja terakhir, tabel semua komoditas + saran | Deskriptif |
| 📈 Tren & Pola | Tren bulanan, komoditas paling naik-turun, pola musiman per bulan, efek menjelang Idul Fitri | Deskriptif, diagnostik |
| 🔮 Prediksi | Perkiraan 4 minggu + rentang 80% dan akurasi model | Prediktif |
| 💡 Rekomendasi Belanja | Saran waktu beli, biaya paket bahan pokok, kalkulator anggaran | Preskriptif |
| 📄 Data & Metodologi | Sumber, batas data, unduhan ringkasan | — |

## Data
- `data/` hanya berisi **ringkasan** (dibuat `siapkan_data.py` dari `data/mentah/`): rata-rata bulanan (2.247 baris),
  rata-rata mingguan 26 minggu terakhir (546 baris), harga harian 20 hari kerja terakhir (420 baris).
  Data lengkap tidak disebarluaskan (lihat `01-riset/sumber-data.md`).
- Tab Pola, Prediksi, dan Rekomendasi membaca hasil analisis dari `hasil_analisis/` di root repo (Issue #6, Kaila).
  Selama folder itu belum ada, dashboard menampilkan pemberitahuan dan tab tersebut menunggu.

## Menjalankan
```bash
pip install -r dashboard/requirements.txt
python dashboard/siapkan_data.py      # perlu data/mentah/ (opsional, data ringkasan sudah ada)
streamlit run dashboard/app.py
```
Deploy di Streamlit Community Cloud: *Main file path* `dashboard/app.py`, Python 3.12.
