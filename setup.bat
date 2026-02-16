@echo off
REM Resume Analyzer - Windows Setup Script
REM This script sets up the complete development environment on Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Resume Analyzer - Windows Setup                           ║
echo ║  Production-Ready AI Resume Analysis System                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python version
echo [1/6] Checking Python installation...
python --version
if errorlevel 1 (
    echo ✗ Python not found! Install Python 3.9+ from python.org
    pause
    exit /b 1
)
echo ✓ Python found
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv (
    echo ✓ Virtual environment already exists
) else (
    python -m venv venv
    echo ✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo [4/6] Installing Python dependencies...
echo        This may take 2-3 minutes...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo ✓ Dependencies installed
echo.

REM Download spaCy model
echo [5/6] Downloading spaCy NLP model...
echo        This may take 1-2 minutes...
python -m spacy download en_core_web_sm --quiet
echo ✓ spaCy model downloaded
echo.

REM Verify installation
echo [6/6] Verifying installation...
python verify_installation.py
echo.

REM Final instructions
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✓ SETUP COMPLETE!                                         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo.
echo 1. Open TWO separate terminal windows
echo.
echo 2. In FIRST terminal:
echo    cd backend
echo    python main.py
echo.
echo 3. In SECOND terminal:
echo    streamlit run frontend/streamlit_app.py
echo.
echo 4. Open browser:
echo    http://localhost:8501
echo.
echo Happy analyzing! 🚀
echo.
pause
