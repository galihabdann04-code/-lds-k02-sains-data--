# Panduan Deploy ke Streamlit Community Cloud

Panduan ini membawa proyek dari folder lokal menjadi **link publik** `https://<nama-app>.streamlit.app`.
Waktu yang dibutuhkan sekitar 15–20 menit. Gratis.

> **Catatan repo kelompok.** Proyek ini berada di folder `dashboard-gizi-bumil/` di repo kelompok
> `galihabdann04-code/-lds-k02-sains-data--` yang bersifat **privat**. Jika deploy dari repo ini:
> isi *Main file path* dengan `dashboard-gizi-bumil/app.py`, dan izinkan Streamlit mengakses repo privat
> saat diminta. Versi yang sedang live (https://gizi-bumil-semarang.streamlit.app) saat ini di-deploy dari
> salinan publik `shaulaputri-tech/dashboard-gizi-bumil-semarang`.

> Tampilan situs GitHub dan Streamlit bisa sedikit berbeda dari panduan ini karena keduanya terus
> diperbarui. Langkah intinya tetap sama.

---

## Langkah 0 — Persiapan

1. **Akun GitHub.** Daftar di https://github.com jika belum punya.
2. **Git terpasang** (hanya untuk Cara A di Langkah 2). Cek dengan menjalankan `git --version` di Terminal.
   - macOS: biasanya sudah ada. Jika belum, jalankan `xcode-select --install`.
   - Windows: unduh dari https://git-scm.com/download/win.
3. **(Disarankan) Uji di komputer sendiri dulu:**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
   Pastikan dashboard terbuka di `http://localhost:8501` tanpa pesan error.

### Daftar file yang WAJIB ikut ke GitHub
Tanpa file-file ini, aplikasi di cloud akan error:

| File/folder | Alasan |
|---|---|
| `app.py` | file utama yang dijalankan Streamlit |
| `src/` (termasuk `src/__init__.py`) | modul grafik, data, dan insight |
| `data/processed/` | data bersih yang dibaca dashboard |
| `data/geo/semarang_kecamatan.geojson` | batas kecamatan untuk peta |
| `requirements.txt` | daftar pustaka yang diinstal oleh cloud |
| `.streamlit/config.toml` | tema warna. Ini **folder tersembunyi**: di macOS Finder, tekan `Cmd + Shift + .` agar terlihat |

Folder `data/raw/`, `scripts/`, dan `reports/` tidak wajib untuk menjalankan aplikasi, tetapi
**disarankan ikut diunggah** supaya proyek bisa diaudit dan diulang. Total ukurannya sekitar 10 MB,
jauh di bawah batas GitHub.

---

## Langkah 1 — Buat repository di GitHub

1. Login ke GitHub, klik **+** di kanan atas, lalu pilih **New repository**.
2. Isi kolom berikut:
   - **Repository name:** misalnya `dashboard-gizi-bumil-semarang`
   - **Visibility:** **Public**. Ini cara paling sederhana. Repo private juga bisa, tetapi Streamlit perlu
     izin tambahan untuk mengaksesnya.
   - **Jangan** centang "Add a README", ".gitignore", atau "license", karena file-file itu sudah ada di proyek.
3. Klik **Create repository**, lalu salin URL repo, misalnya
   `https://github.com/<username>/dashboard-gizi-bumil-semarang.git`.

---

## Langkah 2 — Unggah proyek ke GitHub

### Cara A — lewat Terminal (disarankan)
Buka Terminal **di dalam folder proyek** (folder yang berisi `app.py`), lalu jalankan satu per satu:

```bash
git init
git add .
git commit -m "Dashboard status gizi ibu hamil Kota Semarang"
git branch -M main
git remote add origin https://github.com/<username>/dashboard-gizi-bumil-semarang.git
git push -u origin main
```

Saat `git push` meminta login, **password GitHub biasa tidak akan diterima**. Gunakan salah satu cara berikut:
- **GitHub CLI:** jalankan `gh auth login` lalu ikuti petunjuknya. Setelah itu ulangi `git push`.
- **Personal Access Token:** buka GitHub → Settings → Developer settings → Personal access tokens →
  buat token dengan akses `repo`. Saat diminta password, tempel token tersebut.

Periksa hasilnya: muat ulang halaman repo di GitHub. Folder `src/`, `data/`, `.streamlit/` dan file `app.py`
seharusnya sudah terlihat.

### Cara B — tanpa Terminal (GitHub Desktop)
1. Instal https://desktop.github.com dan login.
2. Pilih **File → Add local repository**, pilih folder proyek, lalu klik **create a repository** jika diminta.
3. Klik **Commit to main**, lalu **Publish repository**. Pada langkah ini **hapus centang "Keep this code private"** jika ingin repo publik.

> Hindari mengunggah lewat drag-and-drop di situs GitHub. Folder tersembunyi `.streamlit/` sering
> tertinggal, dan unggahan web dibatasi 100 file per kali unggah.

---

## Langkah 3 — Deploy di Streamlit Community Cloud

1. Buka **https://share.streamlit.io** dan klik **Continue with GitHub**. Izinkan Streamlit
   mengakses akun GitHub Anda.
2. Klik **Create app**. Jika muncul pilihan, pilih **Deploy a public app from GitHub**.
3. Isi formulir:
   | Kolom | Isi |
   |---|---|
   | Repository | `<username>/dashboard-gizi-bumil-semarang` |
   | Branch | `main` |
   | Main file path | `app.py` |
   | App URL (opsional) | subdomain pilihan Anda, misalnya `gizi-bumil-semarang` → `https://gizi-bumil-semarang.streamlit.app` |
4. Buka **Advanced settings** lalu pilih **Python version: 3.12**.
   Versi pustaka di `requirements.txt` sudah diuji dan kompatibel dengan Python 3.9–3.12.
   **Jangan pilih 3.13**, karena `numpy==2.0.2` tidak tersedia untuk 3.13.
   Kolom *Secrets* dibiarkan kosong karena proyek ini tidak memakai kunci API apa pun.
5. Klik **Deploy**.
6. Tunggu sekitar 2–5 menit. Log instalasi akan berjalan di panel kanan bawah. Setelah selesai,
   dashboard terbuka otomatis.

**🎉 Link publik Anda adalah URL di address bar**, misalnya `https://gizi-bumil-semarang.streamlit.app`.
Siapa pun bisa membukanya tanpa login.

---

## Langkah 4 — Cek setelah deploy

Buka link publik dan pastikan semua hal berikut berfungsi:
- [ ] Kartu metrik menampilkan angka 2024: K1 **18.338**, % KEK **6,67%**, Prevalensi Anemia **4,11%**.
- [ ] Tab **Peta & Wilayah 2022** menampilkan peta 16 kecamatan berwarna.
- [ ] Mengubah filter **Tahun** ke 2025 menampilkan label "Data tidak tersedia", bukan error.
- [ ] Memilih satu **Kecamatan** mempersempit grafik Puskesmas.
- [ ] Tombol **Unduh CSV** di tab Data & Metodologi berfungsi.

Setelah itu, salin link ke baris **Demo** di `README.md`, lalu commit dan push lagi.

---

## Memperbarui aplikasi

Setiap kali Anda melakukan `git push` ke branch `main`, Streamlit Cloud akan **memperbarui aplikasi secara
otomatis** dalam satu sampai dua menit:

```bash
git add .
git commit -m "Perbarui data / tampilan"
git push
```

Jika ada data resmi baru (misalnya Lampiran Profil 2023):
1. Simpan file mentahnya di `data/raw/`.
2. Sesuaikan dan jalankan ulang script di `scripts/`.
3. Commit file `data/processed/` yang baru, lalu push.

---

## Mengatasi masalah umum

| Gejala di log / layar | Penyebab | Solusi |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | folder `src/` atau `src/__init__.py` tidak ikut di-push | `git add src && git commit -m "add src" && git push` |
| `FileNotFoundError: ... data/processed/...` | folder data tidak ikut, atau huruf besar/kecil nama file berbeda (server cloud memakai Linux yang membedakan huruf besar dan kecil) | pastikan nama file persis sama dengan yang ada di `src/data.py` |
| `ModuleNotFoundError: No module named 'plotly'` | `requirements.txt` tidak berada di folder utama repo | pindahkan ke folder utama (sejajar dengan `app.py`) |
| Gagal instal `numpy` | Python 3.13 terpilih | buka **⋮ → Settings** lalu ubah versi Python (jika opsi tidak tersedia, hapus app dan deploy ulang dengan Python 3.12) |
| Tema warna tidak muncul | `.streamlit/config.toml` tidak ikut di-push | cek folder `.streamlit` di halaman repo GitHub |
| Muncul "This app has gone to sleep" | aplikasi gratis tidur jika lama tidak dikunjungi | klik **Yes, get this app back up!**, aplikasi aktif lagi dalam ±30 detik |
| Peta kosong, grafik lain normal | koneksi pengunjung ke server peta dasar (CARTO) terblokir | coba jaringan lain. Warna kecamatan tetap tampil karena berasal dari GeoJSON lokal |

Log lengkap bisa dilihat lewat tombol **Manage app** di pojok kanan bawah aplikasi yang sedang dibuka
(hanya terlihat oleh pemilik).

---

## Catatan keterbukaan data
Semua data di repo berasal dari publikasi resmi yang sudah terbuka untuk publik (Satu Data Kota Semarang,
Profil Kesehatan Dinkes, Geoportal Kota Semarang). Repo ini tidak memuat data pribadi atau data per individu.
Cantumkan sumber yang tertera di `README.md` setiap kali dashboard dibagikan.
