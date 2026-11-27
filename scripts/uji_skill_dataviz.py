"""
Uji skill `dataviz` (SKILL-TERPASANG.md): palet warna DENGAN skill vs TANPA skill.

- Dengan skill : 3 warna seri yang dipakai dashboard (slot kategorikal 1–3 dari panduan skill dataviz).
- Tanpa skill  : 3 warna bawaan Plotly (yang otomatis dipakai bila warna tidak diatur).

Ukuran yang dihitung (hanya numpy, bisa diulang):
- Jarak warna terdekat antar seri (ΔE OKLab × 100) untuk mata normal dan simulasi buta warna
  protanopia, deuteranopia, tritanopia (matriks Machado dkk. 2009, tingkat keparahan penuh).
  Panduan skill: ≥ 8 untuk buta warna, ≥ 15 untuk mata normal.
- Kontras terhadap latar dashboard #f7faf9 (rumus WCAG). Garis/titik grafik idealnya ≥ 3:1.

Jalankan: python scripts/uji_skill_dataviz.py
"""
import itertools

import numpy as np

DENGAN = {"biru": "#2a78d6", "oranye": "#eb6834", "hijau-tosca": "#1baf7a"}
TANPA = {"plotly-1": "#636efa", "plotly-2": "#ef553b", "plotly-3": "#00cc96"}
LATAR = "#f7faf9"

CVD = {
    "protanopia": np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]),
    "deuteranopia": np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]),
    "tritanopia": np.array([[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]),
}


def linear(hexwarna):
    c = np.array([int(hexwarna[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def oklab(lin):
    lms = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                    [0.2119034982, 0.6806995451, 0.1073969566],
                    [0.0883024619, 0.2817188376, 0.6299787005]]) @ np.clip(lin, 0, 1)
    lms = np.cbrt(lms)
    return np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                     [1.9779984951, -2.4285922050, 0.4505937099],
                     [0.0259040371, 0.7827717662, -0.8086757660]]) @ lms


def luminans(hexwarna):
    return float(np.dot([0.2126, 0.7152, 0.0722], linear(hexwarna)))


def kontras(a, b):
    la, lb = sorted([luminans(a), luminans(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def jarak_terdekat(palet, matriks=None):
    lab = {}
    for n, h in palet.items():
        lin = linear(h) if matriks is None else matriks @ linear(h)
        lab[n] = oklab(lin)
    return min((np.linalg.norm(lab[a] - lab[b]) * 100, a, b) for a, b in itertools.combinations(lab, 2))


def nilai(palet):
    hasil = {"normal": jarak_terdekat(palet)}
    for jenis, m in CVD.items():
        hasil[jenis] = jarak_terdekat(palet, m)
    hasil["kontras_min"] = min((kontras(h, LATAR), n) for n, h in palet.items())
    return hasil


def main():
    baris = []
    for label, palet in [("Dengan skill (dashboard)", DENGAN), ("Tanpa skill (bawaan Plotly)", TANPA)]:
        r = nilai(palet)
        cvd_min = min(r[j][0] for j in CVD)
        baris.append((label, r["normal"][0], cvd_min, r["kontras_min"][0]))
        print(f"\n{label}: {', '.join(palet.values())}")
        print(f"  ΔE terdekat mata normal : {r['normal'][0]:.1f} ({r['normal'][1]} vs {r['normal'][2]})")
        for j in CVD:
            print(f"  ΔE terdekat {j:<12}: {r[j][0]:.1f} ({r[j][1]} vs {r[j][2]})")
        print(f"  Kontras terendah vs latar: {r['kontras_min'][0]:.2f}:1 ({r['kontras_min'][1]})")
    print("\nRingkasan | ΔE normal | ΔE buta warna terburuk | kontras terendah")
    for label, n, c, k in baris:
        print(f"{label} | {n:.1f} | {c:.1f} | {k:.2f}:1")


if __name__ == "__main__":
    main()
