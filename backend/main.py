"""
Main FastAPI application.
Sets up routes, middleware, error handling, and startup/shutdown.
"""

import logging
from contextlib import asynccontextmanager
from .config import API_CONFIG, LOGGING_CONFIG
from .api.routes import router


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Relative imports (works within backend package)
from .config import API_CONFIG, LOGGING_CONFIG
from .api.routes import router

# Configure logging
logging.basicConfig(**LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events."""
    logger.info("🚀 Resume Analyzer API starting...")
    logger.info("Loading NLP models... (this may take a moment)")
    yield
    logger.info("🛑 Resume Analyzer API shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis against job descriptions",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Resume Analyzer API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "analyze": "POST /analyze",
            "analyze_text": "POST /analyze-text",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }


# Only use this if you want to run the app with "python -m backend.main"
if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",  # <-- include 'backend.' here
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["reload"],
        workers=API_CONFIG["workers"]
    )
