from autogen import ConversableAgent


def evaluator_agent(structured_resume: str, collection, retry=False) -> str:
    results = collection.query(
        query_texts=[structured_resume],
        n_results=6,
    )

    retrieved_expectations = "\n".join(results["documents"][0])

    agent = ConversableAgent(
        name="resume_evaluator_agent",
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

    retry_note = (
        "\nThis is a retry. The previous output was rejected. "
        "You MUST return ONLY VALID JSON.\n"
        if retry else ""
    )

    prompt = f"""
You are a resume evaluation agent.

{retry_note}

STRICT RULES:
- Output ONLY valid JSON
- No explanations
- No markdown
- No bullet points outside arrays
- Every list item MUST be a quoted string

JSON SCHEMA:

{{
  "strengths": ["string"],
  "skill_gaps": ["string"],
  "improvement_suggestions": ["string"],
  "interview_questions": ["string"],
  "final_verdict": "Applicable" | "Not Applicable",
  "verdict_reason": "string"
}}

Structured Resume:
{structured_resume}

Role Expectations:
{retrieved_expectations}

RETURN ONLY JSON.
"""

    response = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )

    return response["content"]
