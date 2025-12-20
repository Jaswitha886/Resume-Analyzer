# agents/resume_reader_agent.py

from autogen import ConversableAgent

def create_resume_reader(llm_config):
    return ConversableAgent(
        name="ResumeReaderAgent",
        system_message=(
            "You carefully read a cleaned resume.\n"
            "Extract and organize information into clear sections:\n"
            "- Skills\n"
            "- Education\n"
            "- Projects\n"
            "- Experience (if any)\n"
            "- Overall Profile Summary\n\n"
            "Do NOT evaluate or judge.\n"
            "Return structured, human-readable text."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
