# Bagian Mikail — draf siap tempel ke Google Docs

Tanda `{{...}}` = diisi dari **LembarFakta.txt** (cari dengan Ctrl+F).
Tanda `[PERLU DICEK]` = jangan dikumpulkan sebelum dihapus/diganti.

---

## COVER (isi yang kosong di Docs)

- Judul: **Rancangan Data Warehouse dan Dashboard Business Intelligence untuk Pemantauan Harga Pangan Strategis di 34 Provinsi Indonesia (Tingkat Produsen, Pasar Tradisional, dan Pasar Modern)**
  - Versi pendek: *Rancangan Data Warehouse dan Dashboard Pemantauan Harga Pangan Strategis Indonesia*
- Kelompok: 12
- Kelas: BI B
- Dosen Pengampu: Hafizah Hanim, M.Kom
- Oleh: Mikail — NIM [..] · Ikhsan — NIM [..] · Hanif — NIM [..]
- Tahun: 2026
- Nama file PDF: `BI B_12_Harga Pangan Strategis.pdf`

---

## A. ABSTRAK

Harga pangan strategis di Indonesia berubah setiap hari, berbeda antarprovinsi, dan berbeda antara tingkat produsen dan pasar konsumen, sehingga pengambil keputusan membutuhkan informasi yang ringkas untuk memantau kenaikan, fluktuasi, dan kesenjangan harga. Tugas ini bertujuan merancang solusi *Business Intelligence* yang menjawab enam pertanyaan bisnis, yaitu perbandingan harga antarprovinsi, fluktuasi harga komoditas, tren harga bulanan, kenaikan harga menjelang Idulfitri, kesenjangan harga antarwilayah, serta selisih harga dari produsen ke konsumen. Data yang digunakan berasal dari Pusat Informasi Harga Pangan Strategis (PIHPS) Nasional Bank Indonesia yang dihimpun di Kaggle, terdiri atas 30 file harga harian untuk 10 komoditas pada tiga jenis pasar (pasar tradisional, pasar modern, dan produsen) di 34 provinsi, periode 1 Januari 2022 sampai 12 Februari 2026. Metode yang digunakan meliputi analisis kelayakan data dengan *script* Python, analisis kebutuhan informasi, perancangan proses ETL, perancangan *data warehouse* dengan pendekatan dimensional Kimball, dan perancangan *dashboard*. Hasil analisis data menunjukkan bahwa data layak digunakan, dengan catatan berupa format data lebar, cakupan provinsi yang tidak seragam terutama pada tingkat produsen, serta 2.187 nilai ekstrem. Hasil perancangan berupa proses ETL yang mengubah data berformat lebar menjadi 1.354.641 baris fakta sekaligus menandai nilai ekstrem, skema bintang dengan tabel fakta `fact_harga_harian` pada grain harga per komoditas, jenis pasar, provinsi, dan tanggal beserta empat tabel dimensi (tanggal, komoditas, jenis pasar, dan provinsi), serta rancangan *dashboard* yang menampilkan peringkat harga antarprovinsi, tingkat fluktuasi komoditas, tren bulanan, kenaikan harga menjelang Idulfitri, dan perbandingan harga produsen dengan harga pasar.

**Kata kunci:** *business intelligence*, *data warehouse*, Kimball, ETL, harga pangan, PIHPS

---

## 1.1 JUSTIFIKASI

Topik harga pangan strategis dipilih karena harga pangan menyentuh kebutuhan dasar seluruh masyarakat dan termasuk kelompok harga bergejolak (*volatile food*) dalam pengukuran inflasi di Indonesia. Harga beras, cabai, atau bawang dapat berubah dalam hitungan hari dan berbeda antarwilayah, sehingga pemantauannya membutuhkan data yang rinci menurut waktu, komoditas, dan wilayah. Kebutuhan seperti ini sesuai dengan karakter *data warehouse* dan *Business Intelligence*, yaitu menyimpan data historis dalam jumlah besar lalu menyajikannya dari berbagai sudut pandang.

