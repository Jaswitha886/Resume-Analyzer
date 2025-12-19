from autogen import ConversableAgent
import chromadb
from sentence_transformers import SentenceTransformer


# ===============================
# LOAD RESUME
# ===============================
def load_resume(file_path: str) -> str:
    """
    Loads resume text from a file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ===============================
# RAG SETUP
# ===============================
def setup_rag():
    """
    Loads role expectations into a vector database.
    """
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="role_expectations")

    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    with open("rag_data/role_expectations.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = [line for line in text.split("\n") if line.strip()]
    embeddings = embedder.encode(chunks).tolist()

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[str(i)],
        )

    return collection


# ===============================
# RESUME ANALYZER AGENT
# ===============================
def analyze_resume(resume_text: str, collection) -> str:
    """
    Uses RAG to analyze resume against role expectations.
    """
    results = collection.query(
        query_texts=[resume_text],
        n_results=6,
    )

    retrieved_expectations = "\n".join(results["documents"][0])

    prompt = f"""
Resume Content:
{resume_text}

Role Expectations:
{retrieved_expectations}

Analyze the resume against the role expectations and provide the following:

1. Strengths
2. Skill Gaps
3. Improvement Suggestions
4. Interview Questions to Prepare

Finally, give a clear decision:

Final Verdict:
- Applicable OR Not Applicable

Decision Rules:
- Mark as Applicable if most core skills and expectations are met.
- Mark as Not Applicable if major skill gaps exist.
- Provide a short justification (2–3 lines).

Output everything in a clear, structured format.
"""

    resume_agent = ConversableAgent(
        name="resume_analyzer_agent",
        llm_config={
            "config_list": [
                {
                    "model": "llama3.2",
                    "api_type": "ollama",
                    "base_url": "http://localhost:11434",
                }
            ]
        },
        human_input_mode="NEVER",
    )

    response = resume_agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )

    return response["content"]


# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    print("\n🔹 Loading resume...")
    resume_text = load_resume("resume.txt")

    print("\n🔹 Initializing RAG knowledge base...")
    collection = setup_rag()

    print("\n🔹 Analyzing resume using RAG agent...")
    analysis = analyze_resume(resume_text, collection)

    print("\n--- RESUME ANALYSIS REPORT ---\n")
    print(analysis)
