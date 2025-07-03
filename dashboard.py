import streamlit as st
import requests

st.title("Upload CV & Screening")

uploaded_file = st.file_uploader("Upload CV (PDF)")

# List jurusan utama + Other
jurusan_list = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication", "Other (isi manual)"
]

if "jurusan_selected" not in st.session_state:
    st.session_state["jurusan_selected"] = []
if "show_manual_jurusan" not in st.session_state:
    st.session_state["show_manual_jurusan"] = False

# Step 1: Multiselect
jurusan_selected = st.multiselect(
    "Jurusan (bisa pilih lebih dari 1, klik 'Other' jika jurusan tidak ada di list)",
    options=jurusan_list,
    default=st.session_state["jurusan_selected"]
)

# Step 2: Deteksi klik "Other"
if "Other (isi manual)" in jurusan_selected and not st.session_state["show_manual_jurusan"]:
    st.session_state["show_manual_jurusan"] = True

# Step 3: Input manual jika pilih Other
if st.session_state["show_manual_jurusan"]:
    jurusan_manual = st.text_input("Masukkan jurusan manual, lalu tekan Enter")

    # Saat user input jurusan manual dan tekan Enter (bukan kosong)
    if jurusan_manual:
        # Tambah ke list jurusan (pastikan tidak duplikat)
        st.session_state["jurusan_selected"] = [
            j for j in jurusan_selected if j != "Other (isi manual)"
        ] + [jurusan_manual]
        # Reset input manual & kolomnya hilang
        st.session_state["show_manual_jurusan"] = False
        st.experimental_rerun()

else:
    # Jika Other tidak terpilih, simpan jurusan yang ada
    st.session_state["jurusan_selected"] = [j for j in jurusan_selected if j != "Other (isi manual)"]

# --- Tampilkan list jurusan final yang akan di-screening
st.markdown("#### Jurusan yang akan di-screening:")
st.write(st.session_state["jurusan_selected"])

# --- Lanjut field lain seperti sebelumnya ---
ipk = st.number_input(
    "IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f"
)

# Job Role
jobrole_list = [
    "Finance", "Product Manager", "Software Engineer", "Data Analyst",
    "HR", "Marketing", "Other"
]
job_role_select = st.selectbox("Job Role", jobrole_list)
job_role = st.text_input("Job Role (isi jika pilih 'Other')") if job_role_select == "Other" else job_role_select

# Lokasi
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
        # Kirim list jurusan final, join pakai koma
        data = {
            "ipk_min": str(ipk),
            "jurusan_hr": ", ".join(st.session_state["jurusan_selected"]),
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
