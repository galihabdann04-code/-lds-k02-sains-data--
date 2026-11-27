"""
Issue 6 — Analisis 4 jenis harga pangan harian Kota Semarang (PIHPS, 2018–2026).

Disiapkan Shaula (dengan bantuan AI) dari draf untuk Issue 6; Kaila dapat meninjau dan mengubahnya.

Masukan : data/mentah/pihps_kota_semarang_<tahun>.json  (hasil scripts/ambil_data_pihps.py)
Keluaran: hasil_analisis/
  deskriptif_ringkasan.csv   tren & fluktuasi per komoditas
  rata_bulanan.csv           rata-rata harga per bulan per komoditas
  diagnostik_bulan.csv       indeks musiman bulanan (1,00 = rata-rata tahunannya)
  diagnostik_lebaran.csv     perubahan harga menjelang Idul Fitri per tahun
  diagnostik_hari.csv        selisih harga per hari kerja terhadap rata-rata minggunya
  prediksi_akurasi.csv       uji mundur 26 minggu terakhir (MAPE) per model & komoditas
  prediksi_4minggu.csv       perkiraan 4 minggu ke depan + rentang 80%
  preskriptif_waktu_beli.csv bulan & hari kerja termurah + sinyal beli sekarang/tunggu
  preskriptif_paket.csv      biaya paket bahan pokok contoh per bulan + perkiraan
  laporan_analisis.md        ringkasan temuan

Jalankan dari root repo: python scripts/analisis_harga_pangan.py   (default: data/mentah → hasil_analisis)
Butuh   : pandas, numpy
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MENTAH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/mentah")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("hasil_analisis")

# Tanggal Idul Fitri (1 Syawal) hasil sidang isbat pemerintah (Kemenag), dicek 27 Nov 2026 pada pengumuman
# Setkab/Kemenag dan berita resmi tiap tahun. 2026 tidak dimasukkan karena belum dicek.
IDUL_FITRI = ["2018-06-15", "2019-06-05", "2020-05-24", "2021-05-13", "2022-05-02",
              "2023-04-22", "2024-04-10", "2025-03-31"]

# Paket bahan pokok CONTOH untuk 1 orang per minggu (asumsi, bukan standar gizi).
PAKET = {
    "Beras Kualitas Medium I": 2.0,        # kg
    "Telur Ayam Ras Segar": 0.5,           # kg
    "Daging Ayam Ras Segar": 0.5,          # kg
    "Minyak Goreng Curah": 0.25,           # liter
    "Gula Pasir Lokal": 0.25,              # kg
    "Bawang Merah Ukuran Sedang": 0.1,     # kg
    "Bawang Putih Ukuran Sedang": 0.05,    # kg
    "Cabai Rawit Merah": 0.05,             # kg
}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


# ---------------------------------------------------------------- 0. data bersih
def muat_bersih() -> pd.DataFrame:
    """Format panjang: tanggal, komoditas, kategori, harga (sesuai kamus-data.md)."""
    baris = []
    for f in sorted(MENTAH.glob("pihps_kota_semarang_*.json")):
        kategori = None
        for r in json.loads(f.read_text(encoding="utf-8"))["data"]:
            nama = " ".join(str(r["name"]).split())
            if r["level"] == 1:
                kategori = nama
                continue
            for k, v in r.items():
                if "/" in k:
                    harga = None if v in (None, "", "-") else int(str(v).replace(",", ""))
                    baris.append((pd.to_datetime(k, format="%d/%m/%Y"), nama, kategori, harga))
    df = pd.DataFrame(baris, columns=["tanggal", "komoditas", "kategori", "harga"])
    df["harga"] = df["harga"].astype("Float64")
    return df.sort_values(["komoditas", "tanggal"]).reset_index(drop=True)


# ---------------------------------------------------------------- 1. deskriptif
def deskriptif(df):
    d = df.dropna(subset=["harga"]).copy()
    d["harga"] = d["harga"].astype(float)
    d["tahun"] = d.tanggal.dt.year
    out = []
    for (kom, kat), g in d.groupby(["komoditas", "kategori"]):
        awal = g[g.tahun == g.tahun.min()].harga.mean()
        akhir_th = g[g.tahun == g.tahun.max()].harga.mean()
        cv_tahunan = g.groupby("tahun").harga.agg(lambda s: s.std() / s.mean() * 100).mean()
        out.append({"komoditas": kom, "kategori": kat,
                    "rata_2018": round(awal), "rata_2026": round(akhir_th),
                    "perubahan_persen": round((akhir_th / awal - 1) * 100, 1),
                    "harga_min": int(g.harga.min()), "harga_max": int(g.harga.max()),
                    "harga_terakhir": int(g.harga.iloc[-1]), "tanggal_terakhir": g.tanggal.iloc[-1].date(),
                    "cv_dalam_tahun_persen": round(cv_tahunan, 1)})
    ring = pd.DataFrame(out).sort_values("cv_dalam_tahun_persen", ascending=False)
    bulanan = (d.assign(bulan=d.tanggal.dt.to_period("M").astype(str))
                 .groupby(["bulan", "komoditas", "kategori"], as_index=False).harga.mean())
    bulanan["harga"] = bulanan.harga.round(0).astype(int)
    return ring, bulanan


# ---------------------------------------------------------------- 2. diagnostik
def diagnostik(df):
    d = df.dropna(subset=["harga"]).copy()
    d["harga"] = d["harga"].astype(float)
    d["tahun"], d["bulan"] = d.tanggal.dt.year, d.tanggal.dt.month
    # a) indeks musiman bulanan: rata-rata bulan / rata-rata tahun itu, dirata-ratakan antar tahun (tahun penuh saja)
    penuh = d[d.tahun <= 2025]
    mb = penuh.groupby(["komoditas", "tahun", "bulan"]).harga.mean().reset_index()
    mb["indeks"] = mb.harga / mb.groupby(["komoditas", "tahun"]).harga.transform("mean")
    idx_bulan = (mb.groupby(["komoditas", "bulan"]).indeks.agg(["mean", "count"]).reset_index()
                   .rename(columns={"mean": "indeks", "count": "jumlah_tahun"}))
    idx_bulan["indeks"] = idx_bulan.indeks.round(3)
    idx_bulan["nama_bulan"] = idx_bulan.bulan.map(lambda b: BULAN[b - 1])

    # b) menjelang Idul Fitri: rata-rata 14 hari sebelum vs 45–31 hari sebelum
    leb = []
    for tgl in pd.to_datetime(IDUL_FITRI):
        for kom, g in d.groupby("komoditas"):
            dekat = g[(g.tanggal >= tgl - pd.Timedelta(days=14)) & (g.tanggal < tgl)].harga.mean()
            dasar = g[(g.tanggal >= tgl - pd.Timedelta(days=45)) & (g.tanggal < tgl - pd.Timedelta(days=30))].harga.mean()
            if pd.notna(dekat) and pd.notna(dasar):
                leb.append({"tahun": tgl.year, "idul_fitri": tgl.date(), "komoditas": kom,
                            "rata_45_31_hari_sebelum": round(dasar), "rata_14_hari_sebelum": round(dekat),
                            "perubahan_persen": round((dekat / dasar - 1) * 100, 1)})
    lebaran = pd.DataFrame(leb)

    # c) hari kerja: selisih harga terhadap rata-rata minggu yang sama (%)
    d["minggu"] = d.tanggal.dt.to_period("W-SUN")
    d["dev"] = (d.harga / d.groupby(["komoditas", "minggu"]).harga.transform("mean") - 1) * 100
    d["hari"] = d.tanggal.dt.dayofweek
    hari = (d[d.hari < 5].groupby(["komoditas", "hari"]).dev.mean().reset_index())
    hari["nama_hari"] = hari.hari.map(lambda h: HARI[h])
    hari["selisih_persen"] = hari.dev.round(3)
    return idx_bulan, lebaran, hari.drop(columns="dev")


# ---------------------------------------------------------------- 3. prediktif
def mingguan(df) -> pd.DataFrame:
    d = df.dropna(subset=["harga"]).copy()
    d["harga"] = d["harga"].astype(float)
    w = (d.set_index("tanggal").groupby("komoditas").harga.resample("W-FRI").mean().unstack(0))
    return w  # index = Jumat akhir minggu; kolom = komoditas; NaN = minggu tanpa data


def ramal(y: np.ndarray, h: int, model: str) -> float:
    t = len(y) - 1
    if model == "naif":
        return y[t]
    if model == "rata4":
        return y[t - 3:t + 1].mean()
    if model == "drift12":
        return y[t] + h * (y[t] - y[t - 12]) / 12
    if model == "musiman52":
        # pola tahun lalu, disesuaikan dengan level sekarang
        return y[t + h - 52] * (y[t] / y[t - 52])
    raise ValueError(model)


MODEL = ["naif", "rata4", "drift12", "musiman52"]


def prediktif(w: pd.DataFrame, uji=26, H=4):
    akurasi, prediksi = [], []
    for kom in w.columns:
        y_asli = w[kom]
        y = y_asli.ffill().to_numpy()   # minggu kosong diisi nilai minggu sebelumnya HANYA untuk masukan model
        n = len(y)
        err = {m: {h: [] for h in range(1, H + 1)} for m in MODEL}
        for asal in range(n - uji - H, n - H):
            hist = y[:asal + 1]
            for m in MODEL:
                for h in range(1, H + 1):
                    aktual = y_asli.iloc[asal + h]
                    if pd.isna(aktual):
                        continue
                    f = ramal(hist, h, m)
                    err[m][h].append(aktual / f)       # rasio aktual/ramalan
        mape = {m: np.mean([abs(r - 1) for h in err[m] for r in err[m][h]]) * 100 for m in MODEL}
        # Model naif = dasar. Model lain dipakai hanya bila galatnya >= 10% lebih kecil (hindari memilih karena kebetulan).
        terbaik = "naif"
        lain = min((m for m in MODEL if m != "naif"), key=mape.get)
        if mape[lain] <= 0.9 * mape["naif"]:
            terbaik = lain
        for m in MODEL:
            akurasi.append({"komoditas": kom, "model": m, "mape_persen": round(mape[m], 2),
                            "dipakai": m == terbaik})
        terakhir = y_asli.dropna().index[-1]
        for h in range(1, H + 1):
            f = ramal(y, h, terbaik)
            r = np.array(err[terbaik][h])
            lo, hi = np.quantile(r, [0.1, 0.9])
            prediksi.append({"komoditas": kom, "minggu_ke": h,
                             "akhir_minggu": (terakhir + pd.Timedelta(weeks=h)).date(),
                             "perkiraan": round(f), "batas_bawah_80": round(f * lo), "batas_atas_80": round(f * hi),
                             "model": terbaik, "mape_uji_persen": round(mape[terbaik], 2),
                             "harga_minggu_terakhir": round(y_asli.dropna().iloc[-1])})
    return pd.DataFrame(akurasi), pd.DataFrame(prediksi)


# ---------------------------------------------------------------- 4. preskriptif
def preskriptif(idx_bulan, hari, pred, bulanan, w):
    rek = []
    for kom in pred.komoditas.unique():
        ib = idx_bulan[idx_bulan.komoditas == kom]
        hb = hari[hari.komoditas == kom]
        p = pred[(pred.komoditas == kom)]
        akhir = p.iloc[-1]
        naik = (akhir.perkiraan / akhir.harga_minggu_terakhir - 1) * 100
        if akhir.batas_bawah_80 > akhir.harga_minggu_terakhir * 1.02:
            sinyal = "Beli/stok sekarang (diperkirakan naik)"
        elif akhir.batas_atas_80 < akhir.harga_minggu_terakhir * 0.98:
            sinyal = "Tunda bila bisa (diperkirakan turun)"
        else:
            sinyal = "Beli seperti biasa (perkiraan stabil)"
        bln_akhir = pd.Timestamp(akhir.akhir_minggu).month
        bln_kini = pd.Timestamp(p.iloc[0].akhir_minggu - pd.Timedelta(weeks=1)).month
        i_kini = ib.set_index("bulan").indeks.get(bln_kini)
        i_depan = ib.set_index("bulan").indeks.get(bln_akhir if bln_akhir != bln_kini else bln_kini % 12 + 1)
        pola = round((i_depan / i_kini - 1) * 100, 1)
        rek.append({"komoditas": kom,
                    "bulan_termurah": ib.loc[ib.indeks.idxmin(), "nama_bulan"],
                    "indeks_bulan_termurah": ib.indeks.min(),
                    "bulan_termahal": ib.loc[ib.indeks.idxmax(), "nama_bulan"],
                    "indeks_bulan_termahal": ib.indeks.max(),
                    "hari_kerja_termurah": hb.loc[hb.selisih_persen.idxmin(), "nama_hari"],
                    "selisih_hari_termurah_persen": hb.selisih_persen.min(),
                    "perkiraan_4_minggu_persen": round(naik, 1),
                    "pola_historis_bulan_depan_persen": pola,
                    "sinyal": sinyal if sinyal != "Beli seperti biasa (perkiraan stabil)" or abs(pola) < 3
                              else ("Pertimbangkan stok (pola historis: bulan depan cenderung naik)" if pola >= 3
                                    else "Pertimbangkan menunda (pola historis: bulan depan cenderung turun)")})
    rek = pd.DataFrame(rek)

    paket = []
    for bulan, g in bulanan.groupby("bulan"):
        harga = dict(zip(g.komoditas, g.harga))
        if all(k in harga for k in PAKET):
            paket.append({"bulan": bulan, "jenis": "aktual",
                          "biaya_paket": round(sum(harga[k] * q for k, q in PAKET.items()))})
    for h in sorted(pred.minggu_ke.unique()):
        p = pred[pred.minggu_ke == h].set_index("komoditas")
        paket.append({"bulan": str(p.akhir_minggu.iloc[0]), "jenis": f"perkiraan_minggu_{h}",
                      "biaya_paket": round(sum(p.loc[k, "perkiraan"] * q for k, q in PAKET.items())),
                      "batas_bawah_80": round(sum(p.loc[k, "batas_bawah_80"] * q for k, q in PAKET.items())),
                      "batas_atas_80": round(sum(p.loc[k, "batas_atas_80"] * q for k, q in PAKET.items()))})
    return rek, pd.DataFrame(paket)


# ---------------------------------------------------------------- laporan
def rp(x):
    return "Rp" + f"{int(round(x)):,}".replace(",", ".")


def laporan(df, ring, idx_bulan, leb, hari, akur, pred, rek, paket):
    L = ["# Laporan Analisis Harga Pangan Kota Semarang", "",
         f"Data: PIHPS Nasional, pasar tradisional Kota Semarang, {df.tanggal.min().date()} – {df.tanggal.max().date()}, "
         f"{df.komoditas.nunique()} komoditas, {len(df):,} baris ({df.harga.isna().sum():,} kosong).", "",
         "## 1. Deskriptif", "", "Paling naik-turun dalam setahun (rata-rata koefisien variasi per tahun):", ""]
    for _, r in ring.head(5).iterrows():
        L.append(f"- **{r.komoditas}**: CV {r.cv_dalam_tahun_persen}%; rata-rata 2018 {rp(r.rata_2018)} → 2026 {rp(r.rata_2026)} ({r.perubahan_persen:+}%)")
    L += ["", "Paling stabil:", ""]
    for _, r in ring.tail(3).iterrows():
        L.append(f"- **{r.komoditas}**: CV {r.cv_dalam_tahun_persen}%")
    L += ["", "## 2. Diagnostik", "", "Rata-rata perubahan harga 14 hari menjelang Idul Fitri (dibanding 45–31 hari sebelumnya), 2018–2025:", ""]
    lm = leb.groupby("komoditas").perubahan_persen.agg(["mean", lambda s: (s > 0).sum(), "count"]).sort_values("mean", ascending=False)
    for kom, r in lm.head(6).iterrows():
        L.append(f"- **{kom}**: {r['mean']:+.1f}% (naik pada {int(r.iloc[1])} dari {int(r['count'])} tahun)")
    L += ["", "Perbedaan antar hari kerja sangat kecil (rata-rata selisih terbesar per komoditas):", ""]
    hb = hari.groupby("komoditas").selisih_persen.agg(lambda s: s.max() - s.min()).sort_values(ascending=False)
    L.append(f"- terbesar {hb.index[0]}: {hb.iloc[0]:.2f} poin persen; median semua komoditas {hb.median():.2f} poin persen")
    L += ["", "## 3. Prediktif", "", "Uji mundur 26 minggu terakhir (MAPE rata-rata horizon 1–4 minggu). Model naif dipakai kecuali model lain >= 10% lebih akurat:", ""]
    dp = akur[akur.dipakai].sort_values("mape_persen")
    for _, r in dp.iterrows():
        L.append(f"- {r.komoditas}: {r.model} (MAPE {r.mape_persen}%)")
    L += ["", "## 4. Preskriptif", ""]
    for _, r in rek.iterrows():
        L.append(f"- **{r.komoditas}**: bulan termurah {r.bulan_termurah}, termahal {r.bulan_termahal}; "
                 f"perkiraan 4 minggu {r.perkiraan_4_minggu_persen:+}%, pola historis bulan depan {r.pola_historis_bulan_depan_persen:+}% → {r.sinyal}")
    akt = paket[paket.jenis == "aktual"]
    L += ["", f"Paket bahan pokok contoh (1 orang/minggu, asumsi): bulan terakhir {rp(akt.biaya_paket.iloc[-1])}; "
          f"termurah {rp(akt.biaya_paket.min())} ({akt.loc[akt.biaya_paket.idxmin(), 'bulan']}); "
          f"termahal {rp(akt.biaya_paket.max())} ({akt.loc[akt.biaya_paket.idxmax(), 'bulan']}).", "",
          "## Catatan", "- Tanggal Idul Fitri 2018–2025 sudah dicocokkan dengan penetapan sidang isbat pemerintah.",
          "- Minggu tanpa data diisi nilai minggu sebelumnya hanya sebagai masukan model; nilai aktual tidak diubah.",
          "- Paket bahan pokok adalah contoh dengan jumlah asumsi, bukan standar gizi.",
          "- Semua hasil bersifat deskriptif/asosiatif; tidak menyimpulkan sebab-akibat."]
    return "\n".join(L)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = muat_bersih()
    assert len(df) == 48825 and df.harga.isna().sum() == 2376, "Data tidak sama dengan hasil pembersihan Kaila"
    ring, bulanan = deskriptif(df)
    idx_bulan, leb, hari = diagnostik(df)
    w = mingguan(df)
    akur, pred = prediktif(w)
    rek, paket = preskriptif(idx_bulan, hari, pred, bulanan, w)
    for nama, t in [("deskriptif_ringkasan", ring), ("rata_bulanan", bulanan), ("diagnostik_bulan", idx_bulan),
                    ("diagnostik_lebaran", leb), ("diagnostik_hari", hari), ("prediksi_akurasi", akur),
                    ("prediksi_4minggu", pred), ("preskriptif_waktu_beli", rek), ("preskriptif_paket", paket)]:
        t.to_csv(OUT / f"{nama}.csv", index=False)
    (OUT / "laporan_analisis.md").write_text(laporan(df, ring, idx_bulan, leb, hari, akur, pred, rek, paket), encoding="utf-8")
    print((OUT / "laporan_analisis.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
