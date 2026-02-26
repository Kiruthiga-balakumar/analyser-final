# backend/services/analyzer.py

import time
import re
from typing import List

from backend.models.schemas import (
    AnalysisResponse,
    SkillMatch,
    ChartData,
    CourseRecommendation
)

# ------------------------------------------------------------------
# Canonical Skill Set (single source of truth)
# ------------------------------------------------------------------

SKILL_DB = {
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "fastapi", "flask", "django",
    "pandas", "numpy",
    "aws", "docker", "git",
    "data analysis", "data science"
}

# ------------------------------------------------------------------
# Static Course Suggestions (SAFE, NON-DYNAMIC)
# ------------------------------------------------------------------

COURSE_SUGGESTIONS = {
    "python": [
        "Python for Everybody – University of Michigan (Coursera)",
        "Python Basics – Google (Coursera)"
    ],
    "sql": [
        "SQL for Data Science – UC Davis (Coursera)",
        "Databases and SQL – IBM Skills Network"
    ],
    "machine learning": [
        "Machine Learning – Stanford University (Coursera)",
        "Machine Learning Specialization – DeepLearning.AI"
    ],
    "deep learning": [
        "Deep Learning Specialization – DeepLearning.AI",
        "Neural Networks and Deep Learning – Coursera"
    ],
    "nlp": [
        "Natural Language Processing – DeepLearning.AI",
        "Applied NLP – Coursera"
    ],
    "aws": [
        "AWS Cloud Practitioner Essentials – Amazon",
        "AWS Fundamentals – Coursera"
    ],
    "docker": [
        "Docker Essentials – IBM",
        "Docker for Developers – Coursera"
    ]
}

# ------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_skills(text: str) -> set[str]:
    text = normalize(text)
    found = set()

    for skill in SKILL_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.add(skill)

    return found

def count_occurrences(text: str, skill: str) -> int:
    pattern = r"\b" + re.escape(skill) + r"\b"
    return len(re.findall(pattern, normalize(text)))

# ------------------------------------------------------------------
# ATS Analyzer
# ------------------------------------------------------------------

class ATSAnalyzer:
    def analyze_resume(self, jd_text: str, resume_text: str) -> AnalysisResponse:
        start = time.time()

        jd_skills = extract_skills(jd_text)
        resume_skills = extract_skills(resume_text)

        # ATS invariant
        if not jd_skills:
            raise ValueError("No detectable skills in job description")

        matched = jd_skills & resume_skills
        missing = jd_skills - resume_skills
        extra = resume_skills - jd_skills

        matched_count = len(matched)
        total_jd = len(jd_skills)

        ats_score = round((matched_count / total_jd) * 100, 2)

        # -----------------------------
        # Detailed Matches
        # -----------------------------

        detailed_matches = [
            SkillMatch(
                skill=skill,
                similarity_score=1.0,
                frequency_in_jd=count_occurrences(jd_text, skill),
                frequency_in_resume=count_occurrences(resume_text, skill),
            )
            for skill in sorted(matched)
        ]

        # -----------------------------
        # Improvement Suggestions
        # -----------------------------

        suggestions: List[str] = [
            f"Consider adding hands-on experience or projects involving '{skill}'."
            for skill in sorted(missing)
        ]

        if ats_score < 50:
            suggestions.append(
                "Overall skill alignment is low. Tailor your resume more closely to the job description."
            )

        # -----------------------------
        # Course Recommendations (OPTIONAL)
        # -----------------------------

        course_recommendations: List[CourseRecommendation] = []

        for skill in sorted(missing):
            if skill in COURSE_SUGGESTIONS:
                course_recommendations.append(
                    CourseRecommendation(
                        skill=skill,
                        courses=COURSE_SUGGESTIONS[skill]
                    )
                )

        # -----------------------------
        # Charts
        # -----------------------------

        chart_data = {
            "skills": ChartData(
                labels=["Matched", "Missing", "Extra"],
                values=[len(matched), len(missing), len(extra)],
                chart_type="bar"
            )
        }

        return AnalysisResponse(
            ats_score=ats_score,

            matched_skills=sorted(matched),
            missing_skills=sorted(missing),
            extra_skills=sorted(extra),

            skill_coverage_percent=ats_score,
            total_jd_skills=total_jd,
            matched_skill_count=matched_count,

            suggestions=suggestions,
            course_recommendations=course_recommendations or None,

            chart_data=chart_data,
            detailed_matches=detailed_matches,

            processing_time=round(time.time() - start, 3),
        )