# Data Dictionary - df_food.csv

Berikut adalah dokumentasi skema kolom untuk file `df_food.csv` data nutrisi makanan Indonesia:

| # | Nama Kolom | Tipe Data | Deskripsi |
|---|------------|-----------|-----------|
| 1 | `id` | `int64` | Identifier unik untuk setiap entri bahan makanan atau hidangan. |
| 2 | `jenis_makanan` | `object` | Kategori makanan, dipisahkan menjadi 'dish' (makanan siap konsumsi) atau 'komponen' (bahan mentah/tunggal). |
| 3 | `nama_makanan` | `object` | Nama bahan makanan atau hidangan yang sudah melewati proses normalisasi teks (lowercase, tanpa tanda baca). |
| 4 | `kalori` | `float64` | Kandungan energi total per 100 gram bahan makanan, dinyatakan dalam satuan Kalori (Kal/kcal). |
| 5 | `protein` | `float64` | Kandungan protein per 100 gram bahan makanan, dinyatakan dalam satuan gram (g). |
| 6 | `lemak` | `float64` | Kandungan lemak total per 100 gram bahan makanan, dinyatakan dalam satuan gram (g). |
| 7 | `karbohidrat` | `float64` | Kandungan karbohidrat total per 100 gram bahan makanan, dinyatakan dalam satuan gram (g). |
| 8 | `source` | `object` | Sumber asal data operasional, mengindikasikan apakah data berasal dari 'tkpi' atau 'kaggle'. |
| 9 | `protein_per_calorie` | `float64` | Rasio kandungan protein terhadap total kalori (g/Kal), digunakan untuk mengukur efisiensi densitas protein. |
| 10 | `fat_per_calorie` | `float64` | Rasio kandungan lemak terhadap total kalori (g/Kal), digunakan untuk mengukur densitas lemak. |
| 11 | `carb_per_calorie` | `float64` | Rasio kandungan karbohidrat terhadap total kalori (g/Kal), digunakan untuk mengukur densitas karbohidrat. |
| 12 | `protein_fat_ratio` | `float64` | Perbandingan antara total protein terhadap total lemak (protein dibagi lemak) dalam suatu makanan. |
| 13 | `macro_balance_score` | `float64` | Skor kalkulasi hasil feature engineering yang menunjukkan tingkat keseimbangan proporsi zat gizi makro. |
