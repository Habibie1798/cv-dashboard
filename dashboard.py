import streamlit as st
import requests

N8N_URL = "https://talentdna.lintasarta.net/n8n/webhook-test/cv-analyzer"

st.title("Dashboard Hasil CV Screening")

uploaded_file = st.file_uploader("Upload CV (PDF)", type="pdf")

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    with st.spinner("Mengirim file ke n8n..."):
        response = requests.post(N8N_URL, files=files)
        try:
            data = response.json()
            st.success("Data berhasil diambil!")
            st.write("RAW JSON:", data)  # Untuk debugging

            st.header("Detail Kandidat")
            st.write(f"**Nama:** {data.get('full_name', '-')}")
            st.write(f"**Domisili:** {data.get('domicile', '-')}")
            st.write(f"**No. HP:** {data.get('phone_number', '-')}")
            st.write(f"**Email:** {data.get('email', '-')}")
            st.write(f"**Summary:** {data.get('summary', '-')}")

            st.subheader("Skills")
            # skills: dict of skill_name: bool
            skills_true = [k.title() for k, v in data["skills"].items() if v]
            skills_false = [k.title() for k, v in data["skills"].items() if not v]
            st.write("✅ " + ", ".join(skills_true))
            if skills_false:
                st.write("❌ " + ", ".join(skills_false))

            st.subheader("Skor Pengalaman & Pendidikan")
            exp = data.get("experience_score", {})
            for aspek in exp:
                st.write(
                    f"**{aspek.title()} Score:** {exp[aspek].get(aspek + '_score', '-')}"
                )
                st.caption(exp[aspek].get(aspek + "_reason", "-"))

        except Exception as e:
            st.error(f"Error mengambil data: {e}")
else:
    st.info("Silakan upload file CV untuk mulai screening.")
