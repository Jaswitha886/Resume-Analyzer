# tools/json_formatter.py

import re

def clean_markdown(text: str) -> str:
    """Remove basic markdown formatting like **bold**"""
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text).strip()

def analysis_to_json(text: str):
    data = {
        "strengths": [],
        "skill_gaps": [],
        "improvement_suggestions": [],
        "interview_questions": [],
        "final_verdict": {
            "decision": "",
            "reason": ""
        }
    }

    section = None

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        line = clean_markdown(raw_line)
        lower = line.lower()

        # ---- SECTION DETECTION (MARKDOWN SAFE) ----
        if lower.startswith("strengths"):
            section = "strengths"
            continue

        if lower.startswith("skill gaps"):
            section = "skill_gaps"
            continue

        if lower.startswith("improvement suggestions"):
            section = "improvement_suggestions"
            continue

        if lower.startswith("interview questions"):
            section = "interview_questions"
            continue

        if lower.startswith("final verdict"):
            section = "final_verdict"
            continue

        # ---- FINAL VERDICT FIELDS ----
        if section == "final_verdict":
            if lower.startswith("decision"):
                data["final_verdict"]["decision"] = line.split(":", 1)[-1].strip()
            elif lower.startswith("reason"):
                data["final_verdict"]["reason"] = line.split(":", 1)[-1].strip()
            continue

        # ---- LIST ITEM COLLECTION ----
        if section in data:
            cleaned = re.sub(r"^[\-\•\–\d\.\)]\s*", "", line).strip()
            if cleaned:
                data[section].append(cleaned)

    return data
