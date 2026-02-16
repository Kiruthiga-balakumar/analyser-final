"""
NLP utilities for Resume Analyzer: skill extraction, semantic matching, etc.
"""

from typing import List, Dict, Any
import spacy

nlp = spacy.load("en_core_web_sm")


class SkillExtractor:
    """Extracts skills from resume or job description text."""
    def extract_skills(self, text: str) -> List[str]:
        doc = nlp(text)
        skills = [token.text.lower() for token in doc if token.pos_ in ("NOUN", "PROPN")]
        return list(set(skills))


class SemanticMatcher:
    """Matches resume skills to job description skills."""
    def match(self, jd_skills: List[str], resume_skills: List[str]) -> Dict[str, Any]:
        matched = set(jd_skills).intersection(resume_skills)
        score = len(matched) / max(len(jd_skills), 1) * 100
        return {"matched_skills": list(matched), "score": score}


def analyze_resume_with_matcher(jd_text: str, resume_text: str):
    """
    Call ATSAnalyzer without causing circular import.
    Local import prevents circular import error.
    """
    from ..services.analyzer import ATSAnalyzer  # local import
    analyzer = ATSAnalyzer()
    return analyzer.analyze_resume(jd_text, resume_text)
