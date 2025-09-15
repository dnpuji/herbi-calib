import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Herbicide Calibration", layout="centered")

st.title("🌱 Herbicide Calibration Web")

# --- Input Section ---
st.subheader("Input Data")
jerigen_capacity = st.number_input(
    "Kapasitas Jerigen (L)", min_value=1.0, value=20.0, step=1.0
)
dose_per_L = st.number_input(
    "Dosis Herbisida (L konsentrat / L campuran)", min_value=0.0, value=0.24, step=0.01
)
target_mix = st.number_input(
    "Target Campuran Total (L)", min_value=0.0, value=10.0, step=1.0
)

# --- Perhitungan ---
if target_mix > 0 and dose_per_L > 0:
    konsentrat = dose_per_L * target_mix
    air = target_mix - konsentrat

    st.success(f"✅ Untuk {target_mix:.2f} L campuran total:")
    st.info(f"- Konsentrat dibutuhkan: **{konsentrat:.2f} L**")
    st.info(f"- Air yang ditambahkan: **{air:.2f} L**")

    # --- Visualisasi Horizontal ---
    st.subheader("Visualisasi Jerigen (Horizontal)")
    fig, ax = plt.subplots(figsize=(6, 1.5))

    # Bar horizontal: air di kiri, konsentrat di kanan
    ax.barh(0, air, color="skyblue", label=f"Air {air:.2f} L")
    ax.barh(0, konsentrat, left=air, color="green", label=f"Konsentrat {konsentrat:.2f} L")

    # Atur sumbu
    ax.set_xlim(0, jerigen_capacity)
    ax.set_yticks([])
    ax.set_xlabel("Liter")
    ax.set_title("Isi Jerigen (Horizontal)")
    ax.legend(loc="upper right")

    st.pyplot(fig)

# --- History Section ---
st.subheader("Riwayat Input")
if "history" not in st.session_state:
    st.session_state["history"] = []

if st.button("💾 Simpan ke Riwayat"):
    entry = {
        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Kapasitas Jerigen (L)": jerigen_capacity,
        "Dosis (L/L campuran)": dose_per_L,
        "Target Campuran (L)": target_mix,
        "Konsentrat (L)": dose_per_L * target_mix,
        "Air (L)": target_mix - (dose_per_L * target_mix),
    }
    st.session_state["history"].append(entry)

if st.session_state["history"]:
    df = pd.DataFrame(st.session_state["history"])
    st.dataframe(df)

    # Unduh CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Unduh Riwayat (CSV)",
        data=csv,
        file_name="history.csv",
        mime="text/csv",
    )
