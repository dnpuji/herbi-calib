import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

DB_FILE = "calibration.db"

# Setup DB
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        mode TEXT,
        dose_per_L REAL,
        unit TEXT,
        capacity_L REAL,
        used_L REAL,
        to_add REAL,
        note TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_record(mode, dose_per_L, unit, capacity_L, used_L, to_add, note):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO history (timestamp, mode, dose_per_L, unit, capacity_L, used_L, to_add, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mode, dose_per_L, unit, capacity_L, used_L, to_add, note))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
    conn.close()
    return df

def compute_concentrate(mode, dose_per_L, capacity_L, used_L):
    """
    Compute amount of concentrate to add (in same unit as dose_per_L) based on mode:
    - mode="Refill": hanya isi ulang air sebanyak used_L, sehingga konsentrat = used_L * dose_per_L
    - mode="Prepare": jerigen kosong, isi full capacity_L, sehingga konsentrat = capacity_L * dose_per_L
    """
    if mode == "Refill":
        return used_L * dose_per_L
    elif mode == "Prepare":
        return capacity_L * dose_per_L
    else:
        return 0.0

# Streamlit App
def main():
    st.title("🌿 Kalibrasi Herbisida")
    st.markdown("Hitung kebutuhan konsentrat berdasarkan dosis per liter dan kapasitas jerigen.")

    # Form input
    with st.form("calibration_form"):
        mode = st.selectbox("Pilih Mode", ["Refill", "Prepare"])
        dose_per_L = st.number_input("Dosis per Liter", value=0.24, step=0.01, format="%.2f")
        unit = st.selectbox("Satuan dosis", ["L/L", "mL/L", "g/L"])
        capacity_L = st.number_input("Kapasitas Jerigen (L)", value=20.0, step=1.0)
        used_L = st.number_input("Berapa Liter yang Terpakai", value=0.0, step=0.5)
        note = st.text_input("Catatan (opsional)", "")

        submitted = st.form_submit_button("Hitung & Simpan")

        if submitted:
            to_add = compute_concentrate(mode, dose_per_L, capacity_L, used_L)
            save_record(mode, dose_per_L, unit, capacity_L, used_L, to_add, note)
            st.success(f"Konsentrat yang harus ditambahkan: **{to_add:.2f} {unit}**")

            # Visualization
            fig, ax = plt.subplots()
            ax.bar(["Terpakai", "Sisa"], [used_L, capacity_L - used_L], color=["red", "green"])
            ax.set_ylabel("Liter")
            ax.set_title("Kapasitas Jerigen")
            st.pyplot(fig)

    st.subheader("📊 Historis Input")
    df = load_history()
    if not df.empty:
        st.dataframe(df)

        st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "history.csv", "text/csv")

        # Trend
        fig2, ax2 = plt.subplots()
        ax2.plot(pd.to_datetime(df["timestamp"]), df["to_add"], marker="o")
        ax2.set_ylabel("Konsentrat (unit)")
        ax2.set_xlabel("Waktu")
        ax2.set_title("Tren Konsentrat")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
    else:
        st.info("Belum ada data historis.")

if __name__ == "__main__":
    init_db()
    main()
