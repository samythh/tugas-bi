# Bagian Mikail — draf siap tempel ke Google Docs

Tanda `{{...}}` = diisi dari **LembarFakta.txt** (cari dengan Ctrl+F).
Tanda `[PERLU DICEK]` = jangan dikumpulkan sebelum dihapus/diganti.

---

## COVER (isi yang kosong di Docs)

- Judul: **Rancangan Data Warehouse dan Dashboard Business Intelligence Harga Pangan Strategis Indonesia Berbasis Data PIHPS**
- Kelompok: 12
- Dosen Pengampu: [PERLU DICEK]
- Oleh: Mikail — NIM [..] · Ikhsan — NIM [..] · Hanif — NIM [..]
- Tahun: 2026
- Nama file PDF: `[Kode Kelas]_12_Harga Pangan Strategis.pdf`

---

## A. ABSTRAK  *(ditulis TERAKHIR, setelah bagian Ikhsan & Hanif masuk)*

Harga pangan strategis di Indonesia berubah setiap hari, berbeda antarprovinsi, dan berbeda antara tingkat produsen dan pasar konsumen, sehingga pengambil keputusan membutuhkan informasi ringkas untuk memantau kenaikan, fluktuasi, dan kesenjangan harga. Tugas ini bertujuan merancang solusi *Business Intelligence* yang menjawab enam pertanyaan bisnis tentang perbandingan harga antarprovinsi, fluktuasi komoditas, tren bulanan, kenaikan harga menjelang Idulfitri, kesenjangan antarwilayah, dan selisih harga produsen–konsumen. Data yang digunakan berasal dari Pusat Informasi Harga Pangan Strategis (PIHPS) Nasional Bank Indonesia yang dihimpun di Kaggle, terdiri atas 30 file harga harian untuk {{jumlah komoditas, Lembar Fakta Tambahan C}} komoditas pada {{jumlah jenis pasar, B}} jenis pasar di 34 provinsi, periode 1 Januari 2022 sampai 12 Februari 2026. Metode yang digunakan meliputi analisis kelayakan data, analisis kebutuhan informasi, perancangan proses ETL, perancangan *data warehouse* dengan pendekatan dimensional Kimball, dan perancangan *dashboard*. Hasilnya berupa skema bintang dengan tabel fakta `fact_harga_harian` pada grain harga per komoditas, jenis pasar, provinsi, dan tanggal; rancangan ETL yang mengubah data berformat lebar menjadi baris fakta; serta rancangan *dashboard* yang menampilkan {{2–3 visual utama dari bagian Ikhsan}}.

---

## 1.1 JUSTIFIKASI

Topik harga pangan strategis dipilih karena harga pangan menyentuh kebutuhan dasar seluruh masyarakat dan termasuk kelompok harga bergejolak (*volatile food*) dalam pengukuran inflasi di Indonesia. Harga beras, cabai, atau bawang dapat berubah dalam hitungan hari dan berbeda antarwilayah, sehingga pemantauannya membutuhkan data yang rinci menurut waktu, komoditas, dan wilayah. Kebutuhan seperti ini sesuai dengan karakter *data warehouse* dan *Business Intelligence*, yaitu menyimpan data historis dalam jumlah besar lalu menyajikannya dari berbagai sudut pandang.

