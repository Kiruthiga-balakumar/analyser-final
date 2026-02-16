"""
REST API endpoints for Resume Analyzer.
"""
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path

from backend.models.schemas import AnalysisRequest, AnalysisResponse
from backend.utils.parser import extract_text_from_file, clean_text, validate_text
from backend.config import UPLOAD_CONFIG

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
) -> AnalysisResponse:
    """
    Main endpoint: Analyze resume against job description.
    """
    try:
        # Validate job description
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Job description must be at least 50 characters"
            )

        # Check file size
        file_content = await resume_file.read()
        if len(file_content) > UPLOAD_CONFIG["max_file_size"]:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {UPLOAD_CONFIG['max_file_size'] / 1024 / 1024}MB"
            )

        # Check file extension
        file_ext = f".{resume_file.filename.split('.')[-1].lower()}"
        if file_ext not in UPLOAD_CONFIG["allowed_extensions"]:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file format. Allowed: {', '.join(UPLOAD_CONFIG['allowed_extensions'])}"
            )

        # Save temporary file
        temp_path: Path = UPLOAD_CONFIG["temp_upload_dir"] / resume_file.filename
        with open(temp_path, "wb") as f:
            f.write(file_content)

        # Extract text from resume
        try:
            resume_text = extract_text_from_file(str(temp_path))
        except Exception as e:
            logger.error(f"Error extracting text from resume: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Could not read resume file: {str(e)}"
            )
        finally:
            temp_path.unlink(missing_ok=True)

        # Clean and validate texts
        resume_text = clean_text(resume_text)
        jd_text = clean_text(job_description)

        is_valid, error_msg = validate_text(resume_text, min_length=50)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Resume validation failed: {error_msg}")

        is_valid, error_msg = validate_text(jd_text, min_length=50)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Job description validation failed: {error_msg}")

        # Perform analysis using local import to avoid circular import
        from backend.nlp.extraction import analyze_resume_with_matcher
        logger.info("Starting resume analysis...")
        analysis_result = analyze_resume_with_matcher(jd_text, resume_text)

        logger.info(f"Analysis complete. ATS Score: {analysis_result.ats_score}")
        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/analyze-text", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest) -> AnalysisResponse:
    """
    Alternative endpoint: Analyze resume and job description as raw text.
    """
    try:
        if not request.resume_text or len(request.resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume text must be at least 50 characters"
            )

        if not request.job_description or len(request.job_description.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Job description must be at least 50 characters"
            )

        resume_text = clean_text(request.resume_text)
        jd_text = clean_text(request.job_description)

        is_valid, error_msg = validate_text(resume_text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Resume validation failed: {error_msg}")

        is_valid, error_msg = validate_text(jd_text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Job description validation failed: {error_msg}")

        # Perform analysis using local import
        from backend.nlp.extraction import analyze_resume_with_matcher
        logger.info("Starting resume analysis (text mode)...")
        analysis_result = analyze_resume_with_matcher(jd_text, resume_text)

        logger.info(f"Analysis complete. ATS Score: {analysis_result.ats_score}")
        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze-text endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Resume Analyzer API",
        "version": "1.0.0"
    }
