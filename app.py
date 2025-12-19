import streamlit as st
from pypdf import PdfReader

# Import orchestrator from main.py (multi-agent backend)
from main import analyze_resume


# ===============================
# PDF TEXT EXTRACTION
# ===============================
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ===============================
# HEADER
# ===============================
st.markdown(
    "<h1 style='text-align: center;'>📄 Resume Analyzer</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Multi-Agent Resume Evaluation using RAG</p>",
    unsafe_allow_html=True
)

st.divider()

# ===============================
# UPLOAD SECTION
# ===============================
left, right = st.columns([1, 1])

with left:
    uploaded_file = st.file_uploader(
        "📤 Upload Resume (PDF or TXT)",
        type=["pdf", "txt"]
    )

with right:
    st.info(
        "🔍 **What this system does:**\n\n"
        "- Extracts resume content\n"
        "- Understands skills & experience using agents\n"
        "- Compares with role expectations (RAG)\n"
        "- Generates feedback and eligibility verdict"
    )

# ===============================
# PROCESS FILE
# ===============================
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.divider()

    # Show extracted resume text (collapsible)
    with st.expander("📄 View Extracted Resume Text"):
        st.text_area(
            "Resume Content",
            resume_text,
            height=250,
            label_visibility="collapsed"
        )

    analyze_clicked = st.button(
        "🔍 Analyze Resume",
        use_container_width=True
    )

    if analyze_clicked:
        with st.spinner("Analyzing resume using multi-agent RAG pipeline..."):
            analysis_result = analyze_resume(resume_text)

        st.divider()

        # ===============================
        # FINAL VERDICT HIGHLIGHT
        # ===============================
        if "Final Verdict:" in analysis_result:
            verdict_line = analysis_result.split("Final Verdict:")[1].split("\n")[0].strip()

            if "Applicable" in verdict_line:
                st.success("✅ Final Verdict: Applicable")
            else:
                st.error("❌ Final Verdict: Not Applicable")

        # ===============================
        # ANALYSIS REPORT
        # ===============================
        st.subheader("📊 Resume Analysis Report")
        st.markdown(analysis_result)

        # ===============================
        # DOWNLOAD OPTION
        # ===============================
        st.download_button(
            label="📥 Download Analysis Report",
            data=analysis_result,
            file_name="resume_analysis.txt",
            mime="text/plain"
        )

else:
    st.info("Please upload a resume file to begin analysis.")
