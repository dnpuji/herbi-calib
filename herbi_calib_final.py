import streamlit as st
import matplotlib.pyplot as plt
import datetime
import pandas as pd

# Simpan riwayat input
history_file = "history.csv"

def load_history():
    try:
        return pd.read_csv(history_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Waktu", "Kapasitas (L)", "Sisa Isi (L)", "Dosis (L/L)", "Air Tambah (L)", "Konsentrat Tambah (L)"])

def save_history(new_entry):
    df = load_history()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(history_file, index=False)

# Judul aplikasi
st.set_page_config(page_title="Herbicide Calibration Web", page_icon="🌱", layout="centered")
st.title("🌱 Herbicide Calibration Web")

st.subheader("Input Data")
kapasitas = st.number_input("Kapasitas Jerigen (L)", min_value=1.0, value=20.0, step=1.0)
dosis = st.number_input("Dosis Herbisida (L konsentrat / L campuran)", min_value=0.01, value=0.24, step=0.01)
sisa_isi = st.number_input("Sisa Isi Jerigen (L)", min_value=0.0, value=0.0, step=0.1, max_value=kapasitas)

# Hitung tambahan yang diperlukan
total_tambahan = kapasitas - sisa_isi
konsentrat_tambah = dosis * total_tambahan
air_tambah = total_tambahan - konsentrat_tambah

if total_tambahan > 0:
    st.success(f"Untuk mengisi jerigen hingga {kapasitas:.2f} L:")
    st.write(f"- Tambahkan **{air_tambah:.2f} L air**")
    st.write(f"- Tambahkan **{konsentrat_tambah:.2f} L konsentrat**")
else:
    st.info("Jerigen sudah penuh ✅")

# Visualisasi jerigen (vertikal)
st.subheader("Visualisasi Jerigen (Vertikal)")

fig, ax = plt.subplots(figsize=(2, 5))

# Bagian isi
ax.bar(0, sisa_isi, color="green", label=f"Isi {sisa_isi:.2f} L")
# Bagian kosong
ax.bar(0, kapasitas - sisa_isi, bottom=sisa_isi, color="yellow", label=f"Kosong {kapasitas - sisa_isi:.2f} L")

ax.set_ylim(0, kapasitas)
ax.set_xlim(-0.5, 0.5)
ax.set_ylabel("Liter")
ax.set_xticks([])
ax.set_title("Isi Jerigen")
ax.legend()

st.pyplot(fig)

# Simpan ke riwayat
if st.button("💾 Simpan ke Riwayat"):
    entry = {
        "Waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Kapasitas (L)": kapasitas,
        "Sisa Isi (L)": sisa_isi,
        "Dosis (L/L)": dosis,
        "Air Tambah (L)": air_tambah,
        "Konsentrat Tambah (L)": konsentrat_tambah
    }
    save_history(entry)
    st.success("Data berhasil disimpan ke riwayat!")

# Tampilkan riwayat
st.subheader("📜 Riwayat Input")
history = load_history()
st.dataframe(history)
