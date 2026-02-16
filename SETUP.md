# Detailed Setup Instructions

## Step-by-Step Installation Guide

### Prerequisites Check

Verify Python version:
```bash
python --version
# Should be 3.9 or higher
```

### Step 1: Environment Setup

#### Windows (PowerShell)
```powershell
# Navigate to project
cd C:\Users\{YourUsername}\OneDrive\Desktop\resume_analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS/Linux
```bash
cd ~/Desktop/resume_analyzer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 2: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This will install:
# - FastAPI & Uvicorn (backend framework)
# - Streamlit (frontend)
# - spaCy (NLP)
# - sentence-transformers (embeddings)
# - pdfplumber, python-docx (document parsing)
# - plotly (charts)
# - And more...
```

### Step 3: Download NLP Models

```bash
# Download spaCy English model (required)
# This is ~40MB and will be cached
python -m spacy download en_core_web_sm

# The sentence-transformers model will auto-download on first run
# (all-MiniLM-L6-v2 is ~80MB)
```

### Step 4: Verify Installation

Test that all components work:

```bash
# Test spaCy
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ spaCy OK')"

# Test FastAPI
python -c "from fastapi import FastAPI; print('✓ FastAPI OK')"

# Test Streamlit
streamlit --version
# Should show: Streamlit, version 1.28.1

# Test key libraries
python -c "import sentence_transformers; print('✓ sentence-transformers OK')"
python -c "import pdfplumber; print('✓ pdfplumber OK')"
python -c "import docx; print('✓ python-docx OK')"
```

## Running the Application

### Recommended: Two Terminal Windows

#### Terminal Window 1: Backend Server

```bash
cd resume_analyzer

# Activate venv if not already active
# Windows:
# .\venv\Scripts\Activate.ps1
# macOS/Linux:
# source venv/bin/activate

cd backend
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

#### Terminal Window 2: Frontend Server

```bash
cd resume_analyzer

# Activate venv
# Windows:
# .\venv\Scripts\Activate.ps1
# macOS/Linux:
# source venv/bin/activate

streamlit run frontend/streamlit_app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Access the Application

- **Main UI**: http://localhost:8501
- **API Documentation**: http://127.0.0.1:8000/docs (interactive Swagger UI)
- **API Health**: http://127.0.0.1:8000/health

## Testing with Sample Data

1. **Open Streamlit app** (http://localhost:8501)
2. **Upload Resume**:
   - Click "Upload Resume"
   - Select `sample_data/sample_resume.txt`
3. **Paste Job Description**:
   - Click in the text area
   - Open `sample_data/sample_job_description.txt`
   - Copy all content and paste into text area
4. **Click Analyze**
5. **Expected Results**:
   - ATS Score: 78-85
   - Matched Skills: ~10
   - Missing Skills: ~2-3
   - Processing Time: 2-4 seconds

## Configuration Options

### Environment Variables (Optional)

Create `.env` file in `backend/` directory:

```bash
# .env
API_HOST=127.0.0.1
API_PORT=8000
API_RELOAD=true
NLP_BATCH_SIZE=32
LOG_LEVEL=INFO
```

### Modify Thresholds

Edit `backend/config.py`:

```python
# Lower similarity threshold = more matches (more false positives)
NLP_CONFIG = {
    "similarity_threshold": 0.60,  # Default: 0.65
}

# Increase to extract more skills
SKILL_EXTRACTION_CONFIG = {
    "num_keywords": 50,  # Default: 30
}
```

## Troubleshooting Installation

### Issue: "ModuleNotFoundError: No module named 'spacy'"

**Solution**: Reinstall requirements
```bash
pip install --force-reinstall -r requirements.txt
```

### Issue: "No module named 'sentence_transformers'"

**Solution**: Install explicitly
```bash
pip install sentence-transformers
```

### Issue: "PyTorch not found"

**Solution**: Install torch separately
```bash
pip install torch torchvision torchaudio
```

### Issue: "Cannot connect to localhost:8000"

**Solution**: 
- Ensure backend server is running
- Check firewall settings
- Try `http://127.0.0.1:8000` instead

### Issue: "Connection refused on port 8501"

**Solution**:
- Ensure streamlit process is running
- Kill any existing process: `lsof -ti:8501 | xargs kill -9`
- Try different port: `streamlit run frontend/streamlit_app.py --server.port 8502`

### Issue: "spaCy model download fails"

**Solution**: Download manually
```bash
python -m spacy download en_core_web_sm --direct
```

### Issue: Slow on first run

**Solution**: This is normal. On first run:
1. spaCy model loads (~500MB in memory)
2. Embedding model downloads and caches (~500MB)
3. FastAPI app initializes
4. Streamlit app loads

Subsequent runs will be much faster (2-4 seconds).

## Memory Requirements

- **Minimum**: 2GB RAM
- **Recommended**: 4GB+ RAM
- **GPU**: Not required but will accelerate embeddings

If running on low-memory systems:
- Close other applications
- Use CPU-only mode for embeddings
- Process smaller resumes

## Performance Tuning

### For Faster Response Times

Edit `backend/config.py`:

```python
# Use smaller, faster model
NLP_CONFIG = {
    "embedding_model": "all-MiniLM-L6-v2",  # Already optimized
}

# Reduce extraction complexity
SKILL_EXTRACTION_CONFIG = {
    "num_keywords": 15,  # Reduced from 30
}
```

### For Higher Accuracy

```python
# Use larger model (slower)
NLP_CONFIG = {
    "embedding_model": "all-mpnet-base-v2",
    "similarity_threshold": 0.70,  # Higher threshold
}
```

## Data Privacy

- **No data is stored** after analysis
- **Temp files are deleted** immediately
- **Resume text is not logged** (unless logging is enabled)
- All processing is local (no external API calls except model downloads)

## Uninstallation

To remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment folder
# Windows: rmdir /s venv
# macOS/Linux: rm -rf venv

# Or delete the entire project folder
```

## Next Steps

1. ✅ Follow setup steps above
2. ✅ Test with sample data
3. ✅ Customize thresholds if needed
4. ✅ Use with your own resume
5. 📖 Read API documentation at `/docs`
6. 🚀 Deploy to cloud (optional)

## Getting Help

**For Issues:**
1. Check "Troubleshooting" section above
2. Run diagnostic:
   ```bash
   python tests/diagnostics.py
   ```
3. Check logs for detailed error messages
4. Try with sample data first

**For Questions:**
- Review README.md
- Check API docs: http://127.0.0.1:8000/docs
- Examine code comments and docstrings

---

Happy analyzing! 🚀
