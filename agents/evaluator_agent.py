from autogen import ConversableAgent

def evaluator_agent(structured_resume: str, collection) -> str:
    results = collection.query(
        query_texts=[structured_resume],
        n_results=6,
    )

    retrieved_expectations = "\n".join(results["documents"][0])

    agent = ConversableAgent(
        name="resume_evaluator_agent",
        llm_config={
            "config_list": [{
                "model": "llama3.2",
                "api_type": "ollama",
                "base_url": "http://localhost:11434"
            }]
        },
        human_input_mode="NEVER",
    )

    prompt = f"""
Structured Resume:
{structured_resume}

Role Expectations:
{retrieved_expectations}

Provide:
1. Strengths
2. Skill Gaps
3. Improvement Suggestions
4. Interview Questions

Final Verdict:
- Applicable OR Not Applicable
(with short justification)
"""

    response = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )

    return response["content"]
