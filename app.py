# app.py

import sys
import os
import json
import streamlit as st

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import run_resume_analysis
from tools.pdf_extractor import extract_text_from_pdf
from tools.json_formatter import analysis_to_json

st.set_page_config(
    page_title="Agentic Resume Analyzer",
    layout="centered"
)

st.title("📄 Agent-Based Resume Analyzer")
st.write("Upload a resume PDF or paste resume text below.")

# ---------- INPUT SECTION ----------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF only)",
    type=["pdf"]
)

resume_text = ""

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("📄 Extracted Resume Text")
    st.text_area(
        label="Extracted Content",
        value=resume_text,
        height=250
    )
else:
    resume_text = st.text_area(
        label="Paste Resume Text",
        height=250
    )

# ---------- ANALYSIS BUTTON ----------

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please upload a PDF or paste resume text.")
    else:
        with st.spinner("Analyzing resume using AI agents..."):
            analysis = run_resume_analysis(resume_text)

        # Convert analysis to JSON (for UI + download)
        json_data = analysis_to_json(analysis)

        # ---------- OUTPUT UI ----------

        st.subheader("🧠 Analysis Result")

        # Strengths
        st.markdown("**Strengths**")
        for item in json_data["strengths"]:
            st.write(f"- {item}")

        # Skill Gaps
        st.markdown("**Skill Gaps**")
        for item in json_data["skill_gaps"]:
            st.write(f"- {item}")

        # Improvement Suggestions
        st.markdown("**Improvement Suggestions**")
        for item in json_data["improvement_suggestions"]:
            st.write(f"- {item}")

        # Interview Questions
        st.markdown("**Interview Questions**")
        for q in json_data["interview_questions"]:
            st.write(f"- {q}")

        # Final Verdict
        st.markdown("**Final Verdict**")

        st.markdown("**Decision:**")
        st.write(json_data["final_verdict"]["decision"])

        st.markdown("**Reason:**")
        st.write(json_data["final_verdict"]["reason"])

        # ---------- DOWNLOAD JSON ----------

        st.download_button(
            label="⬇️ Download Analysis as JSON",
            data=json.dumps(json_data, indent=2),
            file_name="resume_analysis.json",
            mime="application/json"
        )
