"""Grafik Plotly untuk dashboard. KEK = biru, Anemia = oranye (slot kategorikal tervalidasi CVD)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data import NAMA, fmt_pct

C = {"kek": "#2a78d6", "anemia": "#eb6834", "ref": "#8a8984", "muted": "#cfcec8",
     "text": "#0b1f1c", "text2": "#52514e", "grid": "#e6ebe9", "surface": "rgba(0,0,0,0)"}
SKALA = {  # sekuensial satu hue, terang -> gelap
    "kek": ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"],
    "anemia": ["#fde4d8", "#f7b293", "#eb6834", "#b8461a", "#7a2c0e"],
}
CONFIG = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"], "locale": "id"}


def gaya(fig: go.Figure, judul: str = "", ytitle: str = "", xtitle: str = "", tinggi: int = 400) -> go.Figure:
    fig.update_layout(
        title=dict(text=judul or "", x=0, xanchor="left", font=dict(size=15, color=C["text"])),
        height=tinggi, paper_bgcolor=C["surface"], plot_bgcolor=C["surface"], separators=",.",
        font=dict(family="Inter, 'Source Sans Pro', system-ui, sans-serif", size=12, color=C["text2"]),
        margin=dict(l=8, r=24, t=60 if judul else 30, b=40), hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, bgcolor="rgba(0,0,0,0)", title=dict(text="")),
        hoverlabel=dict(bgcolor="white", font_size=12, font_color=C["text"]),
    )
    fig.update_xaxes(title=xtitle, showgrid=False, linecolor=C["grid"], ticks="outside", tickcolor=C["grid"])
    fig.update_yaxes(title=ytitle, gridcolor=C["grid"], zeroline=False, linecolor=C["grid"])
    return fig


# --------------------------------------------------------------- tren kota
def tren_persen(kota: pd.DataFrame, indikator: list[str], tahun_pilih: int) -> go.Figure:
    kode = {"kek": ("KEK_PERSEN_TURUNAN", "% KEK (LiLA < 23,5 cm ÷ K1)"),
            "anemia": ("ANEMIA_PREVALENSI", "Prevalensi Anemia (resmi)")}
    fig = go.Figure()
    for ind in indikator:
        k, label = kode[ind]
        d = kota[(kota.indikator == k) & kota.nilai.notna()].sort_values("tahun")
        fig.add_trace(go.Scatter(
            x=d.tahun, y=d.nilai, mode="lines+markers", name=label,
            line=dict(color=C[ind], width=2.5), marker=dict(size=9, color=C[ind], line=dict(color="white", width=2)),
            customdata=np.c_[d.status.str.replace("_", " "), d.catatan.fillna("")],
            hovertemplate="<b>%{x}</b> · " + NAMA[ind] + " %{y:.2f}%<br>Status data: %{customdata[0]}"
                          "<br><i>%{customdata[1]}</i><extra></extra>"))
        flag = d[d.status != "valid"]
        if len(flag):
            fig.add_trace(go.Scatter(x=flag.tahun, y=flag.nilai, mode="markers", showlegend=False, hoverinfo="skip",
                                     marker=dict(size=17, color="rgba(0,0,0,0)", line=dict(color=C["text2"], width=1.5))))
        last = d.iloc[-1]
        fig.add_annotation(x=last.tahun, y=last.nilai, text=f"<b>{NAMA[ind]}</b> {fmt_pct(last.nilai)}",
                           showarrow=False, xanchor="left", xshift=10, font=dict(color=C["text"]))
    fig.add_vrect(x0=tahun_pilih - 0.4, x1=tahun_pilih + 0.4, fillcolor="#0f766e", opacity=0.07, line_width=0)
    gaya(fig, ytitle="% ibu hamil", tinggi=400)
    fig.update_xaxes(dtick=1, range=[2016.5, 2025.6])
    fig.update_yaxes(rangemode="tozero")
    return fig


def tren_jumlah(kota: pd.DataFrame, indikator: list[str], tahun_pilih: int) -> go.Figure:
    kode = {"kek": "KEK_JUMLAH", "anemia": "ANEMIA_JUMLAH"}
    fig = go.Figure()
    for ind in indikator:
        d = kota[(kota.indikator == kode[ind]) & (kota.tahun.between(2017, 2024))].sort_values("tahun")
        fig.add_trace(go.Scatter(
            x=d.tahun, y=d.nilai, mode="lines+markers", name=f"Kasus {NAMA[ind]}", connectgaps=False,
            line=dict(color=C[ind], width=2.5), marker=dict(size=9, color=C[ind], line=dict(color="white", width=2)),
            customdata=np.c_[d.status.str.replace("_", " "), d.catatan.fillna("")],
            hovertemplate="<b>%{x}</b> · %{y:,.0f} kasus " + NAMA[ind] +
                          "<br>Status data: %{customdata[0]}<br><i>%{customdata[1]}</i><extra></extra>"))
    fig.add_vrect(x0=tahun_pilih - 0.4, x1=tahun_pilih + 0.4, fillcolor="#0f766e", opacity=0.07, line_width=0)
    gaya(fig, ytitle="Jumlah ibu hamil", tinggi=400)
    fig.update_xaxes(dtick=1, range=[2016.5, 2025.6])
    fig.update_yaxes(rangemode="tozero", tickformat=",.0f")
    return fig


def tren_indeks(kota: pd.DataFrame, indikator: list[str]) -> go.Figure:
    seri = [("BUMIL_K1", "Ibu hamil (K1)", C["ref"], "dot", 9)]
    seri += [("KEK_JUMLAH", "Kasus KEK", C["kek"], "solid", -9)] if "kek" in indikator else []
    seri += [("ANEMIA_JUMLAH", "Kasus Anemia", C["anemia"], "solid", 0)] if "anemia" in indikator else []
    fig = go.Figure()
    for kode, label, warna, dash, geser in seri:
        d = kota[kota.indikator == kode].set_index("tahun")["nilai"].sort_index().loc[2017:2024]
        idx = d / d.loc[2017] * 100
        fig.add_trace(go.Scatter(x=idx.index, y=idx.values, name=label, mode="lines+markers",
                                 line=dict(color=warna, width=2, dash=dash), marker=dict(size=7, color=warna),
                                 customdata=d.values,
                                 hovertemplate="<b>%{x}</b> · " + label +
                                               "<br>Indeks %{y:.1f} (%{customdata:,.0f} orang)<extra></extra>"))
        last = idx.dropna().iloc[-1]
        fig.add_annotation(x=2024, y=last, text=f"<b>{label}</b> {last:.0f}", showarrow=False,
                           xanchor="left", xshift=10, yshift=geser, font=dict(color=C["text"]))
    fig.add_hline(y=100, line=dict(color=C["grid"], width=1))
    gaya(fig, ytitle="Indeks (2017 = 100)", tinggi=360)
    fig.update_xaxes(dtick=1, range=[2016.6, 2025.6])
    return fig


# ----------------------------------------------------------------- wilayah
def peta(kec: pd.DataFrame, geo: dict, ind: str, ukuran: str, pilihan: list[str]) -> go.Figure:
    kol = f"{ind}_persen" if ukuran == "persen" else f"{ind}_jumlah"
    d = kec.copy()
    d["_nilai"] = d[kol]
    d.loc[~d.kecamatan.isin(pilihan), "_nilai"] = np.nan  # di luar filter: tanpa warna
    label = f"% {NAMA[ind]}" if ukuran == "persen" else f"Kasus {NAMA[ind]}"
    fig = px.choropleth_map(
        d, geojson=geo, locations="kecamatan", featureidkey="id", color="_nilai",
        color_continuous_scale=SKALA[ind], range_color=(kec[kol].min(), kec[kol].max()),
        map_style="carto-positron", center={"lat": -7.02, "lon": 110.40}, zoom=10.1, opacity=0.82,
        custom_data=["kecamatan", f"{ind}_persen", f"{ind}_jumlah", "jumlah_bumil", f"{ind}_vs_kota", "kode_kemendagri"],
    )
    fig.update_traces(
        marker_line_color="white", marker_line_width=1.2,
        hovertemplate="<b>%{customdata[0]}</b> (%{customdata[5]})<br>" + NAMA[ind] +
                      ": %{customdata[1]:.2f}% · %{customdata[2]:,} kasus<br>dari %{customdata[3]:,} ibu hamil"
                      "<br>Dibanding kota: %{customdata[4]}<extra></extra>")
    fig.update_layout(height=440, margin=dict(l=0, r=0, t=0, b=0), separators=",.",
                      coloraxis_colorbar=dict(title=dict(text=label, side="right"), thickness=12, len=0.75,
                                              tickformat=".1f" if ukuran == "persen" else ",.0f"))
    return fig


def batang_kecamatan(kec: pd.DataFrame, indikator: list[str], ukuran: str, pilihan: list[str]) -> go.Figure:
    d = kec[kec.kecamatan.isin(pilihan)].copy()
    urut = f"{indikator[0]}_{'persen' if ukuran == 'persen' else 'jumlah'}"
    d = d.sort_values(urut)
    fig = go.Figure()
    for ind in indikator:
        kol = f"{ind}_persen" if ukuran == "persen" else f"{ind}_jumlah"
        fig.add_trace(go.Bar(
            y=d.kecamatan, x=d[kol], name=NAMA[ind], orientation="h",
            marker=dict(color=C[ind], cornerradius=4, line=dict(color="white", width=1.5)),
            customdata=np.c_[d[f"{ind}_persen"], d[f"{ind}_jumlah"], d.jumlah_bumil, d.jumlah_puskesmas],
            hovertemplate="<b>%{y}</b> · " + NAMA[ind] + " %{customdata[0]:.2f}%<br>%{customdata[1]:,} kasus dari "
                          "%{customdata[2]:,} ibu hamil (%{customdata[3]} Puskesmas)<extra></extra>"))
    gaya(fig, xtitle="% ibu hamil" if ukuran == "persen" else "Jumlah kasus", tinggi=max(320, 34 * len(d) + 90))
    fig.update_layout(barmode="group", bargap=0.28, bargroupgap=0.06, showlegend=len(indikator) > 1)
    fig.update_yaxes(showgrid=False, title="")
    fig.update_xaxes(showgrid=True, gridcolor=C["grid"], tickformat=",.0f" if ukuran != "persen" else None)
    return fig


def titik_ci(pkm: pd.DataFrame, ind: str, kota_rate: float) -> go.Figure:
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
            hovertemplate="<b>%{y}</b> · Kec. %{customdata[0]}<br>" + NAMA[ind] +
                          " %{x:.2f}% (%{customdata[1]} dari %{customdata[2]:,} ibu hamil)"
                          "<br>Selang kepercayaan 95%: %{customdata[3]:.1f}–%{customdata[4]:.1f}%<extra></extra>"))
    fig.add_vline(x=kota_rate, line=dict(color=C["text2"], width=1, dash="dash"))
    fig.add_annotation(x=kota_rate, y=1.0, yref="paper", text=f"Kota {fmt_pct(kota_rate)}", showarrow=False,
                       yanchor="bottom", font=dict(color=C["text"], size=11))
    gaya(fig, xtitle=f"% ibu hamil dengan {NAMA[ind]}", tinggi=max(300, 24 * len(d) + 130))
    fig.update_yaxes(categoryorder="array", categoryarray=d.puskesmas.tolist(), showgrid=False, title="")
    fig.update_xaxes(showgrid=True, gridcolor=C["grid"], rangemode="tozero")
    fig.update_layout(margin=dict(t=80), legend=dict(y=1.06))
    return fig


def batang_puskesmas(pkm: pd.DataFrame, ind: str) -> go.Figure:
    d = pkm.sort_values(f"{ind}_jumlah")
    fig = go.Figure(go.Bar(
        y=d.puskesmas, x=d[f"{ind}_jumlah"], orientation="h", name=f"Kasus {NAMA[ind]}",
        marker=dict(color=C[ind], cornerradius=4),
        customdata=np.c_[d.kecamatan, d[f"{ind}_persen"], d.jumlah_bumil],
        hovertemplate="<b>%{y}</b> · Kec. %{customdata[0]}<br>%{x:,} kasus " + NAMA[ind] +
                      " (%{customdata[1]:.2f}% dari %{customdata[2]:,} ibu hamil)<extra></extra>"))
    gaya(fig, xtitle=f"Jumlah kasus {NAMA[ind]}", tinggi=max(300, 24 * len(d) + 100))
    fig.update_yaxes(showgrid=False, title="")
    fig.update_xaxes(showgrid=True, gridcolor=C["grid"])
    return fig


def sebar_kek_anemia(pkm: pd.DataFrame, ref: dict) -> go.Figure:
    fig = go.Figure()
    ganda = pkm.kategori_beban == "KEK & Anemia di atas kota"
    for mask, nama, warna in [(~ganda, "Puskesmas lain", C["ref"]),
                              (ganda, "KEK & Anemia sama-sama di atas kota (bermakna)", C["kek"])]:
        s = pkm[mask]
        if s.empty:
            continue
        fig.add_trace(go.Scatter(
            x=s.kek_persen, y=s.anemia_persen, mode="markers", name=nama,
            marker=dict(size=np.sqrt(s.jumlah_bumil) / 1.6 + 4, color=warna, opacity=0.85,
                        line=dict(color="white", width=1.5)),
            customdata=np.c_[s.puskesmas, s.kecamatan, s.jumlah_bumil, s.kategori_beban],
            hovertemplate="<b>%{customdata[0]}</b> · Kec. %{customdata[1]}<br>KEK %{x:.2f}% · Anemia %{y:.2f}%"
                          "<br>%{customdata[2]:,} ibu hamil<br>%{customdata[3]}<extra></extra>"))
    sorot = pkm[ganda | ((pkm.kek_vs_kota == "di atas kota") & (pkm.anemia_vs_kota == "di bawah kota"))
                | ((pkm.anemia_vs_kota == "di atas kota") & (pkm.kek_vs_kota == "di bawah kota"))]
    for _, r in sorot.iterrows():
        fig.add_annotation(x=r.kek_persen, y=r.anemia_persen, text=r.puskesmas, showarrow=False, yshift=14,
                           font=dict(size=11, color=C["text"]))
    fig.add_vline(x=ref["kek"], line=dict(color=C["text2"], width=1, dash="dash"))
    fig.add_hline(y=ref["anemia"], line=dict(color=C["text2"], width=1, dash="dash"))
    xm, ym = max(pkm.kek_persen.max(), ref["kek"]) * 1.08, max(pkm.anemia_persen.max(), ref["anemia"]) * 1.08
    for x, y, t, xa, ya in [(xm, ym, "KEK ↑ · Anemia ↑", "right", "top"), (0, ym, "KEK ↓ · Anemia ↑", "left", "top"),
                            (xm, 0, "KEK ↑ · Anemia ↓", "right", "bottom"), (0, 0, "KEK ↓ · Anemia ↓", "left", "bottom")]:
        fig.add_annotation(x=x, y=y, text=t, showarrow=False, xanchor=xa, yanchor=ya,
                           font=dict(size=11, color=C["ref"]))
    gaya(fig, xtitle="% KEK", ytitle="% Anemia", tinggi=540)
    fig.update_xaxes(showgrid=True, gridcolor=C["grid"], range=[0, xm])
    fig.update_yaxes(range=[0, ym])
    return fig
