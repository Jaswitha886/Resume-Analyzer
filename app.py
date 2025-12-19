import streamlit as st
from pypdf import PdfReader

# Import core logic from main.py
from main import setup_rag, analyze_resume


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
# STREAMLIT UI
# ===============================
st.set_page_config(
    page_title="Resume Analyzer (RAG)",
    layout="centered"
)

st.title("📄 Resume Analyzer")
st.write(
    "Upload your resume (PDF or TXT) to receive structured feedback, "
    "skill gap analysis, and interview preparation guidance using RAG."
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "txt"]
)

if uploaded_file is not None:
    # Read resume content
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Extracted Resume Content")
    st.text_area(
        label="",
        value=resume_text,
        height=200
    )

    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing resume using RAG..."):
            collection = setup_rag()
            analysis_result = analyze_resume(resume_text, collection)

        st.subheader("📊 Resume Analysis Report")
        st.write(analysis_result)

else:
    st.info("Please upload a resume file to begin analysis.")
