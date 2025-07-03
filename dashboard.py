import streamlit as st
import requests

st.title("Upload CV & Screening")

# --- Session state for jurusan
if "jurusan_final" not in st.session_state:
    st.session_state["jurusan_final"] = []
if "other_mode" not in st.session_state:
    st.session_state["other_mode"] = False

# --- Jurusan options
jurusan_list_awal = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication"
]
options = jurusan_list_awal + ["Other (isi manual)"]

# --- Only use options for default value in multiselect!
default_jurusan = [j for j in st.session_state["jurusan_final"] if j in options]

jurusan_pilihan = st.multiselect(
    "Jurusan (bisa pilih lebih dari 1, klik 'Other' jika jurusan tidak ada di list)",
    options=options,
    default=default_jurusan,
    key="jurusan_multi"
)

# ---- Input jurusan manual jika "Other" dipilih
if "Other (isi manual)" in jurusan_pilihan or st.session_state["other_mode"]:
    st.session_state["other_mode"] = True
    jurusan_manual = st.text_input("Masukkan jurusan manual, lalu tekan Enter", value="")
    if jurusan_manual:
        jurusan_manual_clean = jurusan_manual.strip()
        # Tambahkan ke list final jika belum ada
        if jurusan_manual_clean and jurusan_manual_clean not in st.session_state["jurusan_final"]:
            st.session_state["jurusan_final"].append(jurusan_manual_clean)
        # Hapus "Other" dari list final jika ada
        st.session_state["jurusan_final"] = [j for j in st.session_state["jurusan_final"] if j != "Other (isi manual)"]
        st.session_state["other_mode"] = False
        # Reset input field
        st.experimental_rerun()
else:
    # Update jurusan_final hanya dari pilihan multiselect (kecuali "Other")
    st.session_state["jurusan_final"] = [j for j in jurusan_pilihan if j != "Other (isi manual)"]

jurusan_final = st.session_state["jurusan_final"]

# ----------- IPK (number input, ada panah)
ipk = st.number_input(
    "IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f"
)

# ----------- Job Role
jobrole_list = [
    "Finance", "Product Manager", "Software Engineer", "Data Analyst",
    "HR", "Marketing", "Other"
]
job_role_select = st.selectbox("Job Role", jobrole_list)
job_role = st.text_input("Job Role (isi jika pilih 'Other')") if job_role_select == "Other" else job_role_select

# ----------- Lokasi
lokasi_list = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Remote", "Other"
]
lokasi_select = st.selectbox("Lokasi (opsional)", lokasi_list)
lokasi = st.text_input("Lokasi (isi jika pilih 'Other', boleh kosong)", value="") if lokasi_select == "Other" else lokasi_select

# ----------- Field lain
min_years_exp = st.number_input("Minimal Pengalaman Kerja (tahun)", min_value=0, max_value=50, value=0, step=1)
max_age = st.number_input("Usia Maksimal", min_value=0, max_value=100, value=35, step=1)
sertifikasi_wajib = st.text_input("Sertifikasi Wajib (opsional, pisahkan koma)")
skill_wajib = st.text_input("Skill Wajib (opsional, pisahkan koma)")
nilai_toefl = st.text_input("Nilai TOEFL Minimal (opsional)")

# ----------- Upload CV & Submit
uploaded_file = st.file_uploader("Upload CV (PDF)")

if st.button("Screening"):
    if uploaded_file is not None and len(jurusan_final) > 0:
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
    elif len(jurusan_final) == 0:
        st.warning("Mohon pilih/isi setidaknya 1 jurusan.")
    else:
        st.warning("Mohon upload file CV dulu.")
