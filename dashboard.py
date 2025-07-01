import streamlit as st
import requests

st.title("Upload CV & Screening")

uploaded_file = st.file_uploader("Upload CV (PDF)")
ipk = st.text_input("IPK Minimal")
jurusan = st.text_input("Jurusan")
job_role = st.text_input("Job Role")

if st.button("Screening"):
    if uploaded_file is not None:
        files = {"cv-file": uploaded_file}
        data = {
            "ipk_min": ipk,
            "jurusan_hr": jurusan,
            "job_role": job_role
        }
        # Ganti URL di bawah dengan URL webhook n8n kamu
        res = requests.post("https://talentdna.lintasarta.net/n8n/webhook-test/cv-analyzer", files=files, data=data)
        if res.ok:
            hasil = res.json()
            st.success("Hasil Screening:")
            st.write(hasil.get("hasil_screening", hasil))
        else:
            st.error("Gagal screening. Coba lagi.")
    else:
        st.warning("Mohon upload file CV dulu.")
