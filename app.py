import streamlit as st
from pypdf import PdfReader
from main import analyze_resume


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.markdown("<h1 style='text-align:center;'>📄 Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Multi-Agent Resume Evaluation with Restricted Output</p>", unsafe_allow_html=True)

st.divider()

uploaded_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    with st.expander("View Extracted Resume"):
        st.text_area("Resume", resume_text, height=250, label_visibility="collapsed")

    if st.button("Analyze Resume", use_container_width=True):
        with st.spinner("Analyzing resume..."):
            result = analyze_resume(resume_text)

        st.divider()
        st.markdown(result)
