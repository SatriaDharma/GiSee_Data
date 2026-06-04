# 🍽️ GiSee — Gain Insight See Your Nutrition

Dashboard Streamlit komprehensif untuk eksplorasi dan analisis data nutrisi makanan Indonesia, berdasarkan pipeline EDA dari gabungan dataset **TKPI (Kemenkes RI)** dan **Indonesian Food and Drink Nutrition Dataset (Kaggle)**.

---

## 📋 Fitur Dashboard

| Halaman | Fitur |
|---------|-------|
| 🏠 Ringkasan Eksekutif | KPI cards, distribusi kalori/protein, profil dish vs komponen |
| 🔬 Eksplorasi Data | Histogram interaktif, heatmap korelasi, scatter plot, box plot |
| 📊 Analisis BQ | Jawaban 5 Business Questions dari notebook EDA |
| 🥗 Komparasi Makanan | Bandingkan makanan, radar chart, search & filter, ranking |
| 📋 Tabel Data Lengkap | Full dataset dengan filter, data dictionary, export CSV |

### Filter Global (Sidebar)
- Jenis makanan (dish / komponen)
- Sumber dataset (TKPI / Kaggle)
- Range kalori
- Range protein

---

## 🚀 Cara Menjalankan Lokal

```bash
# 1. Clone / download folder ini
# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan
streamlit run app.py
```

---

## 📂 Struktur Kolom df_food.csv

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `id` | int | ID unik |
| `nama_makanan` | str | Nama makanan (lowercase, normalized) |
| `jenis_makanan` | str | `dish` atau `komponen` |
| `kalori` | float | kal/100g |
| `protein` | float | g/100g |
| `lemak` | float | g/100g |
| `karbohidrat` | float | g/100g |
| `source` | str | `tkpi` atau `kaggle` |
| `protein_per_calorie` | float | Efisiensi protein |
| `fat_per_calorie` | float | Densitas lemak |
| `carb_per_calorie` | float | Densitas karbohidrat |
| `protein_fat_ratio` | float | Rasio protein:lemak |
| `macro_balance_score` | float | Skor keseimbangan gizi (0–1) |

---

## 🛠️ Tech Stack

- **Streamlit** 1.35 — web framework
- **Plotly** 5.22 — visualisasi interaktif
- **Pandas** 2.2 — manipulasi data
- **NumPy** 1.26 — komputasi numerik
- **SciPy** + **scikit-learn** — analisis statistik

---

## 📌 Sumber Data

- **TKPI** — Tabel Komposisi Pangan Indonesia, Kementerian Kesehatan RI
- **Kaggle** — Indonesian Food and Drink Nutrition Dataset

Nilai nutrisi per **100 gram** bahan makanan.
