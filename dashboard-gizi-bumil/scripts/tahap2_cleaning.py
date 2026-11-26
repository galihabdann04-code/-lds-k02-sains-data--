"""
Tahap 2 — Validasi, pembersihan, dan penyeragaman wilayah.

Input  (data/raw/, diunduh pada Tahap 1, tidak diubah):
  - satudata_semarang/elemen_<id>.csv   : Portal Satu Data Kota Semarang (level kota)
  - profil_dinkes/LAMPIRAN_PROFIL_KES_2022_KOTA_SEMARANG.pdf : Tabel 32 (per Puskesmas)

Output:
  - data/processed/kota_tahunan.csv        : tren tahunan level kota (format long)
  - data/processed/puskesmas_2022.csv      : KEK & Anemia per Puskesmas 2022
  - data/processed/kecamatan_2022.csv      : agregasi per Kecamatan 2022
  - data/interim/tabel32_2022_lengkap.csv  : seluruh kolom Tabel 32 (audit trail)
  - data/reference/wilayah_semarang.csv    : daftar baku Kecamatan–Puskesmas
  - reports/tahap2_validasi.md             : laporan pemeriksaan otomatis

Prinsip: tidak ada imputasi/estimasi. Nilai yang tidak valid dikosongkan (NaN)
dan nilai aslinya tetap disimpan di kolom `nilai_asli` beserta alasannya.
Nilai turunan (rasio dari dua angka resmi) selalu diberi label `turunan`.

Jalankan:  pip install pandas pypdf  lalu  python scripts/tahap2_cleaning.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import numpy as np
import pandas as pd
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
REF = ROOT / "data" / "reference"
REPORTS = ROOT / "reports"

SATUDATA_URL = "https://data.semarangkota.go.id/datasektoral/detail/{}"
LAMPIRAN_2022_URL = (
    "https://profil-kesehatan.dinkes.semarangkota.go.id/upload/dataset/"
    "LAMPIRAN%20PROFIL%20KES%202022%20KOTA%20SEMARANG.pdf"
)

# id elemen Satu Data -> (kode indikator, kelompok, satuan, definisi resmi)
ELEMEN = {
    11707: ("KEK_JUMLAH", "KEK", "orang", "Ibu hamil dengan LiLA < 23,5 cm"),
    13476: ("KEK_PERSEN", "KEK", "%", "Persentase ibu hamil yang termasuk KEK"),
    11709: ("ANEMIA_JUMLAH", "Anemia", "orang", "Ibu hamil dengan Hb < 11 g/dl"),
    12282: ("ANEMIA_PREVALENSI", "Anemia", "%", "Prevalensi anemia ibu hamil (Hb < 11,0 g/dl saat kunjungan)"),
    13493: ("BUMIL_JUMLAH", "Sasaran", "orang", "Jumlah ibu hamil di kabupaten/kota"),
    11703: ("BUMIL_K1", "Sasaran", "orang", "Jumlah ibu hamil melakukan K1"),
    11704: ("BUMIL_K4", "Sasaran", "orang", "Jumlah ibu hamil melakukan K4"),
}

# ---------------------------------------------------------------- wilayah
KECAMATAN_BAKU = {
    "smg tengah": "Semarang Tengah", "smg utara": "Semarang Utara",
    "smg timur": "Semarang Timur", "smg selatan": "Semarang Selatan",
    "smg barat": "Semarang Barat", "gayamsari": "Gayamsari",
    "candisari": "Candisari", "gajahmungkur": "Gajahmungkur",
    "genuk": "Genuk", "pedurungan": "Pedurungan", "tembalang": "Tembalang",
    "banyumanik": "Banyumanik", "gunungpati": "Gunungpati", "mijen": "Mijen",
    "ngaliyan": "Ngaliyan", "tugu": "Tugu",
}
PUSKESMAS_ALIAS = {  # singkatan di dokumen sumber -> nama baku
    "ngemplak s": "Ngemplak Simongan",
    "lamper tgh": "Lamper Tengah",
}


def baku_kecamatan(nama: str) -> str:
    key = re.sub(r"\s+", " ", nama.strip().lower()).replace("semarang ", "smg ")
    if key not in KECAMATAN_BAKU:
        raise ValueError(f"Kecamatan tidak dikenal: {nama!r}")
    return KECAMATAN_BAKU[key]


def baku_puskesmas(nama: str) -> str:
    key = re.sub(r"\s+", " ", nama.strip().lower())
    return PUSKESMAS_ALIAS.get(key, nama.strip().title())


# ---------------------------------------------------------- Satu Data kota
def baca_satudata() -> pd.DataFrame:
    rows = []
    for eid, (kode, kelompok, satuan, definisi) in ELEMEN.items():
        # CSV portal tidak mengutip teks: "Lila < 23,5 Cm" memecah kolom Keterangan.
        # Karena itu kolom diselaraskan dari KANAN (tahun..., OPD, KELOMPOK, URUSAN).
        with open(RAW / "satudata_semarang" / f"elemen_{eid}.csv", encoding="utf-8") as f:
            header = next(csv.reader(f))
            baris = next(csv.reader(f))
        n_kanan = len(header) - header.index("Satuan") - 1
        nilai_kanan = dict(zip(header[-n_kanan:], baris[-n_kanan:]))
        tahun_cols = [c for c in header if re.fullmatch(r"\d{4}", c)]
        for th in tahun_cols:
            v = pd.to_numeric(nilai_kanan[th]) if nilai_kanan[th].strip() else np.nan
            rows.append({
                "tahun": int(th), "indikator": kode, "kelompok": kelompok,
                "satuan": satuan, "definisi": definisi,
                "nilai_asli": None if pd.isna(v) else float(v),
                "sumber": f"Satu Data Kota Semarang (elemen {eid})",
                "sumber_url": SATUDATA_URL.format(eid),
            })
    return pd.DataFrame(rows)


def validasi_kota(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["nilai"] = df["nilai_asli"]
    df["jenis_nilai"] = "resmi"
    df["status"] = "valid"
    df["catatan"] = ""

    def tandai(mask, status, catatan, kosongkan=True):
        df.loc[mask, "status"] = status
        df.loc[mask, "catatan"] = catatan
        if kosongkan:
            df.loc[mask, "nilai"] = np.nan

    # 1) sel kosong
    tandai(df["nilai_asli"].isna(), "tidak_tersedia", "Sel kosong di sumber")
    # 2) angka 0 pada indikator jumlah = belum diisi (2016 di semua seri)
    tandai((df["nilai_asli"] == 0) & (df["satuan"] == "orang"), "tidak_tersedia",
           "Bernilai 0 di sumber; diperlakukan sebagai data tidak tersedia, bukan nol kasus")
    # 3) indikator persen berisi angka > 100
    tandai((df["satuan"] == "%") & (df["nilai_asli"] > 100), "tidak_valid",
           "Satuan % tetapi nilainya > 100 (berisi jumlah kasus, sama dengan elemen 11707)")

    piv = df.pivot_table(index="tahun", columns="indikator", values="nilai_asli")

    # 4) jumlah anemia identik dengan jumlah K1 tahun yang sama -> salah input
    for th in piv.index:
        a, k1 = piv.loc[th].get("ANEMIA_JUMLAH"), piv.loc[th].get("BUMIL_K1")
        if pd.notna(a) and pd.notna(k1) and a == k1 and a > 0:
            tandai((df["tahun"] == th) & (df["indikator"] == "ANEMIA_JUMLAH"), "tidak_valid",
                   f"Nilai ({a:,.0f}) identik dengan jumlah K1 tahun {th}; "
                   f"tidak konsisten dengan prevalensi resmi {piv.loc[th].get('ANEMIA_PREVALENSI')}%")

    # 5) prevalensi anemia resmi vs (jumlah anemia / K1) -> tandai bila selisih > 0,5 poin
    for th in piv.index:
        p = piv.loc[th].get("ANEMIA_PREVALENSI")
        a, k1 = piv.loc[th].get("ANEMIA_JUMLAH"), piv.loc[th].get("BUMIL_K1")
        if pd.notna(p) and pd.notna(a) and pd.notna(k1) and a > 0 and a != k1:
            hitung = a / k1 * 100
            if abs(hitung - p) > 0.5:
                m = (df["tahun"] == th) & (df["indikator"] == "ANEMIA_PREVALENSI")
                tandai(m, "perlu_perhatian",
                       f"Tidak konsisten: jumlah anemia/K1 = {hitung:.2f}% vs resmi {p}%",
                       kosongkan=False)

    # 6) prevalensi yang sama persis dua tahun berturut-turut
    prev = piv.get("ANEMIA_PREVALENSI").dropna().sort_index()
    for th in prev.index[1:]:
        if prev.get(th - 1) == prev[th]:
            for t in (th - 1, th):
                m = (df["tahun"] == t) & (df["indikator"] == "ANEMIA_PREVALENSI")
                tambahan = f"Nilai sama persis dengan tahun {th if t != th else th - 1} ({prev[th]}%)"
                df.loc[m, "status"] = "perlu_perhatian"
                df.loc[m, "catatan"] = (df.loc[m, "catatan"] + "; " + tambahan).str.strip("; ")

    # 6b) dua seri berbeda yang bernilai identik pada tahun yang sama
    for a_ind, b_ind, ket in [("BUMIL_K4", "BUMIL_K1", "K4 identik dengan K1 (retensi 100%)"),
                              ("BUMIL_JUMLAH", "BUMIL_K4", "Jumlah ibu hamil identik dengan K4")]:
        for th in piv.index:
            a, b = piv.loc[th].get(a_ind), piv.loc[th].get(b_ind)
            if pd.notna(a) and pd.notna(b) and a == b and a > 0:
                m = (df["tahun"] == th) & (df["indikator"] == a_ind) & (df["status"] == "valid")
                tandai(m, "perlu_perhatian", f"{ket} pada {th} ({a:,.0f}); kemungkinan disalin antar-seri",
                       kosongkan=False)

    # 7) indikator turunan: % KEK = jumlah KEK (LiLA<23,5) / K1 x 100
    #    (penyebut K1 dipakai karena sama dengan metode prevalensi anemia resmi,
    #     dan menghasilkan persis 6,67% untuk 2024 = nilai resmi elemen 13476)
    bersih = df.pivot_table(index="tahun", columns="indikator", values="nilai")
    turunan = []
    for th in bersih.index:
        kek, k1 = bersih.loc[th].get("KEK_JUMLAH"), bersih.loc[th].get("BUMIL_K1")
        if pd.notna(kek) and pd.notna(k1):
            turunan.append({
                "tahun": th, "indikator": "KEK_PERSEN_TURUNAN", "kelompok": "KEK",
                "satuan": "%", "definisi": "Jumlah bumil LiLA < 23,5 cm / jumlah bumil K1 x 100",
                "nilai_asli": np.nan, "nilai": round(kek / k1 * 100, 2),
                "jenis_nilai": "turunan", "status": "valid",
                "catatan": "Dihitung dari elemen 11707 dan 11703",
                "sumber": "Turunan dari Satu Data Kota Semarang (11707/11703)",
                "sumber_url": SATUDATA_URL.format(11707),
            })
    df = pd.concat([df, pd.DataFrame(turunan)], ignore_index=True)
    kolom = ["tahun", "kelompok", "indikator", "nilai", "satuan", "jenis_nilai",
             "status", "catatan", "nilai_asli", "definisi", "sumber", "sumber_url"]
    return df[kolom].sort_values(["kelompok", "indikator", "tahun"]).reset_index(drop=True)


# ------------------------------------------------- Tabel 32 Lampiran 2022
KOLOM_T32 = [
    "jumlah_bumil", "perkiraan_bumil_komplikasi", "komplikasi_ditangani_jumlah",
    "komplikasi_ditangani_persen", "kek", "anemia", "perdarahan", "tuberkulosis",
    "malaria", "infeksi_lainnya", "preeklampsia_eklampsia", "diabetes_melitus",
    "jantung", "covid19", "penyebab_lainnya", "komplikasi_kehamilan",
    "komplikasi_persalinan", "komplikasi_nifas",
]  # urutan diverifikasi visual dari render halaman 48 PDF


def ekstrak_tabel32() -> tuple[pd.DataFrame, dict]:
    pdf = PdfReader(RAW / "profil_dinkes" / "LAMPIRAN_PROFIL_KES_2022_KOTA_SEMARANG.pdf")
    halaman = None
    for i, p in enumerate(pdf.pages):
        t = p.extract_text() or ""
        if "KOMPLIKASI KEBIDANAN" in t and "KURANG" in t and "ANEMIA" in t and "Poncol" in t:
            halaman, teks = i + 1, t
            break
    if halaman is None:
        raise RuntimeError("Tabel 32 tidak ditemukan di PDF")

    pola = re.compile(r"^(?:(\d+)\s+(.+?)\s+)?(\d+)\.\s+(.+?)\s+([\d,.]+(?:\s+[\d,.]+){17})$")
    rows, kec, total = [], None, None
    for line in teks.splitlines():
        line = line.strip()
        if line.startswith("JUMLAH (KAB/KOTA)"):
            total = [float(x.replace(",", "")) for x in line.split()[2:]]
            continue
        m = pola.match(line)
        if not m:
            continue
        if m.group(2):
            kec = m.group(2)
        nilai = [float(x.replace(",", "")) for x in m.group(5).split()]
        rows.append({"no_puskesmas": int(m.group(3)), "kecamatan_sumber": kec,
                     "puskesmas_sumber": m.group(4), **dict(zip(KOLOM_T32, nilai))})
    df = pd.DataFrame(rows)
    return df, {"halaman": halaman, "total": dict(zip(KOLOM_T32, total))}


def main() -> None:
    for d in (OUT, INTERIM, REF, REPORTS):
        d.mkdir(parents=True, exist_ok=True)
    laporan: list[str] = []

    # ---------- level kota
    kota = validasi_kota(baca_satudata())
    kota.to_csv(OUT / "kota_tahunan.csv", index=False)

    # ---------- per puskesmas 2022
    t32, meta = ekstrak_tabel32()
    t32["kecamatan"] = t32["kecamatan_sumber"].map(baku_kecamatan)
    t32["puskesmas"] = t32["puskesmas_sumber"].map(baku_puskesmas)
    t32.insert(0, "tahun", 2022)
    t32.to_csv(INTERIM / "tabel32_2022_lengkap.csv", index=False)

    cek = []
    for col in ["jumlah_bumil", "kek", "anemia"]:
        s, t = t32[col].sum(), meta["total"][col]
        cek.append((col, s, t, s == t))
    jumlah_ok = all(c[3] for c in cek)
    assert len(t32) == 37, f"Jumlah puskesmas {len(t32)} != 37"
    assert t32["kecamatan"].nunique() == 16
    assert t32["puskesmas"].is_unique
    assert jumlah_ok, f"Total tidak cocok: {cek}"

    pkm = t32[["tahun", "kecamatan", "puskesmas", "jumlah_bumil", "kek", "anemia"]].copy()
    pkm = pkm.rename(columns={"kek": "kek_jumlah", "anemia": "anemia_jumlah"})
    for col in ["jumlah_bumil", "kek_jumlah", "anemia_jumlah"]:
        pkm[col] = pkm[col].astype(int)
    pkm["kek_persen"] = (pkm["kek_jumlah"] / pkm["jumlah_bumil"] * 100).round(2)
    pkm["anemia_persen"] = (pkm["anemia_jumlah"] / pkm["jumlah_bumil"] * 100).round(2)
    pkm["jenis_persen"] = "turunan (kasus / jumlah ibu hamil x 100)"
    pkm["sumber"] = f"Lampiran Profil Kesehatan Kota Semarang 2022, Tabel 32, hlm. {meta['halaman']}"
    pkm["sumber_url"] = LAMPIRAN_2022_URL
    pkm.to_csv(OUT / "puskesmas_2022.csv", index=False)

    kec = (pkm.groupby(["tahun", "kecamatan"], as_index=False)
              .agg(jumlah_puskesmas=("puskesmas", "count"), jumlah_bumil=("jumlah_bumil", "sum"),
                   kek_jumlah=("kek_jumlah", "sum"), anemia_jumlah=("anemia_jumlah", "sum")))
    # persen dihitung ulang dari jumlah agregat, BUKAN rata-rata persen puskesmas
    kec["kek_persen"] = (kec["kek_jumlah"] / kec["jumlah_bumil"] * 100).round(2)
    kec["anemia_persen"] = (kec["anemia_jumlah"] / kec["jumlah_bumil"] * 100).round(2)
    kec["sumber"] = pkm["sumber"].iloc[0]
    kec.to_csv(OUT / "kecamatan_2022.csv", index=False)

    ref = t32[["kecamatan", "puskesmas", "kecamatan_sumber", "puskesmas_sumber"]].copy()
    ref.to_csv(REF / "wilayah_semarang.csv", index=False)

    # ---------- laporan
    laporan += ["# Laporan Validasi Tahap 2", "",
                "Dihasilkan otomatis oleh `scripts/tahap2_cleaning.py`.", "",
                "## A. Data level kota (Satu Data Kota Semarang)", "",
                "| Status | Jumlah sel |", "|---|--:|"]
    for s, n in kota["status"].value_counts().items():
        laporan.append(f"| {s} | {n} |")
    laporan += ["", "### Sel yang tidak valid / perlu perhatian", "",
                "| Tahun | Indikator | Nilai asli | Status | Catatan |", "|---|---|--:|---|---|"]
    bermasalah = kota[kota["status"].isin(["tidak_valid", "perlu_perhatian"])]
    for _, r in bermasalah.sort_values(["indikator", "tahun"]).iterrows():
        laporan.append(f"| {r.tahun} | {r.indikator} | {r.nilai_asli:g} | {r.status} | {r.catatan} |")
    laporan += ["", "### Tabel bersih (nilai yang dipakai dashboard)", ""]
    piv = kota.pivot_table(index="indikator", columns="tahun", values="nilai")
    laporan.append("| Indikator | " + " | ".join(str(c) for c in piv.columns) + " |")
    laporan.append("|---|" + "--:|" * len(piv.columns))
    for ind, r in piv.iterrows():
        sel = ["" if pd.isna(v) else (f"{v:,.2f}" if "PERSEN" in ind or "PREVALENSI" in ind else f"{v:,.0f}")
               for v in r]
        laporan.append(f"| {ind} | " + " | ".join(sel) + " |")
    laporan += ["", "_Sel kosong = tidak tersedia atau tidak valid (lihat catatan)._", "",
                "## B. Data per Puskesmas 2022 (Lampiran Profil Kesehatan, Tabel 32)", "",
                f"- Halaman PDF terdeteksi: {meta['halaman']}",
                f"- Jumlah Puskesmas: {len(t32)} | Jumlah Kecamatan: {t32['kecamatan'].nunique()}",
                "", "| Kolom | Jumlah baris | Baris JUMLAH di PDF | Cocok |", "|---|--:|--:|---|"]
    for col, s, t, ok in cek:
        laporan.append(f"| {col} | {s:,.0f} | {t:,.0f} | {'✅' if ok else '❌'} |")
    tp = meta["total"]["komplikasi_ditangani_persen"]
    hitung = meta["total"]["komplikasi_ditangani_jumlah"] / meta["total"]["perkiraan_bumil_komplikasi"] * 100
    laporan += ["", f"- Catatan sumber: baris JUMLAH kolom '% ditangani' tertulis {tp:,.0f} "
                f"(seharusnya {hitung:.1f}%). Kolom ini tidak dipakai dashboard.",
                "- Judul tabel di PDF tertulis 'TAHUN 0.00' (galat template); tahun 2022 dipastikan "
                "dari nama berkas dan jumlah ibu hamil (23.503) = K1 2022 di Satu Data.", "",
                "### Penyeragaman nama wilayah", "", "| Nama di sumber | Nama baku |", "|---|---|"]
    for _, r in ref.iterrows():
        if r.kecamatan_sumber != r.kecamatan or r.puskesmas_sumber != r.puskesmas:
            laporan.append(f"| {r.kecamatan_sumber} / {r.puskesmas_sumber} | {r.kecamatan} / {r.puskesmas} |")
    laporan += ["", "## C. Perbandingan antar-sumber tahun 2022", "",
                "| Indikator | Satu Data (kota) | Tabel 32 (Σ Puskesmas) | Selisih |", "|---|--:|--:|--:|"]
    sd = kota[(kota.tahun == 2022)].set_index("indikator")["nilai"]
    for nama, a, b in [("KEK (jumlah)", sd.get("KEK_JUMLAH"), pkm.kek_jumlah.sum()),
                       ("Anemia (jumlah)", sd.get("ANEMIA_JUMLAH"), pkm.anemia_jumlah.sum()),
                       ("Ibu hamil / K1", sd.get("BUMIL_K1"), pkm.jumlah_bumil.sum())]:
        laporan.append(f"| {nama} | {a:,.0f} | {b:,.0f} | {b - a:+,.0f} |")
    laporan += ["", "Kedua sumber **tidak digabung**: Tabel 32 mencatat KEK/Anemia sebagai "
                "*komplikasi kebidanan*, sedangkan Satu Data memakai definisi LiLA < 23,5 cm / Hb < 11 g/dl. "
                "Dashboard menampilkan masing-masing dengan label sumbernya.", ""]
    (REPORTS / "tahap2_validasi.md").write_text("\n".join(laporan), encoding="utf-8")
    print("\n".join(laporan))


if __name__ == "__main__":
    main()
