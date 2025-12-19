# 📄 Resume Analyzer using Multi-Agent RAG (with UI & PDF Support)

## 📌 Project Overview

This project is a **Resume Analyzer system** built using a **multi-agent architecture** and **Retrieval-Augmented Generation (RAG)**.

The application allows users to upload a **resume in PDF or TXT format**, analyzes it against predefined **role expectations**, and generates:

- Structured resume feedback
- Skill gap analysis
- Improvement suggestions
- Interview preparation questions
- A **final eligibility verdict** (Applicable / Not Applicable)

The system runs **fully locally** using **Ollama**, without any paid APIs.

---

## 🎯 Problem Statement

Manual resume screening is often:
- Time-consuming
- Subjective
- Inconsistent

This project explores how **agentic AI systems + RAG** can assist by providing:
- Objective evaluation
- Role-specific feedback
- Explainable decision-making

---

## 🧠 System Architecture

Resume (PDF / TXT)
↓
Agent 1: Document Processor
↓
Agent 2: Resume Reader
↓
Agent 3: Evaluator (RAG)
↓
Final Analysis + Verdict
↓
Streamlit UI Output



Each agent has a **single responsibility**, making the system modular and explainable.


---

## 🤖 Multi-Agent Design

### 🧑‍🔧 Agent 1: Document Processor
- Cleans and normalizes resume text
- Removes noise and formatting
- Performs no evaluation

### 📖 Agent 2: Resume Reader
- Understands resume content
- Extracts structured information:
  - Education
  - Skills
  - Projects
  - Experience

### 🧠 Agent 3: Evaluator Agent (RAG)
- Retrieves role expectations from the RAG knowledge base
- Compares them with the structured resume
- Generates:
  - Strengths
  - Skill gaps
  - Suggestions
  - Interview questions
  - **Final eligibility decision**

---

## 📚 RAG Knowledge Base

The RAG data contains:
- Role-specific expected skills
- Preferred experience
- Interview focus areas

This ensures:
- Grounded analysis
- Reduced hallucination
- Consistent evaluation logic

---

## 🖥️ User Interface (Streamlit)

The Streamlit UI provides:
- Resume upload (PDF / TXT)
- Collapsible resume preview
- One-click analysis
- Highlighted eligibility verdict
- Downloadable analysis report

The UI is intentionally simple and focused on clarity.

---

## 🛠️ Tech Stack

- **Python**
- **AutoGen** (agent orchestration)
- **Ollama** (local LLM runtime)
- **llama3.2** (text model)
- **ChromaDB** (vector database)
- **Sentence-Transformers** (embeddings)
- **Streamlit** (UI)
- **PyPDF** (PDF text extraction)

---

## 🚀 How to Run the Project

### 1️⃣ Start Ollama
```bash
ollama serve
```
### 2️⃣ Pull required model
```bash
ollama pull llama3.2
```
### 3️⃣ Run the UI
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---


## 📌Example Output

Strengths:
- Strong Python fundamentals
- Relevant academic and personal projects

Skill Gaps:
- Limited real-world experience
- Needs deeper data structures knowledge

Final Verdict:
Applicable

Reason:
The candidate meets most core expectations with minor gaps that can be improved.

---

## ⚠️ Notes

- All resumes used are for demo/testing purposes
- No personal data is stored
- The application runs entirely locally

## 🔮 Future Improvements

- Support for multiple job roles
- Resume scoring system
- Export report as PDF
- Advanced UI enhancements

## 🏁 Conclusion

This project demonstrates how **multi-agent AI systems combined with RAG** can be applied to real-world evaluation problems.

