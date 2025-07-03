import streamlit as st
import requests

st.title("Upload CV & Screening")

uploaded_file = st.file_uploader("Upload CV (PDF)")

# --- IPK (number input)
ipk = st.number_input(
    "IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f"
)

# --- Inisialisasi session_state
if "jurusan_all" not in st.session_state:
    st.session_state["jurusan_all"] = []
if "jurusan_options" not in st.session_state:
    st.session_state["jurusan_options"] = [
        "Business Management", "Accounting", "Computer Science", "Engineering",
        "Law", "Psychology", "Communication", "Other (isi manual)"
    ]

# --- Multiselect jurusan
jurusan_selected = st.multiselect(
    "Jurusan (bisa pilih lebih dari 1, pilih 'Other (isi manual)' jika tidak ada di list)",
    st.session_state["jurusan_options"],
    default=st.session_state["jurusan_all"]
)

# --- Input manual jurusan jika 'Other (isi manual)' dipilih
if "Other (isi manual)" in jurusan_selected:
    jurusan_manual = st.text_input("Masukkan jurusan lain, lalu tekan Enter:")
    if jurusan_manual.strip():
        # tambahkan ke list (tanpa duplikat)
        new_list = [j for j in jurusan_selected if j != "Other (isi manual)"]
        if jurusan_manual.strip() not in st.session_state["jurusan_options"]:
            st.session_state["jurusan_options"].insert(-1, jurusan_manual.strip())
        new_list.append(jurusan_manual.strip())
        st.session_state["jurusan_all"] = new_list
        st.experimental_rerun()  # update state, hilangkan 'Other', tambah jurusan manual

# --- Update pilihan jika bukan di mode Other
else:
    st.session_state["jurusan_all"] = jurusan_selected

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
        jurusan_hr = [j for j in st.session_state["jurusan_all"] if j != "Other (isi manual)"]
        files = {
            "cv-file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        data = {
            "ipk_min": str(ipk),
            "jurusan_hr": ", ".join(jurusan_hr),
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
