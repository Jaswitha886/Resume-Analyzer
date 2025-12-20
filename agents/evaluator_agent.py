from autogen import ConversableAgent

def create_evaluator(llm_config):
    return ConversableAgent(
        name="EvaluatorAgent",
        system_message=(
            "You are a strict resume evaluator.\n\n"
            "OUTPUT FORMAT RULES (MANDATORY):\n"
            "Use the following section headers EXACTLY as written.\n"
            "Each section must start on a new line.\n\n"

            "FORMAT:\n"
            "Strengths:\n"
            "- point\n"
            "- point\n\n"

            "Skill Gaps:\n"
            "- point\n"
            "- point\n\n"

            "Improvement Suggestions:\n"
            "- point\n"
            "- point\n\n"

            "Interview Questions:\n"
            "1. question\n"
            "2. question\n\n"

            "Final Verdict:\n"
            "Decision: Applicable | Not Applicable\n"
            "Reason: short, clear reason\n\n"

            "Rules:\n"
            "- Judge strictly against role expectations.\n"
            "- If a mandatory skill is missing, decision MUST be Not Applicable.\n"
            "- Do NOT merge sections.\n"
            "- Do NOT add extra text."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )
