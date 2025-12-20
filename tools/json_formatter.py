# tools/json_formatter.py

import re

def clean_markdown(text: str) -> str:
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text).strip()

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
    collecting_reason = False

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        line = clean_markdown(raw_line)
        lower = line.lower()

        # ---------- SECTION HEADERS ----------
        if lower.startswith("strengths"):
            section = "strengths"
            collecting_reason = False
            continue

        if lower.startswith("skill gaps"):
            section = "skill_gaps"
            collecting_reason = False
            continue

        if lower.startswith("improvement suggestions"):
            section = "improvement_suggestions"
            collecting_reason = False
            continue

        if lower.startswith("interview questions"):
            section = "interview_questions"
            collecting_reason = False
            continue

        # ---------- FINAL VERDICT ----------
        if lower.startswith("final verdict"):
            section = "final_verdict"
            collecting_reason = True

            # Inline verdict: "Final Verdict: ❌ Not Applicable"
            if ":" in line:
                after = line.split(":", 1)[1].strip().lower()
                if "applicable" in after:
                    if "not" in after:
                        data["final_verdict"]["decision"] = "Not Applicable"
                    else:
                        data["final_verdict"]["decision"] = "Applicable"
            continue

        # ---------- FINAL VERDICT DETAILS ----------
        if section == "final_verdict":
            if lower.startswith("decision"):
                data["final_verdict"]["decision"] = line.split(":", 1)[-1].strip()
                collecting_reason = False
                continue

            if lower.startswith("confidence"):
                nums = re.findall(r"\d+", line)
                if nums:
                    data["final_verdict"]["confidence"] = int(nums[0])
                collecting_reason = False
                continue

            if lower.startswith("reason"):
                data["final_verdict"]["reason"] = line.split(":", 1)[-1].strip()
                collecting_reason = False
                continue

            # 🔥 NEW LOGIC: plain-text reason fallback
            if collecting_reason and not data["final_verdict"]["reason"]:
                data["final_verdict"]["reason"] = line
                continue

        # ---------- LIST ITEMS ----------
        if section in [
            "strengths",
            "skill_gaps",
            "improvement_suggestions",
            "interview_questions"
        ]:
            cleaned = re.sub(r"^[\-\*\•\.\d\)]\s*", "", line).strip()
            if cleaned:
                data[section].append(cleaned)

    return data
