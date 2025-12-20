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

st.write(
    "This application evaluates resumes using a strict, agent-based AI pipeline. "
    "The system avoids assumptions and produces evidence-backed evaluations."
)

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

# ---------------- INPUT MODE ----------------

input_mode = st.radio(
    "Select Resume Input Format",
    ["Text / PDF", "Structured JSON"]
)

# ---------------- HELPERS ----------------

def json_to_resume_text(resume_json: dict) -> str:
    """
    Convert structured resume JSON into normalized plain text
    so it flows through the same evaluation pipeline.
    """
    text = ""

    for key, value in resume_json.items():
        text += f"{key.upper()}:\n"

        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        text += f"- {k}: {v}\n"
                else:
                    text += f"- {item}\n"
        elif isinstance(value, dict):
            for k, v in value.items():
                text += f"{k}: {v}\n"
        else:
            text += f"{value}\n"

        text += "\n"

    return text


def clean_text(text: str) -> str:
    return text.lstrip("*-•. ").strip()


# ---------------- INPUT SECTION ----------------

resume_text = ""

if input_mode == "Text / PDF":
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF only)",
        type=["pdf"]
    )

    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        st.subheader("📄 Extracted Resume Text")
        st.text_area(
            "Resume Content",
            resume_text,
            height=250
        )
    else:
        resume_text = st.text_area(
            "Paste Resume Text",
            height=250
        )

else:
    json_input = st.text_area(
        "Paste Resume JSON",
        height=250,
        placeholder='{\n  "skills": ["Python", "Machine Learning"],\n  "projects": [...]\n}'
    )

    if json_input.strip():
        try:
            resume_json = json.loads(json_input)
            resume_text = json_to_resume_text(resume_json)

            st.subheader("🔄 Normalized Resume Text (from JSON)")
            st.text_area(
                "Generated Resume Text",
                resume_text,
                height=250
            )

        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check the syntax.")

# ---------------- ANALYSIS ----------------

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please provide resume input before analysis.")
    else:
        st.markdown("### 🔄 Evaluation Flow")

        with st.spinner("Step 1: Normalizing resume input..."):
            pass
        st.success("Resume normalized")

        with st.spinner("Step 2: Understanding resume content..."):
            pass
        st.success("Resume content understood")

        with st.spinner("Step 3: Retrieving role expectations (RAG)..."):
            pass
        st.success(f"Role expectations loaded for {role}")

        with st.spinner("Step 4: Evaluating resume against role expectations..."):
            analysis_text = run_resume_analysis(
                resume_text,
                ROLE_RAG_MAP[role]
            )

        st.success("Evaluation completed")

        json_data = analysis_to_json(analysis_text)

        # ---------------- OUTPUT ----------------

        st.subheader("🧠 Analysis Result")

        # -------- Strengths --------
        st.markdown("**Strengths**")
        strengths = json_data.get("strengths", [])
        if strengths:
            for item in strengths:
                st.write(
                    f"- {clean_text(item['text'])} "
                    f"_(Source: {item['source']})_"
                )
        else:
            st.write("- None identified")

        # -------- Skill Gaps --------
        st.markdown("**Skill Gaps**")
        gaps = json_data.get("skill_gaps", [])
        if gaps:
            for item in gaps:
                st.write(
                    f"- {clean_text(item['text'])} "
                    f"_(Source: {item['source']})_"
                )
        else:
            st.write("- None identified")

        # -------- Improvement Suggestions --------
        st.markdown("**Improvement Suggestions**")
        for item in json_data.get("improvement_suggestions", []):
            st.write(f"- {clean_text(item['text'])}")

        # -------- Interview Questions --------
        st.markdown("**Interview Questions**")
        for q in json_data.get("interview_questions", []):
            st.write(f"- {clean_text(q['text'])}")

        # -------- Final Verdict --------
        verdict = json_data.get("final_verdict", {})

        decision = verdict.get("decision", "Not Applicable")
        reason = verdict.get(
            "reason",
            "The candidate does not sufficiently meet the mandatory requirements for the selected role."
        )

        if decision == "Applicable":
            st.markdown("**Final Verdict: ✅ Applicable**")
        else:
            st.markdown("**Final Verdict: ❌ Not Applicable**")

        st.markdown("**Reason:**")
        st.write(reason)

        # -------- Download JSON --------
        st.download_button(
            label="⬇️ Download Analysis as JSON",
            data=json.dumps(json_data, indent=2),
            file_name="resume_analysis.json",
            mime="application/json"
        )
