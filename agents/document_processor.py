# agents/document_processor_agent.py

from autogen import ConversableAgent

def create_document_processor(llm_config):
    return ConversableAgent(
        name="DocumentProcessorAgent",
        system_message=(
            "You clean and normalize resume text.\n"
            "Remove visual noise, excessive symbols, and formatting issues.\n"
            "Do NOT summarize or evaluate.\n"
            "Return clean readable resume text."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
