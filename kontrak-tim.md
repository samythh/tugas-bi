# KONTRAK TIM — Kelompok 12

Semua anggota (dan AI masing-masing) WAJIB mengikuti kontrak ini.
Nama tabel, grain, dan measure di bawah **tidak boleh diganti** tanpa kabar di grup.
Menambah atribut boleh.

> Status: **DRAF.** Final kalau 1 jam setelah dikirim tidak ada yang keberatan.
> Bagian bertanda ⚠️ dicek Mikail terhadap Lembar Fakta sebelum dikirim.

## 1. Pertanyaan bisnis (acuan semua bagian)

| Kode | Pertanyaan bisnis | Measure utama |
|---|---|---|
| Q1 | Provinsi mana yang harga rata-rata tiap komoditasnya tertinggi dan terendah? | `avg_harga` |
| Q2 | Komoditas mana yang harganya paling fluktuatif? | `cv_harga` = simpangan baku ÷ rata-rata |
| Q3 | Bagaimana tren harga bulanan tiap komoditas? | `avg_harga` per bulan |
| Q4 | Berapa kenaikan harga menjelang Idulfitri (H-30 s/d H-1) dibanding rata-rata bulan biasa? | `pct_kenaikan_lebaran` |
| Q5 | Berapa kesenjangan harga antarprovinsi untuk tiap komoditas? | `disparitas_harga` = maks − min antarprovinsi |

## 2. Desain Data Warehouse (Kimball)

- **Proses bisnis:** pemantauan harga eceran harian pangan strategis.
- **Grain:** 1 baris = harga 1 komoditas, di 1 provinsi, pada 1 tanggal.
  ⚠️ Berlaku kalau Lembar Fakta menunjukkan data di level provinsi. Kalau ada kolom pasar/kota, grain turun ke level itu dan ditambah `dim_lokasi`.

| Tabel | Isi minimal |
|---|---|
| `fact_harga_harian` | `tanggal_key`, `komoditas_key`, `provinsi_key`, `harga` (Rp/satuan) |
| `dim_tanggal` | `tanggal_key`, `tanggal`, `hari`, `minggu`, `bulan`, `nama_bulan`, `kuartal`, `tahun`, `is_ramadan`, `hari_ke_lebaran` |
| `dim_komoditas` | `komoditas_key`, `nama_komoditas`, `satuan` |
| `dim_provinsi` | `provinsi_key`, `nama_provinsi`, `pulau`/`wilayah` |

- `avg_harga`, `cv_harga`, `pct_kenaikan_lebaran`, `disparitas_harga` adalah **measure turunan** (dihitung di dashboard), bukan kolom di tabel fakta.
- Nama kolom sumber (bahasa Inggris/Indonesia) **ikut Lembar Fakta**, bukan tebakan.

## 3. Penulisan

- Tulis langsung di Google Docs, di heading masing-masing.
- Sitasi: **APA 7**. Hanya sumber yang sudah dibuka sendiri + URL + tanggal akses.
- Tanggal Idulfitri: dari SKB libur nasional, bukan dari AI.
- Yang belum pasti ditulis **[PERLU DICEK]**.

## 4. Pemetaan bagian → heading Google Docs

| Heading di Docs | PIC |
|---|---|
| Cover, A. Abstrak | Mikail |
| 1.1 Justifikasi | Mikail |
| 1.2 A. Analisis kebutuhan informasi | Ikhsan |
| 1.2 B. Analisis data | Ikhsan |
| 1.3 A. Desain ETL (a–e) | Hanif |
| 1.3 B. Desain Data Warehouse (a–d) | Hanif |
| 1.3 C. Desain dashboard | Ikhsan |
| 2. Kesimpulan, 3. Daftar referensi, PDF | Mikail |
