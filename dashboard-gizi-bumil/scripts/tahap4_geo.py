"""
Tahap 4 (persiapan peta) — unduh & bersihkan batas kecamatan resmi Kota Semarang.

Sumber: Geoportal Kota Semarang (Palapa), layer WFS `palapa:ADMINISTRASI_AR_KECAMATAN_25K`
        "Batas Administrasi Kecamatan", skala 1:25.000, metadata: "Data Distaru Kota Semarang".

Catatan validasi: pada layer ini atribut `WADMKC` TIDAK cocok dengan geometri
(mis. poligon Mijen diberi WADMKC "Semarang Timur"). Atribut `NAMOBJ` dan `KDCPUM`
konsisten dengan letak geografis (diverifikasi via centroid), sehingga keduanya yang dipakai.

Jalankan:  python scripts/tahap4_geo.py   (hanya butuh pustaka standar Python)
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = ("https://geoportal.semarangkota.go.id/geoserver/palapa/wfs?service=WFS&version=1.0.0"
       "&request=GetFeature&typeName=palapa:ADMINISTRASI_AR_KECAMATAN_25K&outputFormat=application/json")
RAW = ROOT / "data" / "raw" / "geoportal_semarang" / "ADMINISTRASI_AR_KECAMATAN_25K.geojson"
OUT = ROOT / "data" / "geo" / "semarang_kecamatan.geojson"
NAMA_BAKU = {"Gajah Mungkur": "Gajahmungkur"}  # samakan dengan nama baku Tahap 2


def bulatkan(coords):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], 5), round(coords[1], 5)]  # buang Z, presisi ~1 m
    return [bulatkan(c) for c in coords]


def main():
    RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not RAW.exists():
        with urllib.request.urlopen(URL, timeout=180) as r:
            RAW.write_bytes(r.read())
    src = json.loads(RAW.read_text(encoding="utf-8"))
    fitur = []
    for f in src["features"]:
        p = f["properties"]
        nama = NAMA_BAKU.get(p["NAMOBJ"], p["NAMOBJ"])
        fitur.append({
            "type": "Feature",
            "id": nama,
            "properties": {"kecamatan": nama, "kode_kemendagri": p["KDCPUM"], "kode_bps": p["KDCBPS"]},
            "geometry": {"type": f["geometry"]["type"], "coordinates": bulatkan(f["geometry"]["coordinates"])},
        })
    assert len(fitur) == 16, len(fitur)
    out = {"type": "FeatureCollection",
           "metadata": {"sumber": "Geoportal Kota Semarang — Batas Administrasi Kecamatan 1:25.000 (Distaru)",
                        "url": "https://geoportal.semarangkota.go.id/", "layer": "palapa:ADMINISTRASI_AR_KECAMATAN_25K"},
           "features": sorted(fitur, key=lambda x: x["properties"]["kode_kemendagri"])}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for f in out["features"]:
        print(f["properties"])
    print(f"{OUT} ({OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
