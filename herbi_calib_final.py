import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Herbicide Calibration", layout="centered")

st.title("🌱 Herbicide Calibration Web")

# --- Input Section ---
st.subheader("Input Data")

jerigen_capacity = st.number_input("Kapasitas Jerigen (L)", min_value=1.0, value=20.0, step=1.0)
dose_per_L = st.number_input("Dosis Herbisida (L / L air)", min_value=0.0, value=0.24, step=0.01)
used_volume = st.number_input("Jumlah Air yang Dipakai (L)", min_value=0.0, step=1.0)

# --- Compute Section ---
if used_volume > 0:
    required_concentrate = used_volume * dose_per_L
    remaining_volume = jerigen_capacity - used_volume

    st.success(f"✅ Konsentrat yang terpakai: **{required_concentrate:.2f} L**")
    st.info(f"💧 Air tersisa di jerigen: **{remaining_volume:.2f} L**")

    if remaining_volume > 0:
        add_concentrate = remaining_volume * dose_per_L
        st.warning(f"⚡ Tambahkan konsentrat: **{add_concentrate:.2f} L** untuk {remaining_volume:.2f} L air tersisa.")

# --- History Section ---
st.subheader("Riwayat Input")

if "history" not in st.session_state:
    st.session_state["history"] = []

if st.button("Simpan ke Riwayat"):
    entry = {
        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Kapasitas Jerigen (L)": jerigen_capacity,
        "Dosis (L/L air)": dose_per_L,
        "Dipakai (L)": used_volume,
        "Konsentrat Terpakai (L)": used_volume * dose_per_L
    }
    st.session_state["history"].append(entry)

if st.session_state["history"]:
    df = pd.DataFrame(st.session_state["history"])
    st.dataframe(df)

    # Option to download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Unduh Riwayat (CSV)", data=csv, file_name="history.csv", mime="text/csv")
