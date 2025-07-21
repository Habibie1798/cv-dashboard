import streamlit as st
import requests

st.title("Upload MULTIPLE CV & Screening Job Role")

# --- Upload MULTIPLE CV
uploaded_files = st.file_uploader(
    "Upload satu atau lebih CV (PDF)", 
    type=["pdf"], 
    accept_multiple_files=True
)

# --- Pilih Job Role (boleh Other/manual)
jobrole_list = [
    "Finance", "Product Manager", "Software Engineer", "Data Analyst",
    "HR", "Marketing", "Other"
]
job_role_select = st.selectbox("Job Role", jobrole_list)
job_role = st.text_input("Job Role (isi jika pilih 'Other')", key="job_role_manual") if job_role_select == "Other" else job_role_select

# --- Input Scope of Work & Qualification (WAJIB)
scope_of_work = st.text_area(
    "Deskripsi Lengkap Scope of Work / Job Description",
    help="Masukkan uraian tugas/jobdesc dari role yang akan di-screening"
)
qualification = st.text_area(
    "Daftar Qualification (kualifikasi minimum, satu baris satu syarat)",
    help="Contoh:\nS1 Akuntansi\nPengalaman min 2 tahun\nBrevet Pajak"
)

# --- Input Parameter Screening Lainnya
ipk = st.number_input("IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f")
min_years_exp = st.number_input("Minimal Pengalaman Kerja (tahun)", min_value=0, max_value=50, value=0, step=1)
max_age = st.number_input("Usia Maksimal", min_value=0, max_value=100, value=35, step=1)
sertifikasi_wajib = st.text_input("Sertifikasi Wajib (opsional, pisahkan koma)")
skill_wajib = st.text_input("Skill Wajib (opsional, pisahkan koma)")
nilai_toefl = st.text_input("Nilai TOEFL Minimal (opsional)")
lokasi_list = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Remote", "Other"
]
lokasi_select = st.selectbox("Lokasi (opsional)", lokasi_list)
lokasi = st.text_input("Lokasi (isi jika pilih 'Other', boleh kosong)", key="lokasi_manual") if lokasi_select == "Other" else lokasi_select

# --- Tombol screening dengan validasi input wajib
if st.button("Screening Semua CV", key="btn_screening_multi"):
    # Validasi field wajib
    if not uploaded_files or len(uploaded_files) == 0:
        st.warning("Mohon upload minimal satu file CV (PDF).")
    elif not job_role or not job_role.strip():
        st.warning("Mohon pilih atau isi job role.")
    elif not scope_of_work or not scope_of_work.strip():
        st.warning("Mohon isi Scope of Work / Jobdesc.")
    elif not qualification or not qualification.strip():
        st.warning("Mohon isi minimal 1 Qualification!")
    else:
        st.info("Screening berjalan... Mohon tunggu hasil tiap CV muncul di bawah.")

        # --- Print DEBUG data yang dikirim (untuk memastikan field tidak kosong)
        st.write("DEBUG Payload yang dikirim (untuk 1 CV):")
        st.code({
            "ipk_min": str(ipk),
            "job_role": job_role.strip(),
            "min_years_exp": str(min_years_exp),
            "max_age": str(max_age),
            "sertifikasi_wajib": sertifikasi_wajib.strip(),
            "skill_wajib": skill_wajib.strip(),
            "lokasi": lokasi.strip(),
            "nilai_toefl": nilai_toefl.strip(),
            "scope_of_work": scope_of_work.strip(),
            "qualification": qualification.strip(),
        })

        for uploaded_file in uploaded_files:
            with st.spinner(f"Screening: {uploaded_file.name} ..."):
                files = {
                    "cv-file": (uploaded_file.name, uploaded_file, "application/pdf")
                }
                data = {
                    "ipk_min": str(ipk),
                    "job_role": job_role.strip(),
                    "min_years_exp": str(min_years_exp),
                    "max_age": str(max_age),
                    "sertifikasi_wajib": sertifikasi_wajib.strip(),
                    "skill_wajib": skill_wajib.strip(),
                    "lokasi": lokasi.strip(),
                    "nilai_toefl": nilai_toefl.strip(),
                    "scope_of_work": scope_of_work.strip(),
                    "qualification": qualification.strip(),
                }
                try:
                    res = requests.post(
                        "https://talentdna.lintasarta.net/n8n/webhook/cv-analyzer",
                        files=files, data=data
                    )
                    if res.ok:
                        hasil = res.json()
                        st.success(f"Hasil Screening: {uploaded_file.name}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Status Akhir:** `{hasil.get('status', '-')}`")
                            st.markdown(f"**Persentase Kecocokan:** `{hasil.get('persentase', '-')}`%")
                            st.markdown(f"**Penjelasan Singkat:** {hasil.get('penjelasan', '-')}")
                        with col2:
                            st.markdown("**Scope of Work:**")
                            st.info(hasil.get("evaluasi_scope", "-"))

                        st.markdown("**Evaluasi Qualification:**")
                        st.info(hasil.get("evaluasi_qualification", "-"))

                        with st.expander(f"Lihat Detail Output Full {uploaded_file.name}"):
                            st.code(hasil.get("hasil_screening_full", "-"))
                    else:
                        st.error(f"Gagal screening {uploaded_file.name}. Status: {res.status_code}, Detail: {res.text}")
                except Exception as e:
                    st.error(f"Terjadi error pada file {uploaded_file.name}: {e}")
