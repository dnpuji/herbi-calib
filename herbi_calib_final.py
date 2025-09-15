import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==========================
# Konfigurasi
# ==========================
HISTORY_FILE = "history.csv"
ADMIN_PASSWORD = "admin1234"

# Google Sheets API setup
SHEET_ID = "uq1boLLUXeuIUtNo2xwCFivgfGPOuZxNDKvbklmWOd4"  # ganti dengan ID Google Sheet
SHEET_NAME = "Sheet1"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Gunakan secrets di Streamlit Cloud
if "gcp_service_account" in st.secrets:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
else:
    sheet = None  # offline mode jika belum ada secrets


# ==========================
# Helper Functions
# ==========================
def save_history(entry):
    """Simpan ke CSV dan Google Sheet jika ada"""
    # simpan CSV
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    else:
        df = pd.DataFrame([entry])
    df.to_csv(HISTORY_FILE, index=False)

    # simpan ke Google Sheet
    if sheet:
        sheet.append_row(list(entry.values()))


def draw_jerigen(current, capacity):
    """Visualisasi jerigen vertikal"""
    empty = capacity - current
    fig, ax = plt.subplots(figsize=(2, 5))
    ax.bar([0], [current], color="green")
    ax.bar([0], [empty], bottom=[current], color="yellow")
    ax.set_ylim(0, capacity)
    ax.set_xticks([])
    ax.set_ylabel("Liter")
    ax.set_title("Isi Jerigen")
    st.pyplot(fig)


# ==========================
# Sidebar Menu
# ==========================
menu = st.sidebar.radio(
    "📌 Pilih Menu",
    ["🍄 Fungisida", "🐛 Furadan", "🌱 Pupuk", "🧺 BIN", "📖 Riwayat"]
)

# ==========================
# Menu Fungisida
# ==========================
if menu == "🍄 Fungisida":
    st.title("🍄 Kalibrasi Fungisida")

    capacity = st.number_input("Kapasitas Jerigen (L)", min_value=1, value=20)
    dose_per_L = st.number_input("Dosis Fungisida (L/L Air)", min_value=0.0, value=0.24)
    current_fill = st.number_input("Sisa Isi Jerigen (L)", min_value=0.0, max_value=float(capacity), value=0.0)

    water_needed = capacity - current_fill
    fungicide_needed = dose_per_L * water_needed

    st.subheader("🔎 Perhitungan")
    st.write(f"💧 Tambahkan **{water_needed:.2f} L air**")
    st.write(f"🧪 Tambahkan **{fungicide_needed:.2f} L fungisida**")

    draw_jerigen(current_fill, capacity)

    if st.button("💾 Simpan Data"):
        now = datetime.datetime.now()
        entry = {
            "Tanggal": now.strftime("%Y-%m-%d"),
            "Waktu": now.strftime("%H:%M:%S"),
            "Menu": "Fungisida",
            "Sisa Jerigen (L)": current_fill,
            "Air Ditambahkan (L)": water_needed,
            "Fungisida Ditambahkan (L)": fungicide_needed
        }
        save_history(entry)
        st.success("Data berhasil disimpan ✅")


# ==========================
# Menu Furadan
# ==========================
elif menu == "🐛 Furadan":
    st.title("🐛 Pemakaian Furadan (kg)")

    furadan_used = st.number_input("Jumlah Furadan yang digunakan (kg)", min_value=0.0, value=0.0)

    if st.button("💾 Simpan Data"):
        now = datetime.datetime.now()
        entry = {
            "Tanggal": now.strftime("%Y-%m-%d"),
            "Waktu": now.strftime("%H:%M:%S"),
            "Menu": "Furadan",
            "Jumlah (kg)": furadan_used
        }
        save_history(entry)
        st.success("Data Furadan tersimpan ✅")


# ==========================
# Menu Pupuk
# ==========================
elif menu == "🌱 Pupuk":
    st.title("🌱 Pemakaian Pupuk (kg)")

    pupuk_used = st.number_input("Jumlah Pupuk yang digunakan (kg)", min_value=0.0, value=0.0)

    if st.button("💾 Simpan Data"):
        now = datetime.datetime.now()
        entry = {
            "Tanggal": now.strftime("%Y-%m-%d"),
            "Waktu": now.strftime("%H:%M:%S"),
            "Menu": "Pupuk",
            "Jumlah (kg)": pupuk_used
        }
        save_history(entry)
        st.success("Data Pupuk tersimpan ✅")


# ==========================
# Menu BIN
# ==========================
elif menu == "🧺 BIN":
    st.title("🧺 Pemakaian BIN (wadah bibit)")

    bin_used = st.number_input("Jumlah BIN yang digunakan", min_value=0, value=0)

    if st.button("💾 Simpan Data"):
        now = datetime.datetime.now()
        entry = {
            "Tanggal": now.strftime("%Y-%m-%d"),
            "Waktu": now.strftime("%H:%M:%S"),
            "Menu": "BIN",
            "Jumlah (BIN)": bin_used
        }
        save_history(entry)
        st.success("Data BIN tersimpan ✅")


# ==========================
# Menu Riwayat
# ==========================
elif menu == "📖 Riwayat":
    st.title("📖 Riwayat Data Penggunaan")

    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        st.dataframe(df)

        # Download button
        st.download_button(
            label="⬇️ Download Semua Data",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="all_history.csv",
            mime="text/csv"
        )

        # Proteksi hapus
        st.subheader("🔑 Hapus Data (Admin Only)")
        password = st.text_input("Masukkan password admin:", type="password")

        if password == ADMIN_PASSWORD:
            index_to_delete = st.selectbox("Pilih index data yang ingin dihapus:", df.index)

            if st.button("🗑️ Hapus Data Terpilih"):
                df = df.drop(index=index_to_delete)
                df.to_csv(HISTORY_FILE, index=False)
                st.success("Data berhasil dihapus ✅")
                st.experimental_rerun()
        elif password != "":
            st.error("❌ Password salah!")

    else:
        st.warning("Belum ada data riwayat.")
