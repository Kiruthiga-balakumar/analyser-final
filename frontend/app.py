"""
Streamlit frontend for Resume Analyzer.
Futuristic glassmorphism-style ATS dashboard.
"""

import streamlit as st
import requests
import json
import pdfplumber
from io import BytesIO

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Resume Analyser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# API CONFIG
# =========================
try:
    API_BASE_URL = st.secrets["API_URL"]
except Exception:
    API_BASE_URL = "http://127.0.0.1:8000"

API_ENDPOINT = f"{API_BASE_URL}/v1/analyze"

# =========================
# FUTURISTIC UI CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(circle at top, #2b1055, #000000 70%);
    color: #ffffff;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, rgba(138,43,226,0.45), rgba(0,255,255,0.25));
    backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 30px 80px rgba(138,43,226,0.45);
    margin-bottom: 2.5rem;
    border: 1px solid rgba(255,255,255,0.15);
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    margin: 0;
}

/* GLASS CARD */
.glass-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 20px;
}

/* SKILL TAGS */
.skill {
    display:inline-block;
    padding:8px 14px;
    margin:6px;
    border-radius:999px;
    font-weight:600;
    font-size:0.9rem;
}

.matched { background: linear-gradient(135deg,#00ff9d,#00c6ff); color:#000 }
.missing { background: linear-gradient(135deg,#ff416c,#ff4b2b); }
.extra   { background: linear-gradient(135deg,#f7971e,#ffd200); color:#000 }

/* SECTION TITLES */
.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 1.2rem 0;
}

/* FOOTER */
.footer {
    margin-top: 3rem;
    padding: 1.5rem;
    text-align: center;
    font-size: 0.95rem;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# =========================
# HELPERS
# =========================
def extract_text_from_pdf(uploaded_file) -> str:
    text = []
    with pdfplumber.open(BytesIO(uploaded_file.getvalue())) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

def hero():
    st.markdown("""
    <div class="hero">
        <h1>Resume Analyser</h1>
    </div>
    """, unsafe_allow_html=True)

def skill_block(title, skills, css):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if not skills:
        st.info("No data available")
        return
    html = "<div class='glass-card'>"
    for s in skills:
        html += f"<span class='skill {css}'>{s}</span>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================
# MAIN APP
# =========================
def main():
    hero()

    col1, col2 = st.columns([0.55, 0.45])

    with col1:
        resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        analyze = st.button("Analyze Resume")

    with col2:
        job_description = st.text_area("Job Description", height=260)

    if analyze:
        if not resume_file or not job_description:
            st.error("Please upload resume and enter job description")
            return

        resume_text = extract_text_from_pdf(resume_file)

        payload = {
            "resume": resume_text,
            "job_description": job_description
        }

        with st.spinner("Analyzing resume..."):
            res = requests.post(API_ENDPOINT, json=payload)
            if res.status_code == 200:
                st.session_state.analysis_result = res.json()
            else:
                st.error(res.text)

    if st.session_state.analysis_result:
        r = st.session_state.analysis_result

        st.markdown("<div class='section-title'>ATS Score</div>", unsafe_allow_html=True)
        st.metric("Score", f"{r['ats_score']} / 100")

        skill_block("Matched Skills", r["matched_skills"], "matched")
        skill_block("Missing Skills", r["missing_skills"], "missing")
        skill_block("Extra Skills", r["extra_skills"], "extra")

        st.markdown("<div class='section-title'>Improvement Suggestions</div>", unsafe_allow_html=True)
        for s in r["suggestions"]:
            st.markdown(f"- {s}")

        st.download_button(
            "Download Analysis (JSON)",
            json.dumps(r, indent=2),
            file_name="analysis.json"
        )

    st.markdown("""
    <div class="footer">
        Resume Analyser is an intelligent ATS-based platform that evaluates resumes
        against job descriptions, identifies skill gaps, and provides actionable
        improvement suggestions to enhance employability.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()