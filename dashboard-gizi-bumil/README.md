# 🤰 Dashboard Monitoring & Analisis Status Gizi Ibu Hamil — Kota Semarang

> **Kelompok 2 — Lab Sains Data, Bisnis Digital FEB UNDIP.** Dikerjakan oleh **Shaula Putri** (shaulaputri-tech) dengan bantuan AI (Claude); catatan prosesnya ada di [`LOG-AI.md`](../LOG-AI.md) di root repo.

Dashboard interaktif (Streamlit + Plotly) untuk memantau dua indikator gizi ibu hamil
yang **dianalisis terpisah**:

- **Kurang Energi Kronis (KEK)**: Lingkar Lengan Atas (LiLA) < 23,5 cm
- **Anemia**: kadar hemoglobin < 11 g/dl

Semua angka berasal dari sumber resmi pemerintah. **Tidak ada data dummy, simulasi, atau
estimasi.** Nilai yang tidak valid di sumber dikosongkan dan diberi catatan.

🔗 **Demo langsung:** https://gizi-bumil-semarang.streamlit.app

## Fitur
| Tab | Isi |
|---|---|
| 📈 Tren Kota | Persentase atau jumlah kasus 2017–2024, indeks kasus vs jumlah ibu hamil, catatan kualitas data |
| 🗺️ Peta & Wilayah 2022 | Peta per kecamatan, grafik batang kecamatan, grafik per Puskesmas dengan selang kepercayaan 95% |
| ⚖️ KEK vs Anemia | Scatter kuadran per Puskesmas, korelasi peringkat, kategori "beban ganda" |
| 💡 Insight & Rekomendasi | Insight otomatis yang mengikuti filter, rekomendasi berbasis data |
| 📄 Data & Metodologi | Tabel data, unduh CSV, definisi, keterbatasan |

Filter: **Tahun**, **Indikator** (KEK & Anemia / KEK / Anemia), **Ukuran** (Persentase / Jumlah kasus),
**Kecamatan**.

## Sumber data
| Data | Penerbit | Cakupan |
|---|---|---|
| [Portal Satu Data Kota Semarang](https://data.semarangkota.go.id/opendata?cari=hamil), elemen 11707, 13476, 11709, 12282, 13493, 11703, 11704 | Dinas Kesehatan Kota Semarang | Kota, 2016–2025 |
| [Lampiran Profil Kesehatan Kota Semarang 2022](https://profil-kesehatan.dinkes.semarangkota.go.id/upload/dataset/LAMPIRAN%20PROFIL%20KES%202022%20KOTA%20SEMARANG.pdf), Tabel 32 | Dinas Kesehatan Kota Semarang | 37 Puskesmas, 16 Kecamatan, 2022 |
| [Geoportal Kota Semarang](https://geoportal.semarangkota.go.id/), layer `ADMINISTRASI_AR_KECAMATAN_25K` | Distaru Kota Semarang | Batas 16 kecamatan, skala 1:25.000 |

## Struktur folder
```
dashboard-gizi-bumil/
├── app.py                      # aplikasi Streamlit (file utama untuk deploy)
├── src/
│   ├── data.py                 # pemuatan data, format angka, selang kepercayaan Wilson
│   ├── charts.py               # grafik Plotly & peta
│   └── insights.py             # insight & rekomendasi otomatis
├── data/
│   ├── raw/                    # unduhan asli dari sumber resmi (tidak diubah)
│   ├── interim/                # ekstraksi lengkap Tabel 32 (audit trail)
│   ├── processed/              # data bersih yang dibaca dashboard
│   ├── reference/              # daftar baku Kecamatan–Puskesmas
│   └── geo/                    # GeoJSON kecamatan (sudah dibersihkan)
├── scripts/                    # pipeline: cleaning (Tahap 2), EDA (Tahap 3), peta (Tahap 4)
├── reports/                    # laporan validasi & EDA
├── .streamlit/config.toml      # tema warna
├── requirements.txt            # dependensi dashboard (untuk deploy)
├── requirements-dev.txt        # + pypdf, untuk menjalankan ulang pipeline
└── DEPLOY.md                   # panduan deploy ke Streamlit Community Cloud
```

## Menjalankan secara lokal
```bash
cd dashboard-gizi-bumil
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Buka `http://localhost:8501`.

## Menjalankan ulang pipeline data (opsional)
```bash
cd dashboard-gizi-bumil
pip install -r requirements-dev.txt
python scripts/tahap2_cleaning.py   # validasi & cleaning  → data/processed, reports/tahap2_validasi.md
python scripts/tahap3_eda.py        # EDA                  → data/processed/eda_*, reports/tahap3_eda.html
python scripts/tahap4_geo.py        # batas kecamatan      → data/geo/semarang_kecamatan.geojson
```

## Keterbatasan utama
1. Data KEK/Anemia per Puskesmas **hanya tersedia untuk tahun 2022**.
2. Angka Tabel 32 (2022) berbeda dari Satu Data 2022 karena definisi pencatatannya berbeda,
   sehingga kedua sumber tidak dicampur.
3. Beberapa nilai Satu Data tidak valid atau perlu perhatian. Rinciannya ada di
   [reports/tahap2_validasi.md](reports/tahap2_validasi.md).
4. Data KEK/Anemia tahun 2025 belum tersedia.
5. Semua analisis bersifat **deskriptif/asosiatif**, bukan sebab-akibat.