Dataset yang digunakan adalah *Indonesia PIHPS Food Commodity Prices Dataset* di Kaggle, yang berisi hasil pengumpulan (*scraping*) data dari PIHPS Nasional Bank Indonesia (https://www.bi.go.id/hargapangan). Berdasarkan pemeriksaan kelompok menggunakan *script* Python, dataset terdiri atas 30 file CSV dengan total 44.014 baris. Setiap file mewakili satu kombinasi dari 10 komoditas (bawang merah, bawang putih, beras, cabai merah, cabai rawit, daging ayam, daging sapi, gula pasir, minyak goreng, dan telur ayam) dan tiga jenis pasar (pasar tradisional, pasar modern, dan produsen). Setiap file memuat kolom tanggal (`Date_Param`) dan 34 kolom provinsi yang berisi harga. Data mencakup 1.493 tanggal dalam rentang 1 Januari 2022 sampai 12 Februari 2026. Setelah diubah ke bentuk satu baris per tanggal, provinsi, komoditas, dan jenis pasar, data berjumlah 1.354.641 baris harga.

Dataset ini dinilai layak digunakan karena tiga alasan. Pertama, **datanya multidimensi**: terdapat dimensi waktu (harian), komoditas, jenis pasar, dan provinsi, yang secara langsung membentuk skema bintang. Adanya harga tingkat produsen dan tingkat pasar juga memungkinkan analisis selisih harga dari produsen ke konsumen. Kedua, **rentang waktunya panjang**, lebih dari empat tahun, sehingga mencakup beberapa periode Ramadan dan Idulfitri untuk analisis pola musiman. Ketiga, **sumber aslinya adalah lembaga resmi**, yaitu Bank Indonesia, sehingga nilainya dapat diverifikasi terhadap situs PIHPS.

Kelompok juga mencatat beberapa keterbatasan. (1) Dataset diunggah oleh pengguna perorangan, bukan dirilis langsung oleh Bank Indonesia, dan berada dalam folder bernama `Cleaned_After_Imputation`, yang menandakan sebagian nilai sudah diisi (imputasi) oleh pengunggah sehingga tidak semuanya merupakan hasil pengamatan asli. (2) Data berformat lebar (provinsi sebagai kolom), sedangkan komoditas dan jenis pasar hanya tercantum pada nama file, sehingga perlu diubah bentuknya sebelum dimuat ke *data warehouse*. (3) Cakupan provinsi tidak seragam: terdapat 12 variasi susunan kolom di antara 30 file. Nilai kosong (3,39% sampai 33,92% per provinsi setelah digabung) seluruhnya berasal dari provinsi yang tidak tercatat pada file tertentu, bukan dari sel kosong di dalam file. Kekosongan terbesar ada di tingkat produsen: bawang putih hanya tercatat di 2 provinsi, gula pasir di 14 provinsi, dan minyak goreng di 15 provinsi, sedangkan DKI Jakarta tidak memiliki data produsen sama sekali. (4) Jumlah tanggal tidak sama antarjenis pasar: file pasar modern dan produsen memuat 1.493 tanggal, sedangkan file pasar tradisional hanya 1.415–1.417 tanggal. Secara keseluruhan terdapat 11 tanggal tanpa data dari 1.504 hari kalender. (5) Kolom tanggal tersimpan sebagai teks. (6) Terdapat 2.187 nilai yang tergolong ekstrem (di atas Q3 + 3×IQR dalam komoditas dan jenis pasar yang sama). Contoh paling mencolok adalah harga gula pasir di pasar modern Kalimantan Selatan yang mencapai Rp605.500 pada 28 Mei–4 Juni 2024, padahal median gula pasir di pasar modern hanya Rp16.700. Nilai sebelumnya naik bertahap sebesar Rp14.700 per hari (Rp502.600 pada 21 Mei hingga Rp590.800 pada 27 Mei), yang mengindikasikan nilai hasil interpolasi di sekitar satu kesalahan input. Nilai seperti ini harus ditandai dan ditangani pada tahap ETL. (7) Data mencakup 34 provinsi, sementara Indonesia saat ini memiliki 38 provinsi setelah pemekaran wilayah Papua, sehingga provinsi hasil pemekaran tidak tercatat terpisah. Di sisi lain, tidak ditemukan baris duplikat maupun harga bernilai nol atau negatif. Keterbatasan-keterbatasan tersebut ditangani pada rancangan ETL (subbab 1.3 A) dan tidak mengurangi kelayakan dataset untuk tujuan perancangan.

> Opsional tapi menguatkan (5 menit): cocokkan 2 harga acak dengan situs PIHPS, lalu tambahkan kalimat: "Pencocokan sampel terhadap situs PIHPS pada {{tanggal}} menunjukkan nilai yang {{sama/berbeda}}."

---

## 2. KESIMPULAN

Berdasarkan analisis dan perancangan yang dilakukan, kelompok menyimpulkan beberapa hal berikut.

1. Dataset harga pangan strategis PIHPS yang terdiri atas 30 file harga harian untuk 10 komoditas, tiga jenis pasar, dan 34 provinsi selama periode 1 Januari 2022 sampai 12 Februari 2026 layak digunakan sebagai dasar perancangan solusi *Business Intelligence*. Kualitas data perlu diperhatikan karena format data lebar, cakupan provinsi yang tidak seragam terutama pada tingkat produsen, data yang sebagian sudah diimputasi oleh pengunggah, dan adanya 2.187 nilai ekstrem.
2. Analisis kebutuhan informasi menghasilkan enam pertanyaan bisnis tentang perbandingan harga antarprovinsi, fluktuasi komoditas, tren bulanan, kenaikan harga menjelang Idulfitri, kesenjangan antarwilayah, dan selisih harga produsen–konsumen.
3. Proses ETL dirancang untuk mengubah data berformat lebar menjadi 1.354.641 baris fakta dengan mengambil komoditas dan jenis pasar dari nama file, mengubah kolom tanggal menjadi tipe tanggal, serta menandai dan menangani nilai ekstrem sebelum data dimuat.
4. *Data warehouse* dirancang dengan skema bintang pendekatan Kimball, terdiri atas tabel fakta `fact_harga_harian` pada grain harga per komoditas, jenis pasar, provinsi, dan tanggal, serta empat tabel dimensi. Grain ini memungkinkan analisis dari sudut pandang waktu, komoditas, jenis pasar, dan wilayah.
5. Rancangan *dashboard* menyajikan setiap pertanyaan bisnis dalam satu visual, sehingga pengguna dapat mengidentifikasi provinsi dan komoditas dengan harga tertinggi atau paling fluktuatif, mengantisipasi kenaikan harga menjelang Idulfitri, dan melihat selisih harga dari produsen ke konsumen sebagai bahan pengambilan keputusan pengendalian harga.

Pengembangan selanjutnya dapat berupa implementasi ETL dan *dashboard* secara nyata, verifikasi sampel data terhadap situs PIHPS, serta penambahan data pendukung seperti inflasi atau jumlah penduduk per provinsi dari BPS.

---

## 3. DAFTAR REFERENSI (APA 7)

Urutkan abjad. Tambahkan referensi dari Ikhsan & Hanif **hanya** kalau ada URL-nya.

- Bank Indonesia. (n.d.). *Pusat Informasi Harga Pangan Strategis Nasional (PIHPS Nasional)*. Diakses {{tanggal}}, dari https://www.bi.go.id/hargapangan
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- muhyusuf1112. (2026). *Indonesia PIHPS food commodity prices dataset* [Data set]. Kaggle. https://www.kaggle.com/datasets/muhyusuf1112/indonesia-commodity-price-based-piphs-source
