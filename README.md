# 📄 Resume Analyzer using RAG (with UI & PDF Support)

## 📌 Project Overview

This project is a **Resume Analyzer** that uses **Retrieval-Augmented Generation (RAG)** to evaluate a candidate’s resume against predefined role expectations.

The system:
- Accepts resumes in **PDF or TXT format**
- Extracts resume content
- Compares it with role-specific expectations using RAG
- Generates structured feedback
- Gives a **final eligibility verdict** (Applicable / Not Applicable)

The project runs **fully locally** using **Ollama**, without any paid APIs.

---

## 🎯 Problem Statement

Evaluating resumes manually is:
- Time-consuming
- Subjective
- Inconsistent

This project explores how **AI + RAG** can assist by:
- Analyzing resumes objectively
- Identifying strengths and skill gaps
- Suggesting improvements
- Helping with interview preparation

---

## 🧠 System Architecture

Resume (PDF / TXT)
↓
Text Extraction
↓
Resume Content
↓
RAG (Role Expectations)
↓
Analysis + Verdict
↓
UI Output

yaml
Copy code

---

## 🤖 Key Components

### 1️⃣ Resume Analyzer Agent
- Uses a text-based LLM
- Analyzes resume content
- Generates:
  - Strengths
  - Skill gaps
  - Improvement suggestions
  - Interview questions
  - Final eligibility decision

### 2️⃣ RAG Knowledge Base
- Stores role expectations
- Used to ground analysis
- Prevents generic or hallucinated feedback

### 3️⃣ Streamlit UI
- Upload resumes via browser
- Supports **PDF and TXT**
- Displays analysis report interactively

---

## 📚 RAG Knowledge Base

The RAG data includes:
- Expected skills for the role
- Preferred experience
- Interview focus areas

This ensures the analysis is **role-specific and consistent**.

---

## 🛠️ Tech Stack

- Python
- AutoGen
- Ollama
- llama3.2 (LLM)
- ChromaDB (vector database)
- Sentence-Transformers (embeddings)
- Streamlit (UI)
- PyPDF (PDF text extraction)

---

## 🚀 How to Run the Project

### 1️⃣ Start Ollama
```bash
ollama serve
```

### 2️⃣ Pull the required model
```bash
ollama pull llama3.2
```
### 3️⃣ Run the UI
```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 📌 Example Output

Copy code
Strengths:
- Strong Python fundamentals
- Relevant academic projects

Skill Gaps:
- Limited real-world experience
- Needs stronger data structures knowledge

Final Verdict:
Applicable

Reason:
Candidate meets most core expectations with minor gaps that can be improved.

## ⚠️ Notes
- All resumes used are for testing/demo purposes
- No real user data is stored
- The project runs entirely locally

## 🔮 Future Improvements
- Support for multiple job roles
- Resume scoring system
- Export analysis as PDF
- Advanced UI enhancements

---

## 🏁 Conclusion
This project demonstrates how RAG can be applied to real-world evaluation tasks, combining AI reasoning with structured knowledge to produce meaningful and explainable results.

It focuses on correctness, clarity, and practical applicability.

