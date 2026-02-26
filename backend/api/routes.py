"""
FastAPI Routes – Resume vs JD Skill Analysis (ATS-safe)
=====================================================
- Deterministic keyword-based extraction
- Exact skill matching
- Schema-aligned response
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
import re
import time

router = APIRouter(prefix="/v1", tags=["analysis"])

# ------------------------------------------------------------------
# Skill Vocabulary (expandable)
# ------------------------------------------------------------------

SKILL_DB = {
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "fastapi", "flask", "django",
    "pandas", "numpy",
    "aws", "docker", "git", "data analysis", "data science"
}

# ------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_skills(text: str) -> set[str]:
    if not text or not text.strip():
        return set()

    text = normalize(text)
    skills = set()

    for skill in SKILL_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            skills.add(skill)

    return skills

# ------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/analyze")
def analyze(payload: Dict):
    """
    Expected payload:
    {
        "resume": "text...",
        "job_description": "text..."
    }
    """

    start = time.time()

    resume_text = payload.get("resume")
    jd_text = payload.get("job_description")

    if not resume_text or not jd_text:
        raise HTTPException(
            status_code=400,
            detail="Both 'resume' and 'job_description' are required."
        )

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    if not jd_skills:
        raise HTTPException(
            status_code=422,
            detail="No recognizable skills found in job description."
        )

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills

    ats_score = round((len(matched) / len(jd_skills)) * 100, 2)

    return {
        "ats_score": ats_score,

        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "extra_skills": sorted(extra),

        "skill_coverage_percent": ats_score,
        "total_jd_skills": len(jd_skills),
        "matched_skill_count": len(matched),

        "suggestions": [
            f"Consider adding experience with '{skill}'"
            for skill in sorted(missing)
        ],

        "chart_data": {
            "skill_distribution": {
                "labels": ["Matched", "Missing"],
                "values": [len(matched), len(missing)],
                "chart_type": "pie"
            }
        },

        "detailed_matches": [
            {
                "skill": skill,
                "similarity_score": 1.0,
                "frequency_in_jd": 1,
                "frequency_in_resume": 1
            }
            for skill in matched
        ],

        "processing_time": round(time.time() - start, 4),
    }