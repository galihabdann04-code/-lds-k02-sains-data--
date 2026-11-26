"""Pemuatan data bersih (hasil Tahap 2–3) dan utilitas format angka."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
GEO = ROOT / "data" / "geo" / "semarang_kecamatan.geojson"

TAHUN_WILAYAH = 2022  # satu-satunya tahun dengan data KEK/Anemia per Puskesmas
NAMA = {"kek": "KEK", "anemia": "Anemia"}
LABEL_PANJANG = {"kek": "Kurang Energi Kronis (KEK)", "anemia": "Anemia"}

SUMBER = {
    "satudata": ("Portal Satu Data Kota Semarang — Dinas Kesehatan",
                 "https://data.semarangkota.go.id/opendata?cari=hamil"),
    "lampiran2022": ("Lampiran Profil Kesehatan Kota Semarang 2022, Tabel 32 — Dinas Kesehatan",
                     "https://profil-kesehatan.dinkes.semarangkota.go.id/upload/dataset/"
                     "LAMPIRAN%20PROFIL%20KES%202022%20KOTA%20SEMARANG.pdf"),
    "geoportal": ("Geoportal Kota Semarang — Batas Administrasi Kecamatan 1:25.000 (Distaru)",
                  "https://geoportal.semarangkota.go.id/"),
}


# ------------------------------------------------------------------ format
def fmt_int(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:,.0f}".replace(",", ".")


def fmt_pct(v, d: int = 2) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:.{d}f}%".replace(".", ",")


def fmt_num(v, d: int = 2) -> str:
    return "—" if v is None or pd.isna(v) else f"{v:.{d}f}".replace(".", ",")


def wilson(x, n, z: float = 1.96):
    x, n = np.asarray(x, float), np.asarray(n, float)
    p = x / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return (c - h) * 100, (c + h) * 100


# ------------------------------------------------------------------ loaders
@st.cache_data
def kota() -> pd.DataFrame:
    return pd.read_csv(PROC / "kota_tahunan.csv")


@st.cache_data
def kota_wide() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Nilai bersih per tahun (kolom = indikator) + status per sel."""
    k = kota()
    nilai = k.pivot_table(index="tahun", columns="indikator", values="nilai")
    status = k.pivot(index="tahun", columns="indikator", values="status")
    catatan = k.pivot(index="tahun", columns="indikator", values="catatan")
    tahun = sorted(k["tahun"].unique())
    return (nilai.reindex(tahun), status.reindex(tahun), catatan.reindex(tahun))


@st.cache_data
def puskesmas() -> pd.DataFrame:
    return pd.read_csv(PROC / "eda_puskesmas_2022.csv")


@st.cache_data
def kota_2022_tabel32() -> dict:
    p = puskesmas()
    n = p["jumlah_bumil"].sum()
    return {"n": int(n), "kek": p["kek_jumlah"].sum() / n * 100, "anemia": p["anemia_jumlah"].sum() / n * 100,
            "kek_jumlah": int(p["kek_jumlah"].sum()), "anemia_jumlah": int(p["anemia_jumlah"].sum())}


@st.cache_data
def kecamatan() -> pd.DataFrame:
    k = pd.read_csv(PROC / "kecamatan_2022.csv")
    ref = kota_2022_tabel32()
    for ind in ("kek", "anemia"):
        lo, hi = wilson(k[f"{ind}_jumlah"], k["jumlah_bumil"])
        k[f"{ind}_ci_bawah"], k[f"{ind}_ci_atas"] = lo.round(2), hi.round(2)
        k[f"{ind}_vs_kota"] = np.select([lo > ref[ind], hi < ref[ind]],
                                        ["di atas kota", "di bawah kota"], "tidak berbeda bermakna")
    geo = geojson()
    kode = {f["id"]: f["properties"]["kode_kemendagri"] for f in geo["features"]}
    k["kode_kemendagri"] = k["kecamatan"].map(kode)
    return k


@st.cache_data
def geojson() -> dict:
    return json.loads(GEO.read_text(encoding="utf-8"))


def daftar_kecamatan() -> list[str]:
    return sorted(puskesmas()["kecamatan"].unique())
