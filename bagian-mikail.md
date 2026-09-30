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

Harga pangan strategis di Indonesia berubah setiap hari dan berbeda antarprovinsi, sehingga pengambil keputusan membutuhkan informasi yang ringkas untuk memantau kenaikan, fluktuasi, dan kesenjangan harga. Tugas ini bertujuan merancang solusi *Business Intelligence* yang mampu menjawab {{jumlah pertanyaan bisnis, lihat Kontrak Tim}} pertanyaan bisnis tersebut. Data yang digunakan adalah harga eceran harian {{jumlah komoditas}} komoditas pangan di {{jumlah provinsi}} provinsi periode {{tanggal awal}} sampai {{tanggal akhir}}, bersumber dari Pusat Informasi Harga Pangan Strategis (PIHPS) Nasional Bank Indonesia yang dihimpun di Kaggle. Metode yang digunakan meliputi analisis kelayakan data, analisis kebutuhan informasi, perancangan proses ETL, perancangan *data warehouse* dengan pendekatan dimensional Kimball, dan perancangan *dashboard*. Hasilnya berupa skema bintang dengan satu tabel fakta `fact_harga_harian` dan {{jumlah tabel dimensi dari bagian Hanif}} tabel dimensi, rancangan ETL untuk menangani {{sebut 2–3 masalah data utama dari bagian Hanif}}, serta rancangan *dashboard* yang menampilkan {{sebut 2–3 visual utama dari bagian Ikhsan}}.

---

## 1.1 JUSTIFIKASI

Topik harga pangan strategis dipilih karena harga pangan menyentuh kebutuhan dasar seluruh masyarakat dan termasuk kelompok harga yang bergejolak (*volatile food*) dalam pengukuran inflasi di Indonesia. Perubahan harga beras, cabai, atau bawang dapat terjadi dalam hitungan hari dan berbeda antarwilayah, sehingga pemantauannya membutuhkan data yang rinci per waktu, per komoditas, dan per wilayah. Kebutuhan pemantauan seperti ini sesuai dengan karakter *data warehouse* dan *Business Intelligence*, yaitu menyimpan data historis dalam jumlah besar lalu menyajikannya dari berbagai sudut pandang.

Dataset yang digunakan adalah *Indonesia PIHPS Food Commodity Prices Dataset* di Kaggle, berisi hasil pengumpulan (*scraping*) data dari PIHPS Nasional Bank Indonesia (https://www.bi.go.id/hargapangan). Berdasarkan pemeriksaan kelompok, dataset terdiri atas {{jumlah file}} file CSV dengan total {{total baris}} baris dan {{jumlah kolom, tanpa _file}} kolom, mencakup {{jumlah komoditas}} komoditas di {{jumlah provinsi}} provinsi pada periode {{tanggal awal}} sampai {{tanggal akhir}}.

Dataset ini dinilai layak digunakan karena tiga alasan. Pertama, **cakupannya lengkap untuk analisis multidimensi**: data memiliki dimensi waktu (harian), komoditas, dan wilayah, yang secara langsung membentuk skema bintang. Kedua, **rentang waktunya panjang**, lebih dari empat tahun, sehingga mencakup beberapa periode Ramadan dan Idulfitri yang memungkinkan analisis pola musiman. Ketiga, **sumber aslinya adalah lembaga resmi**, yaitu Bank Indonesia, sehingga isinya dapat diverifikasi dengan membandingkan beberapa nilai terhadap situs PIHPS.

Kelompok juga mencatat keterbatasan dataset. Dataset diunggah oleh pengguna perorangan dan bukan dirilis langsung oleh Bank Indonesia, sehingga kelengkapan dan ketepatan hasil *scraping* perlu diperiksa. Pemeriksaan awal menunjukkan {{ringkas temuan kualitas: % nilai kosong kolom harga, jumlah harga ≤ 0, jumlah tanggal tanpa data, nilai provinsi/komoditas yang tidak seragam}}. {{HANYA JIKA jumlah provinsi = 34:}} Selain itu, data mencakup 34 provinsi, sementara Indonesia saat ini memiliki 38 provinsi setelah pemekaran wilayah Papua, sehingga provinsi hasil pemekaran belum tercatat terpisah. Temuan-temuan tersebut ditangani pada rancangan ETL (subbab 1.3 A) dan tidak mengurangi kelayakan dataset untuk tujuan perancangan.

> Opsional tapi menguatkan (5 menit): cocokkan 2 harga acak dari Lembar Fakta dengan situs PIHPS, lalu tambahkan kalimat: "Pencocokan sampel terhadap situs PIHPS pada {{tanggal}} menunjukkan nilai yang {{sama/berbeda}}."

---

## 2. KESIMPULAN  *(ditulis TERAKHIR)*

Dataset harga pangan strategis PIHPS dengan {{total baris}} baris data harian dinilai layak digunakan sebagai dasar perancangan solusi *Business Intelligence*, dengan catatan kualitas berupa {{2 masalah data utama}}. Analisis kebutuhan informasi menghasilkan {{jumlah}} pertanyaan bisnis yang berfokus pada perbandingan harga antarprovinsi, fluktuasi komoditas, tren bulanan, dan kenaikan harga menjelang Idulfitri. Kebutuhan tersebut dipenuhi dengan *data warehouse* berbentuk skema bintang pada grain {{grain final dari Kontrak Tim}}, yang diisi melalui proses ETL untuk {{sebut aturan transformasi utama dari Hanif}}. Rancangan *dashboard* menyajikan {{visual utama dari Ikhsan}} sehingga pengguna dapat {{keputusan yang dibantu, dari tabel kebutuhan informasi Ikhsan}}. Pengembangan selanjutnya dapat berupa implementasi ETL secara nyata dan penambahan data pendukung seperti inflasi atau jumlah penduduk per provinsi.

---

## 3. DAFTAR REFERENSI (APA 7)

Urutkan abjad. Tambahkan referensi dari Ikhsan & Hanif **hanya** kalau ada URL-nya.

- Bank Indonesia. (n.d.). *Pusat Informasi Harga Pangan Strategis Nasional (PIHPS Nasional)*. Diakses {{tanggal}}, dari https://www.bi.go.id/hargapangan
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- muhyusuf1112. ({{tahun unggah, lihat halaman Kaggle}}). *Indonesia PIHPS food commodity prices dataset* [Data set]. Kaggle. https://www.kaggle.com/datasets/muhyusuf1112/indonesia-commodity-price-based-piphs-source
