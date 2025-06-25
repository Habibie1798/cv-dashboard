import streamlit as st
import requests

# Ganti URL di bawah dengan endpoint Webhook n8n kamu!
N8N_URL = "https://talentdna.lintasarta.net/n8n/webhook-test/cv-analyzer"

st.title("Dashboard Hasil CV Screening")

# (Opsional) Bisa pakai text_input kalau endpoint dynamic
# N8N_URL = st.text_input("Masukkan URL endpoint:", N8N_URL)

# Ambil data dari n8n Webhook
try:
    response = requests.get(N8N_URL)
    data = response.json()
    st.success("Data berhasil diambil!")

    # Tampilkan data
    st.header("Detail Kandidat")
    st.write(f"**Nama:** {data['full_name']}")
    st.write(f"**Score Kecocokan:** {data['match_score']}")
    st.write(f"**Summary:** {data['summary']}")

    st.subheader("Skills")
    st.write(", ".join(data["skills"]))

    # Visualisasi Score (contoh: gauge atau bar)
    st.progress(int(data['match_score']))

except Exception as e:
    st.error(f"Error mengambil data: {e}")

