"""
app.py — GiSee Dashboard | Gain Insight See Your Nutrition
Streamlit Cloud-ready • Bebas Error, Label Jelas & Urutan BQ Presisi
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
        margin=dict(l=20, r=40, t=40, b=40), # Margin diperluas
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    return fig

# ─── DATA LOADING & FEATURE ENGINEERING ─────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    csv_paths = ["df_food.csv", "data/df_food.csv"]
    df = None
    for path in csv_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
            
    if df is None:
        st.error("❌ File **df_food.csv** tidak ditemukan di root directory!")
        st.stop()

    eps = 1e-6
    if "protein_per_calorie" not in df.columns:
        df["protein_per_calorie"] = df["protein"] / (df["kalori"] + eps)
    if "fat_per_calorie" not in df.columns:
        df["fat_per_calorie"] = df["lemak"] / (df["kalori"] + eps)
    if "carb_per_calorie" not in df.columns:
        df["carb_per_calorie"] = df["karbohidrat"] / (df["kalori"] + eps)
    if "protein_fat_ratio" not in df.columns:
        df["protein_fat_ratio"] = df["protein"] / (df["lemak"] + eps)
        
    if "macro_balance_score" not in df.columns:
        macros = df[["protein", "lemak", "karbohidrat"]].values
        sums = macros.sum(axis=1, keepdims=True)
        sums_safe = np.where(sums < 0.1, 1.0, sums)
        p = macros / sums_safe
        stds = np.std(p, axis=1)
        balance_scores = 1.0 - stds
        balance_scores[sums.flatten() < 0.1] = np.nan
        df["macro_balance_score"] = balance_scores

    if "kelompok" not in df.columns:
        def _get_kelompok(name):
            n = str(name).lower()
            if any(k in n for k in ["ikan","bandeng","lele","gurame","gabus","kayu","udang","cumi","kepiting","kerang","mujahir","mujair","teri","sale"]):
                return "Ikan & Seafood"
            elif any(k in n for k in ["ayam","sapi","kambing","babi","daging","bakso","sosis","hati","dendeng","sayap","paha"]):
                return "Daging"
            elif "telur" in n:
                return "Telur"
            elif any(k in n for k in ["tempe","tahu","oncom","kacang","tolo"]):
                return "Kacang & Produk Olahan"
            elif any(k in n for k in ["pisang","mangga","pepaya","semangka","jeruk","alpukat","nanas","salak","rambutan","durian","jambu","sawo","manggis","belimbing"]):
                return "Buah"
            elif any(k in n for k in ["bayam","kangkung","wortel","tomat","buncis","terong","mentimun","labu","gambas","pare","kol","sawi","daun","taoge","toge","rebung"]):
                return "Sayuran"
            elif any(k in n for k in ["singkong","kentang","ubi","talas","tales"]):
                return "Umbi-umbian"
            elif any(k in n for k in ["beras","nasi","jagung","tepung","roti","mie","bihun","kwetiau","lontong","ketupat","bubur","gerontol","grontol"]):
                return "Serealia & Produk Olahan"
            elif any(k in n for k in ["minyak","mentega","margarin","santan","lard"]):
                return "Lemak & Minyak"
            elif any(k in n for k in ["gula","madu","dodol","kue","onde","wingko","wajit","kolak","opak"]):
                return "Gula & Permen"
            elif any(k in n for k in ["kopi","teh","jamu","sirup","minuman"]):
                return "Minuman"
            else:
                return "Makanan Olahan"
        df["kelompok"] = df["nama_makanan"].apply(_get_kelompok)
        
    return df

# ─── HELPER VIEW ELEMENTS ───────────────────────────────────────────────────
def section_header(icon, title, badge=""):
    badge_html = f'<span class="section-badge">{badge}</span>' if badge else ""
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size:1.4rem;">{icon}</span>
        <h2>{title}</h2>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
df_raw = load_data()
_LOGO_PATH = "assets/logo_gisee.png"

# ─── SIDEBAR FILTER GLOBAL ───────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists(_LOGO_PATH):
        st.image(_LOGO_PATH, use_column_width="always")
    else:
        st.markdown('<div style="text-align:center; font-family:Lora,serif; font-size:1.6rem; font-weight:700; color:#2ecc87; padding:16px 0 8px 0;">GiSee</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align:center; font-size:0.72rem; color:#8892b0; letter-spacing:2px; text-transform:uppercase; margin-bottom:20px;">Gain Insight See Your Nutrition</div>', unsafe_allow_html=True)

    st.markdown("### 🔍 Navigasi Halaman")
    halaman = st.selectbox(
        "Pilih Dashboard View",
        ["🏠 Ringkasan Executive", "🔬 Eksplorasi Data", "📊 Analisis BQ", "🥗 Komparasi Makanan", "📋 Tabel Data Lengkap"],
        key="nav_halaman"
    )

    st.divider()
    st.markdown("### ⚙️ Filter Dashboard Global")

    jenis_filter = st.selectbox("Jenis Klasifikasi Pangan", ["Semua", "dish", "komponen"], key="g_jenis_filter")
    
    available_sources = df_raw["source"].unique().tolist()
    source_filter = st.multiselect("Sumber Dataset Asal", available_sources, default=available_sources, key="g_source_filter")

    max_cal_val = int(df_raw["kalori"].max()) + 10
    max_prot_val = int(df_raw["protein"].max()) + 1
    
    kalori_range = st.slider("Range Batas Kalori (kal/100g)", 0, max_cal_val, (0, max_cal_val), step=10, key="g_kalori_range")
    protein_range = st.slider("Range Batas Protein (g/100g)", 0, max_prot_val, (0, max_prot_val), step=1, key="g_protein_range")

    st.divider()
    st.markdown("""
    <div style="font-size:0.72rem; color:#8892b0; line-height:1.8;">
    📌 <b>Informasi Standardisasi</b><br>
    • Seluruh metrik gizi dihitung berdasarkan takaran <b>per 100g</b> berat bersih bahan makanan.<br>
    • Aplikasi terintegrasi penuh dengan dataset TKPI Kemenkes RI & repositori publik Kaggle.
    </div>
    """, unsafe_allow_html=True)

df = df_raw.copy()
if jenis_filter != "Semua":
    df = df[df["jenis_makanan"] == jenis_filter]
if source_filter:
    df = df[df["source"].isin(source_filter)]
df = df[(df["kalori"] >= kalori_range[0]) & (df["kalori"] <= kalori_range[1])]
df = df[(df["protein"] >= protein_range[0]) & (df["protein"] <= protein_range[1])]

df_clean = df.dropna(subset=["kalori", "protein", "lemak", "karbohidrat"])

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — RINGKASAN EXECUTIVE
# ═══════════════════════════════════════════════════════════════════════════════
if halaman == "🏠 Ringkasan Executive":
    st.markdown("""
    <div style="padding: 4px 0 12px 0;">
        <div class="hero-title">GiSee Dashboard</div>
        <div class="hero-sub">Analisis Eksplanatori Integrasi Dataset Nutrisi Komposisi Pangan Indonesia (TKPI) & Kaggle</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # KPI Metric Cards
    section_header("📈", "Rangkuman Parameter Utama Dataset", "DATASET METRICS")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    
    with k1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df):,}</div><div class="metric-label">Total Kelas Makanan</div><div class="metric-delta">Entri Unik</div></div>', unsafe_allow_html=True)
    with k2:
        dish_count = (df['jenis_makanan']=='dish').sum()
        dish_pct = (df['jenis_makanan']=='dish').mean() * 100 if len(df) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value">{dish_count:,}</div><div class="metric-label">Hidangan Jadi (Dish)</div><div class="metric-delta">{dish_pct:.0f}% Proporsi</div></div>', unsafe_allow_html=True)
    with k3:
        comp_count = (df['jenis_makanan']=='komponen').sum()
        comp_pct = (df['jenis_makanan']=='komponen').mean() * 100 if len(df) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value">{comp_count:,}</div><div class="metric-label">Bahan Baku (Komponen)</div><div class="metric-delta">{comp_pct:.0f}% Proporsi</div></div>', unsafe_allow_html=True)
    with k4:
        avg_cal = df_clean['kalori'].mean() if len(df_clean) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value">{avg_cal:.0f}</div><div class="metric-label">Rerata Energi Total</div><div class="metric-delta">Kkal / 100g</div></div>', unsafe_allow_html=True)
    with k5:
        avg_prot = df_clean['protein'].mean() if len(df_clean) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value">{avg_prot:.1f}g</div><div class="metric-label">Rerata Protein</div><div class="metric-delta">Gram / 100g</div></div>', unsafe_allow_html=True)
    with k6:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{df["source"].nunique()}</div><div class="metric-label">Pilar Sumber Data</div><div class="metric-delta">TKPI + Kaggle</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        section_header("🥧", "Komposisi Berdasarkan Kategori")
        if len(df) > 0:
            jenis_counts = df["jenis_makanan"].value_counts()
            fig_pie = px.pie(
                values=jenis_counts.values, names=jenis_counts.index,
                color_discrete_sequence=["#ff7043", "#2ecc87"], hole=0.55
            )
            fig_pie.update_traces(textinfo="percent+label", marker=dict(line=dict(color="#0d0f1a", width=3)))
            fig_pie.update_layout(
                paper_bgcolor=CHART_PAPER, plot_bgcolor=CHART_BG, font=dict(color=FONT_COLOR),
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                annotations=[dict(text=f"<b>{len(df)}</b><br><span style='font-size:10px'>Total</span>", x=0.5, y=0.5, font_size=15, showarrow=False)]
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Tidak ada data untuk dirender.")

    with c2:
        section_header("📦", "Volume Data per Sumber")
        if len(df) > 0:
            src_counts = df["source"].value_counts()
            fig_bar = go.Figure(go.Bar(
                x=src_counts.index, y=src_counts.values,
                marker=dict(color=["#4f9cf9", "#9b59b6"], line=dict(color="#0d0f1a", width=1)),
                text=src_counts.values, textposition="outside"
            ))
            fig_bar = apply_theme(fig_bar, height=320, showlegend=False)
            fig_bar.update_yaxes(range=[0, max(src_counts.values) * 1.15]) # Perbaikan label terpotong
            st.plotly_chart(fig_bar, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        section_header("🔥", "Sebaran Kepadatan Kalori")
        if len(df_clean) > 0:
            fig_cal = px.histogram(df_clean, x="kalori", color="jenis_makanan", barmode="overlay", opacity=0.7, color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"})
            fig_cal = apply_theme(fig_cal, height=310)
            st.plotly_chart(fig_cal, use_container_width=True)

    with c4:
        section_header("💪", "Sebaran Kepadatan Protein")
        if len(df_clean) > 0:
            fig_pro = px.histogram(df_clean, x="protein", color="jenis_makanan", barmode="overlay", opacity=0.7, color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"})
            fig_pro = apply_theme(fig_pro, height=310)
            st.plotly_chart(fig_pro, use_container_width=True)

    section_header("⚖️", "Profil Gizi Makro Rata-rata: Dish vs Komponen", "BQ5 PREVIEW")
    if len(df_clean) > 0:
        stat_cols = ["kalori", "protein", "lemak", "karbohidrat"]
        profil_mean = df_clean.groupby("jenis_makanan")[stat_cols].mean().round(1).reset_index()
        melted = profil_mean.melt(id_vars="jenis_makanan", value_vars=stat_cols, var_name="Nutrisi", value_name="Nilai")
        nutrisi_labels = {"kalori": "Kalori (kal)", "protein": "Protein (g)", "lemak": "Lemak (g)", "karbohidrat": "Karbohidrat (g)"}
        melted["Nutrisi"] = melted["Nutrisi"].map(nutrisi_labels)
        
        fig_profile = px.bar(
            melted, x="Nutrisi", y="Nilai", color="jenis_makanan", barmode="group",
            color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"}, text="Nilai"
        )
        fig_profile.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_profile = apply_theme(fig_profile, height=350)
        fig_profile.update_layout(xaxis_title="", yaxis_title="Nilai Rata-rata", legend_title="Jenis Pangan")
        fig_profile.update_yaxes(range=[0, max(melted["Nilai"]) * 1.15]) # Perbaikan label terpotong
        st.plotly_chart(fig_profile, use_container_width=True)

    section_header("📐", "Statistik Deskriptif Parameter Utama", "STATISTICAL TABLE")
    if len(df_clean) > 0:
        stat_df = df_clean[stat_cols].describe().round(2).T
        stat_df.columns = ["N", "Rata-rata", "Std Dev", "Minimal", "Kuartil 1 (25%)", "Median (50%)", "Kuartil 3 (75%)", "Maksimal"]
        stat_df.index = ["Kandungan Kalori (Kkal)", "Kandungan Protein (g)", "Kandungan Lemak (g)", "Kandungan Karbohidrat (g)"]
        st.dataframe(stat_df, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 2 — EKSPLORASI DATA
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🔬 Eksplorasi Data":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">🔬 Eksplorasi Lanjutan Multivariat</div>', unsafe_allow_html=True)
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Histogram & Distribusi Detail", "🔗 Matriks Korelasi Heatmap", "🗺️ Scatter Plot Interaktif"])

    with tab1:
        section_header("📊", "Analisis Distribusi Probabilitas")
        col_sel = st.selectbox("Pilih Parameter Nutrisi Analisis", ["kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"])
        
        cx, cy = st.columns([2, 1])
        with cx:
            fig_dist = px.histogram(df_clean, x=col_sel, color="jenis_makanan", marginal="box", barmode="overlay", opacity=0.6, color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"})
            fig_dist = apply_theme(fig_dist, height=400)
            st.plotly_chart(fig_dist, use_container_width=True)
        with cy:
            st.markdown("<div style='padding-top:25px;'></div>", unsafe_allow_html=True)
            for j_type in ["dish", "komponen"]:
                sub_data = df_clean[df_clean["jenis_makanan"] == j_type][col_sel].dropna()
                j_color = "#ff7043" if j_type == "dish" else "#2ecc87"
                if len(sub_data) > 0:
                    st.markdown(f"""
                    <div style="background:#1a1d2e; border-left:4px solid {j_color}; padding:14px; margin-bottom:10px; border-radius:8px;">
                        <h4 style="margin:0 0 8px 0; color:{j_color}; font-size:0.85rem; text-transform:uppercase;">{j_type}</h4>
                        <p style="margin:2px 0; font-size:0.8rem;">Rerata: <b>{sub_data.mean():.2f}</b> | Median: <b>{sub_data.median():.2f}</b></p>
                        <p style="margin:2px 0; font-size:0.8rem;">Rentang: <b>{sub_data.min():.1f}</b> s/d <b>{sub_data.max():.1f}</b></p>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        section_header("🔗", "Matriks Korelasi Linear Pearson")
        corr_targets = ["kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"]
        if len(df_clean) > 0:
            c_matrix = df_clean[corr_targets].corr().round(3)
            fig_heat = px.imshow(c_matrix, color_continuous_scale="RdBu_r", zmin=-1, zmax=1, text_auto=".2f")
            fig_heat = apply_theme(fig_heat, height=420)
            st.plotly_chart(fig_heat, use_container_width=True)
            st.markdown('<div class="info-box">💡 <b>Insight Eksplanatori:</b> Nilai korelasi mendekati +1 menandakan hubungan searah yang kuat. Korelasi lemak terhadap kalori menduduki koefisien tertinggi (r ≈ 0.75), membuktikan pengaruh dominannya pada densitas energi.</div>', unsafe_allow_html=True)

    with tab3:
        section_header("🗺️", "Pemetaan Scatter Dua Dimensi & Pola Distribusi")
        sx, sy = st.columns(2)
        with sx:
            x_sel = st.selectbox("Sumbu Variabel X", ["kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"], index=1)
        with sy:
            y_sel = st.selectbox("Sumbu Variabel Y", ["kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"], index=0)
            
        if len(df_clean) > 2:
            fig_scat = px.scatter(df_clean, x=x_sel, y=y_sel, color="jenis_makanan", hover_name="nama_makanan", opacity=0.6, color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"})
            
            xv = df_clean[x_sel].values
            yv = df_clean[y_sel].values
            idx_valid = ~np.isnan(xv) & ~np.isnan(yv) & ~np.isinf(xv) & ~np.isinf(yv)
            if idx_valid.sum() > 2:
                m_coef, b_val = np.polyfit(xv[idx_valid], yv[idx_valid], 1)
                x_line = np.linspace(xv[idx_valid].min(), xv[idx_valid].max(), 100)
                y_line = m_coef * x_line + b_val
                fig_scat.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Garis Tren Umum', line=dict(color='#f1c40f', width=2, dash='dash')))
                
            fig_scat = apply_theme(fig_scat, height=480)
            st.plotly_chart(fig_scat, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 3 — ANALISIS BQ (BUSINESS QUESTIONS)
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📊 Analisis BQ":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">📊 Pembuktian Empiris Pertanyaan Bisnis (BQ)</div>', unsafe_allow_html=True)
    st.divider()

    bq_tabs = st.tabs(["BQ1: Protein Mutlak", "BQ2: Efisiensi Densitas", "BQ3: Energi Terpadat", "BQ4: Korelasi Koefisien", "BQ5: Komparasi Kelompok"])

    with bq_tabs[0]:
        section_header("💪", "Top Makanan Kandungan Protein Tertinggi", "BQ1")
        n_bq1 = st.slider("Jumlah Baris Data Tampil", 5, 25, 10, key="s_bq1")
        if len(df_clean) > 0:
            # Perbaikan: Urutkan murni berdasarkan protein tertinggi ke terendah
            top_p = df_clean.nlargest(n_bq1, "protein").sort_values("protein", ascending=True)
            
            fig_bq1 = px.bar(
                top_p, x="protein", y="nama_makanan", color="jenis_makanan", 
                orientation="h", text="protein",
                color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"}
            )
            fig_bq1.update_traces(texttemplate="%{text:.1f}g", textposition="outside")
            fig_bq1 = apply_theme(fig_bq1, height=max(380, n_bq1 * 38))
            
            # Paksa sumbu Y mengikuti urutan data murni, bukan di-group kelompok
            fig_bq1.update_yaxes(type='category', categoryorder='array', categoryarray=top_p["nama_makanan"].tolist())
            fig_bq1.update_xaxes(range=[0, max(top_p["protein"]) * 1.15]) # Perbaikan label terpotong
            
            st.plotly_chart(fig_bq1, use_container_width=True)
            st.markdown('<div class="warning-box">🔍 <b>Fakta Temuan Analisis:</b> Jajaran teratas didominasi pangan kering dehidrasi (Kerupuk Kulit, Dendeng, Teri Kering). Pengurangan volume air melipatgandakan konsentrasi protein per 100g berat bahan.</div>', unsafe_allow_html=True)

    with bq_tabs[1]:
        section_header("⚡", "Rasio Efisiensi Kandungan Protein terhadap Kalori", "BQ2")
        n_bq2 = st.slider("Jumlah Baris Data Tampil", 5, 25, 10, key="s_bq2")
        if len(df_clean) > 0:
            df_clean_ratio = df_clean.copy()
            df_clean_ratio["protein_per_calorie"] = df_clean_ratio["protein_per_calorie"].clip(upper=df_clean_ratio["protein_per_calorie"].quantile(0.99))
            
            # Perbaikan: Urutkan murni berdasarkan rasio tertinggi ke terendah
            top_r = df_clean_ratio.nlargest(n_bq2, "protein_per_calorie").sort_values("protein_per_calorie", ascending=True)
            
            fig_bq2 = px.bar(
                top_r, x="protein_per_calorie", y="nama_makanan", color="jenis_makanan", 
                orientation="h", text="protein_per_calorie",
                color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"}
            )
            fig_bq2.update_traces(texttemplate="%{text:.3f}", textposition="outside")
            fig_bq2 = apply_theme(fig_bq2, height=max(380, n_bq2 * 38))
            
            fig_bq2.update_yaxes(type='category', categoryorder='array', categoryarray=top_r["nama_makanan"].tolist())
            fig_bq2.update_xaxes(range=[0, max(top_r["protein_per_calorie"]) * 1.15]) # Perbaikan label terpotong
            
            st.plotly_chart(fig_bq2, use_container_width=True)
            st.markdown('<div class="info-box">💡 <b>Konteks Diet Sehat:</b> Nilai rasio tinggi menandakan makanan memasok protein padat dengan beban kalori minim. Sup kuah kaldu rempah non-santan (Jukku Pallu Kaloa) dan ikan pindang adalah pilihan lean protein terbaik.</div>', unsafe_allow_html=True)

    with bq_tabs[2]:
        section_header("🔥", "Kepadatan Energi Tertinggi per Kategori Bahan", "BQ3")
        n_bq3 = st.slider("Jumlah Baris Data Tampil", 5, 25, 10, key="s_bq3")
        if len(df_clean) > 0:
            # Perbaikan: Urutkan murni berdasarkan kalori tertinggi ke terendah
            top_c = df_clean.nlargest(n_bq3, "kalori").sort_values("kalori", ascending=True)
            
            fig_bq3 = px.bar(top_c, x="kalori", y="nama_makanan", color="kalori", orientation="h", text="kalori", color_continuous_scale="Oranges")
            fig_bq3.update_traces(texttemplate="%{text:.0f} Kkal", textposition="outside")
            fig_bq3 = apply_theme(fig_bq3, height=max(380, n_bq3 * 38))
            
            fig_bq3.update_yaxes(type='category', categoryorder='array', categoryarray=top_c["nama_makanan"].tolist())
            fig_bq3.update_xaxes(range=[0, max(top_c["kalori"]) * 1.15]) # Perbaikan label terpotong
            
            st.plotly_chart(fig_bq3, use_container_width=True)

    with bq_tabs[3]:
        section_header("📊", "Kekuatan Determinan Variabel Komponen Makro", "BQ4")
        if len(df_clean) > 0:
            c_vals = df_clean[["kalori", "protein", "lemak", "karbohidrat"]].corr()["kalori"].drop("kalori").sort_values(ascending=True)
            fig_bq4 = px.bar(x=c_vals.values, y=c_vals.index, orientation="h", text=c_vals.values, color=c_vals.values, color_continuous_scale="Viridis")
            fig_bq4.update_traces(texttemplate="%{text:.3f}", textposition="outside")
            fig_bq4 = apply_theme(fig_bq4, height=300, showlegend=False)
            fig_bq4.update_xaxes(range=[0, max(c_vals.values) * 1.15]) # Perbaikan label terpotong
            st.plotly_chart(fig_bq4, use_container_width=True)

    with bq_tabs[4]:
        section_header("⚖️", "Analisis Komparatif Profil Struktur Gizi", "BQ5")
        if len(df_clean) > 0:
            profil_mean = df_clean.groupby("jenis_makanan")[["kalori", "protein", "lemak", "karbohidrat"]].mean().reset_index()
            melted_prof = profil_mean.melt(id_vars="jenis_makanan", value_vars=["protein", "lemak", "karbohidrat"], var_name="Zat Gizi", value_name="Gram")
            fig_bq5 = px.bar(melted_prof, x="Zat Gizi", y="Gram", color="jenis_makanan", barmode="group", text="Gram", color_discrete_map={"dish": "#ff7043", "komponen": "#2ecc87"})
            fig_bq5.update_traces(texttemplate="%{text:.1f}g", textposition="outside")
            fig_bq5 = apply_theme(fig_bq5, height=360)
            fig_bq5.update_yaxes(range=[0, max(melted_prof["Gram"]) * 1.15]) # Perbaikan label terpotong
            st.plotly_chart(fig_bq5, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 4 — KOMPARASI MAKANAN
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🥗 Komparasi Makanan":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">🥗 Modul Komparasi Interaktif Multi-Variabel</div>', unsafe_allow_html=True)
    st.divider()

    food_list = sorted(df_clean["nama_makanan"].dropna().unique().tolist())
    selected_compare = st.multiselect("Pilih Barisan Nama Makanan untuk Dibandingkan (Maksimal 6)", food_list, default=food_list[:3] if len(food_list) >= 3 else food_list)

    if len(selected_compare) > 0:
        df_sub_compare = df_clean[df_clean["nama_makanan"].isin(selected_compare)]
        
        mc = df_sub_compare.melt(id_vars="nama_makanan", value_vars=["kalori", "protein", "lemak", "karbohidrat"], var_name="Nutrisi", value_name="Nilai")
        fig_m_comp = px.bar(mc, x="Nutrisi", y="Nilai", color="nama_makanan", barmode="group", text="Nilai", color_discrete_sequence=PALETTE)
        fig_m_comp.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_m_comp = apply_theme(fig_m_comp, height=450)
        fig_m_comp.update_yaxes(range=[0, max(mc["Nilai"]) * 1.15]) # Perbaikan label terpotong
        st.plotly_chart(fig_m_comp, use_container_width=True)
        
        st.dataframe(df_sub_compare[["nama_makanan", "jenis_makanan", "kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"]].set_index("nama_makanan").round(2), use_container_width=True)
    else:
        st.info("Pilih minimal satu nama pangan pada filter multiselect di atas.")

# ═══════════════════════════════════════════════════════════════════════════════
# VIEW 5 — TABEL DATA LENGKAP
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📋 Tabel Data Lengkap":
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">📋 Repositori Komprehensif Data & Kamus Kolom</div>', unsafe_allow_html=True)
    st.divider()

    all_cols = df.columns.tolist()
    default_show = ["id", "nama_makanan", "jenis_makanan", "source", "kalori", "protein", "lemak", "karbohidrat", "macro_balance_score"]
    filtered_cols_to_show = [c for c in default_show if c in all_cols]

    selected_columns_table = st.multiselect("Kolom yang Ingin Ditampilkan", all_cols, default=filtered_cols_to_show)

    st.markdown("#### Filter Pencarian Instan")
    search_inline = st.text_input("🔎 Input Kata Kunci Nama Hidangan", key="search_text_table_inline")
    
    df_final_table_view = df.copy()
    if search_inline:
        df_final_table_view = df_final_table_view[df_final_table_view["nama_makanan"].str.contains(search_inline.lower(), na=False)]

    tc1, tc2, tc3 = st.columns(3)
    tc1.metric("Baris Terpilih", f"{len(df_final_table_view):,}")
    tc2.metric("Total Komponen", f"{(df_final_table_view['jenis_makanan']=='komponen').sum():,}")
    tc3.metric("Total Dish", f"{(df_final_table_view['jenis_makanan']=='dish').sum():,}")

    if len(selected_columns_table) > 0:
        st.dataframe(df_final_table_view[selected_columns_table].reset_index(drop=True).round(4), use_container_width=True, height=450)
    else:
        st.warning("Pilih minimal satu kolom untuk merender tabel.")

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("📖", "Data Dictionary Kamus Skema Kolom — df_food")
    dict_schema = {
        "Nama Fitur Kolom": ["id", "nama_makanan", "jenis_makanan", "kalori", "protein", "lemak", "karbohidrat", "source", "protein_per_calorie", "macro_balance_score"],
        "Tipe Skema Data": ["int64", "object (str)", "object (str)", "float64", "float64", "float64", "float64", "object (str)", "float64", "float64"],
        "Satuan Baku": ["ID Unik", "Teks Nama", "dish / komponen", "Kkal / 100g", "Gram / 100g", "Gram / 100g", "Gram / 100g", "Nama Sumber", "Rasio g/Kkal", "Indeks Skala 0-1"],
        "Deskripsi Penjelasan Bisnis": [
            "ID unik representasi indeks pangan.",
            "Nama hidangan pangan lokal Indonesia yang sudah dibersihkan.",
            "Klasifikasi bentuk pangan: 'dish' untuk hidangan jadi, 'komponen' untuk bahan mentah tunggal.",
            "Kandungan pasokan energi total hasil konversi zat makro pangan.",
            "Kandungan protein pembangun struktural jaringan tubuh harian.",
            "Kandungan lemak total sumber cadangan energi sekunder harian.",
            "Kandungan karbohidrat total pemicu energi glukosa darah.",
            "Asal muasal asal repositori data: TKPI Kemenkes atau dataset Kaggle.",
            "Metrik efisiensi kandungan protein terhadap densitas kalori.",
            "Skor tingkat keseimbangan sebaran energi dari ketiga zat gizi makro."
        ]
    }
    st.dataframe(pd.DataFrame(dict_schema), use_container_width=True, hide_index=True)

    st.divider()
    section_header("⬇️", "Ekspor Repositori Dataset Terfilter")
    
    csv_string_data = df_final_table_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Unduh Data Hasil Filter Ekstraksi (.CSV)",
        data=csv_string_data,
        file_name="df_food_filtered_extract.csv",
        mime="text/csv"
    )