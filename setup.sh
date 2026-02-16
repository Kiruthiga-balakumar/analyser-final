#!/bin/bash

# Resume Analyzer - macOS/Linux Setup Script
# This script sets up the complete development environment

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Resume Analyzer - macOS/Linux Setup                       ║"
echo "║  Production-Ready AI Resume Analysis System                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[1/6] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "✗ Python 3 not found! Install Python 3.9+ from python.org"
    exit 1
fi
echo "✓ Python found"
echo ""

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/6] Installing Python dependencies..."
echo "      This may take 2-3 minutes..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Download spaCy model
echo "[5/6] Downloading spaCy NLP model..."
echo "      This may take 1-2 minutes..."
python -m spacy download en_core_web_sm --quiet
echo "✓ spaCy model downloaded"
echo ""

# Verify installation
echo "[6/6] Verifying installation..."
python verify_installation.py
echo ""

# Final instructions
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ SETUP COMPLETE!                                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Open TWO separate terminal windows"
echo ""
echo "2. In FIRST terminal:"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "3. In SECOND terminal:"
echo "   streamlit run frontend/streamlit_app.py"
echo ""
echo "4. Open browser:"
echo "   http://localhost:8501"
echo ""
echo "Happy analyzing! 🚀"
echo ""
