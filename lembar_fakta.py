# =============================================================
# LEMBAR FAKTA DATA — Kelompok 12 (Tugas BI)
# Jalankan di Google Colab. Output = satu-satunya sumber fakta
# yang boleh dipakai tim (dan AI tim) saat menulis laporan.
# =============================================================
# CARA PAKAI (Colab):
# 1. Buka https://colab.research.google.com -> New notebook
# 2. Tempel SELURUH isi file ini ke satu sel -> Run (Ctrl+Enter)
# 3. Kalau download otomatis gagal: unduh ZIP dataset manual dari Kaggle,
#    upload ZIP-nya ke Colab (ikon folder di kiri), lalu isi ZIP_MANUAL di bawah.
# 4. Hasil: file LembarFakta.txt (klik kanan -> Download) -> kirim ke grup.
# =============================================================

import glob, io, os, re, zipfile
from contextlib import redirect_stdout
import pandas as pd

DATASET = "muhyusuf1112/indonesia-commodity-price-based-piphs-source"
ZIP_MANUAL = ""  # contoh: "/content/archive.zip" (kosongkan kalau pakai download otomatis)

# ---------- 1. Ambil data ----------
if ZIP_MANUAL:
    folder = "/content/data"
    zipfile.ZipFile(ZIP_MANUAL).extractall(folder)
else:
    import kagglehub
    folder = kagglehub.dataset_download(DATASET)

files = sorted(glob.glob(os.path.join(folder, "**", "*.csv"), recursive=True))
if not files:
    raise SystemExit(f"Tidak ada file CSV di {folder}. Cek isi folder dataset.")

# ---------- 2. Gabungkan semua CSV ----------
# Dataset bisa berupa 1 file besar atau ratusan file harian;
# keduanya digabung jadi satu tabel, asal file dicatat di kolom _file.
parts, gagal = [], []
for f in files:
    try:
        d = pd.read_csv(f)
        d["_file"] = os.path.relpath(f, folder)
        parts.append(d)
    except Exception as e:
        gagal.append((f, str(e)[:80]))
df = pd.concat(parts, ignore_index=True)

def is_teks(s):
    # pandas 2 menyimpan teks sebagai object, pandas 3 sebagai str
    return s.dtype == object or pd.api.types.is_string_dtype(s)

def potong(xs, n=60):
    xs = list(xs)
    return xs if len(xs) <= n else xs[:n] + [f"... (+{len(xs) - n} lainnya)"]

buf = io.StringIO()
with redirect_stdout(buf):
    print("LEMBAR FAKTA DATA — Kelompok 12")
    print("Dataset:", "https://www.kaggle.com/datasets/" + DATASET)
    print("Dibuat :", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))

    print("\n## 1. FILE")
    print("Jumlah file CSV :", len(files))
    print("Contoh nama file:", [os.path.basename(f) for f in files[:3]], "...",
          [os.path.basename(f) for f in files[-2:]])
    print("File gagal dibaca:", len(gagal), gagal[:5])
    kolom_per_file = pd.Series([tuple(p.columns) for p in parts]).value_counts()
    print("Variasi struktur kolom antar file:", len(kolom_per_file),
          "(1 = semua file seragam)")

    print("\n## 2. UKURAN & KOLOM (gabungan)")
    print("Total baris:", len(df), "| Total kolom (termasuk _file):", df.shape[1])
    print(df.dtypes.to_string())

    print("\n## 3. CONTOH 5 BARIS PERTAMA")
    print(df.head().to_string())

    print("\n## 4. KUALITAS DATA")
    print("-- nilai kosong (null) per kolom --")
    print(df.isna().sum().to_string())
    print("-- persentase kosong --")
    print((df.isna().mean() * 100).round(2).astype(str).add(" %").to_string())
    print("-- baris duplikat penuh (tanpa _file):", df.drop(columns="_file").duplicated().sum())

    # Kolom teks bernilai sedikit = kandidat dimensi (provinsi, komoditas, satuan, dst)
    print("\n## 5. NILAI UNIK KOLOM TEKS (kandidat dimensi)")
    for c in df.columns:
        if c == "_file":
            continue
        if is_teks(df[c]):
            u = df[c].dropna().astype(str)
            print(f"-- {c}: {u.nunique()} nilai unik")
            if u.nunique() <= 120:
                print(potong(sorted(u.unique()), 120))
            # Nama sama tapi beda spasi/kapital = masalah standardisasi (bahan ETL)
            norm = u.str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
            if norm.nunique() < u.nunique():
                print(f"   !! {u.nunique() - norm.nunique()} nilai hanya beda spasi/huruf besar-kecil")

    print("\n## 6. KOLOM TANGGAL")
    kand = [c for c in df.columns if re.search(r"date|tanggal|tgl|waktu|period", c, re.I)]
    if not kand:
        print("Tidak ada kolom bernama tanggal. Cek apakah tanggal ada di NAMA FILE:")
        print([os.path.basename(f) for f in files[:3]])
    for c in kand:
        d = pd.to_datetime(df[c], errors="coerce", dayfirst=False)
        print(f"-- {c}: {d.min()} s/d {d.max()} | gagal parse: {d.isna().sum()} | tanggal unik: {d.nunique()}")
        if d.notna().any():
            penuh = pd.date_range(d.min().normalize(), d.max().normalize())
            hilang = penuh.difference(d.dropna().dt.normalize().unique())
            print(f"   Hari kalender dalam rentang: {len(penuh)} | tanggal tanpa data: {len(hilang)}")
            print("   Contoh tanggal tanpa data:", [str(x.date()) for x in hilang[:10]])

    print("\n## 7. KOLOM ANGKA")
    num = df.select_dtypes("number")
    if num.shape[1]:
        print(num.describe().T.round(2).to_string())
        print("-- jumlah nilai <= 0 --")
        print((num <= 0).sum().to_string())
    # Harga yang tersimpan sebagai teks ("12.500", "Rp 12,500") perlu dibersihkan di ETL
    for c in df.columns:
        if is_teks(df[c]) and c != "_file":
            s = df[c].dropna().astype(str).head(1000)
            if len(s) and s.str.fullmatch(r"[\sRp\.\,\d\-]+").mean() > 0.9:
                print(f"!! Kolom '{c}' berisi angka yang tersimpan sebagai TEKS. Contoh: {s.head(3).tolist()}")

    print("\n## 8. SELESAI")
    print("Aturan tim: angka/kolom/nilai yang tidak ada di lembar ini = [PERLU DICEK].")

teks = buf.getvalue()
open("LembarFakta.txt", "w", encoding="utf-8").write(teks)
print(teks)
print("\n>>> Tersimpan: LembarFakta.txt (panel folder di kiri -> klik kanan -> Download)")
