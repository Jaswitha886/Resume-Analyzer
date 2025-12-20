# app.py

import sys
import os
import json
import streamlit as st

# Ensure project root is in PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import run_resume_analysis
from tools.pdf_extractor import extract_text_from_pdf
from tools.json_formatter import analysis_to_json

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Agentic Resume Analyzer",
    layout="centered"
)

st.title("📄 Agent-Based Resume Analyzer")
st.write("Upload a resume PDF or paste resume text below.")

# ---------------- ROLE SELECTOR ----------------

role = st.selectbox(
    "🎯 Select Target Role",
    [
        "AI / ML Intern",
        "Software Engineering Intern",
        "Data Science Intern"
    ]
)

ROLE_RAG_MAP = {
    "AI / ML Intern": "rag_data/ai_ml_intern.txt",
    "Software Engineering Intern": "rag_data/software_intern.txt",
    "Data Science Intern": "rag_data/data_science_intern.txt"
}

# ---------------- HELPERS ----------------

def clean_bullet(text: str) -> str:
    """Remove any leading bullet symbols from model output"""
    return text.lstrip("*-•. ").strip()

# ---------------- INPUT ----------------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF only)",
    type=["pdf"]
)

resume_text = ""

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("📄 Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=250)
else:
    resume_text = st.text_area("Paste Resume Text", height=250)

# ---------------- ANALYSIS ----------------

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please upload a PDF or paste resume text.")
    else:
        with st.spinner("Analyzing resume using AI agents..."):
            analysis = run_resume_analysis(
                resume_text,
                ROLE_RAG_MAP[role]
            )

        json_data = analysis_to_json(analysis)

        st.subheader("🧠 Analysis Result")

        # ---------------- STRENGTHS ----------------
        st.markdown("**Strengths**")
        for item in json_data.get("strengths", []):
            st.write(f"- {clean_bullet(item)}")

        # ---------------- SKILL GAPS ----------------
        st.markdown("**Skill Gaps**")
        for item in json_data.get("skill_gaps", []):
            st.write(f"- {clean_bullet(item)}")

        # ---------------- IMPROVEMENTS ----------------
        st.markdown("**Improvement Suggestions**")
        for item in json_data.get("improvement_suggestions", []):
            st.write(f"- {clean_bullet(item)}")

        # ---------------- INTERVIEW QUESTIONS ----------------
        st.markdown("**Interview Questions**")
        for q in json_data.get("interview_questions", []):
            st.write(f"- {clean_bullet(q)}")

        # ---------------- FINAL VERDICT ----------------
        verdict = json_data.get("final_verdict", {})

        decision = verdict.get("decision", "Not Applicable")
        confidence = verdict.get("confidence", None)
        reason = verdict.get("reason", "").strip()
        if not reason:
            reason = "The candidate does not sufficiently meet the mandatory requirements for the selected role."


        if decision == "Applicable":
            st.markdown("**Final Verdict: ✅ Applicable**")
        else:
            st.markdown("**Final Verdict: ❌ Not Applicable**")

        if confidence is not None:
            st.write(f"Confidence: {confidence}%")

        st.markdown("**Reason:**")
        st.write(reason)

        # ---------------- DOWNLOAD JSON ----------------
        st.download_button(
            label="⬇️ Download Analysis as JSON",
            data=json.dumps(json_data, indent=2),
            file_name="resume_analysis.json",
            mime="application/json"
        )
