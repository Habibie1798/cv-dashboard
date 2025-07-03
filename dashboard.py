import streamlit as st
import requests

st.title("Upload CV & Screening")

if "jurusan_custom" not in st.session_state:
    st.session_state.jurusan_custom = []

uploaded_file = st.file_uploader("Upload CV (PDF)")

jurusan_list = [
    "Business Management", "Accounting", "Computer Science", "Engineering",
    "Law", "Psychology", "Communication"
]

# Pilih jurusan dari dropdown + Other
jurusan_select = st.multiselect(
    "Jurusan (pilih dari list, klik 'Other' jika ingin jurusan manual)", 
    jurusan_list + ["Other"], 
    default=[]
)

# Jika pilih Other, tampilkan input
if "Other" in jurusan_select:
    custom_jurusan = st.text_input(
        "Masukkan jurusan lain (tekan Enter untuk menambah ke list)", 
        key="input_custom_jurusan"
    )
    # Tambah custom jurusan ke session_state ketika enter
    if custom_jurusan:
        if st.button("Tambah Jurusan"):
            if custom_jurusan not in st.session_state.jurusan_custom:
                st.session_state.jurusan_custom.append(custom_jurusan)
            # Kosongkan field input setelah ditambah
            st.session_state.input_custom_jurusan = ""

# Gabungkan semua jurusan yang akan dikirim
final_jurusan = [j for j in jurusan_select if j != "Other"] + st.session_state.jurusan_custom

st.write("Jurusan yang akan di-screening:", final_jurusan)

# Input lain seperti biasa
ipk = st.number_input("IPK Minimal", min_value=0.00, max_value=4.00, value=3.00, step=0.01, format="%.2f")
# ... [input lainnya, sama seperti sebelumnya]

if st.button("Screening"):
    if uploaded_file is not None:
        files = {
            "cv-file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        data = {
            "ipk_min": str(ipk),
            "jurusan_hr": ",".join(final_jurusan),
            # ... [data lain]
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
