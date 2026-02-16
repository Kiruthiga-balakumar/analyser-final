"""
Streamlit frontend for Resume Analyzer.
Professional ATS-style dashboard with gradient theme and interactive charts.
"""

import streamlit as st
import requests
import json

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Resume Analyzer | ATS Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# API CONFIG
# =========================
# Default local backend URL
API_BASE_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
  :root {
    --purple-1: #6a0dad;
    --purple-2: #3b1f7f;
  }
  html, body {
    background: linear-gradient(180deg, #f5f7ff 0%, #e0e6ff 50%, #f5f7ff 100%);
  }
  .main-header {
    background: linear-gradient(90deg, var(--purple-1), var(--purple-2));
    padding: 2.5rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
  }
  .section-title { font-size: 26px; font-weight:700; margin-bottom: 12px; }
  .card {
    background: rgba(255,255,255,0.95);
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 8px 22px rgba(16,22,64,0.08);
    margin-bottom: 16px;
  }
  .skill-tag {
    display:inline-block;
    padding:6px 12px;
    border-radius:18px;
    margin:6px;
    font-weight:600;
  }
  .matched { background:#38ef7d; color:#0b3d2e }
  .missing { background:#f45c43; color:white }
  .extra { background:#fee140; color:#333 }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# =========================
# UI HELPERS
# =========================
def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Resume Analyzer</h1>
        <p>ATS Scoring & Job Match Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

def render_skill_section(title, skills, cls):
    st.markdown(f"### {title}")
    if not skills:
        st.info("No data available")
        return
    html = "<div class='card'>"
    for s in skills:
        html += f"<span class='skill-tag {cls}'>{s}</span>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================
# MAIN APP
# =========================
def main():
    render_header()

    col_left, col_right = st.columns([0.6, 0.4])

    with col_left:
        st.markdown("### 📄 Upload Resume")
        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "doc", "txt"],
            label_visibility="collapsed"
        )

        analyze_btn = st.button("🔍 Analyze Resume")
        clear_btn = st.button("🔄 Clear")

        if clear_btn:
            st.session_state.analysis_result = None
            st.experimental_rerun()

    with col_right:
        st.markdown("### 📝 Job Description")
        job_description = st.text_area(
            "Paste Job Description",
            height=320,
            label_visibility="collapsed"
        )

    # =========================
    # ANALYSIS
    # =========================
    if analyze_btn:
        if not resume_file:
            st.error("❌ Please upload a resume")
            return
        if not job_description or len(job_description.strip()) < 50:
            st.error("❌ Job description must be at least 50 characters")
            return

        with st.spinner("Analyzing resume..."):
            try:
                # Prepare payload
                files = {"resume_file": (resume_file.name, resume_file.getvalue())}
                data = {"job_description": job_description}

                response = requests.post(
                    f"{API_BASE_URL}/analyze",
                    files=files,
                    data=data,
                    timeout=120
                )

                if response.status_code == 200:
                    st.session_state.analysis_result = response.json()
                    st.success("✅ Analysis Complete")
                else:
                    try:
                        err = response.json()
                        st.error(f"❌ API Error: {err.get('detail','Unknown error')}")
                    except:
                        st.error(f"❌ API Error: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Backend not reachable.\n\n"
                    "Run backend first:\n"
                    "```bash\nuvicorn backend.main:app --reload\n```"
                )
            except requests.exceptions.Timeout:
                st.error("❌ Backend timeout. Try again later.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # =========================
    # RESULTS
    # =========================
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result

        st.markdown("---")
        st.markdown("## 📊 ATS Results")

        col1, col2, col3 = st.columns(3)
        col1.metric("ATS Score", f"{result.get('ats_score','-')} / 100")
        col2.metric("Matched Skills", result.get("matched_skill_count",0))
        col3.metric("Coverage", f"{result.get('skill_coverage_percent',0):.0f}%")

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            render_skill_section("✅ Matched Skills", result.get("matched_skills", []), "matched")
        with col2:
            render_skill_section("⚠️ Missing Skills", result.get("missing_skills", []), "missing")

        render_skill_section("➕ Extra Skills", result.get("extra_skills", []), "extra")

        st.markdown("---")
        st.markdown("### 📥 Export Results")

        st.download_button(
            "📄 Download JSON",
            json.dumps(result, indent=2),
            file_name="resume_analysis.json",
            mime="application/json"
        )

    else:
        st.markdown("""
        <div class="card">
            <h3>🎯 How it Works</h3>
            <ol>
                <li>Upload your resume</li>
                <li>Paste job description</li>
                <li>Click Analyze</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
