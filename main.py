from agents.document_processor import document_processor_agent
from agents.resume_reader import resume_reader_agent
from agents.evaluator_agent import evaluator_agent
from rag.rag_setup import setup_rag


def analyze_resume(resume_text: str) -> str:
    collection = setup_rag()

    cleaned = document_processor_agent(resume_text)
    structured = resume_reader_agent(cleaned)
    final_result = evaluator_agent(structured, collection)

    return final_result
