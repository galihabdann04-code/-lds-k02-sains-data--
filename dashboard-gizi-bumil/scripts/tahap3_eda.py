"""
Tahap 3 — Analisis Data Eksploratif (deskriptif, tanpa klaim kausal).

Input : data/processed/kota_tahunan.csv, data/processed/puskesmas_2022.csv,
        data/processed/kecamatan_2022.csv  (hasil Tahap 2)
Output: data/processed/eda_puskesmas_2022.csv  (+ selang kepercayaan Wilson 95%, kategori)
        data/processed/eda_ringkasan.json      (angka kunci untuk panel insight dashboard)
        reports/tahap3_eda.html                (grafik interaktif Plotly)

Jalankan: pip install pandas plotly  lalu  python scripts/tahap3_eda.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

# Palet (slot kategorikal 1–2 tervalidasi CVD; abu-abu untuk referensi/non-sorotan)
C = {"kek": "#2a78d6", "anemia": "#eb6834", "ref": "#8a8984", "muted": "#c9c8c2",
     "text": "#0b0b0b", "text2": "#52514e", "grid": "#e8e7e3", "surface": "#fcfcfb"}
NAMA = {"kek": "KEK", "anemia": "Anemia"}


def wilson(x, n, z=1.96):
    """Selang kepercayaan Wilson 95% untuk proporsi (dalam %)."""
    x, n = np.asarray(x, float), np.asarray(n, float)
    p = x / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return (c - h) * 100, (c + h) * 100


def spearman(a: pd.Series, b: pd.Series) -> float:
    return round(float(a.rank().corr(b.rank())), 2)


def gaya(fig: go.Figure, judul: str, ytitle: str = "", xtitle: str = "", tinggi: int = 420) -> go.Figure:
    fig.update_layout(
        title=dict(text=judul, x=0, xanchor="left", font=dict(size=16, color=C["text"])),
        height=tinggi, paper_bgcolor=C["surface"], plot_bgcolor=C["surface"],
        font=dict(family="Inter, system-ui, sans-serif", size=12, color=C["text2"]),
        margin=dict(l=10, r=30, t=70, b=40), hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    fig.update_xaxes(title=xtitle, showgrid=False, linecolor=C["grid"], ticks="outside", tickcolor=C["grid"])
    fig.update_yaxes(title=ytitle, gridcolor=C["grid"], zeroline=False, linecolor=C["grid"])
    return fig


# ------------------------------------------------------------------ data
def muat():
    kota = pd.read_csv(PROC / "kota_tahunan.csv")
    pkm = pd.read_csv(PROC / "puskesmas_2022.csv")
    kec = pd.read_csv(PROC / "kecamatan_2022.csv")
    return kota, pkm, kec


def analisis_puskesmas(pkm: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    pkm = pkm.copy()
    kota_pct = {}
    for ind in ("kek", "anemia"):
        rate = pkm[f"{ind}_jumlah"].sum() / pkm["jumlah_bumil"].sum() * 100
        kota_pct[ind] = round(rate, 2)
        lo, hi = wilson(pkm[f"{ind}_jumlah"], pkm["jumlah_bumil"])
        pkm[f"{ind}_ci_bawah"], pkm[f"{ind}_ci_atas"] = lo.round(2), hi.round(2)
        pkm[f"{ind}_vs_kota"] = np.select([lo > rate, hi < rate],
                                          ["di atas kota", "di bawah kota"], "tidak berbeda bermakna")
        pkm[f"{ind}_rank_jumlah"] = pkm[f"{ind}_jumlah"].rank(ascending=False, method="min").astype(int)
        pkm[f"{ind}_rank_persen"] = pkm[f"{ind}_persen"].rank(ascending=False, method="min").astype(int)
    a, b = pkm["kek_vs_kota"] == "di atas kota", pkm["anemia_vs_kota"] == "di atas kota"
    pkm["kategori_beban"] = np.select([a & b, a, b],
                                      ["KEK & Anemia di atas kota", "KEK di atas kota", "Anemia di atas kota"],
                                      "Tidak di atas kota")
    return pkm, kota_pct


def ringkasan(kota: pd.DataFrame, pkm: pd.DataFrame, kota_pct: dict) -> dict:
    p = kota.pivot_table(index="tahun", columns="indikator", values="nilai")
    out = {"kota_2022_tabel32_persen": kota_pct, "tren": {}, "puskesmas_2022": {}}
    for nama, kol in [("K1", "BUMIL_K1"), ("KEK_jumlah", "KEK_JUMLAH"), ("Anemia_jumlah", "ANEMIA_JUMLAH")]:
        s = p[kol].dropna()
        out["tren"][f"{nama}_indeks_2024_vs_2017"] = round(s.loc[2024] / s.loc[2017] * 100, 1)
    out["tren"]["KEK_persen_turunan"] = p["KEK_PERSEN_TURUNAN"].dropna().round(2).to_dict()
    out["tren"]["Anemia_prevalensi"] = p["ANEMIA_PREVALENSI"].dropna().round(2).to_dict()
    for ind in ("kek", "anemia"):
        s = pkm.sort_values(f"{ind}_jumlah", ascending=False)
        top5 = s.head(5)
        out["puskesmas_2022"][ind] = {
            "top5_jumlah": top5["puskesmas"].tolist(),
            "top5_porsi_kasus_persen": round(top5[f"{ind}_jumlah"].sum() / s[f"{ind}_jumlah"].sum() * 100, 1),
            "top5_porsi_bumil_persen": round(top5["jumlah_bumil"].sum() / s["jumlah_bumil"].sum() * 100, 1),
            "top5_persen": pkm.nlargest(5, f"{ind}_persen")["puskesmas"].tolist(),
            "di_atas_kota": pkm.loc[pkm[f"{ind}_vs_kota"] == "di atas kota", "puskesmas"].tolist(),
            "rentang_persen": [float(pkm[f"{ind}_persen"].min()), float(pkm[f"{ind}_persen"].max())],
            "spearman_jumlah_vs_persen": spearman(pkm[f"{ind}_jumlah"], pkm[f"{ind}_persen"]),
        }
    out["puskesmas_2022"]["spearman_kek_vs_anemia_persen"] = spearman(pkm["kek_persen"], pkm["anemia_persen"])
    out["puskesmas_2022"]["beban_ganda"] = pkm.loc[
        pkm["kategori_beban"] == "KEK & Anemia di atas kota", "puskesmas"].tolist()
    return out


# ---------------------------------------------------------------- grafik
def fig_tren_persen(kota: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for ind, kode, label in [("kek", "KEK_PERSEN_TURUNAN", "KEK (% turunan, LiLA<23,5 ÷ K1)"),
                             ("anemia", "ANEMIA_PREVALENSI", "Anemia (prevalensi resmi)")]:
        d = kota[(kota.indikator == kode) & kota.nilai.notna()].sort_values("tahun")
        flag = d.status != "valid"
        fig.add_trace(go.Scatter(
            x=d.tahun, y=d.nilai, mode="lines+markers", name=label,
            line=dict(color=C[ind], width=2), marker=dict(size=9, color=C[ind], line=dict(color=C["surface"], width=2)),
            customdata=np.c_[d.status, d.catatan.fillna("")],
            hovertemplate="<b>%{x}</b> · " + NAMA[ind] + ": %{y:.2f}%<br>Status: %{customdata[0]}<br>%{customdata[1]}<extra></extra>"))
        if flag.any():
            fig.add_trace(go.Scatter(
                x=d.tahun[flag], y=d.nilai[flag], mode="markers", showlegend=False, hoverinfo="skip",
                marker=dict(size=16, color="rgba(0,0,0,0)", line=dict(color=C["text2"], width=1.5))))
        last = d.iloc[-1]
        fig.add_annotation(x=last.tahun, y=last.nilai, text=f"<b>{NAMA[ind]}</b> {last.nilai:.2f}%",
                           showarrow=False, xanchor="left", xshift=10, font=dict(color=C["text"]))
    fig.add_annotation(x=0, y=-0.16, xref="paper", yref="paper", showarrow=False, xanchor="left",
                       text="Lingkaran abu-abu = titik bertanda 'perlu perhatian' di validasi Tahap 2. Sumber: Satu Data Kota Semarang.",
                       font=dict(size=11, color=C["text2"]))
    gaya(fig, "Tren persentase KEK dan Anemia ibu hamil, Kota Semarang 2017–2024", ytitle="% ibu hamil")
    fig.update_xaxes(dtick=1, range=[2016.6, 2025.2])
    fig.update_yaxes(rangemode="tozero")
    return fig


def fig_tren_indeks(kota: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for kode, label, warna, dash, geser in [("BUMIL_K1", "Ibu hamil (K1)", C["ref"], "dot", 9),
                                            ("KEK_JUMLAH", "Kasus KEK", C["kek"], "solid", -9),
                                            ("ANEMIA_JUMLAH", "Kasus Anemia", C["anemia"], "solid", 0)]:
        d = kota[kota.indikator == kode].set_index("tahun")["nilai"].sort_index()
        d = d.loc[2017:2024]
        idx = d / d.loc[2017] * 100
        fig.add_trace(go.Scatter(
            x=idx.index, y=idx.values, name=label, mode="lines+markers", connectgaps=False,
            line=dict(color=warna, width=2, dash=dash), marker=dict(size=8, color=warna),
            customdata=d.values,
            hovertemplate="<b>%{x}</b> · " + label + "<br>Indeks %{y:.1f} (jumlah %{customdata:,.0f})<extra></extra>"))
        last = idx.dropna().iloc[-1]
        fig.add_annotation(x=2024, y=last, text=f"<b>{label}</b> {last:.0f}", showarrow=False,
                           xanchor="left", xshift=10, yshift=geser, font=dict(color=C["text"]))
    fig.add_hline(y=100, line=dict(color=C["grid"], width=1))
    fig.add_annotation(x=0, y=-0.16, xref="paper", yref="paper", showarrow=False, xanchor="left",
                       text="Indeks 2017 = 100. Celah 2023 pada Anemia = data tidak valid (dikosongkan di Tahap 2).",
                       font=dict(size=11, color=C["text2"]))
    gaya(fig, "Jumlah kasus vs jumlah ibu hamil: berapa penurunan yang ikut turunnya sasaran?", ytitle="Indeks (2017 = 100)")
    fig.update_xaxes(dtick=1, range=[2016.6, 2025.4])
    return fig


def fig_dot_ci(pkm: pd.DataFrame, ind: str, kota_rate: float) -> go.Figure:
    d = pkm.sort_values(f"{ind}_persen")
    fig = go.Figure()
    for kat, warna, simbol in [("di atas kota", C[ind], "circle"),
                               ("tidak berbeda bermakna", C["ref"], "circle-open"),
                               ("di bawah kota", C["muted"], "circle")]:
        s = d[d[f"{ind}_vs_kota"] == kat]
        if s.empty:
            continue
        fig.add_trace(go.Scatter(
            x=s[f"{ind}_persen"], y=s.puskesmas, mode="markers", name=kat.capitalize(),
            marker=dict(size=10, color=warna, symbol=simbol, line=dict(width=2, color=warna)),
            error_x=dict(type="data", symmetric=False, color=warna, thickness=1.5, width=0,
                         array=s[f"{ind}_ci_atas"] - s[f"{ind}_persen"],
                         arrayminus=s[f"{ind}_persen"] - s[f"{ind}_ci_bawah"]),
            customdata=np.c_[s.kecamatan, s[f"{ind}_jumlah"], s.jumlah_bumil, s[f"{ind}_ci_bawah"], s[f"{ind}_ci_atas"]],
            hovertemplate="<b>%{y}</b> (Kec. %{customdata[0]})<br>" + NAMA[ind] +
                          ": %{x:.2f}% (%{customdata[1]} dari %{customdata[2]} bumil)"
                          "<br>CI 95%: %{customdata[3]:.1f}–%{customdata[4]:.1f}%<extra></extra>"))
    fig.add_vline(x=kota_rate, line=dict(color=C["text2"], width=1, dash="dash"))
    fig.add_annotation(x=kota_rate, y=1.0, yref="paper", text=f"Kota {kota_rate:.2f}%", showarrow=False,
                       yanchor="bottom", font=dict(color=C["text"], size=11))
    gaya(fig, f"{NAMA[ind]} per Puskesmas 2022 — persentase dengan selang kepercayaan 95%",
         xtitle=f"% ibu hamil dengan {NAMA[ind]}", tinggi=900)
    fig.update_yaxes(categoryorder="array", categoryarray=d.puskesmas.tolist(), showgrid=False, title="")
    fig.update_xaxes(showgrid=True, gridcolor=C["grid"], rangemode="tozero")
    fig.update_layout(margin=dict(t=120), legend=dict(y=1.045))
    return fig


def fig_scatter(pkm: pd.DataFrame, kota_pct: dict) -> go.Figure:
    fig = go.Figure()
    ganda = pkm.kategori_beban == "KEK & Anemia di atas kota"
    for mask, nama, warna in [(~ganda, "Puskesmas lain", C["ref"]),
                              (ganda, "KEK & Anemia sama-sama di atas kota (bermakna)", C["kek"])]:
        s = pkm[mask]
        fig.add_trace(go.Scatter(
            x=s.kek_persen, y=s.anemia_persen, mode="markers", name=nama,
            marker=dict(size=np.sqrt(s.jumlah_bumil) / 1.6 + 4, color=warna, opacity=0.85,
                        line=dict(color=C["surface"], width=2)),
            customdata=np.c_[s.puskesmas, s.kecamatan, s.jumlah_bumil],
            hovertemplate="<b>%{customdata[0]}</b> (Kec. %{customdata[1]})<br>KEK %{x:.2f}% · Anemia %{y:.2f}%"
                          "<br>%{customdata[2]:,} ibu hamil<extra></extra>"))
    for _, r in pkm[ganda | (pkm.puskesmas == "Karangdoro")].iterrows():
        fig.add_annotation(x=r.kek_persen, y=r.anemia_persen, text=r.puskesmas, showarrow=False,
                           yshift=14, font=dict(size=11, color=C["text"]))
    fig.add_vline(x=kota_pct["kek"], line=dict(color=C["text2"], width=1, dash="dash"))
    fig.add_hline(y=kota_pct["anemia"], line=dict(color=C["text2"], width=1, dash="dash"))
    fig.add_annotation(x=0, y=-0.2, xref="paper", yref="paper", showarrow=False, xanchor="left",
                       text=f"Garis putus = angka kota (KEK {kota_pct['kek']}%, Anemia {kota_pct['anemia']}%). "
                            "Ukuran titik = jumlah ibu hamil. Korelasi bukan sebab-akibat.",
                       font=dict(size=11, color=C["text2"]))
    gaya(fig, "KEK vs Anemia per Puskesmas 2022: dua indikator yang tidak selalu searah",
         xtitle="% KEK", ytitle="% Anemia", tinggi=580)
    fig.update_layout(margin=dict(b=90))
    fig.update_xaxes(showgrid=True, gridcolor=C["grid"], rangemode="tozero")
    fig.update_yaxes(rangemode="tozero")
    return fig


def fig_kecamatan(kec: pd.DataFrame, kota_pct: dict) -> go.Figure:
    d = kec.sort_values("kek_persen")
    fig = go.Figure()
    for ind in ("kek", "anemia"):
        fig.add_trace(go.Bar(
            y=d.kecamatan, x=d[f"{ind}_persen"], name=NAMA[ind], orientation="h",
            marker=dict(color=C[ind], cornerradius=4, line=dict(color=C["surface"], width=2)),
            customdata=np.c_[d[f"{ind}_jumlah"], d.jumlah_bumil, d.jumlah_puskesmas],
            hovertemplate="<b>%{y}</b> · " + NAMA[ind] + " %{x:.2f}%<br>%{customdata[0]} dari %{customdata[1]:,} bumil"
                          " (%{customdata[2]} Puskesmas)<extra></extra>"))
    gaya(fig, "KEK dan Anemia per Kecamatan 2022 (diurutkan menurut % KEK)", xtitle="% ibu hamil", tinggi=620)
    fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.05)
    fig.update_yaxes(showgrid=False, title="")
    fig.update_xaxes(showgrid=True, gridcolor=C["grid"])
    return fig


# ------------------------------------------------------------------ main
def main() -> None:
    kota, pkm, kec = muat()
    pkm, kota_pct = analisis_puskesmas(pkm)
    pkm.to_csv(PROC / "eda_puskesmas_2022.csv", index=False)
    rk = ringkasan(kota, pkm, kota_pct)
    (PROC / "eda_ringkasan.json").write_text(json.dumps(rk, indent=2, ensure_ascii=False), encoding="utf-8")

    figs = [
        ("Tren tahunan (level kota)", fig_tren_persen(kota)),
        ("", fig_tren_indeks(kota)),
        ("Perbandingan antarwilayah 2022 — Puskesmas", fig_dot_ci(pkm, "kek", kota_pct["kek"])),
        ("", fig_dot_ci(pkm, "anemia", kota_pct["anemia"])),
        ("", fig_scatter(pkm, kota_pct)),
        ("Perbandingan antarwilayah 2022 — Kecamatan", fig_kecamatan(kec, kota_pct)),
    ]
    bagian = []
    for i, (h, f) in enumerate(figs):
        if h:
            bagian.append(f"<h2>{h}</h2>")
        bagian.append(f.to_html(full_html=False, include_plotlyjs="cdn" if i == 0 else False,
                                config={"displaylogo": False, "responsive": True}))
    html = f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tahap 3 — EDA Status Gizi Ibu Hamil Kota Semarang</title>
<style>
 :root{{color-scheme:light}} body{{margin:0;background:{C['surface']};color:{C['text']};
 font-family:Inter,system-ui,sans-serif;line-height:1.5}}
 main{{max-width:1080px;margin:0 auto;padding:32px 20px 64px}}
 h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:18px;margin:48px 0 8px;border-top:1px solid {C['grid']};padding-top:24px}}
 p.lead{{color:{C['text2']};margin:0 0 8px}} .note{{font-size:13px;color:{C['text2']};background:#f3f2ee;
 border-radius:8px;padding:10px 14px;margin:16px 0}}
</style></head><body><main>
<h1>Analisis Eksploratif — Status Gizi Ibu Hamil Kota Semarang</h1>
<p class="lead">KEK dan Anemia dianalisis sebagai dua indikator terpisah. Semua perbandingan bersifat deskriptif; tidak ada klaim sebab-akibat.</p>
<div class="note"><b>Sumber:</b> Satu Data Kota Semarang (tren kota 2017–2024) dan Lampiran Profil Kesehatan Kota Semarang 2022, Tabel 32 (per Puskesmas).
Persen per wilayah = kasus ÷ jumlah ibu hamil (turunan). Angka kota dari Tabel 32 (KEK {kota_pct['kek']}%, Anemia {kota_pct['anemia']}%) berbeda dari Satu Data 2022 karena definisi pencatatan berbeda.</div>
{''.join(bagian)}
</main></body></html>"""
    (REPORTS / "tahap3_eda.html").write_text(html, encoding="utf-8")
    print(json.dumps(rk, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
