"""
Dashboard Monitoring & Analisis Status Gizi Ibu Hamil — Kota Semarang
Indikator: Kurang Energi Kronis (KEK) dan Anemia (dianalisis terpisah).

Jalankan lokal:  streamlit run app.py
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src import charts, data
from src.data import NAMA, SUMBER, TAHUN_WILAYAH, fmt_int, fmt_num, fmt_pct
from src.insights import insight_tren, insight_wilayah, rekomendasi

st.set_page_config(page_title="Gizi Ibu Hamil · Kota Semarang", page_icon="🤰", layout="wide",
                   initial_sidebar_state="expanded")

# ------------------------------------------------------------------ gaya
st.markdown("""
<style>
  .block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1320px;}
  .hero {background: linear-gradient(120deg, #0f766e 0%, #14918a 55%, #2bb3a3 100%); color: #fff;
         border-radius: 16px; padding: 22px 28px; margin-bottom: 18px;}
  .hero h1 {font-size: 1.65rem; margin: 0 0 4px 0; color: #fff; font-weight: 700; padding: 0;}
  .hero p {margin: 0; opacity: .92; font-size: .95rem;}
  .hero .chips {margin-top: 12px;}
  .chip {display: inline-block; background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.28);
         border-radius: 999px; padding: 2px 12px; font-size: .78rem; margin: 0 6px 6px 0;}
  .kpi {background: #fff; border: 1px solid #e3ebe8; border-radius: 14px; padding: 14px 16px 12px;
        border-top: 4px solid var(--accent); height: 100%; box-shadow: 0 1px 2px rgba(15,118,110,.05);}
  .kpi .lbl {font-size: .8rem; color: #52514e; font-weight: 600; text-transform: uppercase; letter-spacing: .02em;}
  .kpi .val {font-size: 1.85rem; font-weight: 700; color: #0b1f1c; line-height: 1.2; margin-top: 4px;}
  .kpi .sub {font-size: .83rem; color: #52514e; margin-top: 4px;}
  .kpi .badge {display: inline-block; font-size: .72rem; border-radius: 6px; padding: 1px 7px; margin-top: 6px;
               background: #fff4e5; color: #8a4b00; border: 1px solid #f6d7a7;}
  .kpi .badge.na {background: #f1f1ef; color: #52514e; border-color: #e1e0db;}
  .note {background: #eef7f5; border-left: 4px solid #0f766e; border-radius: 8px; padding: 10px 14px;
         font-size: .9rem; color: #0b1f1c; margin: 6px 0 14px;}
  .warn {background: #fff8ec; border-left: 4px solid #e8a33d;}
  .rek {background: #fff; border: 1px solid #e3ebe8; border-radius: 12px; padding: 14px 16px; margin-bottom: 12px;}
  .rek .tag {font-size: .72rem; font-weight: 700; border-radius: 6px; padding: 2px 8px; margin-right: 8px;
             background: #e6f4f1; color: #0f766e;}
  .rek .tag.Tinggi {background: #fde8e8; color: #9b1c1c;}
  .rek .tag.Sedang {background: #fff4e5; color: #8a4b00;}
  .rek h4 {display: inline; font-size: 1rem; margin: 0;}
  .rek .dasar {font-size: .86rem; color: #52514e; margin: 8px 0 4px;}
  .rek .saran {font-size: .92rem; color: #0b1f1c; margin: 0;}
  .src {font-size: .8rem; color: #6b6a66;}
  div[data-testid="stTabs"] button p {font-size: .95rem; font-weight: 600;}
</style>
""", unsafe_allow_html=True)


def kartu(label: str, nilai: str, sub: str = "", accent: str = "#0f766e", badge: str | None = None,
          badge_na: bool = False) -> str:
    b = f'<div class="badge{" na" if badge_na else ""}">{badge}</div>' if badge else ""
    return (f'<div class="kpi" style="--accent:{accent}"><div class="lbl">{label}</div>'
            f'<div class="val">{nilai}</div><div class="sub">{sub}</div>{b}</div>')


def kotak(teks: str, warn: bool = False):
    st.markdown(f'<div class="note{" warn" if warn else ""}">{teks}</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ data
kota = data.kota()
nilai, status, catatan = data.kota_wide()
pkm_all = data.puskesmas()
kec_all = data.kecamatan()
geo = data.geojson()
ref = data.kota_2022_tabel32()

# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.markdown("### 🔎 Filter")
    tahun = st.select_slider("Tahun (tren kota)", options=list(range(2017, 2026)), value=2024, key="f_tahun",
                             help="Data level kota tersedia 2017–2024. Data 2025 KEK/Anemia belum tersedia.")
    pilihan_ind = st.radio("Indikator", ["KEK & Anemia", "KEK", "Anemia"], horizontal=False, key="f_ind",
                           help="KEK dan Anemia selalu dihitung terpisah — tidak pernah dijumlahkan.")
    indikator = {"KEK & Anemia": ["kek", "anemia"], "KEK": ["kek"], "Anemia": ["anemia"]}[pilihan_ind]
    ukuran_lbl = st.segmented_control("Ukuran", ["Persentase", "Jumlah kasus"], default="Persentase", key="f_ukuran",
                                      help="Persentase = risiko relatif. Jumlah kasus = beban layanan.")
    ukuran = "jumlah" if ukuran_lbl == "Jumlah kasus" else "persen"
    kec_pilih = st.multiselect("Kecamatan (data wilayah 2022)", data.daftar_kecamatan(),
                               placeholder="Semua kecamatan", key="f_kec")
    semua_kec = len(kec_pilih) == 0
    kec_aktif = data.daftar_kecamatan() if semua_kec else kec_pilih
    st.divider()
    st.markdown("**Sumber data resmi**")
    for nama, url in SUMBER.values():
        st.markdown(f'<div class="src">• <a href="{url}" target="_blank">{nama}</a></div>', unsafe_allow_html=True)
    st.caption("Tanpa data simulasi. Sel yang tidak valid dikosongkan, bukan diestimasi.")

pkm = pkm_all[pkm_all.kecamatan.isin(kec_aktif)]

# ------------------------------------------------------------------ header
st.markdown(f"""
<div class="hero">
  <h1>🤰 Monitoring Status Gizi Ibu Hamil — Kota Semarang</h1>
  <p>Kurang Energi Kronis (KEK, LiLA &lt; 23,5 cm) dan Anemia (Hb &lt; 11 g/dl) sebagai dua indikator terpisah ·
     analisis deskriptif tanpa klaim sebab-akibat</p>
  <div class="chips"><span class="chip">Tren kota 2017–2024</span><span class="chip">37 Puskesmas · 16 Kecamatan (2022)</span>
  <span class="chip">Sumber: Dinkes · Satu Data · Geoportal Kota Semarang</span></div>
</div>""", unsafe_allow_html=True)

# ------------------------------------------------------------------ KPI
def kpi_indikator(ind: str) -> list[str]:
    kp = "KEK_PERSEN_TURUNAN" if ind == "kek" else "ANEMIA_PREVALENSI"
    kj = "KEK_JUMLAH" if ind == "kek" else "ANEMIA_JUMLAH"
    accent = charts.C[ind]
    v, j = nilai.at[tahun, kp], nilai.at[tahun, kj]
    s_v, s_j = status.at[tahun, kp], status.at[tahun, kj]
    prev = nilai[kp].dropna()
    prev = prev[prev.index < tahun]
    if pd.isna(v):
        sub, badge, na = "Belum tersedia di sumber resmi", "Data tidak tersedia", True
    else:
        sub = ""
        if len(prev):
            d = v - prev.iloc[-1]
            panah = "▲" if d > 0 else "▼" if d < 0 else "■"
            sub = f"{panah} {fmt_num(abs(d))} poin vs {prev.index[-1]}"
        badge = "⚠ Perlu perhatian" if s_v != "valid" else None
        na = False
        if ind == "kek":
            sub += " · turunan (kasus ÷ K1)" if tahun != 2024 else " · sesuai angka resmi"
    label_p = "% KEK" if ind == "kek" else "Prevalensi Anemia"
    k1 = [kartu(f"{label_p} · {tahun}", fmt_pct(v), sub, accent, badge, na)]
    if pd.isna(j):
        alasan = "Nilai sumber tidak valid" if s_j == "tidak_valid" else "Belum tersedia"
        k1.append(kartu(f"Kasus {NAMA[ind]} · {tahun}", "—", alasan, accent, "Data tidak tersedia", True))
    else:
        k1.append(kartu(f"Kasus {NAMA[ind]} · {tahun}", fmt_int(j), "ibu hamil", accent))
    return k1


cards = [kartu(f"Ibu hamil (K1) · {tahun}", fmt_int(nilai.at[tahun, "BUMIL_K1"]), "sasaran pelayanan antenatal",
               "#0f766e", "⚠ Perlu perhatian" if status.at[tahun, "BUMIL_K1"] != "valid" else None)]
for ind in indikator:
    cards += kpi_indikator(ind)
if len(indikator) == 2:
    ganda = pkm[pkm.kategori_beban == "KEK & Anemia di atas kota"]
    cards.append(kartu("Puskesmas beban ganda · 2022", f"{len(ganda)}",
                       f"dari {len(pkm)} Puskesmas: KEK & Anemia bermakna di atas kota", "#6250d6"))
else:
    ind = indikator[0]
    atas = (pkm[f"{ind}_vs_kota"] == "di atas kota").sum()
    cards.append(kartu(f"Puskesmas {NAMA[ind]} > kota · 2022", f"{atas}",
                       f"dari {len(pkm)} Puskesmas (selang kepercayaan 95%)", charts.C[ind]))
cols = st.columns(len(cards))
for c, html in zip(cols, cards):
    c.markdown(html, unsafe_allow_html=True)
st.write("")

# ------------------------------------------------------------------ tabs
tab_tren, tab_wil, tab_vs, tab_ins, tab_data = st.tabs(
    ["📈 Tren Kota", "🗺️ Peta & Wilayah 2022", "⚖️ KEK vs Anemia", "💡 Insight & Rekomendasi", "📄 Data & Metodologi"])

# ---------- Tren
with tab_tren:
    judul = "Persentase" if ukuran == "persen" else "Jumlah kasus"
    st.subheader(f"{judul} {' & '.join(NAMA[i] for i in indikator)} ibu hamil, 2017–2024")
    fig = charts.tren_persen(kota, indikator, tahun) if ukuran == "persen" else charts.tren_jumlah(kota, indikator, tahun)
    st.plotly_chart(fig, config=charts.CONFIG)
    st.caption("Lingkaran abu-abu = titik bertanda *perlu perhatian*. Celah garis = nilai tidak valid/tidak tersedia. "
               "Pita hijau = tahun terpilih. Sumber: Satu Data Kota Semarang.")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("##### Insight")
        for t in insight_tren(nilai, status, tahun, indikator):
            st.markdown(f"- {t}")
    with c2:
        st.markdown("##### Jumlah kasus vs jumlah ibu hamil")
        st.plotly_chart(charts.tren_indeks(kota, indikator), config=charts.CONFIG)
    kode_terpilih = {"kek": ["KEK_JUMLAH", "KEK_PERSEN", "KEK_PERSEN_TURUNAN"],
                     "anemia": ["ANEMIA_JUMLAH", "ANEMIA_PREVALENSI"]}
    masalah = kota[kota.indikator.isin(sum((kode_terpilih[i] for i in indikator), ["BUMIL_K1", "BUMIL_K4", "BUMIL_JUMLAH"]))
                   & kota.status.isin(["tidak_valid", "perlu_perhatian"])]
    with st.expander(f"⚠ Catatan kualitas data ({len(masalah)} sel)"):
        st.dataframe(masalah[["tahun", "indikator", "nilai_asli", "status", "catatan"]].sort_values(["indikator", "tahun"]),
                     hide_index=True,
                     column_config={"nilai_asli": st.column_config.NumberColumn("Nilai di sumber", format="%.2f")})

# ---------- Wilayah
with tab_wil:
    if tahun != TAHUN_WILAYAH:
        kotak(f"Data KEK & Anemia per Kecamatan/Puskesmas <b>hanya tersedia untuk tahun {TAHUN_WILAYAH}</b> "
              f"(Lampiran Profil Kesehatan, Tabel 32). Tahun {tahun} yang dipilih berlaku untuk tren kota saja.", warn=True)
    kotak(f"Angka kota menurut Tabel 32 (2022): <b>KEK {fmt_pct(ref['kek'])}</b> · <b>Anemia {fmt_pct(ref['anemia'])}</b> "
          f"dari {fmt_int(ref['n'])} ibu hamil. Angka ini berbeda dari Satu Data 2022 karena definisi pencatatan berbeda, "
          "sehingga kedua sumber tidak dicampur.")
    ind_peta = indikator[0]
    if len(indikator) == 2:
        ind_peta = st.radio("Indikator pada peta", ["kek", "anemia"], format_func=lambda x: NAMA[x], horizontal=True,
                            key="f_peta")
    c1, c2 = st.columns([1.15, 1])
    with c1:
        st.markdown(f"##### Peta {'persentase' if ukuran == 'persen' else 'jumlah kasus'} {NAMA[ind_peta]} per Kecamatan")
        st.plotly_chart(charts.peta(kec_all, geo, ind_peta, ukuran, kec_aktif), config=charts.CONFIG)
        st.caption(f"Batas wilayah: {SUMBER['geoportal'][0]}. Kecamatan di luar filter tidak diberi warna.")
    with c2:
        st.markdown("##### Per Kecamatan")
        st.plotly_chart(charts.batang_kecamatan(kec_all, indikator, ukuran, kec_aktif), config=charts.CONFIG)

    st.markdown("##### Per Puskesmas" + ("" if semua_kec else f" — {', '.join(kec_pilih)}"))
    if ukuran == "persen":
        st.caption("Titik = persentase; garis = selang kepercayaan 95% (Wilson). Puskesmas dengan sedikit ibu hamil "
                   "memiliki garis lebar — angkanya kurang stabil. Warna penuh = bermakna di atas angka kota.")
    pc = st.columns(len(indikator))
    for c, ind in zip(pc, indikator):
        with c:
            st.markdown(f"**{NAMA[ind]}**")
            fig = charts.titik_ci(pkm, ind, ref[ind]) if ukuran == "persen" else charts.batang_puskesmas(pkm, ind)
            st.plotly_chart(fig, config=charts.CONFIG, key=f"pkm_{ind}")
    st.markdown("##### Insight wilayah")
    for t in insight_wilayah(pkm, ref, indikator, semua_kec):
        st.markdown(f"- {t}")

# ---------- KEK vs Anemia
with tab_vs:
    st.subheader("Apakah wilayah dengan KEK tinggi juga tinggi Anemia-nya? (2022)")
    kotak("Setiap titik adalah satu Puskesmas; ukuran titik = jumlah ibu hamil. Garis putus-putus = angka kota. "
          "Hubungan antar-indikator bersifat <b>asosiatif</b>, bukan sebab-akibat.")
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.plotly_chart(charts.sebar_kek_anemia(pkm, ref), config=charts.CONFIG)
    with c2:
        rho = pkm.kek_persen.rank().corr(pkm.anemia_persen.rank()) if len(pkm) > 2 else float("nan")
        st.metric("Korelasi peringkat % KEK vs % Anemia", fmt_num(rho), help="Spearman ρ. 0 = tidak berhubungan, 1 = searah sempurna.")
        tabel = (pkm.groupby("kategori_beban").puskesmas.agg(["count", lambda s: ", ".join(sorted(s))])
                 .rename(columns={"count": "Jumlah", "<lambda_0>": "Puskesmas"}))
        urutan = ["KEK & Anemia di atas kota", "KEK di atas kota", "Anemia di atas kota", "Tidak di atas kota"]
        tabel = tabel.reindex([u for u in urutan if u in tabel.index]).rename_axis("Kategori")
        st.dataframe(tabel, column_config={"Puskesmas": st.column_config.TextColumn(width="large")})
        st.caption("Kategori memakai selang kepercayaan 95%: \"di atas kota\" hanya jika seluruh selang berada di atas angka kota.")

# ---------- Insight & rekomendasi
with tab_ins:
    st.subheader("Insight utama")
    st.caption("Diperbarui otomatis mengikuti filter Tahun, Indikator, dan Kecamatan.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Tren kota ({tahun})**")
        for t in insight_tren(nilai, status, tahun, indikator):
            st.markdown(f"- {t}")
    with c2:
        st.markdown(f"**Wilayah ({TAHUN_WILAYAH})**")
        for t in insight_wilayah(pkm, ref, indikator, semua_kec):
            st.markdown(f"- {t}")
    st.subheader("Rekomendasi berbasis data")
    st.caption("Disusun dari seluruh 37 Puskesmas. Rekomendasi adalah bahan pertimbangan program, bukan kesimpulan kausal.")
    for r in rekomendasi(pkm_all, nilai, status):
        st.markdown(f"""<div class="rek"><span class="tag {r['prioritas'].split()[0]}">{r['prioritas']}</span>
        <h4>{r['judul']}</h4><p class="dasar"><b>Dasar data:</b> {r['dasar']}</p>
        <p class="saran">{r['saran']}</p></div>""", unsafe_allow_html=True)

# ---------- Data & metodologi
with tab_data:
    st.subheader("Data yang digunakan")
    d1, d2, d3 = st.tabs(["Kota (tahunan)", "Puskesmas 2022", "Kecamatan 2022"])
    with d1:
        tampil = kota[["tahun", "kelompok", "indikator", "nilai", "satuan", "jenis_nilai", "status", "catatan", "sumber"]]
        st.dataframe(tampil, hide_index=True, height=360)
        st.download_button("⬇ Unduh CSV", kota.to_csv(index=False).encode("utf-8"), "kota_tahunan.csv", "text/csv")
    with d2:
        kolom = ["kecamatan", "puskesmas", "jumlah_bumil", "kek_jumlah", "kek_persen", "kek_ci_bawah", "kek_ci_atas",
                 "kek_vs_kota", "anemia_jumlah", "anemia_persen", "anemia_ci_bawah", "anemia_ci_atas", "anemia_vs_kota"]
        st.dataframe(pkm[kolom], hide_index=True, height=360, column_config={
            "kek_persen": st.column_config.ProgressColumn("% KEK", format="%.2f", min_value=0, max_value=35),
            "anemia_persen": st.column_config.ProgressColumn("% Anemia", format="%.2f", min_value=0, max_value=35)})
        st.download_button("⬇ Unduh CSV", pkm_all.to_csv(index=False).encode("utf-8"), "puskesmas_2022.csv", "text/csv")
    with d3:
        st.dataframe(kec_all.drop(columns=["sumber"]), hide_index=True, height=360)
        st.download_button("⬇ Unduh CSV", kec_all.to_csv(index=False).encode("utf-8"), "kecamatan_2022.csv", "text/csv")

    st.subheader("Metodologi & keterbatasan")
    st.markdown(f"""
- **Definisi.** KEK = ibu hamil dengan Lingkar Lengan Atas (LiLA) < 23,5 cm. Anemia = ibu hamil dengan kadar
  hemoglobin < 11 g/dl. Keduanya **tidak pernah digabung** menjadi satu indikator.
- **Tren kota** (Satu Data): prevalensi Anemia adalah angka resmi. % KEK 2017–2023 adalah **turunan**
  (kasus LiLA < 23,5 cm ÷ ibu hamil K1); untuk 2024 hasilnya sama dengan angka resmi (6,67%).
- **Validasi.** Nilai 0 pada 2016 diperlakukan sebagai *tidak tersedia*. Nilai yang mustahil (mis. "%" berisi jumlah
  kasus) atau identik dengan seri lain (jumlah Anemia 2023 = jumlah K1) **dikosongkan**, bukan diganti estimasi.
- **Wilayah 2022** (Tabel 32): persentase = kasus ÷ jumlah ibu hamil. Selang kepercayaan 95% memakai metode Wilson;
  "di atas/di bawah kota" hanya jika seluruh selang berada di sisi tersebut. Persentase kecamatan dihitung dari jumlah
  agregat, bukan rata-rata persen Puskesmas.
- **Keterbatasan.** (1) Data per wilayah hanya satu tahun (2022). (2) Angka Tabel 32 ≠ Satu Data 2022
  (KEK {fmt_int(ref['kek_jumlah'])} vs {fmt_int(nilai.at[2022, 'KEK_JUMLAH'])}; Anemia {fmt_int(ref['anemia_jumlah'])} vs
  {fmt_int(nilai.at[2022, 'ANEMIA_JUMLAH'])}). (3) Cakupan skrining LiLA/Hb per Puskesmas tidak tersedia.
  (4) Data 2025 KEK/Anemia belum tersedia. (5) Puskesmas Plamongan Sari belum ada pada data 2022.
- **Peta.** Batas kecamatan dari Geoportal Kota Semarang (WFS `ADMINISTRASI_AR_KECAMATAN_25K`); atribut nama memakai
  `NAMOBJ` dan kode Kemendagri `KDCPUM` (atribut `WADMKC` pada layer tidak konsisten dengan geometri).
""")
    st.markdown("**Tautan sumber:** " + " · ".join(f"[{n}]({u})" for n, u in SUMBER.values()))