Dataset yang digunakan adalah *Indonesia PIHPS Food Commodity Prices Dataset* di Kaggle, yang berisi hasil pengumpulan (*scraping*) data dari PIHPS Nasional Bank Indonesia (https://www.bi.go.id/hargapangan). Berdasarkan pemeriksaan kelompok menggunakan *script* Python, dataset terdiri atas 30 file CSV dengan total 44.014 baris. Setiap file mewakili satu kombinasi komoditas dan jenis pasar, misalnya beras di pasar modern atau telur ayam di tingkat produsen. Setiap file memuat kolom tanggal (`Date_Param`) dan 34 kolom provinsi yang berisi harga. Data mencakup 1.493 tanggal dalam rentang 1 Januari 2022 sampai 12 Februari 2026.

Dataset ini dinilai layak digunakan karena tiga alasan. Pertama, **datanya multidimensi**: terdapat dimensi waktu (harian), komoditas, jenis pasar, dan provinsi, yang secara langsung membentuk skema bintang. Adanya harga tingkat produsen dan tingkat pasar juga memungkinkan analisis selisih harga dari produsen ke konsumen. Kedua, **rentang waktunya panjang**, lebih dari empat tahun, sehingga mencakup beberapa periode Ramadan dan Idulfitri untuk analisis pola musiman. Ketiga, **sumber aslinya adalah lembaga resmi**, yaitu Bank Indonesia, sehingga nilainya dapat diverifikasi terhadap situs PIHPS.

Kelompok juga mencatat beberapa keterbatasan. (1) Dataset diunggah oleh pengguna perorangan, bukan dirilis langsung oleh Bank Indonesia, dan berada dalam folder bernama `Cleaned_After_Imputation`, yang menandakan sebagian nilai sudah diisi (imputasi) oleh pengunggah sehingga tidak semuanya merupakan hasil pengamatan asli. (2) Data berformat lebar (provinsi sebagai kolom), sedangkan komoditas dan jenis pasar hanya tercantum pada nama file, sehingga perlu diubah bentuknya sebelum dimuat ke *data warehouse*. (3) Struktur kolom tidak seragam: terdapat 12 variasi susunan kolom di antara 30 file, dan persentase nilai kosong per provinsi berkisar 3,39% sampai 33,92% (tertinggi DKI Jakarta). {{Jika Lembar Fakta Tambahan D menunjukkan provinsi tidak ada di file tertentu: "Nilai kosong ini terutama muncul karena provinsi tertentu tidak tercatat pada file komoditas/jenis pasar tertentu."}} (4) Terdapat 11 tanggal tanpa data dari 1.504 hari kalender dalam rentang tersebut. (5) Kolom tanggal tersimpan sebagai teks. (6) Terdapat nilai ekstrem yang perlu diperiksa, misalnya harga maksimum Kalimantan Selatan sebesar Rp605.500, jauh di atas maksimum provinsi lain yang berada di bawah Rp300.000. (7) Data mencakup 34 provinsi, sementara Indonesia saat ini memiliki 38 provinsi setelah pemekaran wilayah Papua, sehingga provinsi hasil pemekaran tidak tercatat terpisah. Di sisi lain, tidak ditemukan baris duplikat maupun harga bernilai nol atau negatif. Keterbatasan-keterbatasan tersebut ditangani pada rancangan ETL (subbab 1.3 A) dan tidak mengurangi kelayakan dataset untuk tujuan perancangan.

> Opsional tapi menguatkan (5 menit): cocokkan 2 harga acak dengan situs PIHPS, lalu tambahkan kalimat: "Pencocokan sampel terhadap situs PIHPS pada {{tanggal}} menunjukkan nilai yang {{sama/berbeda}}."

---

## 2. KESIMPULAN  *(ditulis TERAKHIR)*

Dataset harga pangan strategis PIHPS yang terdiri atas 30 file harga harian di 34 provinsi dinilai layak digunakan sebagai dasar perancangan solusi *Business Intelligence*, dengan catatan kualitas berupa {{2 masalah data utama}}. Analisis kebutuhan informasi menghasilkan enam pertanyaan bisnis yang berfokus pada perbandingan harga antarprovinsi, fluktuasi komoditas, tren bulanan, kenaikan harga menjelang Idulfitri, kesenjangan antarwilayah, dan selisih harga produsen–konsumen. Kebutuhan tersebut dipenuhi dengan *data warehouse* berbentuk skema bintang pada grain harga per komoditas, jenis pasar, provinsi, dan tanggal, yang diisi melalui proses ETL untuk {{sebut aturan transformasi utama dari Hanif}}. Rancangan *dashboard* menyajikan {{visual utama dari Ikhsan}} sehingga pengguna dapat {{keputusan yang dibantu, dari tabel kebutuhan informasi Ikhsan}}. Pengembangan selanjutnya dapat berupa implementasi ETL secara nyata dan penambahan data pendukung seperti inflasi atau jumlah penduduk per provinsi.

---

## 3. DAFTAR REFERENSI (APA 7)

Urutkan abjad. Tambahkan referensi dari Ikhsan & Hanif **hanya** kalau ada URL-nya.

- Bank Indonesia. (n.d.). *Pusat Informasi Harga Pangan Strategis Nasional (PIHPS Nasional)*. Diakses {{tanggal}}, dari https://www.bi.go.id/hargapangan
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- muhyusuf1112. ({{tahun unggah, lihat halaman Kaggle}}). *Indonesia PIHPS food commodity prices dataset* [Data set]. Kaggle. https://www.kaggle.com/datasets/muhyusuf1112/indonesia-commodity-price-based-piphs-source
