"""
Issue 7 — Menyiapkan data RINGKASAN untuk dashboard "Belanja Hemat Bergizi Semarang".

Sesuai kesepakatan di 01-riset/sumber-data.md (data lengkap tidak disebarluaskan), dashboard hanya memakai:
  data/ringkasan_bulanan.csv    rata-rata harga per bulan per komoditas
  data/ringkasan_mingguan.csv   rata-rata harga per minggu, 26 minggu terakhir
  data/harga_terbaru.csv        harga harian 20 hari kerja terakhir
Hasil analisis (prediksi, pola, rekomendasi) dibaca dari folder hasil_analisis/ di root repo (Issue 6).

Jalankan dari root repo:  python dashboard/siapkan_data.py   (butuh pandas)
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MENTAH = ROOT / "data" / "mentah"
OUT = Path(__file__).resolve().parent / "data"


def muat() -> pd.DataFrame:
    baris = []
    for f in sorted(MENTAH.glob("pihps_kota_semarang_*.json")):
        kategori = None
        for r in json.loads(f.read_text(encoding="utf-8"))["data"]:
            nama = " ".join(str(r["name"]).split())
            if r["level"] == 1:
                kategori = nama
                continue
            for k, v in r.items():
                if "/" in k and v not in (None, "", "-"):
                    baris.append((pd.to_datetime(k, format="%d/%m/%Y"), nama, kategori, int(str(v).replace(",", ""))))
    return pd.DataFrame(baris, columns=["tanggal", "komoditas", "kategori", "harga"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = muat()
    bulanan = (df.assign(bulan=df.tanggal.dt.to_period("M").dt.to_timestamp())
                 .groupby(["bulan", "kategori", "komoditas"], as_index=False).harga.mean())
    bulanan["harga"] = bulanan.harga.round().astype(int)
    mingguan = (df.set_index("tanggal").groupby(["kategori", "komoditas"]).harga.resample("W-FRI").mean()
                  .dropna().reset_index().rename(columns={"tanggal": "akhir_minggu"}))
    batas = mingguan.akhir_minggu.max() - pd.Timedelta(weeks=25)
    mingguan = mingguan[mingguan.akhir_minggu >= batas]
    mingguan["harga"] = mingguan.harga.round().astype(int)
    tgl = sorted(df.tanggal.unique())[-20:]
    terbaru = df[df.tanggal.isin(tgl)].sort_values(["komoditas", "tanggal"])
    for nama, t in [("ringkasan_bulanan", bulanan), ("ringkasan_mingguan", mingguan), ("harga_terbaru", terbaru)]:
        t.to_csv(OUT / f"{nama}.csv", index=False, date_format="%Y-%m-%d")
        print(f"{nama}.csv: {len(t)} baris")


if __name__ == "__main__":
    main()
