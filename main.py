import json
import re

from agents.document_processor import document_processor_agent
from agents.resume_reader import resume_reader_agent
from agents.evaluator_agent import evaluator_agent
from rag.rag_setup import setup_rag


def try_parse_json(text: str):
    """
    Try to extract and parse JSON from LLM output.
    Returns dict if successful, else None.
    """
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None

        cleaned = match.group()
        cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)
        cleaned = cleaned.replace("“", "\"").replace("”", "\"")

        try:
            return json.loads(cleaned)
        except Exception:
            return None


def analyze_resume(resume_text: str) -> str:
    collection = setup_rag()

    # Agent 1: Clean document
    cleaned_text = document_processor_agent(resume_text)

    # Agent 2: Understand resume
    structured_resume = resume_reader_agent(cleaned_text)

    # Agent 3: Evaluate (attempt 1)
    raw_output = evaluator_agent(structured_resume, collection)
    parsed = try_parse_json(raw_output)

    # Retry once if invalid
    if parsed is None:
        raw_output = evaluator_agent(structured_resume, collection, retry=True)
        parsed = try_parse_json(raw_output)

    # Controlled fallback (never crash UI)
    if parsed is None:
        parsed = {
            "strengths": ["Resume content partially aligns with expectations"],
            "skill_gaps": ["Structured evaluation could not be fully generated"],
            "improvement_suggestions": ["Improve resume clarity and formatting"],
            "interview_questions": ["Explain your key projects in detail"],
            "final_verdict": "Not Applicable",
            "verdict_reason": "Model failed to produce valid structured output"
        }

    return f"""
### Strengths
- {"\n- ".join(parsed["strengths"])}

### Skill Gaps
- {"\n- ".join(parsed["skill_gaps"])}

### Improvement Suggestions
- {"\n- ".join(parsed["improvement_suggestions"])}

### Interview Questions
- {"\n- ".join(parsed["interview_questions"])}

### Final Verdict
**{parsed["final_verdict"]}**

**Reason:** {parsed["verdict_reason"]}
""".strip()
