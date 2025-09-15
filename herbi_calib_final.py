import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

HISTORY_FILE = "history.csv"

# Fungsi simpan history
def save_history(menu, data_dict):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {"menu": menu, "timestamp": now}
    record.update(data_dict)

    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])
    df.to_csv(HISTORY_FILE, index=False)

# Sidebar
st.sidebar.title("📌 Menu Utama")
menu = st.sidebar.radio(
    "Pilih menu:",
    ["🍄 Fungisida", "🐛 Furadan", "🌿 Pupuk", "🧺 BIN", "📖 Riwayat"]
)

# ---------------- Fungisida ----------------
if menu == "🍄 Fungisida":
    st.title("🍄 Kebutuhan Fungisida")

    kapasitas = st.number_input("Kapasitas jerigen (L)", min_value=1, value=20)
    dosis = st.number_input("Dosis fungisida (L konsentrat / L air)", min_value=0.0, value=0.24, step=0.01)
    sisa_jerigen = st.number_input("Sisa isi di jerigen (L)", min_value=0.0, value=0.0)

    sudah_terisi = sisa_jerigen
    masih_kosong = kapasitas - sudah_terisi

    air_tambah = masih_kosong
    konsentrat_tambah = masih_kosong * dosis

    st.subheader("📊 Hasil Perhitungan")
    st.success(f"Sisa isi di jerigen: **{sudah_terisi} L**")
    st.info(f"Tambahkan Air: **{air_tambah:.2f} L**")
    st.warning(f"Tambahkan Fungisida: **{konsentrat_tambah:.2f} L**")
    st.write(f"Kapasitas penuh jerigen: **{kapasitas} L (air + fungisida)**")

    # Visualisasi jerigen
    fig, ax = plt.subplots(figsize=(2,6))
    ax.bar(0, sudah_terisi, color="green", label="Isi (L)")
    ax.bar(0, masih_kosong, bottom=sudah_terisi, color="yellow", label="Kosong (L)")
    ax.set_ylim(0, kapasitas)
    ax.set_xticks([])
    ax.set_ylabel("Liter")
    ax.legend()
    st.pyplot(fig)

    # Simpan history
    save_history("Fungisida", {
        "kapasitas": kapasitas,
        "sisa": sudah_terisi,
        "air_tambah": air_tambah,
        "fungisida_tambah": konsentrat_tambah
    })

    # Download CSV khusus Fungisida
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df_fungisida = df[df["menu"] == "Fungisida"]
        st.download_button(
            label="⬇️ Download Data Fungisida",
            data=df_fungisida.to_csv(index=False).encode("utf-8"),
            file_name="fungisida_history.csv",
            mime="text/csv"
        )

# ---------------- Furadan ----------------
elif menu == "🐛 Furadan":
    st.title("🐛 Total Furadan yang Digunakan (kg)")
    furadan_total = st.number_input("Masukkan total Furadan (kg)", min_value=0.0, value=0.0, step=0.1)
    st.success(f"Total Furadan digunakan: **{furadan_total} kg**")

    save_history("Furadan", {"furadan_total_kg": furadan_total})

    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df_furadan = df[df["menu"] == "Furadan"]
        st.download_button(
            label="⬇️ Download Data Furadan",
            data=df_furadan.to_csv(index=False).encode("utf-8"),
            file_name="furadan_history.csv",
            mime="text/csv"
        )

# ---------------- Pupuk ----------------
elif menu == "🌿 Pupuk":
    st.title("🌿 Total Pupuk yang Digunakan (kg)")
    pupuk_total = st.number_input("Masukkan total Pupuk (kg)", min_value=0.0, value=0.0, step=0.1)
    st.success(f"Total Pupuk digunakan: **{pupuk_total} kg**")

    save_history("Pupuk", {"pupuk_total_kg": pupuk_total})

    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df_pupuk = df[df["menu"] == "Pupuk"]
        st.download_button(
            label="⬇️ Download Data Pupuk",
            data=df_pupuk.to_csv(index=False).encode("utf-8"),
            file_name="pupuk_history.csv",
            mime="text/csv"
        )

# ---------------- BIN ----------------
elif menu == "🧺 BIN":
    st.title("🧺 Data BIN (wadah bibit)")
    jumlah_bin = st.number_input("Jumlah BIN terpakai", min_value=1, value=10)
    st.success(f"Total BIN digunakan: **{jumlah_bin} BIN**")

    save_history("BIN", {"jumlah_bin": jumlah_bin})

    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        df_bin = df[df["menu"] == "BIN"]
        st.download_button(
            label="⬇️ Download Data BIN",
            data=df_bin.to_csv(index=False).encode("utf-8"),
            file_name="bin_history.csv",
            mime="text/csv"
        )

# ---------------- Riwayat ----------------
elif menu == "📖 Riwayat":
    st.title("📖 Riwayat Data Penggunaan")
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download Semua Data",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="all_history.csv",
            mime="text/csv"
        )
    else:
        st.warning("Belum ada riwayat data yang tersimpan.")
