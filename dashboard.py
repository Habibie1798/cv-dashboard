import streamlit as st
import requests

st.title("Upload CV & Screening")

# --- List jurusan dan session state
JURUSAN_DEFAULT = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication"
]

if "jurusan_options" not in st.session_state:
    st.session_state.jurusan_options = JURUSAN_DEFAULT.copy()
if "jurusan_selected" not in st.session_state:
    st.session_state.jurusan_selected = []
if "jurusan_manual_list" not in st.session_state:
    st.session_state.jurusan_manual_list = []

# --- Checkbox list jurusan
st.subheader("Pilih Jurusan")
selected_jurusan = []
for jurusan in st.session_state.jurusan_options:
    cek = st.checkbox(jurusan, key=f"cek_{jurusan}", value=jurusan in st.session_state.jurusan_selected)
    if cek:
        selected_jurusan.append(jurusan)

# --- Tambah jurusan manual
with st.expander("Tambah Jurusan Lain (Manual)"):
    jurusan_manual = st.text_input("Masukkan jurusan lain", key="jurusan_manual_input", value="")
    if st.button("Tambah jurusan manual"):
        jur_baru = jurusan_manual.strip()
        if jur_baru and jur_baru not in st.session_state.jurusan_options:
            st.session_state.jurusan_options.append(jur_baru)
            st.session_state.jurusan_manual_list.append(jur_baru)
            st.success(f"Jurusan '{jur_baru}' berhasil ditambahkan!")
            st.experimental_rerun()
        elif jur_baru in st.session_state.jurusan_options:
            st.warning("Jurusan sudah ada di list.")
        else:
            st.warning("Input jurusan tidak boleh kosong.")

# --- Simpan selection jurusan di session state
st.session_state.jurusan_selected = selected_jurusan

# --- Upload CV
uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

# --- Input lain
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
        jurusan_final = st.session_state.jurusan_selected
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
