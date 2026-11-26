# Tahap 3 — Analisis Data Eksploratif

**Topik:** Status gizi ibu hamil Kota Semarang, dengan KEK dan Anemia sebagai dua indikator terpisah.
**Sifat analisis:** deskriptif. Korelasi dan perbedaan antarwilayah **tidak** ditafsirkan sebagai sebab-akibat.
**Grafik interaktif:** [tahap3_eda.html](tahap3_eda.html) · **Script:** [`scripts/tahap3_eda.py`](../scripts/tahap3_eda.py)

---

## 1. Tren tahunan level kota (Satu Data, 2017–2024)

| Tahun | Ibu hamil (K1) | Kasus KEK | % KEK *(turunan)* | Kasus Anemia | Prevalensi Anemia *(resmi)* |
|---|--:|--:|--:|--:|--:|
| 2017 | 28.758 | 1.979 | 6,88 | 4.006 | 18,34 ⚠ |
| 2018 | 26.131 | 1.493 | 5,71 | 4.718 | 17,24 ⚠ |
| 2019 | 25.655 | 1.331 | 5,19 | 4.026 | 15,05 ⚠ |
| 2020 | 25.981 | 881 | 3,39 | 4.030 | 15,05 ⚠ |
| 2021 | 23.075 | 1.721 | 7,46 | 2.962 | 12,84 |
| 2022 | 23.503 | 1.790 | 7,62 | 2.971 | 12,60 |
| 2023 | 21.375 | 1.237 | 5,79 | *tidak valid* | 8,80 |
| 2024 | 18.338 | 1.224 | 6,67 | 755 | 4,11 |

⚠ = ditandai "perlu perhatian" saat validasi di Tahap 2.

**Temuan:**
1. **Jumlah kasus dan persentase memberi gambaran yang berbeda.** Dari 2017 ke 2024, jumlah ibu hamil (K1) turun ke indeks 64, dan kasus KEK turun ke indeks 62. Artinya, penurunan kasus KEK hampir seluruhnya sejalan dengan berkurangnya jumlah ibu hamil. **Persentase KEK relatif datar** di kisaran 5–8% (6,88% → 6,67%). Kalau hanya melihat jumlah kasus, kesannya KEK "membaik", padahal persentasenya tidak banyak berubah.
2. **Titik terendah KEK ada di 2020 (3,39%).** Data yang tersedia tidak menjelaskan penyebabnya. Pada 2021 persentasenya kembali ke 7,46%.
3. **Anemia menurun tajam dan konsisten:** dari 18,34% (2017) menjadi 4,11% (2024). Kasusnya turun ke indeks 19, jauh lebih cepat daripada penurunan jumlah ibu hamil. Ada tiga catatan kehati-hatian:
   - Angka 2017–2020 tidak konsisten dengan hasil hitung kasus ÷ K1. Angka 2019 dan 2020 juga sama persis.
   - Penurunan 2022 → 2024 (12,6% → 4,1%, kasus 2.971 → 755) sangat curam dalam dua tahun. Data yang ada tidak bisa membedakan apakah ini penurunan nyata atau perubahan cara skrining/pencatatan.
   - Dashboard akan menampilkan peringatan pada titik-titik ini.
4. **Sejak 2023 kedua indikator mendekat.** Pada 2024, persentase KEK (6,67%) lebih tinggi daripada Anemia (4,11%), kebalikan dari 2017–2022.

## 2. Perbandingan antarwilayah 2022 (Tabel 32, 37 Puskesmas)

Angka kota dari Tabel 32: **KEK 8,18%**, **Anemia 13,46%** (n = 23.503 ibu hamil).

### 2a. Jumlah kasus vs persentase: peringkatnya berbeda
| | 5 terbanyak menurut **jumlah kasus** | 5 tertinggi menurut **persentase** |
|---|---|---|
| **KEK** | Bangetayu, Kedungmundu, Tlogosari Wetan, Bandarharjo, Mijen | Purwoyoso (18,3%), Karangdoro (16,6%), Bangetayu (15,3%), Poncol (13,7%), Pudak Payung (12,9%) |
| **Anemia** | Bangetayu, Kedungmundu, Tlogosari Wetan, Ngaliyan, Genuk | Bangetayu (32,9%), Purwoyoso (32,9%), Krobokan (28,0%), Poncol (26,6%), Karanganyar (25,9%) |

- Lima Puskesmas dengan kasus terbanyak menanggung **38,7% kasus KEK** dan **43,8% kasus Anemia**, padahal hanya melayani 31% dan 26% ibu hamil. Kasus Anemia lebih terkonsentrasi daripada KEK.
- Korelasi peringkat (Spearman) antara jumlah kasus dan persentase hanya 0,69 untuk KEK dan 0,74 untuk Anemia. Ada beberapa pergeseran peringkat yang besar:
  - **Poncol:** peringkat 20 menurut jumlah kasus KEK, tetapi peringkat 4 menurut persentase. Untuk Anemia, peringkat 17 menjadi 4.
  - **Tlogosari Wetan:** peringkat 3 menurut jumlah kasus Anemia, tetapi peringkat 17 menurut persentase. Wilayah ini punya banyak kasus karena ibu hamilnya banyak, bukan karena persentasenya tinggi.
  - **Tlogosari Kulon:** peringkat 7 menjadi 23 untuk KEK.
- Dashboard karena itu perlu bisa beralih antara tampilan **jumlah kasus** (beban layanan) dan **persentase** (risiko relatif).

### 2b. Mana yang berbeda bermakna dari angka kota? (selang kepercayaan Wilson 95%)
Puskesmas kecil punya angka persen yang tidak stabil. Contohnya Miroto, dengan hanya 166 ibu hamil, punya selang kepercayaan KEK 3,7–11,6%. Karena itu, sebuah wilayah dikategorikan "di atas kota" hanya jika **seluruh selang kepercayaannya** berada di atas angka kota.

