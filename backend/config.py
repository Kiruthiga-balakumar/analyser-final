"""
Configuration settings for Resume Analyzer.
"""

import os
from pathlib import Path

# =================================================
# PROJECT ROOT
# =================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =================================================
# NLP CONFIGURATION
# =================================================
NLP_CONFIG = {
    "spacy_model": "en_core_web_sm",
    "embedding_model": "all-MiniLM-L6-v2",
    "keybert_model": "all-MiniLM-L6-v2",
    "similarity_threshold": 0.65,
    "fuzzy_match_threshold": 85,
}

# =================================================
# API CONFIGURATION
# =================================================
API_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
    "reload": True,
    "workers": 1,
}

# =================================================
# UPLOAD CONFIGURATION
# =================================================
UPLOAD_CONFIG = {
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "allowed_extensions": {".pdf", ".docx", ".doc", ".txt"},
    "temp_upload_dir": PROJECT_ROOT / "temp_uploads",
}

# Ensure upload directory exists
UPLOAD_CONFIG["temp_upload_dir"].mkdir(parents=True, exist_ok=True)

# =================================================
# SKILL EXTRACTION CONFIG
# =================================================
SKILL_EXTRACTION_CONFIG = {
    "min_skill_length": 2,
    "max_skill_length": 50,
    "ngram_range": (1, 3),
    "num_keywords": 30,
    "language": "english",
}

# =================================================
# SCORING CONFIG
# =================================================
SCORING_CONFIG = {
    "base_match_weight": 1.0,
    "frequency_bonus": 0.1,
    "primary_skill_multiplier": 1.2,
    "exact_match_boost": 0.15,
}

# =================================================
# LOGGING CONFIG
# =================================================
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}
