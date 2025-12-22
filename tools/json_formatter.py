# tools/json_formatter.py

import re


def get_role_based_questions(role: str):
    if role == "AI / ML Intern":
        return [
            "Explain the difference between supervised and unsupervised learning with an example.",
            "How would you evaluate the performance of a classification model?",
            "Describe a machine learning project you would build end-to-end."
        ]

    if role == "Software Engineering Intern":
        return [
            "Explain the difference between an array and a linked list.",
            "How would you debug a program that produces incorrect output?",
            "What is the time complexity of common sorting algorithms?"
        ]

    if role == "Data Science Intern":
        return [
            "How do you handle missing values in a dataset?",
            "Explain the difference between precision and recall.",
            "Describe your approach to exploratory data analysis."
        ]

    # Safe fallback
    return [
        "Explain a technical project you have worked on.",
        "How do you approach problem-solving in programming?",
        "What challenges do you face when learning new technologies?"
    ]


def analysis_to_json(analysis_text: str, role: str) -> dict:
    """
    Converts evaluator agent output (plain text) into structured JSON.
    Defensive, role-aware, and hallucination-safe.
    """

    strengths = []
    skill_gaps = []
    improvement_suggestions = []
    interview_questions = []

    final_verdict = {
        "decision": "",
        "confidence": None,
        "reason": ""
    }

    current_section = None
    lines = analysis_text.splitlines()

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        lower = line.lower()

        # -------- SECTION DETECTION --------
        if "strengths" in lower:
            current_section = "strengths"
            continue

        if "skill gaps" in lower:
            current_section = "skill_gaps"
            continue

        if "improvement suggestions" in lower:
            current_section = "improvement_suggestions"
            continue

        if "interview questions" in lower:
            current_section = "interview_questions"
            continue

        if "final verdict" in lower:
            current_section = "final_verdict"
            continue

        if lower.startswith("reason"):
            current_section = "verdict_reason"
            continue

        # -------- CONTENT PARSING --------
        cleaned = re.sub(r"^[\-\*\•\.\d]+\s*", "", line).strip()

        if not cleaned:
            continue

        if current_section == "strengths":
            strengths.append({
                "text": cleaned,
                "source": "Resume content"
            })

        elif current_section == "skill_gaps":
            # Skip weak / administrative gaps
            if any(x in cleaned.lower() for x in [
                "certificate",
                "certification",
                "documentation",
                "missing proof"
            ]):
                continue

            skill_gaps.append({
                "text": cleaned,
                "source": "Resume content"
            })

        elif current_section == "improvement_suggestions":
            improvement_suggestions.append({
                "text": cleaned
            })

        elif current_section == "interview_questions":
            interview_questions.append({
                "text": cleaned,
                "source": "Evaluator"
            })

        elif current_section == "final_verdict":
            if "not applicable" in lower:
                final_verdict["decision"] = "Not Applicable"
            elif "applicable" in lower:
                final_verdict["decision"] = "Applicable"

        elif current_section == "verdict_reason":
            final_verdict["reason"] += cleaned + " "

    # -------- POST-PROCESSING SAFETY NETS --------

    # Ensure verdict decision exists
    if not final_verdict["decision"]:
        final_verdict["decision"] = "Not Applicable"

    # Ensure verdict reason exists AND MATCHES decision
    if not final_verdict["reason"].strip():
        if final_verdict["decision"] == "Applicable":
            final_verdict["reason"] = (
                "The candidate meets the core requirements for the selected role "
                "based on demonstrated skills, academic background, and relevant experience."
            )
        else:
            final_verdict["reason"] = (
                "The candidate does not sufficiently meet the mandatory requirements "
                "for the selected role."
            )
    else:
        final_verdict["reason"] = final_verdict["reason"].strip()

    # -------- ROLE-AWARE INTERVIEW QUESTIONS SAFETY NET --------
    role_based_defaults = get_role_based_questions(role)

    while len(interview_questions) < 3:
        interview_questions.append({
            "text": role_based_defaults[len(interview_questions)],
            "source": "System generated"
        })

    # -------- LIMIT LIST SIZES --------
    strengths = strengths[:5]
    skill_gaps = skill_gaps[:5]
    improvement_suggestions = improvement_suggestions[:5]
    interview_questions = interview_questions[:5]

    return {
        "strengths": strengths,
        "skill_gaps": skill_gaps,
        "improvement_suggestions": improvement_suggestions,
        "interview_questions": interview_questions,
        "final_verdict": final_verdict
    }
