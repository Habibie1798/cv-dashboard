import streamlit as st
import requests

st.title("Upload CV & Screening")

uploaded_file = st.file_uploader("Upload CV (PDF)")

# --- IPK (number input)
ipk = st.number_input(
    "IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f"
)

# --- Inisialisasi Session State untuk jurusan
if "jurusan_final" not in st.session_state:
    st.session_state["jurusan_final"] = []
if "other_mode" not in st.session_state:
    st.session_state["other_mode"] = False

# --- List pilihan jurusan
jurusan_list = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication"
]

# --- Multiselect jurusan + tombol "Other"
col1, col2 = st.columns([6,1])
with col1:
    jurusan_pilihan = st.multiselect(
        "Jurusan (pilih lebih dari 1 jika perlu)",
        jurusan_list + st.session_state["jurusan_final"],
        default=st.session_state["jurusan_final"]
    )
with col2:
    if st.button("Other"):
        st.session_state["other_mode"] = True

# --- Input manual jurusan jika klik "Other"
if st.session_state.get("other_mode", False):
    jurusan_manual = st.text_input("Masukkan jurusan lain (enter untuk tambah ke list):", key="input_jurusan")
    if jurusan_manual:
        jurusan_manual_clean = jurusan_manual.strip()
        # Tambahkan ke list jika belum ada
        if jurusan_manual_clean and jurusan_manual_clean not in st.session_state["jurusan_final"] and jurusan_manual_clean not in jurusan_list:
            st.session_state["jurusan_final"].append(jurusan_manual_clean)
        st.session_state["other_mode"] = False
        st.rerun()

# Update jurusan_final hanya jika multiselect diubah manual
# (tidak perlu reset saat nambah jurusan baru)
if not st.session_state.get("other_mode", False):
    st.session_state["jurusan_final"] = [j for j in jurusan_pilihan if j not in jurusan_list or j in st.session_state["jurusan_final"]]

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
