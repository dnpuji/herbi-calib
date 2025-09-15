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
waktu = now.strftime("%H:%M:%S")

# ---------------- Fungisida ----------------
with menu[0]:
    st.header("🍄 Input Fungisida (Kalibrasi)")
    kapasitas = st.number_input("Kapasitas Jerigen (L)", min_value=1.0, value=20.0)
    dosis = st.number_input("Dosis Fungisida (L/L campuran)", min_value=0.0, value=0.24)
    sisa = st.number_input("Sisa isi di Jerigen (L)", min_value=0.0, value=10.0)

    air = kapasitas - sisa
    konsentrat = dosis * air

    st.write(f"💧 Tambahkan **{air:.2f} L air**")
    st.write(f"🧪 Tambahkan **{konsentrat:.2f} L fungisida**")

    draw_jerigen(sisa, kapasitas)

    if st.button("💾 Simpan Data", key="fungi_save"):
        entry = {
            "Tanggal": tanggal,
            "Waktu": waktu,
            "Menu": "Fungisida",
            "Kapasitas (L)": kapasitas,
            "Sisa Jerigen (L)": sisa,
            "Air Ditambahkan (L)": air,
            "Fungisida Ditambahkan (L)": konsentrat
        }
        save_history(entry, SHEET_NAME_FUNGISIDA)
        st.success("Data Fungisida berhasil disimpan ✅")


# ---------------- Furadan ----------------
with menu[1]:
    st.header("🐛 Input Furadan (kg)")
    jumlah = st.number_input("Jumlah Furadan (kg)", min_value=0.0, value=0.0)

    if st.button("💾 Simpan Data", key="fura_save"):
        entry = {
            "Tanggal": tanggal,
            "Waktu": waktu,
            "Menu": "Furadan",
            "Jumlah (kg)": jumlah
        }
        save_history(entry, SHEET_NAME_FURADAN)
        st.success("Data Furadan berhasil disimpan ✅")


# ---------------- Pupuk ----------------
with menu[2]:
    st.header("🌱 Input Pupuk (kg)")
    jumlah = st.number_input("Jumlah Pupuk (kg)", min_value=0.0, value=0.0)

    if st.button("💾 Simpan Data", key="pupuk_save"):
        entry = {
            "Tanggal": tanggal,
            "Waktu": waktu,
            "Menu": "Pupuk",
            "Jumlah (kg)": jumlah
        }
        save_history(entry, SHEET_NAME_PUPUK)
        st.success("Data Pupuk berhasil disimpan ✅")


# ---------------- BIN ----------------
with menu[3]:
    st.header("🧺 Input BIN (unit)")
    jumlah = st.number_input("Jumlah BIN", min_value=0, value=0)

    if st.button("💾 Simpan Data", key="bin_save"):
        entry = {
            "Tanggal": tanggal,
            "Waktu": waktu,
            "Menu": "BIN",
            "Jumlah (BIN)": jumlah
        }
        save_history(entry, SHEET_NAME_BIN)
        st.success("Data BIN berhasil disimpan ✅")


# ---------------- Riwayat ----------------
with menu[4]:
    st.header("📖 Riwayat Data")
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)

        # Tampilkan ringkasan per Tanggal + Menu
        numeric_cols = df.select_dtypes(include="number").columns
        summary = df.groupby(["Tanggal", "Menu"])[numeric_cols].sum().reset_index()

        st.subheader("📊 Ringkasan Harian")
        st.dataframe(summary)

        # Download ringkasan
        st.download_button(
            label="⬇️ Download Ringkasan",
            data=summary.to_csv(index=False).encode("utf-8"),
            file_name="riwayat_ringkasan.csv",
            mime="text/csv"
        )

        # Opsi: tampilkan data mentah juga
        with st.expander("📂 Lihat Data Mentah"):
            st.dataframe(df)

        # Hapus data dengan password
        st.subheader("🔑 Hapus Data (Admin Only)")
        pw = st.text_input("Masukkan password admin:", type="password")
        if pw == ADMIN_PASSWORD:
            index_to_delete = st.selectbox("Pilih index untuk dihapus:", df.index)
            if st.button("🗑️ Hapus Data"):
                df = df.drop(index=index_to_delete)
                df.to_csv(HISTORY_FILE, index=False)
                st.success("Data berhasil dihapus ✅")
                st.experimental_rerun()
        elif pw != "":
            st.error("❌ Password salah!")
    else:
        st.warning("Belum ada data riwayat.")
