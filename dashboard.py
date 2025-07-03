import streamlit as st
import requests

st.title("Upload CV & Screening")

# List jurusan awal
jurusan_list_awal = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication"
]

# State untuk jurusan
if "jurusan_final" not in st.session_state:
    st.session_state["jurusan_final"] = []
if "other_mode" not in st.session_state:
    st.session_state["other_mode"] = False
if "jurusan_manual" not in st.session_state:
    st.session_state["jurusan_manual"] = ""

# Pilih dari list (multi)
jurusan_pilihan = st.multiselect(
    "Jurusan (bisa pilih lebih dari 1, klik 'Other' jika jurusan tidak ada di list)",
    options=jurusan_list_awal + ["Other (isi manual)"],
    default=st.session_state["jurusan_final"] if not st.session_state["other_mode"] else [],
    key="jurusan_multi"
)

# Jika pilih Other (isi manual), munculkan input
if "Other (isi manual)" in jurusan_pilihan or st.session_state["other_mode"]:
    st.session_state["other_mode"] = True
    jurusan_manual = st.text_input("Masukkan jurusan manual, lalu tekan Enter", key="jurusan_manual")
    # Jika ada input, tambahkan ke list lalu reset mode
    if jurusan_manual:
        if jurusan_manual not in st.session_state["jurusan_final"]:
            st.session_state["jurusan_final"].append(jurusan_manual)
        st.session_state["other_mode"] = False
        st.session_state["jurusan_manual"] = ""
        st.experimental_set_query_params(**{})  # mini refresh
        st.stop()
else:
    # Update list kalau tidak sedang mode other
    st.session_state["jurusan_final"] = jurusan_pilihan

# Tampilkan jurusan final (hanya untuk cek, bisa dihapus)
# st.write("Jurusan yang dipilih:", st.session_state["jurusan_final"])

# Input lain seperti sebelumnya...
ipk = st.number_input("IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f")
jobrole_list = [
    "Finance", "Product Manager", "Software Engineer", "Data Analyst",
    "HR", "Marketing", "Other"
]
job_role_select = st.selectbox("Job Role", jobrole_list)
job_role = st.text_input("Job Role (isi jika pilih 'Other')") if job_role_select == "Other" else job_role_select
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
uploaded_file = st.file_uploader("Upload CV (PDF)")

if st.button("Screening"):
    if uploaded_file is not None:
        files = {
            "cv-file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        data = {
            "ipk_min": str(ipk),
            "jurusan_hr": ", ".join(st.session_state["jurusan_final"]),
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
