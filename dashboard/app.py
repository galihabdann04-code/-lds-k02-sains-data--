"""
Dashboard "Belanja Hemat Bergizi Semarang" — harga pangan harian Kota Semarang (PIHPS Bank Indonesia, 2018–2026).
Issue 7 (Shaula). Analisis (prediksi, pola, rekomendasi) dibaca dari hasil_analisis/ (Issue 6, Kaila).

Jalankan:  streamlit run dashboard/app.py
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DIR = Path(__file__).resolve().parent
DATA = DIR / "data"
HASIL = Path(os.environ.get("HASIL_ANALISIS", DIR.parent / "hasil_analisis"))
SUMBER_URL = "https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah"

# Palet kategorikal (3 slot pertama tervalidasi aman buta warna) + diverging biru–abu–merah
SERI = ["#2a78d6", "#eb6834", "#1baf7a"]
ABU, TEKS, TEKS2, GRID = "#8a8984", "#0b1f1c", "#52514e", "#e6ebe9"
DIVERGING = [[0, "#2a78d6"], [0.5, "#f0efec"], [1, "#e34948"]]
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
SATUAN = lambda k: "liter" if k.startswith("Minyak") else "kg"

st.set_page_config(page_title="Belanja Hemat Bergizi Semarang", page_icon="🛒", layout="wide")
st.markdown("""
<style>
  .block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1320px;}
  .hero {background: linear-gradient(120deg, #0f766e 0%, #14918a 55%, #2bb3a3 100%); color:#fff;
         border-radius:16px; padding:22px 28px; margin-bottom:18px;}
  .hero h1 {font-size:1.65rem; margin:0 0 4px 0; color:#fff; font-weight:700; padding:0;}
  .hero p {margin:0; opacity:.92; font-size:.95rem;}
  .chip {display:inline-block; background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.28);
         border-radius:999px; padding:2px 12px; font-size:.78rem; margin:10px 6px 0 0;}
  .kpi {background:#fff; border:1px solid #e3ebe8; border-radius:14px; padding:14px 16px 12px;
        border-top:4px solid var(--accent); height:100%;}
  .kpi .lbl {font-size:.78rem; color:#52514e; font-weight:600; text-transform:uppercase; letter-spacing:.02em;}
  .kpi .val {font-size:1.7rem; font-weight:700; color:#0b1f1c; line-height:1.2; margin-top:4px;}
  .kpi .sub {font-size:.83rem; color:#52514e; margin-top:4px;}
  .note {background:#eef7f5; border-left:4px solid #0f766e; border-radius:8px; padding:10px 14px;
         font-size:.9rem; margin:6px 0 14px;}
  .warn {background:#fff8ec; border-left:4px solid #e8a33d;}
  div[data-testid="stTabs"] button p {font-size:.95rem; font-weight:600;}
</style>""", unsafe_allow_html=True)


# ------------------------------------------------------------------ utilitas
def rp(x) -> str:
    return "—" if x is None or pd.isna(x) else "Rp" + f"{int(round(x)):,}".replace(",", ".")


def pct(x, d=1) -> str:
    return "—" if x is None or pd.isna(x) else f"{x:+.{d}f}%".replace(".", ",")


def kotak(teks, warn=False):
    st.markdown(f'<div class="note{" warn" if warn else ""}">{teks}</div>', unsafe_allow_html=True)


def kartu(label, nilai, sub, warna):
    return (f'<div class="kpi" style="--accent:{warna}"><div class="lbl">{label}</div>'
            f'<div class="val">{nilai}</div><div class="sub">{sub}</div></div>')


def gaya(fig, ytitle="", xtitle="", tinggi=380):
    fig.update_layout(height=tinggi, separators=",.", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=12, color=TEKS2), margin=dict(l=8, r=24, t=30, b=40), hovermode="x unified",
                      legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, title=dict(text="")),
                      title=dict(text=""))
    fig.update_xaxes(title=xtitle, showgrid=False, linecolor=GRID)
    fig.update_yaxes(title=ytitle, gridcolor=GRID, zeroline=False, tickformat=",.0f")
    return fig


CFG = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]}


# ------------------------------------------------------------------ data
@st.cache_data
def muat_ringkasan():
    b = pd.read_csv(DATA / "ringkasan_bulanan.csv", parse_dates=["bulan"])
    w = pd.read_csv(DATA / "ringkasan_mingguan.csv", parse_dates=["akhir_minggu"])
    t = pd.read_csv(DATA / "harga_terbaru.csv", parse_dates=["tanggal"])
    return b, w, t


@st.cache_data
def muat_hasil():
    nama = ["deskriptif_ringkasan", "diagnostik_bulan", "diagnostik_lebaran", "diagnostik_hari",
            "prediksi_akurasi", "prediksi_4minggu", "preskriptif_waktu_beli", "preskriptif_paket"]
    if not all((HASIL / f"{n}.csv").exists() for n in nama):
        return None
    return {n: pd.read_csv(HASIL / f"{n}.csv") for n in nama}


bulanan, mingguan, terbaru = muat_ringkasan()
hasil = muat_hasil()
KOMODITAS = sorted(bulanan.komoditas.unique())
KATEGORI = sorted(bulanan.kategori.unique())
TGL_AKHIR = terbaru.tanggal.max()

# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.markdown("### 🔎 Filter")
    kat = st.selectbox("Kategori", ["Semua kategori"] + KATEGORI, key="f_kat")
    pilihan = KOMODITAS if kat == "Semua kategori" else sorted(bulanan[bulanan.kategori == kat].komoditas.unique())
    bawaan = [k for k in ["Beras Kualitas Medium I", "Telur Ayam Ras Segar", "Daging Ayam Ras Segar"] if k in pilihan] or pilihan[:3]
    kom = st.multiselect("Komoditas (maks. 3 untuk dibandingkan)", pilihan, default=bawaan, max_selections=3, key="f_kom")
    if not kom:
        kom = pilihan[:1]
    th = st.slider("Rentang tahun (tren)", 2018, int(bulanan.bulan.dt.year.max()), (2018, int(bulanan.bulan.dt.year.max())), key="f_th")
    st.divider()
    st.markdown(f"**Sumber data:** [PIHPS Nasional — Bank Indonesia]({SUMBER_URL}), pasar tradisional Kota Semarang, "
                f"harga harian 1 Jan 2018 – {TGL_AKHIR:%d %b %Y}.")
    st.caption("Dashboard hanya memuat data ringkasan (bulanan, mingguan, 20 hari terakhir). Tidak ada data karangan.")

# ------------------------------------------------------------------ header & KPI
st.markdown(f"""<div class="hero"><h1>🛒 Belanja Hemat Bergizi Semarang</h1>
<p>Harga pangan pokok harian di pasar tradisional Kota Semarang — kapan sebaiknya membeli supaya hemat.</p>
<span class="chip">Data PIHPS 2018–{TGL_AKHIR:%Y}</span><span class="chip">21 komoditas pokok</span>
<span class="chip">Data terakhir {TGL_AKHIR:%d %b %Y}</span></div>""", unsafe_allow_html=True)


def ringkas_komoditas(k):
    t = terbaru[terbaru.komoditas == k].sort_values("tanggal")
    w = mingguan[mingguan.komoditas == k].sort_values("akhir_minggu")
    b = bulanan[bulanan.komoditas == k].set_index("bulan").harga
    akhir = t.iloc[-1]
    minggu_lalu = w.harga.iloc[-2] if len(w) > 1 else np.nan
    bln = akhir.tanggal.to_period("M").to_timestamp()
    tahun_lalu = b.get(bln - pd.DateOffset(years=1))
    return {"harga": akhir.harga, "tanggal": akhir.tanggal, "kategori": akhir.kategori,
            "vs_minggu": (w.harga.iloc[-1] / minggu_lalu - 1) * 100 if pd.notna(minggu_lalu) else np.nan,
            "vs_tahun": (b.get(bln) / tahun_lalu - 1) * 100 if tahun_lalu else np.nan}


cards = []
for i, k in enumerate(kom):
    r = ringkas_komoditas(k)
    cards.append(kartu(k, rp(r["harga"]) + f"<span style='font-size:.9rem;color:{TEKS2}'>/{SATUAN(k)}</span>",
                       f"{pct(r['vs_minggu'])} vs minggu lalu · {pct(r['vs_tahun'])} vs bulan sama tahun lalu",
                       SERI[i]))
if hasil:
    pk = hasil["preskriptif_paket"]
    akt = pk[pk.jenis == "aktual"].iloc[-1]
    cards.append(kartu("Paket bahan pokok / minggu", rp(akt.biaya_paket),
                       f"contoh 1 orang · bulan {akt.bulan}", "#6250d6"))
cols = st.columns(len(cards))
for c, h in zip(cols, cards):
    c.markdown(h, unsafe_allow_html=True)
st.write("")

if hasil is None:
    kotak("⏳ <b>Hasil analisis belum tersedia.</b> Tab Pola, Prediksi, dan Rekomendasi akan terisi setelah hasil "
          "analisis (Issue 6) disimpan di folder <code>hasil_analisis/</code>.", warn=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🛒 Harga Terbaru", "📈 Tren & Pola", "🔮 Prediksi",
                                        "💡 Rekomendasi Belanja", "📄 Data & Metodologi"])

# ------------------------------------------------------------------ 1. harga terbaru
with tab1:
    st.subheader(f"Harga 20 hari kerja terakhir (s.d. {TGL_AKHIR:%d %b %Y})")
    fig = go.Figure()
    for i, k in enumerate(kom):
        t = terbaru[terbaru.komoditas == k]
        fig.add_trace(go.Scatter(x=t.tanggal, y=t.harga, name=k, mode="lines+markers",
                                 line=dict(color=SERI[i], width=2.5), marker=dict(size=7),
                                 hovertemplate="%{y:,.0f}<extra>" + k + "</extra>"))
    st.plotly_chart(gaya(fig, ytitle=f"Rp per kg/liter"), config=CFG)
    st.caption("Hanya hari kerja (Senin–Jumat). Hari tanpa data tidak ditampilkan.")

    rows = []
    for k in pilihan:
        r = ringkas_komoditas(k)
        row = {"Komoditas": k, "Kategori": r["kategori"], "Harga terbaru": rp(r["harga"]) + "/" + SATUAN(k), "vs minggu lalu (%)": round(r["vs_minggu"], 1),
               "vs tahun lalu (%)": round(r["vs_tahun"], 1) if pd.notna(r["vs_tahun"]) else None}
        if hasil:
            s = hasil["preskriptif_waktu_beli"].set_index("komoditas")
            row["Saran"] = s.loc[k, "sinyal"] if k in s.index else "—"
        rows.append(row)
    st.markdown("##### Semua komoditas" + ("" if kat == "Semua kategori" else f" — {kat}"))
    st.dataframe(pd.DataFrame(rows), hide_index=True, column_config={
        "vs minggu lalu (%)": st.column_config.NumberColumn(format="%+.1f"),
        "vs tahun lalu (%)": st.column_config.NumberColumn(format="%+.1f")})

# ------------------------------------------------------------------ 2. tren & pola
with tab2:
    st.subheader("Tren harga bulanan")
    b = bulanan[(bulanan.bulan.dt.year >= th[0]) & (bulanan.bulan.dt.year <= th[1])]
    fig = go.Figure()
    for i, k in enumerate(kom):
        s = b[b.komoditas == k]
        fig.add_trace(go.Scatter(x=s.bulan, y=s.harga, name=k, mode="lines", line=dict(color=SERI[i], width=2.5),
                                 hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra>" + k + "</extra>"))
    st.plotly_chart(gaya(fig, ytitle="Rp per kg/liter (rata-rata bulanan)"), config=CFG)

    if hasil:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Paling naik-turun dalam setahun (deskriptif)")
            d = hasil["deskriptif_ringkasan"].sort_values("cv_dalam_tahun_persen")
            fig = go.Figure(go.Bar(x=d.cv_dalam_tahun_persen, y=d.komoditas, orientation="h",
                                   marker=dict(color=[SERI[1] if v >= 10 else ABU for v in d.cv_dalam_tahun_persen], cornerradius=4),
                                   customdata=np.c_[d.rata_2018, d.rata_2026, d.perubahan_persen],
                                   hovertemplate="<b>%{y}</b><br>Koefisien variasi %{x:.1f}%<br>Rata-rata 2018 Rp%{customdata[0]:,.0f} → "
                                                 "2026 Rp%{customdata[1]:,.0f} (%{customdata[2]:+.1f}%)<extra></extra>"))
            gaya(fig, xtitle="Koefisien variasi rata-rata per tahun (%)", tinggi=560)
            fig.update_yaxes(tickformat=None, showgrid=False)
            fig.update_layout(hovermode="closest")
            st.plotly_chart(fig, config=CFG)
            st.caption("Oranye = berfluktuasi tinggi (≥10%). Semakin panjang batang, semakin tidak stabil harganya dalam setahun.")
        with c2:
            st.markdown("##### Pola musiman per bulan (diagnostik)")
            ib = hasil["diagnostik_bulan"].pivot(index="komoditas", columns="bulan", values="indeks")
            ib.columns = [BULAN[c - 1] for c in ib.columns]
            z = (ib - 1) * 100
            lim = float(np.nanmax(np.abs(z.values)))
            fig = go.Figure(go.Heatmap(z=z.values, x=list(z.columns), y=list(z.index), colorscale=DIVERGING,
                                       zmin=-lim, zmax=lim, xgap=2, ygap=2,
                                       colorbar=dict(title=dict(text="% vs rata-rata tahun", side="right"), thickness=12),
                                       hovertemplate="<b>%{y}</b> · %{x}: %{z:+.1f}% dari rata-rata tahunannya<extra></extra>"))
            gaya(fig, tinggi=560)
            fig.update_yaxes(tickformat=None, showgrid=False, autorange="reversed")
            fig.update_layout(hovermode="closest")
            st.plotly_chart(fig, config=CFG)
            st.caption("Merah = bulan yang biasanya lebih mahal, biru = lebih murah (rata-rata 2018–2025).")

        st.markdown("##### Menjelang Idul Fitri (diagnostik)")
        lb = hasil["diagnostik_lebaran"]
        g = (lb.groupby("komoditas").agg(rata=("perubahan_persen", "mean"),
                                         naik=("perubahan_persen", lambda s: int((s > 0).sum())),
                                         n=("perubahan_persen", "count")).reset_index().sort_values("rata"))
        fig = go.Figure(go.Bar(x=g.rata, y=g.komoditas, orientation="h",
                               marker=dict(color=[SERI[1] if v > 0 else SERI[0] for v in g.rata], cornerradius=4),
                               customdata=np.c_[g.naik, g.n],
                               hovertemplate="<b>%{y}</b><br>Rata-rata %{x:+.1f}%<br>Naik di %{customdata[0]} dari %{customdata[1]} tahun<extra></extra>"))
        gaya(fig, xtitle="Perubahan harga 14 hari sebelum Idul Fitri vs 45–31 hari sebelumnya (%)", tinggi=520)
        fig.update_yaxes(tickformat=None, showgrid=False)
        fig.update_layout(hovermode="closest")
        st.plotly_chart(fig, config=CFG)
        top = g.sort_values("rata", ascending=False).iloc[0]
        kons = g[g.rata > 0].assign(r=lambda x: x.naik / x.n).sort_values(["r", "rata"], ascending=False).iloc[0]
        kotak(f"Kenaikan rata-rata terbesar menjelang Idul Fitri: <b>{top.komoditas}</b> {pct(top.rata)} "
              f"(naik di {int(top.naik)} dari {int(top.n)} tahun). Paling konsisten: <b>{kons.komoditas}</b> "
              f"{pct(kons.rata)}, naik di {int(kons.naik)} dari {int(kons.n)} tahun. "
              "Pola ini berulang, tetapi bukan bukti sebab-akibat.")
        hr = hasil["diagnostik_hari"].groupby("komoditas").selisih_persen.agg(lambda s: s.max() - s.min())
        st.caption(f"Perbedaan harga antar hari kerja sangat kecil: median {hr.median():.2f} poin persen "
                   f"(terbesar {hr.idxmax()}, {hr.max():.2f} poin persen). Data akhir pekan tidak tersedia.")

# ------------------------------------------------------------------ 3. prediksi
with tab3:
    if not hasil:
        kotak("Prediksi akan tampil setelah hasil analisis Issue 6 tersedia.", warn=True)
    else:
        k = st.selectbox("Komoditas", kom + [x for x in pilihan if x not in kom], key="f_pred")
        p = hasil["prediksi_4minggu"][hasil["prediksi_4minggu"].komoditas == k]
        p = p.assign(akhir_minggu=pd.to_datetime(p.akhir_minggu))
        w = mingguan[mingguan.komoditas == k]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=w.akhir_minggu, y=w.harga, name="Harga aktual (rata-rata mingguan)",
                                 mode="lines+markers", line=dict(color=SERI[0], width=2.5), marker=dict(size=6),
                                 hovertemplate="%{x|%d %b %Y}: %{y:,.0f}<extra>aktual</extra>"))
        x_band = list(p.akhir_minggu) + list(p.akhir_minggu[::-1])
        y_band = list(p.batas_atas_80) + list(p.batas_bawah_80[::-1])
        fig.add_trace(go.Scatter(x=x_band, y=y_band, fill="toself", fillcolor="rgba(235,104,52,0.15)",
                                 line=dict(width=0), name="Rentang 80%", hoverinfo="skip"))
        sambung = pd.concat([w.tail(1).rename(columns={"harga": "perkiraan"})[["akhir_minggu", "perkiraan"]],
                             p[["akhir_minggu", "perkiraan"]]])
        fig.add_trace(go.Scatter(x=sambung.akhir_minggu, y=sambung.perkiraan, name="Perkiraan",
                                 mode="lines+markers", line=dict(color=SERI[1], width=2.5, dash="dash"), marker=dict(size=7),
                                 hovertemplate="%{x|%d %b %Y}: %{y:,.0f}<extra>perkiraan</extra>"))
        st.plotly_chart(gaya(fig, ytitle=f"Rp per {SATUAN(k)}", tinggi=420), config=CFG)
        r = p.iloc[-1]
        kotak(f"<b>{k}</b>: perkiraan 4 minggu ke depan {rp(r.perkiraan)} (rentang 80%: {rp(r.batas_bawah_80)}–"
              f"{rp(r.batas_atas_80)}). Model <b>{r.model}</b>, galat rata-rata saat diuji pada 26 minggu terakhir "
              f"<b>{str(r.mape_uji_persen).replace('.', ',')}%</b>. Perkiraan ditampilkan terpisah dari data asli.")
        st.markdown("##### Akurasi model per komoditas (uji 26 minggu terakhir)")
        ak = hasil["prediksi_akurasi"]
        tabel = ak[ak.dipakai].sort_values("mape_persen")[["komoditas", "model", "mape_persen"]]
        st.dataframe(tabel.rename(columns={"komoditas": "Komoditas", "model": "Model dipakai", "mape_persen": "Galat rata-rata (MAPE, %)"}),
                     hide_index=True)
        st.caption("Model naif = harga minggu depan sama dengan minggu ini; dipakai kecuali model lain ≥10% lebih akurat. "
                   "Galat besar pada cabai menunjukkan harganya sulit diprediksi.")

# ------------------------------------------------------------------ 4. rekomendasi
with tab4:
    if not hasil:
        kotak("Rekomendasi akan tampil setelah hasil analisis Issue 6 tersedia.", warn=True)
    else:
        st.subheader("Kapan sebaiknya membeli?")
        rk = hasil["preskriptif_waktu_beli"]
        rk = rk[rk.komoditas.isin(pilihan)]
        st.dataframe(rk[["komoditas", "sinyal", "pola_historis_bulan_depan_persen", "perkiraan_4_minggu_persen",
                         "bulan_termurah", "bulan_termahal", "hari_kerja_termurah"]].rename(columns={
            "komoditas": "Komoditas", "sinyal": "Saran", "pola_historis_bulan_depan_persen": "Pola bulan depan (%)",
            "perkiraan_4_minggu_persen": "Perkiraan 4 minggu (%)", "bulan_termurah": "Bulan termurah",
            "bulan_termahal": "Bulan termahal", "hari_kerja_termurah": "Hari kerja termurah"}),
            hide_index=True, column_config={"Pola bulan depan (%)": st.column_config.NumberColumn(format="%+.1f"),
                                            "Perkiraan 4 minggu (%)": st.column_config.NumberColumn(format="%+.1f")})
        st.caption("Saran memakai perkiraan 4 minggu dan pola rata-rata 2018–2025. Selisih antar hari kerja sangat kecil, "
                   "jadi hari belanja tidak terlalu berpengaruh.")

        st.subheader("Paket bahan pokok mingguan")
        c1, c2 = st.columns([1.6, 1])
        pk = hasil["preskriptif_paket"]
        a = pk[pk.jenis == "aktual"].assign(t=lambda x: pd.to_datetime(x.bulan))
        a = a[(a.t.dt.year >= th[0]) & (a.t.dt.year <= th[1])]
        f = pk[pk.jenis != "aktual"].assign(t=lambda x: pd.to_datetime(x.bulan))
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=a.t, y=a.biaya_paket, name="Biaya aktual (rata-rata bulanan)", mode="lines",
                                     line=dict(color=SERI[0], width=2.5), hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra></extra>"))
            fig.add_trace(go.Scatter(x=f.t, y=f.biaya_paket, name="Perkiraan 4 minggu", mode="markers+lines",
                                     line=dict(color=SERI[1], dash="dash"), error_y=dict(type="data", symmetric=False,
                                     array=f.batas_atas_80 - f.biaya_paket, arrayminus=f.biaya_paket - f.batas_bawah_80,
                                     color=SERI[1]), hovertemplate="%{x|%d %b %Y}: %{y:,.0f}<extra>perkiraan</extra>"))
            st.plotly_chart(gaya(fig, ytitle="Rp per orang per minggu"), config=CFG)
            st.caption("Paket contoh 1 orang/minggu (asumsi, bukan standar gizi): beras medium 2 kg, telur 0,5 kg, "
                       "daging ayam 0,5 kg, minyak goreng curah 0,25 L, gula 0,25 kg, bawang merah 0,1 kg, "
                       "bawang putih 0,05 kg, cabai rawit merah 0,05 kg.")
        with c2:
            anggaran = st.slider("Anggaran belanja per minggu (Rp)", 50_000, 300_000, 150_000, 10_000, key="f_ang")
            orang = st.number_input("Jumlah orang", 1, 8, 1, key="f_org")
            biaya = f.biaya_paket.iloc[-1] * orang
            sisa = anggaran - biaya
            st.markdown(kartu("Perkiraan biaya paket", rp(biaya), f"{orang} orang · minggu ke-4 perkiraan", "#6250d6"),
                        unsafe_allow_html=True)
            st.write("")
            if sisa >= 0:
                kotak(f"✅ Anggaran {rp(anggaran)} <b>cukup</b>, sisa sekitar {rp(sisa)} untuk sayur, buah, atau lauk lain.")
            else:
                kotak(f"⚠️ Anggaran {rp(anggaran)} <b>kurang</b> sekitar {rp(-sisa)} untuk paket ini.", warn=True)

# ------------------------------------------------------------------ 5. data & metodologi
with tab5:
    st.subheader("Data & metodologi")
    st.markdown(f"""
- **Sumber:** [PIHPS Nasional — Bank Indonesia]({SUMBER_URL}), pasar tradisional Kota Semarang, laporan harian,
  1 Januari 2018 – {TGL_AKHIR:%d %B %Y}. Hak cipta PIHPS Nasional; dipakai untuk keperluan akademik dengan menyebut sumber.
- **Isi dashboard:** hanya data **ringkasan** — rata-rata bulanan, rata-rata mingguan 26 minggu terakhir, dan harga
  harian 20 hari kerja terakhir. Data lengkap tidak disebarluaskan.
- **Batas data:** satu harga rata-rata untuk Kota Semarang (bukan per pasar), 21 komoditas pokok (tanpa sayuran),
  hanya hari kerja, tanpa data gizi. Tanda "-" di sumber dibiarkan kosong, tidak diisi tebakan.
- **Analisis:** deskriptif (koefisien variasi), diagnostik (pola bulan, menjelang Idul Fitri, hari kerja), prediktif
  (model naif/rata-rata/drift/musiman, uji mundur 26 minggu), preskriptif (saran waktu beli & paket bahan pokok).
  Semua hasil bersifat deskriptif/asosiatif, bukan sebab-akibat.
- **Kelompok 2 — Lab Sains Data, Bisnis Digital FEB UNDIP:** Galih (riset & pertanyaan), Kaila (pembersihan data &
  analisis), Shaula (pengambilan data & dashboard).
""")
    c1, c2 = st.columns(2)
    c1.download_button("⬇ Unduh ringkasan bulanan (CSV)", bulanan.to_csv(index=False).encode("utf-8"),
                       "ringkasan_bulanan.csv", "text/csv")
    if hasil:
        c2.download_button("⬇ Unduh prediksi 4 minggu (CSV)", hasil["prediksi_4minggu"].to_csv(index=False).encode("utf-8"),
                           "prediksi_4minggu.csv", "text/csv")
