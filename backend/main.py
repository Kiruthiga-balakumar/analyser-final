"""
Main FastAPI application.
Initializes app, middleware, lifespan, and API routes.
"""
print("🔥 LOADED backend.main 🔥")

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Local imports
from .api.routes import router

# ------------------------------------------------------------------
# Logging configuration (safe default)
# ------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Resume Analyzer API starting up")
    yield
    logger.info("🛑 Resume Analyzer API shutting down")

# ------------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------------

app = FastAPI(
    title="Resume Analyzer API",
    description="Resume vs Job Description skill analysis",
    version="1.0.0",
    lifespan=lifespan,
)

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Global exception handler
# ------------------------------------------------------------------

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
        },
    )

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

# API routes (/v1/*)
app.include_router(router)
print("🔥 ROUTES:", [r.path for r in app.routes])
# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Resume Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "POST /v1/analyze",
            "health": "GET /v1/health",
            "docs": "GET /docs",
        },
    }

# ------------------------------------------------------------------
# Run with: python -m backend.main
# ------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )