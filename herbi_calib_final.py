import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ==============================
# GOOGLE SHEETS SETUP
# ==============================
SHEET_ID = "1uq1boLLUXeuIUtNo2xwCFivgfGPOuZxNDKvbklmWOd4"  # ganti dengan ID Google Sheets Anda
SHEET_NAME_FUNGISIDA = "Fungisida"
SHEET_NAME_FURADAN = "Furadan"
SHEET_NAME_PUPUK = "Pupuk"
SHEET_NAME_BIN = "BIN"

# Koneksi ke Google Sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"], scope
)
client = gspread.authorize(creds)


# ==============================
# SIMPAN DATA KE GOOGLE SHEETS
# ==============================
def append_to_sheet(sheet_name, row_data):
    try:
        sheet = client.open_by_key(SHEET_ID).worksheet(sheet_name)
        sheet.append_row(row_data)
    except Exception as e:
        st.error(f"Gagal menyimpan ke Google Sheets ({sheet_name}): {e}")


# ==============================
# STREAMLIT UI
# ==============================
st.set_page_config(page_title="Aplikasi Input Tebu", layout="wide")

st.title("🌱 Aplikasi Input Tebu")
menu = st.sidebar.radio(
    "Pilih Menu:",
    ["🍄 Fungisida", "🐛 Furadan", "🌱 Pupuk", "🧺 BIN", "📖 Riwayat"]
)

now = datetime.now()
tanggal = now.strftime("%d/%m/%Y")
waktu = now.strftime("%H:%M:%S")

# ---------------- Fungisida ----------------
if menu == "🍄 Fungisida":
    st.header("🍄 Input Fungisida (Kalibrasi)")
    kapasitas = st.number_input("Kapasitas Jerigen (L)", min_value=1.0, value=20.0)
    dosis = st.number_input("Dosis Fungisida (L/L campuran)", min_value=0.0, value=0.24)
    target = st.number_input("Sisa isi di Jerigen (L)", min_value=0.0, value=10.0)

    if st.button("Hitung"):
        konsentrat = dosis * target
        air = target - konsentrat

        st.success(f"Untuk {target:.2f} L campuran:")
        st.write(f"- Konsentrat: **{konsentrat:.2f} L**")
        st.write(f"- Air: **{air:.2f} L**")

        # Visualisasi Jerigen
        fig, ax = plt.subplots(figsize=(2, 6))
        ax.bar(0, target, color="green", label="Isi")
        ax.bar(0, kapasitas - target, bottom=target, color="yellow", label="Kosong")
        ax.set_ylim(0, kapasitas)
        ax.set_xticks([])
        ax.set_ylabel("Liter")
        ax.set_title("Visualisasi Jerigen")
        ax.legend()
        st.pyplot(fig)

        # Simpan ke Google Sheets
        row = [tanggal, waktu, kapasitas, dosis, target, konsentrat, air]
        append_to_sheet(SHEET_NAME_FUNGISIDA, row)

# ---------------- Furadan ----------------
elif menu == "🐛 Furadan":
    st.header("🐛 Input Furadan (kg)")
    jumlah = st.number_input("Jumlah Furadan (kg)", min_value=0.0, value=0.0)

    if st.button("Simpan Furadan"):
        row = [tanggal, waktu, jumlah]
        append_to_sheet(SHEET_NAME_FURADAN, row)
        st.success(f"Data Furadan {jumlah} kg tersimpan")

# ---------------- Pupuk ----------------
elif menu == "🌱 Pupuk":
    st.header("🌱 Input Pupuk (kg)")
    jumlah = st.number_input("Jumlah Pupuk (kg)", min_value=0.0, value=0.0)

    if st.button("Simpan Pupuk"):
        row = [tanggal, waktu, jumlah]
        append_to_sheet(SHEET_NAME_PUPUK, row)
        st.success(f"Data Pupuk {jumlah} kg tersimpan")

# ---------------- BIN ----------------
elif menu == "🧺 BIN":
    st.header("🧺 Input BIN (unit)")
    jumlah = st.number_input("Jumlah BIN", min_value=0, value=0)

    if st.button("Simpan BIN"):
        row = [tanggal, waktu, jumlah]
        append_to_sheet(SHEET_NAME_BIN, row)
        st.success(f"Data BIN {jumlah} unit tersimpan")

# ---------------- Riwayat ----------------
elif menu == "📖 Riwayat":
    st.header("📖 Riwayat Input (Google Sheets)")
    st.info("Riwayat hanya bisa dilihat di Google Sheets langsung untuk performa lebih cepat.")
