import streamlit as st
import requests

st.title("Upload CV & Screening")

# --- Inisialisasi Session State
if "jurusan_options" not in st.session_state:
    st.session_state.jurusan_options = [
        "Business Management", "Accounting", "Computer Science", "Engineering",
        "Law", "Psychology", "Communication", "Other (isi manual)"
    ]
if "jurusan_selected" not in st.session_state:
    st.session_state.jurusan_selected = []

# --- Multiselect Jurusan
jurusan_selected = st.multiselect(
    "Jurusan (bisa pilih lebih dari 1, pilih 'Other (isi manual)' jika tidak ada di list)",
    options=st.session_state.jurusan_options,
    default=st.session_state.jurusan_selected,
    key="jurusan_multi"
)

# --- LOGIKA TAMBAH JURUSAN MANUAL
if "Other (isi manual)" in jurusan_selected:
    # Eksekusi logic tambah manual jika flag submit_jurusan_manual ada dan True
    if st.session_state.get("submit_jurusan_manual", False):
        st.session_state["submit_jurusan_manual"] = False  # Reset flag
        jurusan_manual_value = st.session_state.get("jurusan_manual", "").strip()
        if jurusan_manual_value:
            jur_baru = jurusan_manual_value
            # Cek agar tidak duplikat
            if jur_baru not in st.session_state.jurusan_options:
                idx = st.session_state.jurusan_options.index("Other (isi manual)")
                st.session_state.jurusan_options.insert(idx, jur_baru)
                st.session_state.jurusan_options.remove("Other (isi manual)")
                # Ganti "Other (isi manual)" di selected dengan jur_baru
                new_selected = [j for j in jurusan_selected if j != "Other (isi manual)"]
                new_selected.append(jur_baru)
                st.session_state.jurusan_selected = new_selected
                st.success(f"Jurusan '{jur_baru}' berhasil ditambahkan!")
            else:
                st.warning("Jurusan sudah ada di daftar.")
        else:
            st.warning("Input jurusan tidak boleh kosong.")
        # Reset field input manual (akan auto kosong setelah rerun)
        st.session_state["jurusan_manual"] = ""
        st.experimental_rerun()  # Jika error di versi lama, bisa dikomen saja

    # Widget input jurusan manual DIBAWAH logika submit!
    jurusan_manual = st.text_input(
        "Masukkan jurusan lain, lalu klik Tambah/Enter",
        key="jurusan_manual"
    )
    if st.button("Tambah jurusan manual"):
        st.session_state["submit_jurusan_manual"] = True
        st.experimental_rerun()  # Trigger rerun agar eksekusi logic di atas

# --- Sinkronisasi selected (penting untuk update state)
if set(jurusan_selected) != set(st.session_state.jurusan_selected):
    st.session_state.jurusan_selected = jurusan_selected

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

# --- Submit Screening
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
