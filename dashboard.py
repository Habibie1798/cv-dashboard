import streamlit as st
from streamlit_tags import st_tags
import requests

st.title("Upload CV & Screening")

# --- List jurusan awal
JURUSAN_AWAL = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication"
]

if "jurusan_list" not in st.session_state:
    st.session_state.jurusan_list = []

jurusan_list = st_tags(
    label="Jurusan (boleh lebih dari satu, boleh input manual!)",
    text="Ketik jurusan lalu tekan Enter. Atau pilih dari dropdown.",
    value=st.session_state.jurusan_list,
    suggestions=JURUSAN_AWAL,
    maxtags=10,
    key="jurusan_tags"
)

# Simpan hasil ke session state
st.session_state.jurusan_list = jurusan_list

# --- Upload CV
uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

# --- Input lainnya
ipk = st.number_input("IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f")

jobrole_list = [
    "Finance", "Product Manager", "Software Engineer", "Data Analyst",
    "HR", "Marketing", "Other"
]
job_role_select = st.selectbox("Job Role", jobrole_list)
job_role = st.text_input("Job Role (isi jika pilih 'Other')", key="job_role_manual") if job_role_select == "Other" else job_role_select

lokasi_list = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Remote", "Other"
]
lokasi_select = st.selectbox("Lokasi (opsional)", lokasi_list)
lokasi = st.text_input("Lokasi (isi jika pilih 'Other', boleh kosong)", key="lokasi_manual") if lokasi_select == "Other" else lokasi_select

min_years_exp = st.number_input("Minimal Pengalaman Kerja (tahun)", min_value=0, max_value=50, value=0, step=1)
max_age = st.number_input("Usia Maksimal", min_value=0, max_value=100, value=35, step=1)

sertifikasi_wajib = st.text_input("Sertifikasi Wajib (opsional, pisahkan koma)")
skill_wajib = st.text_input("Skill Wajib (opsional, pisahkan koma)")
nilai_toefl = st.text_input("Nilai TOEFL Minimal (opsional)")

if st.button("Screening", key="btn_screening"):
    if uploaded_file is not None:
        jurusan_final = st.session_state.jurusan_list
        files = {
            "cv-file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        data = {
            "ipk_min": str(ipk),
            "jurusan_hr": ", ".join(jurusan_final),
            "job_role": job_role,
            "min_years_exp": str(min_years_exp),
            "max_age": str(max_age),
            "sertifikasi_wajib": sertifikasi_wajib,
            "skill_wajib": skill_wajib,
            "lokasi": lokasi,
            "nilai_toefl": nilai_toefl
        }
        try:
            res = requests.post(
                "https://talentdna.lintasarta.net/n8n/webhook-test/cv-analyzer",
                files=files, data=data
            )
            if res.ok:
                hasil = res.json()
                st.success("Hasil Screening:")
                st.write(hasil.get("hasil_screening", hasil))
            else:
                st.error(f"Gagal screening. Status: {res.status_code}, Detail: {res.text}")
        except Exception as e:
            st.error(f"Terjadi error saat screening: {e}")
    else:
        st.warning("Mohon upload file CV dulu.")
