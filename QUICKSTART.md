# Resume Analyzer - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.9+
- pip

### Installation & Running

#### 1️⃣ Install (2 min)
```bash
# Navigate to project
cd resume_analyzer

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm
```

#### 2️⃣ Start Backend (Terminal 1)
```bash
cd backend
python main.py
```
✓ You should see: `Uvicorn running on http://127.0.0.1:8000`

#### 3️⃣ Start Frontend (Terminal 2)
```bash
streamlit run frontend/streamlit_app.py
```
✓ You should see: `Local URL: http://localhost:8501`

#### 4️⃣ Open App
- Visit **http://localhost:8501**
- Upload a resume
- Paste a job description
- Click **Analyze**

---

## 🧪 Quick Test

```bash
# In a third terminal (or after stopping servers):
python tests/test_api.py
```

Expected output:
```
✓ Health Check: PASSED
✓ Text Analysis: PASSED  
✓ Sample Files: PASSED

✓ All tests passed! Application is ready to use.
```

---

## 📊 What You'll See

The dashboard shows:
- **ATS Score** (0-100)
- **Skill Match** visualization
- **Matched Skills** from your resume
- **Missing Skills** to add
- **Improvement Suggestions**
- **Interactive Charts**

---

## 📁 Project Structure

```
backend/
  ├── main.py          ← FastAPI app
  ├── config.py        ← Configuration
  ├── nlp/extraction.py ← NLP pipeline
  ├── services/analyzer.py ← Scoring engine
  └── ...
  
frontend/
  └── streamlit_app.py  ← UI dashboard
  
sample_data/
  ├── sample_resume.txt
  └── sample_job_description.txt

requirements.txt       ← Dependencies
README.md             ← Full documentation
```

---

## 🔧 Troubleshooting

**Backend won't start?**
```bash
pip install --force-reinstall -r requirements.txt
python -m spacy download en_core_web_sm
```

**Frontend won't connect?**
- Ensure backend is running on port 8000
- Check firewall settings

**Analysis takes too long?**
- First run loads ML models (2-4 seconds)
- Subsequent runs are faster (~2 seconds)

---

## ✨ Key Features

✅ No hardcoded skill lists  
✅ Semantic skill matching  
✅ NLP-powered extraction  
✅ ATS score calculation  
✅ Visual analytics  
✅ Improvement suggestions  
✅ Multiple file formats (PDF, DOCX, DOC, TXT)  

---

## 📚 Full Documentation

See [README.md](README.md) for:
- Detailed feature explanation
- API reference
- Architecture details
- Configuration options
- Deployment guides

See [SETUP.md](SETUP.md) for:
- Step-by-step installation
- Troubleshooting
- Performance tuning
- Data privacy

---

## 🎯 Common Questions

**Q: Can I modify skill matching thresholds?**  
A: Yes, edit `backend/config.py` → `NLP_CONFIG["similarity_threshold"]`

**Q: Does it upload my resume to a server?**  
A: No, everything runs locally. No data is stored.

**Q: What file formats are supported?**  
A: PDF, DOCX, DOC, TXT (max 10MB)

**Q: Can I use different NLP models?**  
A: Yes, edit `backend/config.py` → `"embedding_model"`

---

## 📞 Support

- Check [README.md](README.md) for detailed documentation
- Review [SETUP.md](SETUP.md) for troubleshooting
- Run `python tests/test_api.py` to diagnose issues
- Visit API docs: http://127.0.0.1:8000/docs

---

**Enjoy your AI-powered resume analyzer! 🎉**
