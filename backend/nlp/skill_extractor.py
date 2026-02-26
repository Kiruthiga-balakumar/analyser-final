"""
Skill Extraction + Token Overlap Matching (ATS-style V1)
======================================================
- Uses spaCy
- Strong normalization
- Phrase + keyword extraction
- Token overlap matching
- No ML / no embeddings (safe for placements)
"""

import re
import spacy
from typing import List, Dict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ------------------ Utils ------------------

STOP_SKILLS = {
    "experience", "knowledge", "ability", "skills",
    "project", "projects", "work", "working",
    "using", "use", "based", "good"
}

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def valid_skill(skill: str) -> bool:
    if len(skill) < 2:
        return False
    if skill in STOP_SKILLS:
        return False
    if skill.isdigit():
        return False
    return True

# ------------------ Skill Extractor ------------------

class SkillExtractor:
    """
    Extract clean skill phrases + keywords
    """

    def extract_skills(self, text: str) -> List[str]:
        if not text:
            return []

        text = normalize(text)
        doc = nlp(text)

        skills = set()

        # 1️⃣ Phrase-level skills (noun chunks)
        for chunk in doc.noun_chunks:
            phrase = normalize(chunk.text)

            if 1 <= len(phrase.split()) <= 4 and valid_skill(phrase):
                skills.add(phrase)

        # 2️⃣ Keyword-level skills (fallback)
        for token in doc:
            if token.pos_ in {"NOUN", "PROPN"}:
                lemma = normalize(token.lemma_)
                if valid_skill(lemma):
                    skills.add(lemma)

        return sorted(skills)

# ------------------ Matcher ------------------

class SemanticMatcher:
    """
    Token-overlap matcher (ATS-safe)
    """

    def match(
        self,
        jd_skills: List[str],
        resume_skills: List[str]
    ) -> Dict[str, List[str]]:

        matched = []
        missing = []
        extra = []

        resume_tokens = set(" ".join(resume_skills).split())

        # JD → Resume matching
        for jd_skill in jd_skills:
            jd_tokens = set(jd_skill.split())

            overlap = jd_tokens.intersection(resume_tokens)

            if overlap:
                matched.append(jd_skill)
            else:
                missing.append(jd_skill)

        # Resume extras
        for r_skill in resume_skills:
            r_tokens = set(r_skill.split())
            found = False

            for j_skill in jd_skills:
                if r_tokens.intersection(set(j_skill.split())):
                    found = True
                    break

            if not found:
                extra.append(r_skill)

        return {
            "matched": sorted(set(matched)),
            "missing": sorted(set(missing)),
            "extra": sorted(set(extra)),
        }
