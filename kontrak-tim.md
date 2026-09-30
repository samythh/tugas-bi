# KONTRAK TIM — Kelompok 12

Semua anggota (dan AI masing-masing) WAJIB mengikuti kontrak ini.
Nama tabel, grain, dan measure di bawah **tidak boleh diganti** tanpa kabar di grup.
Menambah atribut boleh.

> Status: **DRAF.** Final kalau 1 jam setelah dikirim tidak ada yang keberatan.
> Sudah dicocokkan dengan `LembarFakta.txt` dan `LembarFaktaTambahan.txt`.

## 0. Fakta struktur data yang WAJIB diketahui semua anggota

- Dataset = **30 file CSV**, satu file per **komoditas × jenis pasar**
  (contoh: `final_komoditas_modern_beras_2022_2026.csv`, `final_komoditas_produsen_telur_ayam_2022_2026.csv`).
- Format **WIDE**: kolom `Date_Param` (tanggal, tersimpan sebagai teks) + **34 kolom provinsi** berisi harga.
- **Komoditas dan jenis pasar TIDAK ada sebagai kolom**, hanya di nama file.
- Folder sumber bernama `Cleaned_After_Imputation` → data sudah diimputasi oleh pengunggah.
- **10 komoditas:** bawang_merah, bawang_putih, beras, cabai_merah, cabai_rawit, daging_ayam, daging_sapi, gula_pasir, minyak_goreng, telur_ayam.
- **3 jenis pasar:** tradisional, modern, produsen (masing-masing 10 file, folder terpisah).
- Baris per file: modern & produsen 1.493; tradisional 1.415–1.417 (lebih sedikit tanggal).
- Nilai kosong = **provinsi tidak ada di file tertentu** (0 sel kosong di dalam file). Paling parah di produsen: bawang_putih 2 provinsi, gula_pasir 14, minyak_goreng 15; DKI Jakarta tanpa data produsen.
- Setelah unpivot: **1.354.641 baris** harga, 0 duplikat → ini jumlah baris `fact_harga_harian`.
- **2.187 kandidat outlier.** Contoh: gula_pasir modern Kalimantan Selatan Rp605.500 (28 Mei–4 Jun 2024), median Rp16.700.
- Jadi ETL wajib: unpivot provinsi → baris, ambil komoditas & jenis pasar dari nama file, ubah `Date_Param` jadi tanggal.

## 1. Pertanyaan bisnis (acuan semua bagian)

| Kode | Pertanyaan bisnis | Measure utama |
|---|---|---|
| Q1 | Provinsi mana yang harga rata-rata tiap komoditasnya tertinggi dan terendah? | `avg_harga` |
| Q2 | Komoditas mana yang harganya paling fluktuatif? | `cv_harga` = simpangan baku ÷ rata-rata |
| Q3 | Bagaimana tren harga bulanan tiap komoditas? | `avg_harga` per bulan |
| Q4 | Berapa kenaikan harga menjelang Idulfitri (H-30 s/d H-1) dibanding rata-rata bulan biasa? | `pct_kenaikan_lebaran` |
| Q5 | Berapa kesenjangan harga antarprovinsi untuk tiap komoditas? | `disparitas_harga` = maks − min antarprovinsi |
| Q6 | Berapa selisih harga dari tingkat produsen ke pasar konsumen untuk tiap komoditas dan provinsi? | `selisih_produsen_konsumen` = harga pasar − harga produsen. Hanya untuk provinsi yang punya data produsen (bawang putih cuma 2 provinsi) |

## 2. Desain Data Warehouse (Kimball)

- **Proses bisnis:** pemantauan harga harian pangan strategis.
- **Grain:** 1 baris = harga 1 komoditas, pada 1 jenis pasar, di 1 provinsi, pada 1 tanggal.

| Tabel | Isi minimal |
|---|---|
| `fact_harga_harian` | `tanggal_key`, `komoditas_key`, `jenis_pasar_key`, `provinsi_key`, `harga` (Rp) |
| `dim_tanggal` | `tanggal_key`, `tanggal`, `hari`, `minggu`, `bulan`, `nama_bulan`, `kuartal`, `tahun`, `is_ramadan`, `hari_ke_lebaran` |
| `dim_komoditas` | `komoditas_key`, `nama_komoditas` (10 nilai di atas), `satuan` |
| `dim_jenis_pasar` | `jenis_pasar_key`, `nama_jenis_pasar` (tradisional / modern / produsen), `tingkat` (konsumen / produsen) |
| `dim_provinsi` | `provinsi_key`, `nama_provinsi` (34 nama persis seperti header kolom), `pulau`/`wilayah` |

- `avg_harga`, `cv_harga`, `pct_kenaikan_lebaran`, `disparitas_harga`, `selisih_produsen_konsumen` adalah **measure turunan** (dihitung di dashboard), bukan kolom di tabel fakta.
- Satuan harga (per kg/liter) **tidak tercantum di data** → tulis [PERLU DICEK], cek halaman Kaggle/PIHPS.
- Statistik bagian 7 di LembarFakta.txt **mencampur semua komoditas** → jangan dipakai untuk analisis; pakai bagian F di LembarFaktaTambahan.txt.

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
