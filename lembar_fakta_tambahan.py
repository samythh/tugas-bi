# =============================================================
# LEMBAR FAKTA TAMBAHAN — Kelompok 12
# Dijalankan SETELAH lembar_fakta.py, di notebook Colab yang sama.
# Kenapa perlu: Lembar Fakta pertama menunjukkan data berformat WIDE
# (provinsi = kolom), sedangkan komoditas & jenis pasar hanya ada di NAMA FILE.
# Statistik gabungan mencampur beras dan daging sapi, jadi tidak bermakna.
# Script ini memecah fakta per file (= per komoditas x jenis pasar).
# Hasil: LembarFaktaTambahan.txt -> kirim ke grup bersama LembarFakta.txt
# =============================================================
import glob, io, os, re
from contextlib import redirect_stdout
import pandas as pd

try:
    folder  # dari sel lembar_fakta.py
except NameError:
    import kagglehub
    folder = kagglehub.dataset_download("muhyusuf1112/indonesia-commodity-price-based-piphs-source")

files = sorted(glob.glob(os.path.join(folder, "**", "*.csv"), recursive=True))
pola = re.compile(r"final_komoditas_([a-z]+)_(.+)_(\d{4})_(\d{4})\.csv$")

ringkas, longs, semua_prov = [], [], set()
for f in files:
    d = pd.read_csv(f)
    semua_prov |= set(c for c in d.columns if c != "Date_Param")
for f in files:
    d = pd.read_csv(f)
    nama = os.path.basename(f)
    m = pola.match(nama)
    jenis, kom = (m.group(1), m.group(2)) if m else ("[TIDAK COCOK POLA]", nama)
    prov = [c for c in d.columns if c != "Date_Param"]
    # unpivot: 1 baris = 1 tanggal x 1 provinsi (bentuk yang dibutuhkan tabel fakta)
    lg = d.melt(id_vars="Date_Param", var_name="provinsi", value_name="harga")
    lg["jenis_pasar"], lg["komoditas"] = jenis, kom
    longs.append(lg)
    ringkas.append(dict(
        folder=os.path.dirname(os.path.relpath(f, folder)),
        jenis_pasar=jenis, komoditas=kom, baris=len(d),
        tgl_duplikat=int(d["Date_Param"].duplicated().sum()),
        tgl_awal=d["Date_Param"].min(), tgl_akhir=d["Date_Param"].max(),
        n_provinsi=len(prov), null_di_kolom_ada=int(lg["harga"].isna().sum()),
        provinsi_tidak_ada=", ".join(sorted(semua_prov - set(prov))) or "-",
    ))
R = pd.DataFrame(ringkas)
L = pd.concat(longs, ignore_index=True)

buf = io.StringIO()
with redirect_stdout(buf):
    print("LEMBAR FAKTA TAMBAHAN — Kelompok 12")
    print("\n## A. FOLDER SUMBER"); print(R["folder"].value_counts().to_string())
    print("\n## B. JENIS PASAR (dari nama file)"); print(sorted(R["jenis_pasar"].unique()))
    print("\n## C. KOMODITAS (dari nama file)"); print(sorted(R["komoditas"].unique()))
    print("\n## D. RINGKASAN PER FILE")
    with pd.option_context("display.max_colwidth", 200, "display.width", 250):
        print(R.drop(columns="folder").to_string(index=False))
    print("\n## E. SETELAH UNPIVOT (bentuk panjang)")
    ada = L.dropna(subset=["harga"])
    print("Total baris panjang (termasuk kosong):", len(L))
    print("Baris berisi harga                  :", len(ada))
    print("Kombinasi tanggal+provinsi+pasar+komoditas duplikat:",
          int(L.duplicated(["Date_Param", "provinsi", "jenis_pasar", "komoditas"]).sum()))
    print("\n## F. STATISTIK HARGA PER KOMODITAS x JENIS PASAR (Rp)")
    st = ada.groupby(["komoditas", "jenis_pasar"])["harga"].describe()[["count", "mean", "min", "50%", "max"]]
    print(st.round(0).to_string())
    print("\n## G. KANDIDAT OUTLIER (> Q3 + 3xIQR dalam komoditas x jenis pasar yang sama)")
    g = ada.groupby(["komoditas", "jenis_pasar"])["harga"]
    q1, q3 = g.transform(lambda s: s.quantile(.25)), g.transform(lambda s: s.quantile(.75))
    out = ada[ada["harga"] > q3 + 3 * (q3 - q1)]
    print("Jumlah:", len(out))
    print(out.sort_values("harga", ascending=False).head(15).to_string(index=False))
    print("\nAturan tim: yang tidak tertulis di lembar ini = [PERLU DICEK].")

teks = buf.getvalue()
open("LembarFaktaTambahan.txt", "w", encoding="utf-8").write(teks)
print(teks)
print(">>> Tersimpan: LembarFaktaTambahan.txt")
