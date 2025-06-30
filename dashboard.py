import streamlit as st
import requests

N8N_URL = "https://talentdna.lintasarta.net/n8n/webhook-test/cv-analyzer"

st.title("Dashboard Hasil CV Screening")

with st.form("hr_requirement"):
    position = st.text_input("Posisi yang dicari", "Product Manager")
    required_skills = st.text_input("Skill wajib (pisahkan koma)", "leadership, digital marketing")
    min_gpa = st.number_input("Minimal IPK", 0.0, 4.0, 3.0, 0.01)
    uploaded_file = st.file_uploader("Upload CV (PDF)", type="pdf")
    submitted = st.form_submit_button("Screening Sekarang")

if submitted and uploaded_file:
    files = {"cv-file": (uploaded_file.name, uploaded_file, "application/pdf")}
    data = {
        "position": position,
        "required_skills": required_skills,
        "min_gpa": min_gpa
    }
    with st.spinner("Mengirim file ke n8n..."):
        response = requests.post(N8N_URL, files=files, data=data)
        try:
            data = response.json()
            st.success("Data berhasil diambil!")
            # --- Tampilkan hasil screening dengan rapih ---
            st.header("Detail Kandidat")
            st.write(f"**Nama:** {data.get('full_name', '-')}")
            st.write(f"**Domisili:** {data.get('domicile', '-')}")
            st.write(f"**No. HP:** {data.get('phone_number', '-')}")
            st.write(f"**Email:** {data.get('email', '-')}")
            st.write(f"**Summary:** {data.get('summary', '-')}")

            st.subheader("Skills Kandidat")
            skills_true = [k.title() for k, v in data["skills"].items() if v]
            skills_false = [k.title() for k, v in data["skills"].items() if not v]
            st.write("✅ " + ", ".join(skills_true))
            if skills_false:
                st.write("❌ " + ", ".join(skills_false))

            # --- BAGIAN PENTING: Hasil Screening otomatis ---
            st.subheader("Hasil Screening Requirement HR")
            result = data.get("requirement_match", {})
            st.write(f"**Posisi:** {result.get('position', '-')}")
            st.write(f"**Overall Status:** {'🟢 LOLOS' if result.get('overall_status') == 'LOLOS' else '🔴 TIDAK LOLOS'}")
            st.write(f"**Minimal IPK:** {result.get('min_gpa', '-')}")
            st.write(f"**IPK Kandidat:** {result.get('gpa_value', '-')}")
            st.write(f"**Cocok IPK?** {'✅' if result.get('gpa_match') else '❌'}")
            st.write(f"**Skill Match:** ✅ " + ", ".join(result.get('skills_match', [])))
            st.write(f"**Skill Not Match:** ❌ " + ", ".join(result.get('skills_not_match', [])))
        except Exception as e:
            st.error(f"Error mengambil data: {e}")

elif uploaded_file is None:
    st.info("Silakan upload file CV untuk mulai screening.")
