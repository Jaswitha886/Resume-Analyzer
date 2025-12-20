# 📄 Agent-Based Resume Analyzer (Precision-Focused)

## 📌 Overview

This project is a **local, agent-based Resume Analyzer** designed to demonstrate **agentic AI reasoning with strict control and no hallucinations**.

The system follows a **clear, deterministic evaluation flow** instead of relying on a single LLM call.  
Every evaluation point is **evidence-backed** and traceable to resume content or role expectations.

---

## 🎯 Objectives

- Avoid hallucinations and assumptions
- Ensure traceability for every evaluation point
- Demonstrate multi-agent reasoning
- Ground evaluation using role-based RAG
- Produce structured yet human-readable output

---

## 🧠 Evaluation Flow

 ```mermaid
flowchart TD
    A[User] --> B[Resume Input (Text / PDF / JSON)]
    B --> C[Normalization Layer]
    C --> D[Resume Reader Agent]
    D --> E[Role Expectations (RAG)]
    E --> F[Evaluator Agent (Strict)]
    F --> G[Structured Output + Verdict]
```


---

## 🧩 Agents

### 1️⃣ Document Processor Agent
- Cleans and normalizes resume text
- Removes formatting noise
- Prepares input for downstream agents

### 2️⃣ Resume Reader Agent
- Understands resume content
- Identifies skills, education, projects, and experience
- Does **not** perform evaluation

### 3️⃣ Evaluator Agent (Strict)
- Compares resume content against role expectations
- Uses **only explicit evidence**
- Avoids assumptions and vague language
- Produces limited, factual output

---

## 📚 Role-Based Grounding (RAG)

- Role expectations are stored as simple text files
- Retrieved before evaluation
- Ensures decisions are role-specific, not generic

Supported roles:
- AI / ML Intern
- Software Engineering Intern
- Data Science Intern

---

## 📝 Supported Resume Inputs

### ✅ Text Input
- Paste resume text directly

### ✅ PDF Input
- Resume text extracted locally
- No external APIs used

### ✅ Structured JSON Input
Used to demonstrate **structured → normalized → evaluated** flow.

Example:
```json
{
  "skills": ["Python", "Machine Learning"],
  "projects": ["Smart Event Management Assistant"],
  "education": "B.Tech CSE, CGPA 9.91"
}
```

---

## 🧪 Hallucination Control Strategy

- Strict evaluator constraints
- No assumed skills or experience
- Limited output size
- Deterministic JSON parsing
- Conservative defaults
If information is missing, it is stated explicitly.

---

## 🖥️ User Interface

- Clean Streamlit UI
- Step-by-step evaluation flow
- Human-readable results
- Optional JSON download

---

## 🛠️ Tech Stack

- Python
- AutoGen (ConversableAgent – v0.7.x)
- Ollama (local LLMs)
- Streamlit
- Sentence Transformers

---

## 🚀 Running the Project

``` bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```
---

## 📌 Project Status

- Stable and demo-ready
- Focused on learning agentic AI concepts
- Not production-hardened by design

---

## 🧠 Key Learnings

- Agent-based reasoning pipelines
- Resume understanding vs evaluation separation
- Role-grounded evaluation using RAG
- Hallucination control in LLM systems
- Evidence-backed decision making

---

## ✅ Conclusion

This project demonstrates how agent-based AI systems can be designed with **clear flow, strict constraints, and explainable reasoning**.

By separating resume understanding from evaluation, grounding decisions using role-based retrieval, and enforcing evidence-backed outputs, the system avoids hallucinations and produces **precise, defensible results**.

The project intentionally prioritizes **clarity and correctness over feature complexity**, making it suitable for learning, review, and demonstration of agentic AI concepts.
