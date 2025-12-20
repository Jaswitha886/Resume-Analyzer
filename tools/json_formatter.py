import re

def infer_source(text: str) -> str:
    text = text.lower()

    if any(k in text for k in ["python", "java", "c++", "machine learning", "tensorflow", "keras"]):
        return "Skills section"
    if any(k in text for k in ["project", "hackathon", "assistant", "application"]):
        return "Projects section"
    if any(k in text for k in ["bachelor", "b.tech", "degree", "cgpa"]):
        return "Education section"
    if any(k in text for k in ["experience", "intern", "company"]):
        return "Experience section"

    return "Resume content"


def analysis_to_json(text: str):
    data = {
        "strengths": [],
        "skill_gaps": [],
        "improvement_suggestions": [],
        "interview_questions": [],
        "final_verdict": {
            "decision": "",
            "confidence": None,
            "reason": ""
        }
    }

    section = None
    verdict_block = []
    capture_verdict = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        lower = line.lower()

        # ---------- SECTION HEADERS ----------
        if lower.startswith("strengths"):
            section = "strengths"
            capture_verdict = False
            continue

        if lower.startswith("skill gaps"):
            section = "skill_gaps"
            capture_verdict = False
            continue

        if lower.startswith("improvement suggestions"):
            section = "improvement_suggestions"
            capture_verdict = False
            continue

        if lower.startswith("interview questions"):
            section = "interview_questions"
            capture_verdict = False
            continue

        # ---------- FINAL VERDICT ----------
        if lower.startswith("final verdict"):
            section = "final_verdict"
            capture_verdict = True
            verdict_block.append(line)
            continue

        if capture_verdict:
            verdict_block.append(line)
            continue

        # ---------- LIST ITEMS ----------
        if section in [
            "strengths",
            "skill_gaps",
            "improvement_suggestions",
            "interview_questions"
        ]:
            cleaned = re.sub(r"^[\-\*\•\.\d\)]\s*", "", line)
            if cleaned:
                source = infer_source(cleaned)
                data[section].append({
                    "text": cleaned,
                    "source": source
                })

    # ---------- PROCESS FINAL VERDICT ----------
    verdict_text = " ".join(verdict_block).lower()

    if "not applicable" in verdict_text:
        data["final_verdict"]["decision"] = "Not Applicable"
    elif "applicable" in verdict_text:
        data["final_verdict"]["decision"] = "Applicable"
    else:
        data["final_verdict"]["decision"] = "Not Applicable"

    reason_match = re.search(
        r"reason[:\s]*(.*)", " ".join(verdict_block), re.IGNORECASE
    )

    if reason_match:
        data["final_verdict"]["reason"] = reason_match.group(1).strip()
    else:
        data["final_verdict"]["reason"] = (
            "The candidate does not sufficiently meet the mandatory requirements for the selected role."
        )

    return data
