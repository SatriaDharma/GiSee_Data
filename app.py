"""
app.py — GiSee Dashboard | Gain Insight See Your Nutrition
Streamlit Cloud-ready • siap deploy tanpa file CSV eksternal
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─── KONFIGURASI HALAMAN ────────────────────────────────────────────────────
st.set_page_config(
    page_title="GiSee — Gain Insight See Your Nutrition",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── TEMA & CSS KUSTOM ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

/* Root variables */
:root {
    --bg-primary: #0f1117;
    --bg-card: #1a1d2e;
    --bg-card-hover: #1f2235;
    --accent-green: #2ecc87;
    --accent-orange: #ff7043;
    --accent-blue: #4f9cf9;
    --accent-purple: #9b59b6;
    --accent-yellow: #f1c40f;
    --text-primary: #e8eaf6;
    --text-secondary: #8892b0;
    --border: rgba(255,255,255,0.07);
}

/* Global */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-primary);
}

.stApp { background: #0d0f1a; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111326 !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent-green) !important;
}

/* Metric cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
}
.metric-card:hover { background: var(--bg-card-hover); transform: translateY(-2px); }
.metric-value { font-size: 2rem; font-weight: 800; color: var(--accent-green); line-height: 1; }
.metric-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px; }
.metric-delta { font-size: 0.8rem; color: var(--accent-orange); margin-top: 4px; }

/* Section header */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.section-header h2 {
    font-family: 'Lora', serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}
.section-badge {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 10px;
    border-radius: 20px;
    background: rgba(46,204,135,0.12);
    color: var(--accent-green);
    border: 1px solid rgba(46,204,135,0.25);
}

/* Data table */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.stDataFrame table { font-size: 0.83rem !important; }
.stDataFrame thead th {
    background: #1a1d2e !important;
    color: var(--accent-green) !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.72rem !important;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: var(--accent-green) !important;
    color: #0d0f1a !important;
}

/* Select/multiselect */
[data-baseweb="select"] { border-radius: 10px !important; }
[data-testid="stMultiSelect"] .st-bu { background: var(--bg-card) !important; }

/* Slider */
.stSlider { padding: 0 4px; }
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent-green) !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--bg-card);
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* Alert */
.info-box {
    background: rgba(79,156,249,0.08);
    border: 1px solid rgba(79,156,249,0.2);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.85rem;
    color: #a8c7fa;
    margin: 8px 0;
}
.warning-box {
    background: rgba(255,112,67,0.08);
    border: 1px solid rgba(255,112,67,0.2);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.85rem;
    color: #ffb39a;
    margin: 8px 0;
}

/* Hero title */
.hero-title {
    font-family: 'Lora', serif;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #2ecc87 0%, #4f9cf9 60%, #9b59b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 0;
}
.hero-sub {
    font-size: 1rem;
    color: var(--text-secondary);
    margin-top: 8px;
    font-weight: 400;
}

/* Tag pills */
.tag-dish {
    display: inline-block;
    background: rgba(255,112,67,0.15);
    color: #ff7043;
    border: 1px solid rgba(255,112,67,0.3);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.tag-komponen {
    display: inline-block;
    background: rgba(46,204,135,0.12);
    color: #2ecc87;
    border: 1px solid rgba(46,204,135,0.25);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Plotly chart background */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #111326; }
::-webkit-scrollbar-thumb { background: #2a2d40; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-green); }
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY GLOBAL TEMPLATE ─────────────────────────────────────────────────
CHART_BG    = "#0d0f1a"
CHART_PAPER = "#0d0f1a"
FONT_COLOR  = "#e8eaf6"
GRID_COLOR  = "rgba(255,255,255,0.05)"
PALETTE     = ["#2ecc87", "#4f9cf9", "#ff7043", "#f1c40f", "#9b59b6",
               "#1abc9c", "#e74c3c", "#3498db", "#e67e22", "#8e44ad"]

def hex_to_rgba(hex_color: str, alpha: float = 0.15) -> str:
    """Konversi hex color (#rrggbb) ke string rgba(r,g,b,alpha) yang valid untuk Plotly."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def apply_theme(fig, height=400, showlegend=True):
    fig.update_layout(
        height=height,
        paper_bgcolor=CHART_PAPER,
        plot_bgcolor=CHART_BG,
        font=dict(family="Plus Jakarta Sans", color=FONT_COLOR, size=12),
        showlegend=showlegend,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    return fig

# ─── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load df_food.csv dari root atau subfolder data/."""
    csv_paths = ["df_food.csv", "data/df_food.csv"]
    for path in csv_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            eps = 1e-6
            # Hitung kolom feature engineering jika belum ada di CSV
            if "protein_per_calorie" not in df.columns:
                df["protein_per_calorie"] = df["protein"] / (df["kalori"] + eps)
            if "fat_per_calorie" not in df.columns:
                df["fat_per_calorie"] = df["lemak"] / (df["kalori"] + eps)
            if "carb_per_calorie" not in df.columns:
                df["carb_per_calorie"] = df["karbohidrat"] / (df["kalori"] + eps)
            if "protein_fat_ratio" not in df.columns:
                df["protein_fat_ratio"] = df["protein"] / (df["lemak"] + eps)
            if "macro_balance_score" not in df.columns:
                def _balance(row):
                    m = np.array([row["protein"], row["lemak"], row["karbohidrat"]])
                    if m.sum() < 0.1:
                        return np.nan
                    p = m / m.sum()
                    return float(1 - p.std())
                df["macro_balance_score"] = df.apply(_balance, axis=1)
            # Kolom kelompok (opsional, buat dari nama jika belum ada)
            if "kelompok" not in df.columns:
                def _kelompok(name):
                    n = str(name).lower()
                    if any(k in n for k in ["ikan","bandeng","lele","gurame","gabus","kayu","udang","cumi","kepiting","kerang"]):
                        return "Ikan & Seafood"
                    elif any(k in n for k in ["ayam","sapi","kambing","babi","daging","bakso","sosis","hati"]):
                        return "Daging"
                    elif "telur" in n:
                        return "Telur"
                    elif any(k in n for k in ["tempe","tahu","oncom","kacang"]):
                        return "Kacang & Produk Olahan"
                    elif any(k in n for k in ["pisang","mangga","pepaya","semangka","jeruk","alpukat","nanas","salak","rambutan","durian","jambu","sawo","manggis","belimbing"]):
                        return "Buah"
                    elif any(k in n for k in ["bayam","kangkung","wortel","tomat","buncis","terong","mentimun","labu","gambas","pare","kol","sawi","daun"]):
                        return "Sayuran"
                    elif any(k in n for k in ["singkong","kentang","ubi","talas"]):
                        return "Umbi-umbian"
                    elif any(k in n for k in ["beras","nasi","jagung","tepung","roti","mie","bihun","kwetiau","lontong","ketupat","bubur"]):
                        return "Serealia & Produk Olahan"
                    elif any(k in n for k in ["minyak","mentega","margarin","santan"]):
                        return "Lemak & Minyak"
                    elif any(k in n for k in ["gula","madu","dodol","kue","onde","wingko","wajit","kolak"]):
                        return "Gula & Permen"
                    elif any(k in n for k in ["kopi","teh","jamu","sirup","minuman"]):
                        return "Minuman"
                    else:
                        return "Makanan Olahan"
                df["kelompok"] = df["nama_makanan"].apply(_kelompok)
            return df

    st.error(
        "❌ File **df_food.csv** tidak ditemukan!\n\n"
        "Letakkan file tersebut di folder yang sama dengan `app.py`, lalu refresh halaman."
    )
    st.stop()

# ─── LOGO (helper) ───────────────────────────────────────────────────────────
# Logo ditampilkan via st.image() di sidebar — tidak pakai st.logo() atau
# HTML <img src> karena keduanya tidak bisa serve file lokal di Streamlit.
# st.image() adalah satu-satunya cara yang reliable untuk file lokal.
_LOGO_PATH = "assets/logo_gisee.png"

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo via st.image — satu-satunya cara reliable serve file lokal
    if os.path.exists(_LOGO_PATH):
        st.image(_LOGO_PATH, use_column_width="always")
    else:
        st.markdown(
            '<div style="text-align:center; font-family:Lora,serif; font-size:1.6rem;'
            ' font-weight:700; color:#2ecc87; padding:16px 0 8px 0;">GiSee</div>',
            unsafe_allow_html=True
        )
    st.markdown(
        '<div style="text-align:center; font-size:0.72rem; color:#8892b0;'
        ' letter-spacing:2px; text-transform:uppercase; margin-bottom:20px;">'
        'Gain Insight See Your Nutrition</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🔍 Filter Data")

    # Navigasi
    halaman = st.selectbox(
        "Pilih Halaman",
        ["🏠 Ringkasan Eksekutif", "🔬 Eksplorasi Data", "📊 Analisis BQ", "🥗 Komparasi Makanan", "📋 Tabel Data Lengkap"],
        key="nav"
    )

    st.divider()
    st.markdown("### ⚙️ Filter Global")

    # Filter jenis
    jenis_options = ["Semua", "dish", "komponen"]
    jenis_filter = st.selectbox("Jenis Makanan", jenis_options, key="jenis_filter")

    # Filter sumber
    source_filter = st.multiselect(
        "Sumber Dataset", ["TKPI", "Indonesian Food and Drink Nutrition Dataset (Kaggle)"],
        default=["TKPI", "Indonesian Food and Drink Nutrition Dataset (Kaggle)"], key="source_filter"
    )

    # Range kalori
    kalori_range = st.slider("Range Kalori (kal/100g)", 0, 1000, (0, 1000), step=10, key="kalori_range")

    # Range protein
    protein_range = st.slider("Range Protein (g/100g)", 0, 90, (0, 90), step=1, key="protein_range")

    st.divider()
    st.markdown("""
    <div style="font-size:0.72rem; color:#8892b0; line-height:1.8;">
    📌 <b>Sumber Data</b><br>
    • TKPI — Kemenkes RI<br>
    • Indonesian Food and Drink Nutrition Dataset (Kaggle)<br><br>
    📌 <b>Nilai per 100g bahan</b>
    </div>
    """, unsafe_allow_html=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
df_raw = load_data()

# Terapkan filter global
df = df_raw.copy()
if jenis_filter != "Semua":
    df = df[df["jenis_makanan"] == jenis_filter]
if source_filter:
    df = df[df["source"].isin(source_filter)]
df = df[(df["kalori"] >= kalori_range[0]) & (df["kalori"] <= kalori_range[1])]
df = df[(df["protein"] >= protein_range[0]) & (df["protein"] <= protein_range[1])]

df_clean = df.dropna(subset=["kalori", "protein", "lemak", "karbohidrat"])

# ─── HELPER: section header ──────────────────────────────────────────────────
def section_header(icon, title, badge=""):
    badge_html = f'<span class="section-badge">{badge}</span>' if badge else ""
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size:1.4rem;">{icon}</span>
        <h2>{title}</h2>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 1 — RINGKASAN EKSEKUTIF
# ═══════════════════════════════════════════════════════════════════════════════
if halaman == "🏠 Ringkasan Eksekutif":
    # Hero
    # Logo di hero pakai st.image dengan kolom agar tidak terlalu lebar
    _hc1, _hc2, _hc3 = st.columns([1, 2, 1])
    with _hc2:
        if os.path.exists(_LOGO_PATH):
            st.image(_LOGO_PATH, use_column_width="always")
    st.markdown("""
    <div style="padding: 8px 0 8px 0;">
        <div class="hero-title">GiSee</div>
        <div style="font-size:1rem; color:#8892b0; margin-top:4px; font-style:italic;">Gain Insight See Your Nutrition</div>
        <div class="hero-sub">Analisis komprehensif dataset TKPI + Indonesian Food and Drink Nutrition Dataset (Kaggle) • Data nutrisi per 100g bahan makanan</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    section_header("📈", "Ringkasan Dataset", "OVERVIEW")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    metrics = [
        ("Total Makanan", f"{len(df):,}", "entri unik", k1),
        ("Dish (Olahan)", f"{(df['jenis_makanan']=='dish').sum():,}", f"{(df['jenis_makanan']=='dish').mean()*100:.0f}% dari total", k2),
        ("Komponen", f"{(df['jenis_makanan']=='komponen').sum():,}", f"{(df['jenis_makanan']=='komponen').mean()*100:.0f}% dari total", k3),
        ("Rata-rata Kalori", f"{df_clean['kalori'].mean():.0f}", "kal/100g", k4),
        ("Rata-rata Protein", f"{df_clean['protein'].mean():.1f}g", "/100g", k5),
        ("Sumber Data", "2", "TKPI + Indonesian Food and Drink Nutrition Dataset (Kaggle)", k6),
    ]
    for label, val, delta, col in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Distribusi Jenis & Sumber ──────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        section_header("🥧", "Proporsi Jenis Makanan")
        jenis_counts = df["jenis_makanan"].value_counts()
        fig_pie = px.pie(
            values=jenis_counts.values,
            names=jenis_counts.index,
            color_discrete_sequence=["#ff7043", "#2ecc87"],
            hole=0.55,
        )
        fig_pie.update_traces(
            textinfo="percent+label",
            textfont_size=12,
            marker=dict(line=dict(color="#0d0f1a", width=3)),
        )
        fig_pie.update_layout(
            paper_bgcolor=CHART_PAPER, plot_bgcolor=CHART_BG,
            font=dict(color=FONT_COLOR, family="Plus Jakarta Sans"),
            height=320, margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True, legend=dict(bgcolor="rgba(0,0,0,0)"),
            annotations=[dict(text=f"<b>{len(df)}</b><br><span style='font-size:10px'>makanan</span>",
                              x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#e8eaf6")]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        section_header("📦", "Distribusi Sumber Data")
        src_counts = df["source"].value_counts()
        fig_bar = go.Figure(go.Bar(
            x=src_counts.index,
            y=src_counts.values,
            marker=dict(
                color=["#4f9cf9", "#2ecc87"],
                line=dict(color="#0d0f1a", width=1.5)
            ),
            text=src_counts.values,
            textposition="outside",
            textfont=dict(color=FONT_COLOR, size=13, family="Plus Jakarta Sans"),
        ))
        fig_bar = apply_theme(fig_bar, height=320)
        fig_bar.update_layout(showlegend=False, xaxis_title="", yaxis_title="Jumlah Item")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Row 2: Distribusi Kalori & Protein ────────────────────────────────────
    c3, c4 = st.columns(2)
    with c3:
        section_header("🔥", "Distribusi Kalori")
        fig_cal = px.histogram(
            df_clean, x="kalori", nbins=40,
            color="jenis_makanan",
            color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"},
            barmode="overlay", opacity=0.75,
        )
        fig_cal = apply_theme(fig_cal, height=310)
        fig_cal.update_layout(
            xaxis_title="Kalori (kal/100g)", yaxis_title="Frekuensi",
            legend_title="Jenis"
        )
        st.plotly_chart(fig_cal, use_container_width=True)

    with c4:
        section_header("💪", "Distribusi Protein")
        fig_pro = px.histogram(
            df_clean, x="protein", nbins=40,
            color="jenis_makanan",
            color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"},
            barmode="overlay", opacity=0.75,
        )
        fig_pro = apply_theme(fig_pro, height=310)
        fig_pro.update_layout(
            xaxis_title="Protein (g/100g)", yaxis_title="Frekuensi",
            legend_title="Jenis"
        )
        st.plotly_chart(fig_pro, use_container_width=True)

    # ── Statistik Deskriptif ──────────────────────────────────────────────────
    section_header("📐", "Statistik Deskriptif", "RINGKASAN STATISTIK")

    stat_cols = ["kalori", "protein", "lemak", "karbohidrat"]
    stat_df = df_clean[stat_cols].describe().round(2).T
    stat_df.columns = ["N", "Rata-rata", "Std Dev", "Min", "Q1 (25%)", "Median (50%)", "Q3 (75%)", "Maks"]
    stat_df.index = ["Kalori (kal)", "Protein (g)", "Lemak (g)", "Karbohidrat (g)"]
    st.dataframe(stat_df, use_container_width=True)

    # ── Profil rata-rata dish vs komponen ─────────────────────────────────────
    section_header("⚖️", "Profil Gizi: Dish vs Komponen", "BQ5 PREVIEW")

    profil = df_clean.groupby("jenis_makanan")[stat_cols].mean().round(1).reset_index()
    fig_grouped = go.Figure()
    macros = ["kalori", "protein", "lemak", "karbohidrat"]
    labels = ["Kalori", "Protein", "Lemak", "Karbohidrat"]
    colors_macro = ["#f1c40f", "#4f9cf9", "#ff7043", "#2ecc87"]
    for jenis, row in profil.iterrows():
        pass

    for i, (macro, label, color) in enumerate(zip(macros, labels, colors_macro)):
        for _, row in profil.iterrows():
            fig_grouped.add_trace(go.Bar(
                name=f"{label} — {row['jenis_makanan']}",
                x=[row["jenis_makanan"]],
                y=[row[macro]],
                marker_color=color,
                opacity=0.9 if row["jenis_makanan"] == "dish" else 0.55,
                legendgroup=label,
                showlegend=(i == 0),
                text=[f"{row[macro]:.1f}"],
                textposition="outside",
            ))

    # Simplified profil chart
    melted = profil.melt(id_vars="jenis_makanan", value_vars=stat_cols,
                         var_name="Nutrisi", value_name="Nilai")
    nutrisi_labels = {"kalori": "Kalori (kal)", "protein": "Protein (g)",
                       "lemak": "Lemak (g)", "karbohidrat": "Karbohidrat (g)"}
    melted["Nutrisi"] = melted["Nutrisi"].map(nutrisi_labels)
    fig_profile = px.bar(
        melted, x="Nutrisi", y="Nilai",
        color="jenis_makanan", barmode="group",
        color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"},
        text="Nilai",
    )
    fig_profile.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_profile = apply_theme(fig_profile, height=350)
    fig_profile.update_layout(
        xaxis_title="", yaxis_title="Nilai Rata-rata",
        legend_title="Jenis Makanan",
    )
    st.plotly_chart(fig_profile, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 2 — EKSPLORASI DATA
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🔬 Eksplorasi Data":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">🔬 Eksplorasi Data Nutrisi</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Visualisasi distribusi dan hubungan antar fitur</div><br>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribusi", "🔗 Korelasi & Heatmap", "🗺️ Scatter Plot", "📦 Box Plot"])

    with tab1:
        section_header("📊", "Distribusi Zat Gizi per Kategori")
        col_sel = st.selectbox(
            "Pilih nutrisi",
            ["kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"],
            format_func=lambda x: {"kalori": "Kalori (kal/100g)", "protein": "Protein (g/100g)",
                                    "lemak": "Lemak (g/100g)", "karbohidrat": "Karbohidrat (g/100g)",
                                    "macro_balance_score": "Macro Balance Score"}[x]
        )

        c1, c2 = st.columns([2, 1])
        with c1:
            fig_dist = px.histogram(
                df_clean, x=col_sel, nbins=50,
                color="jenis_makanan",
                color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"},
                marginal="violin", barmode="overlay", opacity=0.7,
            )
            fig_dist = apply_theme(fig_dist, height=400)
            fig_dist.update_layout(legend_title="Jenis Makanan")
            st.plotly_chart(fig_dist, use_container_width=True)

        with c2:
            # Stats card
            for jenis in ["dish", "komponen"]:
                sub = df_clean[df_clean["jenis_makanan"] == jenis][col_sel]
                color = "#ff7043" if jenis == "dish" else "#2ecc87"
                st.markdown(f"""
                <div style="background:#1a1d2e; border:1px solid rgba(255,255,255,0.07);
                            border-radius:12px; padding:16px; margin-bottom:12px;
                            border-left: 3px solid {color};">
                    <div style="color:{color}; font-weight:700; text-transform:uppercase;
                                font-size:0.72rem; letter-spacing:1px; margin-bottom:10px;">{jenis}</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:0.82rem;">
                        <div><span style="color:#8892b0;">Mean:</span> <b>{sub.mean():.2f}</b></div>
                        <div><span style="color:#8892b0;">Median:</span> <b>{sub.median():.2f}</b></div>
                        <div><span style="color:#8892b0;">Min:</span> <b>{sub.min():.2f}</b></div>
                        <div><span style="color:#8892b0;">Max:</span> <b>{sub.max():.2f}</b></div>
                        <div><span style="color:#8892b0;">Std:</span> <b>{sub.std():.2f}</b></div>
                        <div><span style="color:#8892b0;">Q75:</span> <b>{sub.quantile(0.75):.2f}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Distribusi per sumber
        section_header("📦", "Distribusi per Sumber Dataset")
        fig_src = px.violin(
            df_clean, x="source", y=col_sel, color="source",
            color_discrete_map={"TKPI": "#4f9cf9", "Indonesian Food and Drink Nutrition Dataset (Kaggle)": "#9b59b6"},
            box=True, points="outliers",
        )
        fig_src = apply_theme(fig_src, height=350)
        fig_src.update_layout(xaxis_title="Sumber", legend_title="Sumber")
        st.plotly_chart(fig_src, use_container_width=True)

    with tab2:
        section_header("🔗", "Heatmap Korelasi Makronutrien", "BQ4")

        corr_cols = ["kalori", "protein", "lemak", "karbohidrat",
                     "protein_per_calorie", "macro_balance_score"]
        corr_labels = ["Kalori", "Protein", "Lemak", "Karbohidrat",
                        "Protein/Kal", "Balance Score"]

        corr_df = df_clean[corr_cols].copy()
        corr_df.columns = corr_labels
        # Clip outliers for cleaner correlation
        for col in ["Protein/Kal"]:
            corr_df[col] = corr_df[col].clip(upper=corr_df[col].quantile(0.99))

        corr_matrix = corr_df.corr().round(3)

        fig_heatmap = px.imshow(
            corr_matrix,
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            text_auto=".2f",
            aspect="auto",
        )
        fig_heatmap.update_traces(textfont_size=12, textfont_color="white")
        fig_heatmap = apply_theme(fig_heatmap, height=450)
        fig_heatmap.update_layout(
            coloraxis_colorbar=dict(title="Korelasi", tickfont_color=FONT_COLOR),
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.markdown("""
        <div class="info-box">
        💡 <b>Temuan BQ4:</b> Lemak memiliki korelasi terkuat terhadap kalori (r ≈ 0.75), diikuti Karbohidrat (r ≈ 0.45) dan Protein (r ≈ 0.37).
        Ini selaras dengan teori gizi — lemak memiliki densitas energi 9 kal/g vs protein & karbohidrat 4 kal/g.
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        section_header("🗺️", "Scatter Plot Interaktif")
        col1, col2, col3 = st.columns(3)
        with col1:
            x_axis = st.selectbox("Sumbu X", ["kalori", "protein", "lemak", "karbohidrat",
                                               "protein_per_calorie", "macro_balance_score"],
                                   index=0, key="scatter_x")
        with col2:
            y_axis = st.selectbox("Sumbu Y", ["kalori", "protein", "lemak", "karbohidrat",
                                               "protein_per_calorie", "macro_balance_score"],
                                   index=1, key="scatter_y")
        with col3:
            color_by = st.selectbox("Warna berdasarkan", ["jenis_makanan", "source"], key="scatter_color")

        df_scatter = df_clean.copy()
        # Clip extreme values for readability
        for col in ["protein_per_calorie", "fat_per_calorie", "protein_fat_ratio"]:
            if col in df_scatter.columns:
                df_scatter[col] = df_scatter[col].clip(upper=df_scatter[col].quantile(0.99))

        fig_scatter = px.scatter(
            df_scatter, x=x_axis, y=y_axis,
            color=color_by,
            hover_name="nama_makanan",
            hover_data={"kalori": True, "protein": True, "lemak": True, "karbohidrat": True},
            color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87",
                                  "TKPI": "#4f9cf9", "Indonesian Food and Drink Nutrition Dataset (Kaggle)": "#9b59b6"},
            size_max=8, opacity=0.7,
        )
        # Trendline manual pakai numpy (tanpa statsmodels)
        _x = df_scatter[x_axis].dropna()
        _y = df_scatter[y_axis].dropna()
        _idx = _x.index.intersection(_y.index)
        if len(_idx) > 2:
            _xv, _yv = _x[_idx].values, _y[_idx].values
            _m, _b = np.polyfit(_xv, _yv, 1)
            _xl = np.linspace(_xv.min(), _xv.max(), 200)
            fig_scatter.add_trace(go.Scatter(
                x=_xl, y=_m * _xl + _b,
                mode="lines", name="Trendline",
                line=dict(color="#f1c40f", width=2, dash="dash"),
                showlegend=True,
            ))
        fig_scatter = apply_theme(fig_scatter, height=500)
        fig_scatter.update_traces(selector=dict(mode="markers"), marker=dict(size=6))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab4:
        section_header("📦", "Box Plot Perbandingan")
        nutrisi_sel = st.multiselect(
            "Pilih nutrisi untuk dibandingkan",
            ["kalori", "protein", "lemak", "karbohidrat"],
            default=["kalori", "protein", "lemak", "karbohidrat"],
            key="boxplot_sel"
        )
        group_by = st.radio("Kelompokkan berdasarkan", ["jenis_makanan", "source"],
                            horizontal=True, key="box_group")

        if nutrisi_sel:
            fig_box = go.Figure()
            color_map = {"dish": "#ff7043", "komponen": "#2ecc87",
                          "TKPI": "#4f9cf9", "Indonesian Food and Drink Nutrition Dataset (Kaggle)": "#9b59b6"}
            for grp in df_clean[group_by].unique():
                sub = df_clean[df_clean[group_by] == grp]
                for nutrisi in nutrisi_sel:
                    data = sub[nutrisi].clip(upper=sub[nutrisi].quantile(0.98))
                    fig_box.add_trace(go.Box(
                        y=data,
                        name=f"{grp} | {nutrisi}",
                        marker_color=color_map.get(grp, "#aaa"),
                        boxpoints="outliers",
                        jitter=0.3,
                        pointpos=-1.8,
                    ))
            fig_box = apply_theme(fig_box, height=480)
            fig_box.update_layout(xaxis_title="", yaxis_title="Nilai (g atau kal/100g)")
            st.plotly_chart(fig_box, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 3 — ANALISIS BQ (BUSINESS QUESTIONS)
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📊 Analisis BQ":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">📊 Pertanyaan Bisnis (BQ)</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Jawaban empiris dari 5 pertanyaan bisnis utama</div><br>', unsafe_allow_html=True)

    bq_tab = st.tabs(["BQ1 — Protein Tertinggi", "BQ2 — Efisiensi Protein",
                       "BQ3 — Kepadatan Energi", "BQ4 — Korelasi Kalori",
                       "BQ5 — Dish vs Komponen"])

    # ── BQ1 ──────────────────────────────────────────────────────────────────
    with bq_tab[0]:
        section_header("💪", "Makanan dengan Protein Tertinggi (per 100g)", "BQ1")
        n_top = st.slider("Tampilkan top-N", 5, 30, 10, key="bq1_n")
        top_protein = df_clean.nlargest(n_top, "protein")[
            ["nama_makanan", "jenis_makanan", "protein", "kalori", "lemak", "karbohidrat", "source"]
        ]
        fig_bq1 = px.bar(
            top_protein.iloc[::-1],
            x="protein", y="nama_makanan",
            color="jenis_makanan",
            color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"},
            orientation="h",
            hover_data={"kalori": True, "lemak": True, "karbohidrat": True},
            text="protein",
        )
        fig_bq1.update_traces(texttemplate="%{text:.1f}g", textposition="outside")
        fig_bq1 = apply_theme(fig_bq1, height=max(380, n_top * 38))
        fig_bq1.update_layout(
            xaxis_title="Protein (g/100g)", yaxis_title="",
            legend_title="Jenis Makanan", yaxis=dict(tickfont=dict(size=11))
        )
        st.plotly_chart(fig_bq1, use_container_width=True)

        st.markdown("""
        <div class="warning-box">
        🔍 <b>Insight:</b> Dominasi produk kering/dehidrasi seperti kerupuk kulit, ikan kering, dan udang kering.
        Proses dehidrasi menghilangkan air sehingga konsentrasi protein per 100g menjadi sangat tinggi.
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 Lihat tabel detail"):
            st.dataframe(top_protein.reset_index(drop=True), use_container_width=True)

    # ── BQ2 ──────────────────────────────────────────────────────────────────
    with bq_tab[1]:
        section_header("⚡", "Efisiensi Protein (Protein per Kalori) — Dish Only", "BQ2")

        jenis_bq2 = st.radio("Filter jenis", ["dish", "komponen", "Semua"], horizontal=True, key="bq2_jenis")
        n_bq2 = st.slider("Top-N", 5, 25, 10, key="bq2_n")

        df_bq2 = df_clean.copy()
        if jenis_bq2 != "Semua":
            df_bq2 = df_bq2[df_bq2["jenis_makanan"] == jenis_bq2]

        df_bq2["ppc_clipped"] = df_bq2["protein_per_calorie"].clip(
            upper=df_bq2["protein_per_calorie"].quantile(0.99)
        )
        top_ratio = df_bq2.nlargest(n_bq2, "ppc_clipped")[
            ["nama_makanan", "protein", "kalori", "ppc_clipped", "jenis_makanan", "source"]
        ].rename(columns={"ppc_clipped": "protein_per_calorie"})

        fig_bq2 = px.bar(
            top_ratio.iloc[::-1],
            x="protein_per_calorie", y="nama_makanan",
            color="jenis_makanan",
            color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"},
            orientation="h",
            hover_data={"protein": True, "kalori": True},
            text="protein_per_calorie",
        )
        fig_bq2.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig_bq2 = apply_theme(fig_bq2, height=max(380, n_bq2 * 38))
        fig_bq2.update_layout(
            xaxis_title="Rasio Protein per Kalori (g/kal)",
            yaxis_title="", legend_title="Jenis",
            yaxis=dict(tickfont=dict(size=11))
        )
        st.plotly_chart(fig_bq2, use_container_width=True)

        st.markdown("""
        <div class="info-box">
        💡 <b>Insight:</b> Hidangan ikan kuah rendah kalori seperti pindang dan ikan gabus kering memiliki 
        efisiensi protein tertinggi. Ideal untuk program diet tinggi protein rendah kalori.
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 Lihat tabel detail"):
            st.dataframe(top_ratio.reset_index(drop=True), use_container_width=True)

    # ── BQ3 ──────────────────────────────────────────────────────────────────
    with bq_tab[2]:
        section_header("🔥", "Kepadatan Energi Tertinggi (Kalori per 100g)", "BQ3")

        n_bq3 = st.slider("Top-N", 5, 25, 10, key="bq3_n")
        top_cal = df_clean.nlargest(n_bq3, "kalori")[
            ["nama_makanan", "jenis_makanan", "kalori", "lemak", "protein", "karbohidrat", "source"]
        ]

        fig_bq3 = px.bar(
            top_cal.iloc[::-1],
            x="kalori", y="nama_makanan",
            color="kalori",
            color_continuous_scale=["#2ecc87", "#f1c40f", "#ff7043", "#e74c3c"],
            orientation="h",
            hover_data={"lemak": True, "protein": True, "karbohidrat": True},
            text="kalori",
        )
        fig_bq3.update_traces(texttemplate="%{text:.0f} kal", textposition="outside")
        fig_bq3 = apply_theme(fig_bq3, height=max(380, n_bq3 * 38))
        fig_bq3.update_layout(
            xaxis_title="Kalori (kal/100g)", yaxis_title="",
            coloraxis_colorbar=dict(title="Kal", tickfont_color=FONT_COLOR),
            yaxis=dict(tickfont=dict(size=11))
        )
        st.plotly_chart(fig_bq3, use_container_width=True)

        # Sunburst untuk kepadatan energi
        st.markdown("#### Distribusi Kepadatan Energi per Kelompok")
        if "kelompok" in df_clean.columns:
            grp_cal = df_clean.groupby("kelompok")["kalori"].mean().round(1).reset_index()
            grp_cal.columns = ["Kelompok", "Rata-rata Kalori"]
            grp_cal = grp_cal.sort_values("Rata-rata Kalori", ascending=False)
            fig_grp = px.bar(
                grp_cal, x="Rata-rata Kalori", y="Kelompok",
                orientation="h", text="Rata-rata Kalori",
                color="Rata-rata Kalori",
                color_continuous_scale=["#2ecc87", "#f1c40f", "#e74c3c"],
            )
            fig_grp.update_traces(texttemplate="%{text:.0f}", textposition="outside")
            fig_grp = apply_theme(fig_grp, height=400)
            fig_grp.update_layout(
                xaxis_title="Kalori rata-rata (kal/100g)", yaxis_title="",
                coloraxis_showscale=False,
                yaxis=dict(tickfont=dict(size=10))
            )
            st.plotly_chart(fig_grp, use_container_width=True)

        with st.expander("📋 Lihat tabel detail"):
            st.dataframe(top_cal.reset_index(drop=True), use_container_width=True)

    # ── BQ4 ──────────────────────────────────────────────────────────────────
    with bq_tab[3]:
        section_header("🔗", "Korelasi Makronutrien terhadap Kalori", "BQ4")

        corr_df_bq4 = df_clean[["kalori", "protein", "lemak", "karbohidrat"]].copy()
        corr_values = corr_df_bq4.corr()["kalori"].drop("kalori").sort_values(ascending=False)

        c1, c2 = st.columns([1, 2])
        with c1:
            # Korelasi bar
            colors_corr = ["#2ecc87" if v > 0 else "#ff7043" for v in corr_values]
            fig_corr_bar = go.Figure(go.Bar(
                x=corr_values.values,
                y=["Lemak", "Karbohidrat", "Protein"],
                orientation="h",
                marker_color=colors_corr,
                text=[f"r = {v:.3f}" for v in corr_values.values],
                textposition="outside",
            ))
            fig_corr_bar = apply_theme(fig_corr_bar, height=280)
            fig_corr_bar.update_layout(
                xaxis_title="Koefisien Korelasi Pearson",
                xaxis_range=[-0.1, 1.0],
                showlegend=False
            )
            st.plotly_chart(fig_corr_bar, use_container_width=True)

            st.markdown(f"""
            <div style="background:#1a1d2e; border-radius:12px; padding:16px; font-size:0.85rem;">
            <div style="color:#2ecc87; font-weight:700; margin-bottom:10px;">📊 Hasil Korelasi</div>
            <div>🏆 <b>Lemak</b>: r = {corr_df_bq4.corr().loc['kalori','lemak']:.3f}</div>
            <div style="margin-top:6px;">🥈 <b>Karbohidrat</b>: r = {corr_df_bq4.corr().loc['kalori','karbohidrat']:.3f}</div>
            <div style="margin-top:6px;">🥉 <b>Protein</b>: r = {corr_df_bq4.corr().loc['kalori','protein']:.3f}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            # Scatter tiap makro vs kalori
            macro_sel = st.selectbox("Visualisasikan hubungan:", ["lemak", "karbohidrat", "protein"], key="bq4_macro")
            df_bq4_plot = df_clean.copy()
            df_bq4_plot[macro_sel] = df_bq4_plot[macro_sel].clip(upper=df_bq4_plot[macro_sel].quantile(0.99))
            df_bq4_plot["kalori"] = df_bq4_plot["kalori"].clip(upper=df_bq4_plot["kalori"].quantile(0.99))

            fig_scatter_bq4 = px.scatter(
                df_bq4_plot, x=macro_sel, y="kalori",
                color="jenis_makanan",
                color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"},
                hover_name="nama_makanan",
                opacity=0.65,
            )
            # Trendline manual per jenis_makanan (tanpa statsmodels)
            for jenis, color in [("dish", "#ff7043"), ("komponen", "#2ecc87")]:
                _sub = df_bq4_plot[df_bq4_plot["jenis_makanan"] == jenis]
                _xv = _sub[macro_sel].dropna().values
                _yv = _sub.loc[_sub[macro_sel].notna(), "kalori"].values
                if len(_xv) > 2:
                    _m, _b = np.polyfit(_xv, _yv, 1)
                    _xl = np.linspace(_xv.min(), _xv.max(), 200)
                    fig_scatter_bq4.add_trace(go.Scatter(
                        x=_xl, y=_m * _xl + _b,
                        mode="lines", name=f"Trend {jenis}",
                        line=dict(color=color, width=2, dash="dash"),
                        showlegend=True,
                    ))
            fig_scatter_bq4 = apply_theme(fig_scatter_bq4, height=380)
            fig_scatter_bq4.update_layout(
                xaxis_title=f"{macro_sel.capitalize()} (g/100g)",
                yaxis_title="Kalori (kal/100g)",
                legend_title="Jenis"
            )
            st.plotly_chart(fig_scatter_bq4, use_container_width=True)

    # ── BQ5 ──────────────────────────────────────────────────────────────────
    with bq_tab[4]:
        section_header("⚖️", "Perbandingan Profil Nutrisi: Dish vs Komponen", "BQ5")

        profil_bq5 = df_clean.groupby("jenis_makanan")[
            ["kalori", "protein", "lemak", "karbohidrat"]
        ].agg(["mean", "median", "std"]).round(2)

        # Radar chart
        categories = ["Kalori/10", "Protein", "Lemak", "Karbohidrat"]
        fig_radar = go.Figure()
        for jenis, color in [("dish", "#ff7043"), ("komponen", "#2ecc87")]:
            sub = df_clean[df_clean["jenis_makanan"] == jenis]
            values = [
                sub["kalori"].mean() / 10,
                sub["protein"].mean(),
                sub["lemak"].mean(),
                sub["karbohidrat"].mean(),
            ]
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill="toself",
                name=jenis.capitalize(),
                line=dict(color=color, width=2),
                fillcolor=hex_to_rgba(color, 0.15),
                opacity=0.8,
            ))

        fig_radar.update_layout(
            polar=dict(
                bgcolor="#1a1d2e",
                radialaxis=dict(visible=True, color="#8892b0", gridcolor=GRID_COLOR),
                angularaxis=dict(color=FONT_COLOR, gridcolor=GRID_COLOR),
            ),
            paper_bgcolor=CHART_PAPER,
            font=dict(color=FONT_COLOR, family="Plus Jakarta Sans"),
            height=400, margin=dict(l=40, r=40, t=40, b=40),
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            st.plotly_chart(fig_radar, use_container_width=True)

        with c2:
            # Side-by-side comparison
            cols_compare = ["kalori", "protein", "lemak", "karbohidrat"]
            labels_compare = ["Kalori (kal)", "Protein (g)", "Lemak (g)", "Karbohidrat (g)"]
            dish_means = df_clean[df_clean["jenis_makanan"] == "dish"][cols_compare].mean().round(1)
            komp_means = df_clean[df_clean["jenis_makanan"] == "komponen"][cols_compare].mean().round(1)

            st.markdown("#### Rata-rata per 100g")
            for col, label in zip(cols_compare, labels_compare):
                d_val = dish_means[col]
                k_val = komp_means[col]
                delta = ((d_val - k_val) / (k_val + 1e-6)) * 100
                delta_str = f"+{delta:.0f}%" if delta > 0 else f"{delta:.0f}%"
                delta_color = "#ff7043" if delta > 0 else "#2ecc87"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            padding:10px 14px; background:#1a1d2e; border-radius:10px; margin-bottom:8px;">
                    <span style="color:#8892b0; font-size:0.8rem; width:110px;">{label}</span>
                    <span style="color:#ff7043; font-weight:700;">Dish: {d_val}</span>
                    <span style="color:#2ecc87; font-weight:700;">Komponen: {k_val}</span>
                    <span style="color:{delta_color}; font-size:0.75rem; font-weight:600;">{delta_str}</span>
                </div>
                """, unsafe_allow_html=True)

        # Tabel profil lengkap
        st.markdown("#### Tabel Statistik Lengkap")
        profil_display = df_clean.groupby("jenis_makanan")[
            ["kalori", "protein", "lemak", "karbohidrat"]
        ].describe().round(2)
        st.dataframe(profil_display, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 4 — KOMPARASI MAKANAN
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🥗 Komparasi Makanan":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">🥗 Komparasi & Cari Makanan</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Bandingkan profil nutrisi berbagai makanan secara interaktif</div><br>', unsafe_allow_html=True)

    tab_comp, tab_search, tab_rank = st.tabs(["⚖️ Komparasi", "🔍 Cari Makanan", "🏆 Ranking"])

    with tab_comp:
        section_header("⚖️", "Bandingkan Profil Nutrisi")
        all_foods = sorted(df_clean["nama_makanan"].unique().tolist())
        selected_foods = st.multiselect(
            "Pilih makanan untuk dibandingkan (maks 8):",
            all_foods,
            default=all_foods[:5] if len(all_foods) >= 5 else all_foods[:3],
            max_selections=8,
            key="comp_foods"
        )

        if selected_foods:
            df_comp = df_clean[df_clean["nama_makanan"].isin(selected_foods)]

            # Grouped bar chart
            melted_comp = df_comp.melt(
                id_vars="nama_makanan",
                value_vars=["kalori", "protein", "lemak", "karbohidrat"],
                var_name="Nutrisi", value_name="Nilai"
            )
            nutrisi_labels = {"kalori": "Kalori (kal)", "protein": "Protein (g)",
                               "lemak": "Lemak (g)", "karbohidrat": "Karbohidrat (g)"}
            melted_comp["Nutrisi"] = melted_comp["Nutrisi"].map(nutrisi_labels)

            fig_comp = px.bar(
                melted_comp, x="Nutrisi", y="Nilai",
                color="nama_makanan",
                barmode="group",
                text="Nilai",
                color_discrete_sequence=PALETTE,
            )
            fig_comp.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig_comp = apply_theme(fig_comp, height=480)
            fig_comp.update_layout(
                xaxis_title="", yaxis_title="Nilai per 100g",
                legend_title="Makanan",
            )
            st.plotly_chart(fig_comp, use_container_width=True)

            # Radar chart komparasi
            st.markdown("#### Radar Chart Perbandingan")
            fig_radar_comp = go.Figure()
            cats = ["Kalori/10", "Protein", "Lemak", "Karbohidrat", "Balance×10"]

            for i, food in enumerate(selected_foods):
                row = df_comp[df_comp["nama_makanan"] == food].iloc[0] if not df_comp[df_comp["nama_makanan"] == food].empty else None
                if row is not None:
                    vals = [
                        row["kalori"] / 10,
                        row["protein"],
                        row["lemak"],
                        row["karbohidrat"],
                        (row.get("macro_balance_score", 0) or 0) * 10,
                    ]
                    color = PALETTE[i % len(PALETTE)]
                    fig_radar_comp.add_trace(go.Scatterpolar(
                        r=vals + [vals[0]],
                        theta=cats + [cats[0]],
                        fill="toself",
                        name=food[:30],
                        line=dict(color=color, width=2),
                        opacity=0.75,
                    ))

            fig_radar_comp.update_layout(
                polar=dict(
                    bgcolor="#1a1d2e",
                    radialaxis=dict(visible=True, color="#8892b0", gridcolor=GRID_COLOR),
                    angularaxis=dict(color=FONT_COLOR, gridcolor=GRID_COLOR),
                ),
                paper_bgcolor=CHART_PAPER,
                font=dict(color=FONT_COLOR, family="Plus Jakarta Sans"),
                height=450, margin=dict(l=40, r=40, t=40, b=40),
                showlegend=True,
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_radar_comp, use_container_width=True)

            # Tabel komparasi
            st.markdown("#### Tabel Detail")
            show_cols = ["nama_makanan", "jenis_makanan", "source", "kalori",
                          "protein", "lemak", "karbohidrat", "macro_balance_score"]
            available_cols = [c for c in show_cols if c in df_comp.columns]
            st.dataframe(
                df_comp[available_cols].set_index("nama_makanan").round(2),
                use_container_width=True
            )
        else:
            st.info("Pilih minimal 2 makanan untuk membandingkan profil nutrisinya.")

    with tab_search:
        section_header("🔍", "Cari & Filter Makanan")

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            search_query = st.text_input("🔎 Cari nama makanan", placeholder="contoh: ayam, nasi, ikan...", key="search_q")
        with col_s2:
            filter_jenis = st.selectbox("Jenis", ["Semua", "dish", "komponen"], key="search_jenis")
        with col_s3:
            if "kelompok" in df_clean.columns:
                kelompok_list = ["Semua"] + sorted(df_clean["kelompok"].dropna().unique().tolist())
                filter_kelompok = st.selectbox("Kelompok", kelompok_list, key="search_kelompok")
            else:
                filter_kelompok = "Semua"

        col_s4, col_s5 = st.columns(2)
        with col_s4:
            sort_col = st.selectbox("Urutkan berdasarkan", ["kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"], key="sort_col")
        with col_s5:
            sort_asc = st.radio("Urutan", ["Terbesar ke terkecil", "Terkecil ke terbesar"], horizontal=True, key="sort_asc")

        df_search = df_clean.copy()
        if search_query:
            df_search = df_search[df_search["nama_makanan"].str.contains(search_query.lower(), na=False)]
        if filter_jenis != "Semua":
            df_search = df_search[df_search["jenis_makanan"] == filter_jenis]
        if filter_kelompok != "Semua" and "kelompok" in df_search.columns:
            df_search = df_search[df_search["kelompok"] == filter_kelompok]

        ascending = sort_asc == "Terkecil ke terbesar"
        df_search = df_search.sort_values(sort_col, ascending=ascending)

        st.markdown(f"**{len(df_search)} makanan ditemukan**")
        disp_cols = ["nama_makanan", "jenis_makanan", "source", "kalori",
                      "protein", "lemak", "karbohidrat"]
        if "kelompok" in df_search.columns:
            disp_cols.insert(2, "kelompok")
        disp_cols = [c for c in disp_cols if c in df_search.columns]
        st.dataframe(df_search[disp_cols].reset_index(drop=True).round(2),
                     use_container_width=True, height=500)

    with tab_rank:
        section_header("🏆", "Ranking Makanan per Kategori")

        rank_cat = st.selectbox(
            "Ranking berdasarkan",
            {
                "protein": "Protein Tertinggi (g/100g)",
                "kalori": "Kalori Tertinggi (kal/100g)",
                "lemak": "Lemak Tertinggi (g/100g)",
                "karbohidrat": "Karbohidrat Tertinggi (g/100g)",
                "macro_balance_score": "Keseimbangan Gizi Terbaik",
                "protein_per_calorie": "Efisiensi Protein (per kalori)",
            },
            format_func=lambda x: {
                "protein": "💪 Protein Tertinggi",
                "kalori": "🔥 Kalori Tertinggi",
                "lemak": "🧈 Lemak Tertinggi",
                "karbohidrat": "🍚 Karbohidrat Tertinggi",
                "macro_balance_score": "⚖️ Keseimbangan Gizi Terbaik",
                "protein_per_calorie": "⚡ Efisiensi Protein",
            }[x],
            key="rank_cat"
        )

        top15 = df_clean.nlargest(15, rank_cat)
        if rank_cat == "protein_per_calorie":
            top15[rank_cat] = top15[rank_cat].clip(upper=top15[rank_cat].quantile(0.99))

        medals = ["🥇", "🥈", "🥉"] + ["#" + str(i) for i in range(4, 16)]
        for i, (_, row) in enumerate(top15.iterrows()):
            tag = '<span class="tag-dish">dish</span>' if row["jenis_makanan"] == "dish" else '<span class="tag-komponen">komponen</span>'
            val = row[rank_cat]
            val_fmt = f"{val:.3f}" if rank_cat in ["protein_per_calorie", "macro_balance_score"] else f"{val:.1f}"
            unit = "" if rank_cat in ["protein_per_calorie", "macro_balance_score"] else (
                " kal" if rank_cat == "kalori" else " g"
            )
            src_color = "#4f9cf9" if row["source"] == "tkpi" else "#9b59b6"
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:12px 16px;
                        background:#1a1d2e; border-radius:10px; margin-bottom:8px;
                        border-left: 3px solid {'#f1c40f' if i==0 else '#aaa' if i==1 else '#cd7f32' if i==2 else '#333'};">
                <span style="font-size:1.2rem; min-width:32px;">{medals[i]}</span>
                <span style="flex:1; font-weight:600; font-size:0.9rem;">{row['nama_makanan']}</span>
                {tag}
                <span style="color:{src_color}; font-size:0.72rem; font-weight:600; text-transform:uppercase;">{row['source']}</span>
                <span style="font-size:1.1rem; font-weight:800; color:#2ecc87; min-width:80px; text-align:right;">{val_fmt}{unit}</span>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 5 — TABEL DATA LENGKAP
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📋 Tabel Data Lengkap":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">📋 Tabel Data Lengkap</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Seluruh data dengan kolom fitur teknik dari notebook EDA</div><br>', unsafe_allow_html=True)

    # ── Kontrol kolom ─────────────────────────────────────────────────────────
    all_cols = df.columns.tolist()
    default_cols = ["id", "nama_makanan", "jenis_makanan", "source",
                     "kalori", "protein", "lemak", "karbohidrat",
                     "macro_balance_score", "protein_per_calorie"]
    default_cols = [c for c in default_cols if c in all_cols]

    col_select = st.multiselect("Tampilkan kolom:", all_cols, default=default_cols, key="col_sel_table")

    # ── Summary cards ─────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Baris", f"{len(df):,}")
    with m2:
        st.metric("Total Kolom", f"{len(col_select)}")
    with m3:
        st.metric("Dish", f"{(df['jenis_makanan']=='dish').sum():,}")
    with m4:
        st.metric("Komponen", f"{(df['jenis_makanan']=='komponen').sum():,}")

    st.divider()

    # ── Filter inline ─────────────────────────────────────────────────────────
    with st.expander("⚙️ Filter Tambahan", expanded=False):
        fc1, fc2 = st.columns(2)
        with fc1:
            min_cal_t, max_cal_t = st.slider(
                "Kalori", 0, int(df["kalori"].max()) + 10,
                (0, int(df["kalori"].max())), key="tbl_cal"
            )
        with fc2:
            min_prot_t, max_prot_t = st.slider(
                "Protein (g)", 0, int(df["protein"].max()) + 1,
                (0, int(df["protein"].max())), key="tbl_prot"
            )

        search_inline = st.text_input("🔎 Cari nama", key="tbl_search")

    df_table = df.copy()
    df_table = df_table[(df_table["kalori"] >= min_cal_t) & (df_table["kalori"] <= max_cal_t)]
    df_table = df_table[(df_table["protein"] >= min_prot_t) & (df_table["protein"] <= max_prot_t)]
    if search_inline:
        df_table = df_table[df_table["nama_makanan"].str.contains(search_inline.lower(), na=False)]

    st.markdown(f"**{len(df_table):,} baris ditampilkan** dari {len(df):,} total")

    if col_select:
        avail = [c for c in col_select if c in df_table.columns]
        st.dataframe(
            df_table[avail].reset_index(drop=True).round(4),
            use_container_width=True,
            height=550,
        )
    else:
        st.info("Pilih minimal 1 kolom untuk ditampilkan.")

    st.divider()

    # ── Data Dictionary ────────────────────────────────────────────────────────
    section_header("📖", "Data Dictionary — df_food")
    dict_data = {
        "Kolom": ["id", "nama_makanan", "jenis_makanan", "kalori", "protein",
                   "lemak", "karbohidrat", "source", "protein_per_calorie",
                   "fat_per_calorie", "carb_per_calorie", "protein_fat_ratio", "macro_balance_score"],
        "Tipe": ["int", "str", "str", "float", "float", "float", "float", "str",
                  "float", "float", "float", "float", "float"],
        "Satuan": ["-", "-", "dish/komponen", "kal/100g", "g/100g", "g/100g",
                    "g/100g", "TKPI/Indonesian Food and Drink Nutrition Dataset (Kaggle)", "g/kal", "g/kal", "g/kal", "rasio", "0–1"],
        "Deskripsi": [
            "ID unik per entri",
            "Nama bahan makanan/hidangan (sudah dinormalisasi lowercase)",
            "Kategori: 'dish' (makanan jadi) atau 'komponen' (bahan mentah/tunggal)",
            "Kandungan energi total per 100g",
            "Kandungan protein per 100g",
            "Kandungan lemak total per 100g",
            "Kandungan karbohidrat total per 100g",
            "Asal dataset: TKPI (Kemenkes RI) atau Indonesian Food and Drink Nutrition Dataset (Kaggle)",
            "Efisiensi protein = protein / kalori — makin tinggi makin baik untuk diet",
            "Densitas lemak terhadap kalori",
            "Densitas karbohidrat terhadap kalori",
            "Perbandingan protein vs lemak — tinggi = high-protein low-fat",
            "Keseimbangan distribusi makronutrien (0=tidak seimbang, 1=sangat seimbang)",
        ],
    }
    st.dataframe(pd.DataFrame(dict_data), use_container_width=True, hide_index=True)

    # ── Download ────────────────────────────────────────────────────────────────
    st.divider()
    section_header("⬇️", "Export Data")

    @st.cache_data
    def to_csv_bytes(dataframe):
        return dataframe.to_csv(index=False).encode("utf-8")

    csv_bytes = to_csv_bytes(df_table)
    st.download_button(
        label="⬇️ Download data sebagai CSV",
        data=csv_bytes,
        file_name="df_food_filtered.csv",
        mime="text/csv",
    )