| Indikator | Di atas kota | Tidak berbeda bermakna | Di bawah kota |
|---|--:|--:|--:|
| KEK | 9 | 14 | 14 |
| Anemia | 13 | 6 | 18 |

- **KEK di atas kota:** Poncol, Karangdoro, Krobokan, Genuk, Bangetayu, Kedungmundu, Padangsari, Pudak Payung, Purwoyoso.
- **Anemia di atas kota:** Poncol, Miroto, Lamper Tengah, Lebdosari, Manyaran, Krobokan, Genuk, Bangetayu, Kedungmundu, Rowosari, Purwoyoso, Ngaliyan, Karanganyar.
- **Keduanya di atas kota (6 Puskesmas):** Poncol, Krobokan, Genuk, Bangetayu, Kedungmundu, Purwoyoso.

### 2c. KEK dan Anemia tidak selalu searah
- Korelasi peringkat antara % KEK dan % Anemia hanya **0,38**, artinya hubungannya lemah.
- Contoh paling mencolok adalah **Karangdoro**: KEK-nya tertinggi ke-2 (16,6%), tetapi Anemia-nya termasuk yang terendah (3,9%, bermakna di bawah kota).
- **Mijen** memiliki Anemia terendah (3,1%) dengan KEK mendekati angka kota (8,0%).
- Ini mendukung keputusan untuk menyajikan KEK dan Anemia secara terpisah. Wilayah yang perlu diperhatikan untuk KEK belum tentu sama dengan wilayah untuk Anemia.
- Variasi Anemia antar-Puskesmas jauh lebih lebar (3,1–32,9%, rasio 10,6×) dibanding KEK (3,2–18,3%, rasio 5,8×).
- Ukuran Puskesmas (jumlah ibu hamil) hampir tidak berkaitan dengan % KEK (ρ = 0,08) dan hanya lemah berkaitan dengan % Anemia (ρ = −0,21).

### 2d. Level Kecamatan
| Kecamatan | Puskesmas | Ibu hamil | % KEK | % Anemia |
|---|--:|--:|--:|--:|
| Genuk | 2 | 2.217 | **13,98** | **30,67** |
| Semarang Tengah | 2 | 392 | 10,71 | 25,77 |
| Ngaliyan | 3 | 1.954 | 9,62 | 19,09 |
| Tembalang | 2 | 2.363 | 9,10 | 18,37 |
| Gayamsari | 1 | 924 | 8,98 | 6,49 |
| Semarang Timur | 3 | 1.129 | 8,50 | 8,06 |
| Tugu | 2 | 634 | 8,04 | 15,46 |
| Semarang Utara | 2 | 1.956 | 8,03 | 7,36 |
| Mijen | 2 | 1.359 | 7,95 | 3,61 |
| Pedurungan | 2 | 2.709 | 7,79 | 11,30 |
| Banyumanik | 4 | 2.044 | 7,63 | 8,61 |
| Candisari | 2 | 987 | 6,28 | 12,26 |
| Semarang Barat | 5 | 1.986 | 5,64 | 16,77 |
| Semarang Selatan | 2 | 654 | 5,05 | 12,69 |
| Gunungpati | 2 | 1.462 | 4,72 | 5,61 |
| Gajahmungkur | 1 | 733 | 3,96 | 4,37 |

- **Genuk** tertinggi untuk kedua indikator. Kecamatan ini berisi Bangetayu, Puskesmas dengan kasus KEK dan Anemia terbanyak di kota.
- Agregasi ke tingkat kecamatan **menutupi variasi di dalamnya**. Contohnya, di Semarang Barat, Krobokan bermakna di atas kota untuk KEK, sedangkan Karangayu, Lebdosari, dan Manyaran bermakna di bawah kota. Karena itu dashboard sebaiknya bisa menelusuri dari Kecamatan ke Puskesmas.

## 3. Keterbatasan yang wajib ditampilkan di dashboard
1. Data per wilayah hanya ada untuk **satu tahun (2022)**, sehingga tidak ada tren per Puskesmas.
2. Angka 2022 dari Tabel 32 (KEK 8,18%, Anemia 13,46%) **berbeda** dari Satu Data (7,62%, 12,60%) karena definisi pencatatannya berbeda. Kedua sumber tidak dicampur.
3. Persentase per wilayah dan % KEK kota adalah **nilai turunan** (kasus ÷ ibu hamil). Hanya prevalensi Anemia dan % KEK 2024 yang merupakan angka resmi.
4. Selang kepercayaan mengasumsikan setiap ibu hamil sebagai pengamatan independen. Tidak ada informasi tentang cakupan skrining LiLA/Hb per Puskesmas.
5. Semua temuan bersifat **asosiatif/deskriptif**. Faktor seperti sosial-ekonomi atau akses layanan tidak tersedia di data ini, sehingga tidak dianalisis.

## 4. Implikasi untuk desain dashboard (Tahap 4)
- **Kartu metrik:** % KEK dan prevalensi Anemia tahun terpilih, ditambah jumlah kasus, ditampilkan berdampingan tetapi terpisah.
- **Tombol "Jumlah kasus ↔ Persentase"** pada grafik wilayah.
- **Penanda status data** (⚠) pada titik tren yang bermasalah.
- **Grafik titik dengan CI** per Puskesmas, plus kategori "di atas / tidak berbeda / di bawah kota".
- **Scatter KEK vs Anemia** untuk menampilkan beban ganda.
- **Filter Tahun** yang otomatis membatasi tampilan wilayah hanya ke 2022.
