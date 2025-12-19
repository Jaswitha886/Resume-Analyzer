from autogen import ConversableAgent


def resume_reader_agent(cleaned_resume: str) -> str:
    agent = ConversableAgent(
        name="resume_reader_agent",
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
You are a resume understanding agent.

Extract and structure the resume into:
- Education
- Skills
- Projects
- Experience

Resume Text:
{cleaned_resume}

Return a structured summary in plain text.
"""

    response = agent.generate_reply(
        messages=[{"role": "user", "content": prompt}]
    )

    return response["content"]
