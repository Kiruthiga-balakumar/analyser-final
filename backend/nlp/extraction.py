# backend/nlp/extraction.py

import re
from collections import Counter
from typing import Dict, Set

# Canonical skill vocabulary (expand safely)
SKILL_DB = {
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "fastapi", "flask", "django",
    "data analysis", "data science",
    "pandas", "numpy",
    "aws", "docker", "git"
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_skills_with_frequency(text: str) -> Dict[str, int]:
    """
    Returns:
        {
            "python": 2,
            "sql": 1,
            ...
        }
    """
    if not text or not text.strip():
        raise ValueError("Empty text passed to extractor")

    text = normalize_text(text)
    frequencies = Counter()

    for skill in SKILL_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        matches = re.findall(pattern, text)
        if matches:
            frequencies[skill] = len(matches)

    return dict(frequencies)


def extract_skill_set(text: str) -> Set[str]:
    return set(extract_skills_with_frequency(text).keys())