"""Insight & rekomendasi yang dihasilkan otomatis dari data (deskriptif, tanpa klaim kausal)."""
from __future__ import annotations

import pandas as pd

from src.data import NAMA, fmt_int, fmt_num, fmt_pct

KODE_PERSEN = {"kek": "KEK_PERSEN_TURUNAN", "anemia": "ANEMIA_PREVALENSI"}
KODE_JUMLAH = {"kek": "KEK_JUMLAH", "anemia": "ANEMIA_JUMLAH"}


def _daftar(nama, maks: int = 6) -> str:
    nama = list(nama)
    if not nama:
        return "—"
    return ", ".join(nama[:maks]) + (f", dan {len(nama) - maks} lainnya" if len(nama) > maks else "")


def _tahun_sebelumnya(seri: pd.Series, tahun: int):
    s = seri.dropna()
    s = s[s.index < tahun]
    return (s.index[-1], s.iloc[-1]) if len(s) else (None, None)


def insight_tren(nilai: pd.DataFrame, status: pd.DataFrame, tahun: int, indikator: list[str]) -> list[str]:
    out = []
    for ind in indikator:
        kp, kj = KODE_PERSEN[ind], KODE_JUMLAH[ind]
        v = nilai.at[tahun, kp] if tahun in nilai.index else None
        label = "% KEK" if ind == "kek" else "Prevalensi Anemia"
        if v is None or pd.isna(v):
            out.append(f"**{label} {tahun}: data tidak tersedia** di sumber resmi. Tren hanya tersedia sampai 2024.")
            continue
        t0, v0 = _tahun_sebelumnya(nilai[kp], tahun)
        teks = f"**{label} {tahun}: {fmt_pct(v)}**"
        if t0:
            arah = "naik" if v > v0 else "turun" if v < v0 else "tetap"
            teks += f", {arah} {fmt_num(abs(v - v0))} poin dari {fmt_pct(v0)} ({t0})"
        if tahun != 2017 and not pd.isna(nilai.at[2017, kp]):
            teks += f"; dibanding 2017 ({fmt_pct(nilai.at[2017, kp])})"
        st_sel = status.at[tahun, kp] if kp in status.columns else "valid"
        if isinstance(st_sel, str) and st_sel != "valid":
            teks += " ⚠ *nilai ini ditandai perlu perhatian pada validasi data*"
        out.append(teks + ".")

    # jumlah kasus vs jumlah sasaran
    k1 = nilai["BUMIL_K1"]
    if tahun in nilai.index and tahun != 2017 and not pd.isna(k1.get(tahun)):
        idx_k1 = k1[tahun] / k1[2017] * 100
        for ind in indikator:
            j = nilai[KODE_JUMLAH[ind]]
            if not pd.isna(j.get(tahun)):
                idx_j = j[tahun] / j[2017] * 100
                selisih = idx_j - idx_k1
                pola = ("turun hampir sejajar dengan" if abs(selisih) < 5 else
                        "turun lebih cepat daripada" if selisih < 0 else "turun lebih lambat daripada")
                out.append(f"Kasus {NAMA[ind]} {tahun} berada di indeks **{idx_j:.0f}** (2017 = 100), sementara "
                           f"jumlah ibu hamil (K1) di indeks **{idx_k1:.0f}**: jumlah kasus {pola} jumlah ibu hamil. "
                           "Karena itu, persentase lebih tepat untuk menilai perubahan risiko.")
    return out


