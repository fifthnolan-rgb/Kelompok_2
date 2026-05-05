import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Dashboard Analisis Properti", layout="wide")

# Tambahkan Judul Utama di Tengah
st.markdown("<h1 style='text-align: center;'>Dashboard Analisis Properti</h1>", unsafe_allow_html=True)

# --- Fungsi Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Cleaned_Final_Rumah.csv')
        return df
    except FileNotFoundError:
        return None

dataset = load_data()

if dataset is not None:
    # --- Persiapan Data ---
    # 1. Bar Chart Data (Top 50)
    location_counts = dataset['Lokasi'].value_counts().reset_index()
    location_counts.columns = ['Lokasi', 'Jumlah Properti']
    top_50_locations = location_counts.head(50)

    # 2. Pie Chart Data (Top 5 + Lainnya)
    top_5_locations = location_counts.head(5)
    other_count = location_counts['Jumlah Properti'].iloc[5:].sum()
    pie_data = pd.concat([top_5_locations, pd.DataFrame({'Lokasi': ['Lainnya'], 'Jumlah Properti': [other_count]})])

    # 3. Scatter Plot Data (50 Data Pertama)
    df_scatter = dataset.head(50).copy()
    def format_harga(nominal):
        if nominal >= 1_000_000_000:
            return f"{nominal / 1_000_000_000:.1f} Miliar".replace('.', ',')
        else:
            return f"{int(nominal / 1_000_000)} Juta"
    df_scatter['Harga_Label'] = df_scatter['Harga'].apply(format_harga)

    # --- Baris 1: Bar Chart & Pie Chart ---
    col1, col2 = st.columns(2)

    with col1:
        # Plot 1: Bar Chart
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        sns.barplot(x='Lokasi', y='Jumlah Properti', data=top_50_locations, hue='Lokasi', palette='viridis', legend=False, ax=ax1)
        ax1.set_title('Jumlah Properti per Lokasi (50 Teratas)', fontsize=16)
        ax1.set_xlabel('Lokasi', fontsize=12)
        ax1.set_ylabel('Jumlah Properti', fontsize=12)
        plt.xticks(rotation=90)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig1)

    with col2:
        # Plot 2: Pie Chart
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        ax2.pie(pie_data['Jumlah Properti'], labels=pie_data['Lokasi'], autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
        ax2.set_title('Proporsi Properti per Lokasi (Top 5 + Lainnya)', fontsize=16)
        st.pyplot(fig2)

    # --- Baris 2: Scatter Plot ---
    # Plot 3: Scatter Plot (Lebar Penuh)
    st.markdown("---")
    fig3, ax3 = plt.subplots(figsize=(16, 12))
    ax3.scatter(df_scatter['Luas Bangunan'], df_scatter['Harga_Label'], alpha=0.6, s=100)
    ax3.set_title('Hubungan Luas Bangunan dan Harga (50 Data Pertama)', fontsize=18)
    ax3.set_xlabel('Luas Bangunan (m²)', fontsize=14)
    ax3.set_ylabel('Harga', fontsize=14)
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.invert_yaxis() # Membalik sumbu Y sesuai permintaan kode asli/gambar
    
    st.pyplot(fig3)

else:
    st.error("File 'Data_bersih_rumah.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")