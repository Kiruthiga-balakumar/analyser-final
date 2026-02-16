"""
ATS scoring engine and analysis service.
Performs comprehensive resume-to-job-description matching.
"""
import logging
import time
from typing import List, Dict, Set, Tuple
from collections import Counter

from backend.config import SCORING_CONFIG
from backend.nlp.extraction import SkillExtractor, SemanticMatcher
from backend.models.schemas import AnalysisResponse, SkillMatch, ChartData

logger = logging.getLogger(__name__)


class ATSAnalyzer:
    """
    Main analysis engine that compares resume against job description.
    Calculates ATS score, identifies matched/missing skills, and provides suggestions.
    """

    def __init__(self):
        """Initialize analyzer with NLP components."""
        self.skill_extractor = SkillExtractor()
        self.semantic_matcher = SemanticMatcher()

    def analyze_resume(self, job_description: str, resume_text: str) -> AnalysisResponse:
        """
        Complete analysis of resume against job description.

        Args:
            job_description: Job description text
            resume_text: Resume text

        Returns:
            AnalysisResponse with complete analysis results
        """
        start_time = time.time()

        try:
            # Extract skills from both texts
            jd_skills = self.skill_extractor.extract_skills_from_text(job_description)
            resume_skills = self.skill_extractor.extract_skills_from_text(resume_text)

            if not jd_skills:
                jd_skills = self._extract_fallback_skills(job_description)

            if not resume_skills:
                raise ValueError("No skills found in resume. Please check file format.")

            logger.info(f"Extracted {len(jd_skills)} JD skills and {len(resume_skills)} resume skills")

            # Normalize skills
            jd_skills_norm = [self.skill_extractor.normalize_skill(s) for s in jd_skills]
            resume_skills_norm = [self.skill_extractor.normalize_skill(s) for s in resume_skills]

            # Match skills semantically
            matched_skills, missing_skills, extra_skills, detailed_matches = self._match_skills(
                resume_skills_norm,
                jd_skills_norm,
                resume_text,
                job_description,
            )

            # Calculate ATS score
            ats_score = self._calculate_ats_score(
                matched_skills,
                jd_skills_norm,
                resume_text,
                job_description,
            )

            # Coverage percentage
            skill_coverage_percent = (
                (len(matched_skills) / len(jd_skills_norm) * 100)
                if jd_skills_norm
                else 0
            )

            # Suggestions
            suggestions = self._generate_suggestions(
                missing_skills,
                matched_skills,
                jd_skills_norm,
                ats_score,
            )

            # Charts
            chart_data = self._generate_chart_data(
                matched_skills,
                missing_skills,
                extra_skills,
                ats_score,
            )

            processing_time = time.time() - start_time

            return AnalysisResponse(
                ats_score=int(ats_score),
                matched_skills=list(matched_skills),
                missing_skills=list(missing_skills),
                extra_skills=list(extra_skills),
                skill_coverage_percent=round(skill_coverage_percent, 2),
                total_jd_skills=len(jd_skills_norm),
                matched_skill_count=len(matched_skills),
                suggestions=suggestions,
                chart_data=chart_data,
                detailed_matches=detailed_matches,
                processing_time=round(processing_time, 3),
            )

        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise

    def _extract_fallback_skills(self, text: str) -> List[str]:
        """Fallback skill extraction using simple regex."""
        import re

        common_skills = [
            r"\bpython\b",
            r"\bjava\b",
            r"\bc\+\+\b",
            r"\bjavascript\b",
            r"\breact\b",
            r"\bdjango\b",
            r"\bflask\b",
            r"\bsql\b",
            r"\baws\b",
            r"\bazure\b",
            r"\bdocker\b",
            r"\bkubernetes\b",
            r"\bgit\b",
            r"\blinux\b",
            r"\bwindows\b",
        ]

        found = []
        for pattern in common_skills:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                found.append(match.group().lower())

        return list(set(found))

    def _match_skills(
        self,
        resume_skills: List[str],
        jd_skills: List[str],
        resume_text: str,
        jd_text: str,
    ) -> Tuple[Set[str], Set[str], Set[str], List[SkillMatch]]:

        matched_skills = set()
        detailed_matches = []

        resume_freq = Counter(resume_skills)
        jd_freq = Counter(jd_skills)

        for resume_skill in set(resume_skills):
            best_match, score = self.semantic_matcher.find_best_match(
                resume_skill,
                list(set(jd_skills)),
            )

            if score >= self.semantic_matcher.similarity_threshold:
                matched_skills.add(best_match)

                detailed_matches.append(
                    SkillMatch(
                        skill=best_match,
                        similarity_score=round(score, 3),
                        frequency_in_jd=jd_freq[best_match],
                        frequency_in_resume=resume_freq[resume_skill],
                    )
                )

        missing_skills = set(jd_skills) - matched_skills
        extra_skills = set(resume_skills) - matched_skills

        return matched_skills, missing_skills, extra_skills, detailed_matches

    def _calculate_ats_score(
        self,
        matched_skills: Set[str],
        jd_skills: List[str],
        resume_text: str,
        jd_text: str,
    ) -> float:

        if not jd_skills:
            return 0.0

        base_score = (len(matched_skills) / len(jd_skills)) * 100

        resume_word_count = len(resume_text.split())
        text_bonus = min(10, resume_word_count / 100)

        frequency_bonus = 0
        for skill in matched_skills:
            occurrences = resume_text.lower().count(skill.lower())
            if occurrences > 1:
                frequency_bonus += min(
                    5,
                    (occurrences - 1) * SCORING_CONFIG["frequency_bonus"],
                )

        exact_matches = sum(
            1 for skill in matched_skills
            if any(skill.lower() == s.lower() for s in jd_skills)
        )

        exact_bonus = exact_matches * SCORING_CONFIG["exact_match_boost"]

        return min(100, base_score + frequency_bonus + exact_bonus + text_bonus)

    def _generate_suggestions(
        self,
        missing: Set[str],
        matched: Set[str],
        jd_skills: List[str],
        ats_score: float,
    ) -> List[str]:

        suggestions = []

        if ats_score < 50:
            suggestions.append(
                f"⚠️ Low ATS score ({int(ats_score)}/100). Add more relevant skills."
            )

        if missing:
            top_missing = sorted(list(missing))[:3]
            suggestions.append(
                f"🎯 Priority skills to add: {', '.join(top_missing)}"
            )

        if len(missing) > 5:
            suggestions.append(
                f"📚 Missing {len(missing)} skills. Create a focused learning plan."
            )

        if matched:
            suggestions.append(
                f"✅ You matched {len(matched)} skills. Highlight them clearly."
            )

        if ats_score >= 70:
            suggestions.append(
                "💡 Strong alignment. Use matched keywords in your summary."
            )

        suggestions.append(
            "📄 Mention skills inside real projects for better ATS ranking."
        )

        return suggestions[:5]

    def _generate_chart_data(
        self,
        matched: Set[str],
        missing: Set[str],
        extra: Set[str],
        ats_score: float,
    ) -> Dict[str, ChartData]:

        total_jd = len(matched) + len(missing)

        return {
            "skill_match_pie": ChartData(
                labels=["Matched Skills", "Missing Skills"],
                values=[len(matched), len(missing)],
                chart_type="pie",
            ),
            "coverage_bar": ChartData(
                labels=["Required Skills Found", "Skills to Add"],
                values=[
                    (len(matched) / total_jd * 100) if total_jd else 0,
                    (len(missing) / total_jd * 100) if total_jd else 0,
                ],
                chart_type="bar",
            ),
            "score_gauge": ChartData(
                labels=["ATS Score", "Remaining"],
                values=[ats_score, 100 - ats_score],
                chart_type="gauge",
            ),
        }
