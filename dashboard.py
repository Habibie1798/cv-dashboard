import streamlit as st
import requests

st.title("Upload CV & Screening")

uploaded_file = st.file_uploader("Upload CV (PDF)")

# --- IPK (bisa klik panah, default 3.00, min 0, max 4, step 0.01)
ipk = st.number_input("IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f")

# --- Jurusan (multi-select + custom)
jurusan_list = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication", "Other (isi manual)"
]
jurusan_multi = st.multiselect(
    "Jurusan (bisa pilih lebih dari 1)",
    jurusan_list,
    default=[]
)

# Input manual jika pilih 'Other (isi manual)'
jurusan_lain = ""
if "Other (isi manual)" in jurusan_multi:
    jurusan_lain = st.text_input("Tambahkan jurusan lain (pisahkan koma jika lebih dari 1)")

# Gabungkan semua jurusan ke satu list
jurusan_hr = [j for j in jurusan_multi if j != "Other (isi manual)"]
if jurusan_lain:
    jurusan_hr += [j.strip() for j in jurusan_lain.split(",") if j.strip()]

# Ubah ke string (biar gampang, nanti di n8n bisa split atau langsung pakai LLM prompt)
jurusan_hr_str = ", ".join(jurusan_hr)

# --- Job Role (dropdown + custom)
jobrole_list = [
    "Finance", "Product Manager", "Software Engineer", "Data Analyst",
    "HR", "Marketing", "Other"
]
job_role_select = st.selectbox("Job Role", jobrole_list)
job_role = st.text_input("Job Role (isi jika pilih 'Other')") if job_role_select == "Other" else job_role_select

# --- Lokasi (dropdown + custom)
lokasi_list = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Remote", "Other"
]
lokasi_select = st.selectbox("Lokasi (opsional)", lokasi_list)
lokasi = st.text_input("Lokasi (isi jika pilih 'Other', boleh kosong)", value="") if lokasi_select == "Other" else lokasi_select

min_years_exp = st.number_input("Minimal Pengalaman Kerja (tahun)", min_value=0, max_value=50, value=0, step=1)
max_age = st.number_input("Usia Maksimal", min_value=0, max_value=100, value=35, step=1)

sertifikasi_wajib = st.text_input("Sertifikasi Wajib (opsional, pisahkan koma)")
skill_wajib = st.text_input("Skill Wajib (opsional, pisahkan koma)")
nilai_toefl = st.text_input("Nilai TOEFL Minimal (opsional)")

if st.button("Screening"):
    if uploaded_file is not None:
        files = {
            "cv-file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        data = {
            "ipk_min": str(ipk),
            "jurusan_hr": jurusan_hr_str,   # multi-jurusan dipisah koma
            "job_role": job_role,
            "min_years_exp": str(min_years_exp),
            "max_age": str(max_age),
            "sertifikasi_wajib": sertifikasi_wajib,
            "skill_wajib": skill_wajib,
            "lokasi": lokasi,
            "nilai_toefl": nilai_toefl
        }
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
    else:
        st.warning("Mohon upload file CV dulu.")
