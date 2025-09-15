import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==============================
# KONFIGURASI
# ==============================
HISTORY_FILE = "history.csv"
ADMIN_PASSWORD = "admin1234"

# Google Sheets setup
SHEET_ID = "1uq1boLLUXeuIUtNo2xwCFivgfGPOuZxNDKvbklmWOd4"  # ganti dengan ID Google Sheets
SHEET_NAME_FUNGISIDA = "Fungisida"
SHEET_NAME_FURADAN = "Furadan"
SHEET_NAME_PUPUK = "Pupuk"
SHEET_NAME_BIN = "BIN"

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

if "gcp_service_account" in st.secrets:
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope
    )
    client = gspread.authorize(creds)
else:
    client = None  # offline mode

# ==============================
# Helper Functions
# ==============================
def save_history(entry, sheet_name):
    """Simpan data ke CSV dan Google Sheets"""
    # Simpan ke CSV
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    else:
        df = pd.DataFrame([entry])
    df.to_csv(HISTORY_FILE, index=False)

    # Simpan ke Google Sheets
    if client:
        try:
            sheet = client.open_by_key(SHEET_ID).worksheet(sheet_name)
            sheet.append_row(list(entry.values()))
        except Exception as e:
            st.error(f"Gagal simpan ke Google Sheets: {e}")


def draw_jerigen(current, capacity):
    """Visualisasi jerigen vertikal"""
    empty = capacity - current
    fig, ax = plt.subplots(figsize=(2, 6))
    ax.bar([0], [current], color="green", label="Isi")
    ax.bar([0], [empty], bottom=[current], color="yellow", label="Kosong")
    ax.set_ylim(0, capacity)
    ax.set_xticks([])
    ax.set_ylabel("Liter")
    ax.set_title("Visualisasi Jerigen")
    ax.legend()
    st.pyplot(fig)


# ==============================
# UI
# ==============================
st.set_page_config(page_title="Aplikasi Input Tebu", layout="wide")
st.title("🌱 Aplikasi Input Tebu")

menu = st.tabs(["🍄 Fungisida", "🐛 Furadan", "🌱 Pupuk", "🧺 BIN", "📖 Riwayat"])
now = datetime.now()
tanggal = now.strftime("%d/%m/%Y")
waktu = now.strftime("%H:%M:%
