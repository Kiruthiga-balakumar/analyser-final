"""
Concept-based skill mapping engine.
Maps raw text → normalized concept skills using concept_groups.json
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


class ConceptMapper:
    """
    Maps resume and JD text to domain-agnostic skill concepts.
    """

    def __init__(self, concept_file: str = None):
        if concept_file is None:
            concept_file = Path(__file__).parent / "concept_groups.json"

        self.concept_groups = self._load_concepts(concept_file)
        self.phrase_to_concept = self._build_reverse_index(self.concept_groups)

    # ------------------------
    # Load & preprocess
    # ------------------------

    def _load_concepts(self, path: str) -> Dict[str, List[str]]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                concept: [p.lower().strip() for p in phrases]
                for concept, phrases in data.items()
            }
        except Exception as e:
            raise RuntimeError(f"Failed to load concept file: {e}")

    def _build_reverse_index(self, concepts: Dict[str, List[str]]) -> Dict[str, str]:
        """
        phrase -> concept mapping
        """
        index = {}
        for concept, phrases in concepts.items():
            for phrase in phrases:
                index[phrase] = concept
        return index

    # ------------------------
    # Core public methods
    # ------------------------

    def extract_concepts(self, text: str) -> List[str]:

        """
        Extract normalized concept skills from raw text.
        """
        text = self._normalize_text(text)
        found_concepts = set()

        for phrase, concept in self.phrase_to_concept.items():
            if self._phrase_exists(phrase, text):
                found_concepts.add(concept)

        return found_concepts

    def match_concepts(
        self, resume_text: str, jd_text: str
    ) -> Tuple[Set[str], Set[str], Set[str]]:
        """
        Returns matched, missing, extra concepts
        """
        resume_concepts = self.extract_concepts(resume_text)
        jd_concepts = self.extract_concepts(jd_text)

        matched = resume_concepts & jd_concepts
        missing = jd_concepts - resume_concepts
        extra = resume_concepts - jd_concepts

        return matched, missing, extra

    # ------------------------
    # Helpers
    # ------------------------

    def _normalize_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _phrase_exists(self, phrase: str, text: str) -> bool:
        """
        Ensures phrase-level matching, not token overlap.
        """
        pattern = r"\b" + re.escape(phrase) + r"\b"
        return phrase in text

