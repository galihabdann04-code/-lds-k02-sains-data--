# Keputusan dan Pertanyaan Analitik

> **Status: DRAF** — disusun dari pekerjaan dashboard gizi ibu hamil (Shaula Putri,
> [`dashboard-gizi-bumil/`](../dashboard-gizi-bumil/)). Pengguna, keputusan, dan pertanyaan perlu disepakati kelompok.

## Pengguna
Pengelola program gizi dan kesehatan ibu di **Dinas Kesehatan Kota Semarang** (seksi yang menangani kesehatan
keluarga dan gizi), yang membagi pendampingan ke 37 Puskesmas.

## Keputusan
Dinas Kesehatan Kota Semarang memutuskan **Puskesmas mana yang diprioritaskan untuk pendampingan gizi ibu hamil
(KEK dan Anemia, ditangani terpisah)** setiap awal tahun perencanaan program.

## Empat pertanyaan analitik

| Jenis | Pertanyaan | Progres |
|---|---|---|
| Deskriptif | Berapa persentase dan jumlah ibu hamil KEK dan Anemia di tiap Puskesmas/Kecamatan, dan bagaimana trennya di tingkat kota? | ✅ Terjawab di dashboard (tab Tren Kota, Peta & Wilayah 2022) |
| Diagnostik | Apakah Puskesmas dengan kasus terbanyak memang berisiko tinggi, atau hanya karena ibu hamilnya banyak? Apakah wilayah KEK tinggi juga Anemia tinggi? | 🟡 Sebagian: peringkat jumlah vs persen hanya berkorelasi sedang (ρ ≈ 0,7); KEK vs Anemia lemah (ρ = 0,38). Bersifat asosiatif, penyebab belum bisa dijawab dengan data yang ada |
| Prediktif | Berapa perkiraan persentase KEK dan Anemia tahun depan per Puskesmas? | ❌ Belum: data per Puskesmas hanya 1 tahun (2022) dan tren kota hanya 8 titik tahunan — belum cukup untuk prediksi yang layak |
| Preskriptif | Puskesmas mana yang perlu didahulukan untuk pendampingan KEK, untuk Anemia, atau keduanya, dengan sumber daya yang terbatas? | 🟡 Sebagian: dashboard memberi rekomendasi berbasis aturan (mis. 6 Puskesmas "beban ganda"), belum memakai batasan anggaran/tenaga nyata |

Satuan yang dipakai bersama oleh keempat pertanyaan: **Puskesmas per tahun**, dengan ukuran
**% ibu hamil** (kasus ÷ jumlah ibu hamil) dan **jumlah kasus**.

## Hasil uji dengan AI
⚠ _(Belum dilakukan. Tempel hasil saat AI diminta menandai pertanyaan yang tidak membantu keputusan, lalu apa yang diperbaiki.)_