def insight_wilayah(pkm: pd.DataFrame, ref: dict, indikator: list[str], semua: bool) -> list[str]:
    out = []
    lingkup = "di seluruh kota" if semua else "di kecamatan terpilih"
    for ind in indikator:
        atas = pkm[pkm[f"{ind}_vs_kota"] == "di atas kota"].sort_values(f"{ind}_persen", ascending=False)
        top_p = pkm.nlargest(1, f"{ind}_persen").iloc[0]
        top_n = pkm.nlargest(1, f"{ind}_jumlah").iloc[0]
        teks = (f"**{NAMA[ind]}** — {len(atas)} dari {len(pkm)} Puskesmas {lingkup} bermakna di atas angka kota "
                f"({fmt_pct(ref[ind])})")
        teks += f": {_daftar(atas.puskesmas)}." if len(atas) else "."
        seri = pkm[pkm[f"{ind}_persen"] == top_p[f"{ind}_persen"]]
        if len(seri) > 1:
            teks += (f" Persentase tertinggi sama-sama {fmt_pct(top_p[f'{ind}_persen'])} di "
                     f"**{' dan '.join(seri.puskesmas)}**; kasus terbanyak di **{top_n.puskesmas}** "
                     f"({fmt_int(top_n[f'{ind}_jumlah'])} kasus).")
        elif top_p.puskesmas != top_n.puskesmas:
            teks += (f" Persentase tertinggi di **{top_p.puskesmas}** ({fmt_pct(top_p[f'{ind}_persen'])}), "
                     f"tetapi kasus terbanyak di **{top_n.puskesmas}** ({fmt_int(top_n[f'{ind}_jumlah'])} kasus).")
        else:
            teks += (f" **{top_p.puskesmas}** tertinggi baik persentase ({fmt_pct(top_p[f'{ind}_persen'])}) "
                     f"maupun jumlah kasus ({fmt_int(top_n[f'{ind}_jumlah'])}).")
        out.append(teks)
    if len(indikator) == 2:
        ganda = pkm[pkm.kategori_beban == "KEK & Anemia di atas kota"]
        beda = pkm[((pkm.kek_vs_kota == "di atas kota") & (pkm.anemia_vs_kota == "di bawah kota")) |
                   ((pkm.anemia_vs_kota == "di atas kota") & (pkm.kek_vs_kota == "di bawah kota"))]
        if len(ganda):
            out.append(f"**Beban ganda:** {_daftar(ganda.puskesmas)} — KEK dan Anemia sama-sama bermakna di atas kota.")
        if len(beda):
            contoh = "; ".join(f"{r.puskesmas} (KEK {fmt_pct(r.kek_persen, 1)}, Anemia {fmt_pct(r.anemia_persen, 1)})"
                               for _, r in beda.iterrows())
            out.append(f"**Arah berlawanan:** {contoh}. KEK dan Anemia adalah masalah gizi yang berbeda; "
                       "wilayah prioritasnya tidak selalu sama.")
    return out


