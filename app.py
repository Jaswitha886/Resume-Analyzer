# app.py

import sys
import os
import json
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import run_resume_analysis
from tools.pdf_extractor import extract_text_from_pdf
from tools.json_formatter import analysis_to_json

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Agentic Resume Analyzer",
    layout="centered"
)

# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("📄 Agentic Resume Analyzer")
st.caption(
    "Flow-based, role-grounded resume evaluation with strict and explainable reasoning."
)

st.divider()

# -------------------------------------------------
# Role Selection
# -------------------------------------------------

st.markdown("### 🎯 Select Target Role")

role = st.selectbox(
    "",
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

st.divider()

# -------------------------------------------------
# Resume Input
# -------------------------------------------------

st.markdown("### 📥 Resume Input")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Extracting resume content..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=220
    )
else:
    resume_text = st.text_area(
        "Paste Resume Text",
        height=220
    )

st.divider()

# -------------------------------------------------
# Flow Explanation
# -------------------------------------------------

st.markdown("### 🔄 Evaluation Flow")
st.info(
    "Input → Normalization → Resume Understanding → Role Grounding → Strict Evaluation"
)

# -------------------------------------------------
# Helper
# -------------------------------------------------

def clean_text(text: str) -> str:
    return text.lstrip("*-•. ").strip()

# -------------------------------------------------
# Analysis Trigger
# -------------------------------------------------

if st.button("Analyze Resume", type="primary"):
    if not resume_text.strip():
        st.warning("Please provide resume content before analysis.")
    else:
        with st.spinner("Running agent-based evaluation..."):
            analysis_text = run_resume_analysis(
                resume_text,
                ROLE_RAG_MAP[role]
            )

        json_data = analysis_to_json(analysis_text, role)

        st.divider()
        st.markdown("## 🧠 Analysis Result")

        # ---------------- Strengths ----------------
        st.markdown("### ✅ Strengths")
        for item in json_data.get("strengths", []):
            st.write(f"- {clean_text(item['text'])}")

        # ---------------- Skill Gaps ----------------
        st.markdown("### ⚠️ Skill Gaps")
        for item in json_data.get("skill_gaps", []):
            st.write(f"- {clean_text(item['text'])}")

        # ---------------- Improvements ----------------
        st.markdown("### 🔧 Improvement Suggestions")
        for item in json_data.get("improvement_suggestions", []):
            st.write(f"- {clean_text(item['text'])}")

        # ---------------- Interview Questions ----------------
        with st.expander("💬 Interview Questions"):
            for q in json_data.get("interview_questions", []):
                st.write(f"- {clean_text(q['text'])}")

        # ---------------- Final Verdict ----------------
        verdict = json_data.get("final_verdict", {})
        decision = verdict.get("decision", "Not Applicable")
        reason = verdict.get(
            "reason",
            "The candidate does not sufficiently meet the mandatory requirements for the selected role."
        )

        st.divider()
        st.markdown("### 🧾 Final Verdict")

        verdict_col, reason_col = st.columns([1, 3])

        with verdict_col:
            if decision == "Applicable":
                st.success("Applicable")
            else:
                st.error("Not Applicable")

        with reason_col:
            st.markdown("**Reason**")
            st.write(reason)

        # ---------------- Download JSON ----------------
        st.divider()
        st.download_button(
            "⬇️ Download Analysis as JSON",
            data=json.dumps(json_data, indent=2),
            file_name="resume_analysis.json",
            mime="application/json"
        )
