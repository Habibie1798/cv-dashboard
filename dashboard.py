import streamlit as st
import requests

N8N_URL = "https://talentdna.lintasarta.net/n8n/webhook-test/cv-analyzer"

st.title("Dashboard CV Screening")

with st.form("hr_requirement"):
    col1, col2 = st.columns(2)
    with col1:
        position = st.text_input("Position", "Product Manager")
        required_skills = st.text_input("Required Skills (comma separated)", "leadership, digital marketing")
        min_gpa = st.number_input("Minimum GPA", 0.0, 4.0, 3.0, 0.01)
    with col2:
        min_exp = st.number_input("Minimum Years of Experience", 0, 50, 2, 1)
        min_edu = st.text_input("Minimum Education", "Bachelor")
        required_cert = st.text_input("Expected Certifications (comma separated)", "")
        relevant_field = st.text_input("Required Relevant Field", "")
    uploaded_file = st.file_uploader("Upload CV (PDF)", type="pdf")
    submitted = st.form_submit_button("Screen Now")

if submitted and uploaded_file:
    files = {"cv-file": (uploaded_file.name, uploaded_file, "application/pdf")}
    data = {
        "position": position,
        "required_skills": required_skills,
        "min_gpa": min_gpa,
        "min_experience": min_exp,
        "min_education": min_edu,
        "required_cert": required_cert,
        "relevant_exp": relevant_field,
    }
    with st.spinner("Sending file to AI screening..."):
        response = requests.post(N8N_URL, files=files, data=data)
        try:
            data = response.json()
            st.success("Screening completed!")
            # --- Show Candidate Details ---
            st.header("Candidate Details")
            st.write(f"**Name:** {data.get('full_name', '-')}")
            st.write(f"**Domicile:** {data.get('domicile', '-')}")
            st.write(f"**Phone:** {data.get('phone_number', '-')}")
            st.write(f"**Email:** {data.get('email', '-')}")
            st.write(f"**Summary:** {data.get('summary', '-')}")

            # --- Show Skills ---
            st.subheader("Candidate Skills")
            skills_true = [k.title() for k, v in data.get("skills", {}).items() if v]
            skills_false = [k.title() for k, v in data.get("skills", {}).items() if not v]
            if skills_true:
                st.write("✅ " + ", ".join(skills_true))
            if skills_false:
                st.write("❌ " + ", ".join(skills_false))

            # --- Show Screening Result ---
            st.subheader("HR Requirement Screening Result")
            result = data.get("requirement_match", {})
            st.write(f"**Position:** {result.get('position', '-')}")
            st.write(f"**Overall Status:** {'🟢 PASS' if result.get('overall_status', '').upper() == 'LOLOS' else '🔴 NOT PASS'}")
            st.write(f"**Minimum GPA:** {result.get('min_gpa', '-')}")
            st.write(f"**Candidate GPA:** {result.get('gpa_value', '-')}")
            st.write(f"**GPA Match:** {'✅' if result.get('gpa_match') else '❌'}")
            st.write(f"**Minimum Experience:** {result.get('min_experience', '-')}")
            st.write(f"**Candidate Experience:** {result.get('exp_value', '-')}")
            st.write(f"**Experience Match:** {'✅' if result.get('exp_match') else '❌'}")
            st.write(f"**Minimum Education:** {result.get('min_education', '-')}")
            st.write(f"**Candidate Education:** {result.get('education_major', '-')}")
            st.write(f"**Education Match:** {'✅' if result.get('edu_match') else '❌'}")
            st.write(f"**Required Certifications:** {result.get('required_cert', '-')}")
            st.write(f"**Candidate Certifications:** {result.get('certifications', '-')}")
            st.write(f"**Certification Match:** {'✅' if result.get('cert_match') else '❌'}")
            st.write(f"**Relevant Field Required:** {result.get('relevant_exp', '-')}")
            st.write(f"**Candidate Field:** {result.get('cv_exp_field', '-')}")
            st.write(f"**Relevant Field Match:** {'✅' if result.get('relevant_exp_match') else '❌'}")
            st.write(f"**Skills Match:** ✅ " + ", ".join(result.get('skills_match', [])))
            st.write(f"**Skills Not Match:** ❌ " + ", ".join(result.get('skills_not_match', [])))

            # --- Show AI (LLM) Explanation if available ---
            explanation = data.get("explanation_llm") or data.get("llm_reasoning") or ""
            if explanation:
                st.subheader("AI Reasoning / Explanation")
                st.info(explanation)
        except Exception as e:
            st.error(f"Error processing data: {e}")

elif uploaded_file is None:
    st.info("Please upload a CV PDF file to start screening.")