def rekomendasi(pkm: pd.DataFrame, nilai: pd.DataFrame, status: pd.DataFrame) -> list[dict]:
    """Rekomendasi berbasis data. Setiap butir menyebut dasar datanya; tidak mengklaim penyebab."""
    rek = []
    ganda = pkm[pkm.kategori_beban == "KEK & Anemia di atas kota"]
    kek_saja = pkm[(pkm.kek_vs_kota == "di atas kota") & (pkm.anemia_vs_kota != "di atas kota")]
    an_saja = pkm[(pkm.anemia_vs_kota == "di atas kota") & (pkm.kek_vs_kota != "di atas kota")]
    beban = pkm.nlargest(3, "anemia_jumlah")

    if len(ganda):
        rek.append({"prioritas": "Tinggi", "judul": "Pendampingan gizi terpadu di Puskesmas beban ganda",
                    "dasar": f"{len(ganda)} Puskesmas memiliki KEK dan Anemia yang sama-sama bermakna di atas kota (2022): "
                             f"{_daftar(ganda.puskesmas, 10)}.",
                    "saran": "Jadikan wilayah ini prioritas pertama untuk verifikasi data lapangan, skrining LiLA dan Hb "
                             "pada kunjungan pertama, serta paket intervensi gizi ibu hamil yang menangani kedua masalah."})
    if len(kek_saja):
        rek.append({"prioritas": "Tinggi", "judul": "Fokus penanganan KEK",
                    "dasar": f"KEK bermakna di atas kota, tetapi Anemia tidak: {_daftar(kek_saja.puskesmas, 10)}.",
                    "saran": "Arahkan sumber daya penanganan KEK (mis. pemberian makanan tambahan ibu hamil KEK dan "
                             "konseling gizi) ke wilayah ini, tanpa harus menyamakan dengan program anemia."})
    if len(an_saja):
        rek.append({"prioritas": "Tinggi", "judul": "Telusuri kepatuhan konsumsi Tablet Tambah Darah (TTD)",
                    "dasar": f"Anemia bermakna di atas kota, tetapi KEK tidak: {_daftar(an_saja.puskesmas, 10)}. "
                             "Cakupan pemberian TTD dilaporkan 100% (Lampiran Profil 2021; Satu Data elemen 13474/13475 "
                             "untuk 2024–2025).",
                    "saran": "Karena cakupan *pemberian* sudah dilaporkan penuh, telusuri *kepatuhan konsumsi* TTD dan "
                             "pemeriksaan Hb ulang di wilayah ini. Data kepatuhan belum tersedia publik, sehingga ini "
                             "adalah pertanyaan untuk diverifikasi, bukan kesimpulan."})
    rek.append({"prioritas": "Sedang", "judul": "Bedakan target berbasis persentase dan beban layanan berbasis jumlah",
                "dasar": f"Kasus Anemia terbanyak 2022 ada di {_daftar(beban.puskesmas)}, namun peringkat jumlah dan "
                         "persentase hanya berkorelasi sedang (Spearman ≈ 0,7).",
                "saran": "Gunakan persentase untuk menentukan wilayah berisiko, dan jumlah kasus untuk "
                         "perencanaan logistik (stok PMT, TTD, tenaga gizi)."})
    if not pd.isna(nilai.at[2022, "ANEMIA_PREVALENSI"]) and not pd.isna(nilai.at[2024, "ANEMIA_PREVALENSI"]):
        rek.append({"prioritas": "Sedang", "judul": "Kaji penurunan tajam prevalensi Anemia 2022–2024",
                    "dasar": f"Prevalensi Anemia turun dari {fmt_pct(nilai.at[2022, 'ANEMIA_PREVALENSI'])} (2022) ke "
                             f"{fmt_pct(nilai.at[2024, 'ANEMIA_PREVALENSI'])} (2024); kasus dari "
                             f"{fmt_int(nilai.at[2022, 'ANEMIA_JUMLAH'])} ke {fmt_int(nilai.at[2024, 'ANEMIA_JUMLAH'])}.",
                    "saran": "Pastikan metode skrining (alat ukur Hb, trimester pemeriksaan, cakupan pemeriksaan) "
                             "tidak berubah sebelum penurunan ini disimpulkan sebagai keberhasilan program."})
    kp = nilai["KEK_PERSEN_TURUNAN"].dropna()
    rek.append({"prioritas": "Sedang", "judul": "KEK belum menunjukkan penurunan persentase",
                "dasar": f"% KEK berkisar {fmt_pct(kp.min())}–{fmt_pct(kp.max())} pada 2017–2024 "
                         f"({fmt_pct(kp.iloc[0])} → {fmt_pct(kp.iloc[-1])}), walau jumlah kasus turun bersama jumlah ibu hamil.",
                "saran": "Laporkan capaian KEK dalam bentuk persentase, bukan hanya jumlah kasus, agar penurunan "
                         "jumlah ibu hamil tidak terbaca sebagai perbaikan status gizi."})
    masalah = status.stack()
    n_masalah = int((masalah.isin(["tidak_valid", "perlu_perhatian"])).sum())
    rek.append({"prioritas": "Tata kelola data", "judul": "Perbaikan dan keterbukaan data",
                "dasar": f"{n_masalah} sel data kota ditandai tidak valid atau perlu perhatian (mis. persen KEK 2021–2022 "
                         "berisi jumlah kasus; jumlah Anemia 2023 sama dengan jumlah K1). Data per Puskesmas hanya "
                         "tersedia untuk 2022.",
                "saran": "Perbaiki elemen Satu Data 13476 dan 11709, terbitkan data KEK/Anemia per Puskesmas setiap "
                         "tahun dalam format CSV, dan samakan definisi antara Profil Kesehatan dan Satu Data."})
    return rek
