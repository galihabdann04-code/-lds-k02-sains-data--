# KENAPA KAMI (v1)

Pertanyaan v1: mengapa perlu sistem database dan analisis kelompok (**Belanja Hemat Bergizi Semarang**), padahal sudah ada dasbor pemantau harga pangan dari pemerintah?

> **Status: v1** — disusun untuk topik harga pangan harian Kota Semarang berdasarkan evaluasi langsung terhadap tiga platform pemantau harga pangan dan data daerah yang sudah ada.

## Alternatif yang sudah ada

| Alternatif | Biaya (sumber, tanggal cek) | Kelebihan | Kelemahan dan celah |
|---|---|---|---|
| Portal Satu Data Kota Semarang | Gratis (data.semarangkota.go.id, dicek 27 Nov 2026) | Resmi dikelola Pemkot Semarang, dataset bisa diunduh langsung (CSV/Excel), dan memuat indikator lokal Semarang | Tidak menyajikan pemantauan harga pangan eceran harian secara *real-time* maupun rekomendasi belanja praktis bagi konsumen (bukti: `00-admin/bukti/bukti-1-satu-data-semarang.png`) |
| Panel Harga Pangan (Bapanas) | Gratis (panelharga.badanpangan.go.id, dicek 27 Nov 2026) | Antarmuka visual mudah dibaca dan membandingkan harga aktual dengan Harga Acuan Penjualan (HAP) pemerintah | Agregasi hanya sampai level kota/kabupaten (tidak mendetail ke perilaku belanja harian konsumen di Semarang) dan tidak menjawab kapan hari terbaik belanja dalam seminggu (bukti: `00-admin/bukti/bukti-2-panel-harga-bapanas.png`) |
| SP2KP (Kementerian Perdagangan RI) | Gratis (sp2kp.kemendag.go.id, dicek 27 Nov 2026) | Memuat pantauan harga kebutuhan pokok harian resmi dan indikator fluktuasi harga lintas wilayah | Tidak menghubungkan data harga pangan dengan nilai gizi dasar maupun batas anggaran belanja mingguan ibu rumah tangga/anak kos (bukti: `00-admin/bukti/bukti-3-sp2kp-kemendag.png`) |

## Alasan sistem kami dibuat
1. **Menjembatani data makro ke keputusan mikro harian:** Platform pemerintah dirancang untuk memantau inflasi dan stabilitas pasokan, sedangkan sistem kami menerjemahkan data historis PIHPS Semarang (2018–2026) menjadi panduan belanja praktis bagi ibu rumah tangga dan anak kos.
2. **Menggabungkan aspek biaya dan gizi:** Sistem kami tidak hanya menampilkan harga termurah, tetapi menyusun kombinasi bahan pangan sumber karbohidrat, protein, dan serat yang paling ekonomis dalam satu anggaran mingguan.
3. **Sinyal waktu belanja berbasis pola historis:** Mengidentifikasi komoditas dengan volatilitas tertinggi dan pola hari/musim kenaikan harga agar pengguna tahu kapan waktu terbaik membeli atau menyetok bahan pangan.
4. **Proyeksi harga jangka pendek:** Memberikan gambaran perkiraan harga komoditas utama untuk minggu berikutnya sehingga pengguna dapat menyesuaikan rencana belanja sebelum harga melonjak.

## Kapan alternatif lebih baik
- Jika pengguna hanya ingin mengecek harga rata-rata nasional atau membandingkan harga antar provinsi di seluruh Indonesia secara *real-time*, **Panel Harga Bapanas** atau **SP2KP Kemendag** sudah mencukupi.
- Jika peneliti atau warga membutuhkan dataset statistik resmi Kota Semarang lintas sektor dalam format tabel mentah, **Portal Satu Data Kota Semarang** tetap menjadi rujukan utama.
