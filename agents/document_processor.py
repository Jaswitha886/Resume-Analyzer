from autogen import ConversableAgent


def document_processor_agent(resume_text: str) -> str:
    agent = ConversableAgent(
        name="document_processor_agent",
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

    prompt = f"""
You are a document processing agent.

Task:
- Clean the resume text
- Remove noise and formatting artifacts
- Keep only meaningful content

Resume Text:
{resume_text}

Return only the cleaned resume text.
"""

    response = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )

    return response["content"]
