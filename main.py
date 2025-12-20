# main.py

from agents.document_processor import create_document_processor
from agents.resume_reader import create_resume_reader
from agents.evaluator_agent import create_evaluator
from rag.rag_setup import SimpleRAG

LLM_CONFIG = {
    "model": "llama3.2",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama"
}

def run_resume_analysis(resume_text: str):
    doc_agent = create_document_processor(LLM_CONFIG)
    reader_agent = create_resume_reader(LLM_CONFIG)
    evaluator_agent = create_evaluator(LLM_CONFIG)

    # Step 1: Clean resume
    cleaned = doc_agent.generate_reply(messages=[{"role": "user", "content": resume_text}])

    # Step 2: Understand resume
    structured = reader_agent.generate_reply(messages=[{"role": "user", "content": cleaned}])

    # Step 3: RAG
    rag = SimpleRAG("rag_data/role_expectations.txt")
    expectations = rag.retrieve(structured)

    # Step 4: Evaluate
    eval_prompt = (
        "Resume Summary:\n"
        f"{structured}\n\n"
        "Role Expectations:\n"
        + "\n".join(expectations)
    )

    final_analysis = evaluator_agent.generate_reply(
        messages=[{"role": "user", "content": eval_prompt}]
    )

    return final_analysis
