"""
Issue 4 — Pengambilan data mentah harga pangan harian Kota Semarang dari PIHPS Nasional (Bank Indonesia).

Sumber   : https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah
Filter   : Provinsi Jawa Tengah (id 14) → Kota Semarang (id 35), Pasar Tradisional (price_type_id 1),
           Laporan Harian (tipe_laporan 1), semua komoditas.
Keluaran : data/mentah/pihps_kota_semarang_<tahun>.json  — respons asli, TIDAK diubah
           data/mentah/pihps_kota_semarang_<tahun>.csv   — tabel lebar persis seperti respons (tanpa pembersihan)
           data/mentah/metadata_pengambilan.json         — parameter, waktu ambil, ringkasan

Data mentah tidak di-commit (aturan kelompok). Pembersihan dilakukan di Issue 5.

Jalankan : python scripts/ambil_data_pihps.py [tahun_awal] [tahun_akhir]
           (hanya pustaka standar Python; default 2018 s.d. tahun berjalan)
"""
import csv
import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "mentah"
URL = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataDaerah"
PARAM_TETAP = {
    "price_type_id": "1",   # Pasar Tradisional
    "comcat_id": "",        # kosong = semua komoditas
    "province_id": "14",    # Jawa Tengah
    "regency_id": "35",     # Kota Semarang
    "market_id": "",        # kosong = semua pasar di Kota Semarang
    "tipe_laporan": "1",    # Laporan Harian
}
JEDA_DETIK = 3


def ambil(mulai: str, selesai: str) -> dict:
    q = urllib.parse.urlencode({**PARAM_TETAP, "start_date": mulai, "end_date": selesai})
    req = urllib.request.Request(f"{URL}?{q}", headers={"User-Agent": "Mozilla/5.0 (tugas kuliah; data publik)"})
    for percobaan in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # jaringan / server sibuk
            print(f"  gagal ({e}), coba lagi...")
            time.sleep(10 * (percobaan + 1))
    raise RuntimeError(f"Gagal mengambil {mulai}..{selesai}")


def main():
    hari_ini = dt.date.today()
    awal = int(sys.argv[1]) if len(sys.argv) > 1 else 2018
    akhir = int(sys.argv[2]) if len(sys.argv) > 2 else hari_ini.year
    OUT.mkdir(parents=True, exist_ok=True)
    ringkas = []
    for th in range(awal, akhir + 1):
        mulai = f"{th}-01-01"
        selesai = min(dt.date(th, 12, 31), hari_ini).isoformat()
        print(f"Mengambil {mulai} .. {selesai}")
        respon = ambil(mulai, selesai)
        (OUT / f"pihps_kota_semarang_{th}.json").write_text(json.dumps(respon, ensure_ascii=False), encoding="utf-8")
        baris = respon.get("data", [])
        tanggal = [k for k in (baris[0] if baris else {}) if "/" in k]
        with open(OUT / f"pihps_kota_semarang_{th}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["no", "name", "level"] + tanggal)
            for b in baris:
                w.writerow([b.get("no"), b.get("name"), b.get("level")] + [b.get(t) for t in tanggal])
        terisi = sum(1 for b in baris for t in tanggal if b.get(t) not in (None, "", "-"))
        ringkas.append({"tahun": th, "baris_komoditas": len(baris), "jumlah_tanggal": len(tanggal),
                        "tanggal_pertama": tanggal[0] if tanggal else None,
                        "tanggal_terakhir": tanggal[-1] if tanggal else None,
                        "sel_terisi": terisi, "sel_total": len(baris) * len(tanggal)})
        print(f"  {len(baris)} baris komoditas × {len(tanggal)} tanggal, terisi {terisi}")
        time.sleep(JEDA_DETIK)
    meta = {"sumber": "PIHPS Nasional - Bank Indonesia",
            "halaman": "https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah",
            "endpoint": URL, "parameter": PARAM_TETAP,
            "diambil_pada": dt.datetime.now().isoformat(timespec="seconds"),
            "catatan": "Respons disimpan apa adanya. Angka memakai koma ribuan ('16,100'); '-' = tidak ada data. "
                       "Baris level 1 = kategori (rata-rata), level 2 = komoditas.",
            "ringkasan_per_tahun": ringkas}
    (OUT / "metadata_pengambilan.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Selesai →", OUT)


if __name__ == "__main__":
    main()
