import streamlit as st
import pandas as pd
import os
import time
import random
import sys

# ─── Path Setup ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ─── Page Config (MUST be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="CareerAI Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}
[data-testid="stSidebar"] .stRadio > label {
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b9dc3 !important;
    margin-bottom: 0.5rem;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.6rem 1rem;
    margin: 0.25rem 0;
    transition: all 0.2s ease;
    cursor: pointer;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    color: #c8d0e0 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.4);
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(168,85,247,0.15) 50%, rgba(236,72,153,0.1) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 24px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    backdrop-filter: blur(10px);
}
.hero-banner h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
}
.hero-banner p {
    color: #9ca3af;
    font-size: 1.05rem;
    margin: 0;
}

/* ── Section Header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}
.section-header h2 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e5e7eb;
    margin: 0;
}
.section-badge {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Cards ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.75rem 0;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s;
}
.glass-card:hover {
    border-color: rgba(99,102,241,0.3);
}

/* ── Metric Cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.metric-card {
    flex: 1;
    min-width: 140px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.25rem;
    text-align: center;
}
.metric-card .metric-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-card .metric-label {
    font-size: 0.78rem;
    color: #6b7280;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Skill Pills ── */
.skill-pill {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.2rem;
}
.skill-pill.missing {
    background: rgba(239,68,68,0.1);
    border-color: rgba(239,68,68,0.3);
    color: #fca5a5;
}
.skill-pill.success {
    background: rgba(34,197,94,0.1);
    border-color: rgba(34,197,94,0.3);
    color: #86efac;
}

/* ── Score Ring ── */
.score-container {
    text-align: center;
    padding: 1rem;
}
.score-ring {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.score-label {
    font-size: 0.85rem;
    color: #6b7280;
    font-weight: 500;
    margin-top: 0.25rem;
}

/* ── Alert Boxes ── */
.alert-success {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    color: #86efac;
    margin: 0.5rem 0;
}
.alert-warning {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    color: #fcd34d;
    margin: 0.5rem 0;
}
.alert-danger {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    color: #fca5a5;
    margin: 0.5rem 0;
}
.alert-info {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    color: #a5b4fc;
    margin: 0.5rem 0;
}

/* ── Progress Bar ── */
.progress-bar-wrapper {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 10px;
    margin: 0.5rem 0;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    transition: width 0.5s ease;
}
.progress-bar-fill.danger {
    background: linear-gradient(90deg, #ef4444, #f97316);
}
.progress-bar-fill.success {
    background: linear-gradient(90deg, #10b981, #34d399);
}

/* ── Streamlit Overrides ── */
.stTextArea textarea, .stTextInput input, .stSelectbox > div > div, .stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e5e7eb !important;
}
.stButton button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: transform 0.1s, box-shadow 0.2s !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.45) !important;
}
.stFileUploader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px dashed rgba(99,102,241,0.4) !important;
    border-radius: 12px !important;
}
.stDataFrame {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.75rem 1rem;
}
[data-testid="stMetric"] label {
    color: #6b7280 !important;
    font-size: 0.75rem !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #e5e7eb !important;
    font-weight: 700 !important;
}

div[data-testid="stMarkdownContainer"] > p {
    color: #d1d5db;
}
h1, h2, h3, h4, h5, h6 {
    color: #f3f4f6 !important;
}
label {
    color: #9ca3af !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
.stSlider > div > div > div {
    color: #a5b4fc !important;
}
.stDivider {
    border-color: rgba(255,255,255,0.08) !important;
}

/* ── Course Card ── */
.course-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s;
}
.course-card:hover {
    border-color: rgba(99,102,241,0.4);
}
.course-icon {
    font-size: 1.8rem;
    flex-shrink: 0;
}
.course-info h4 {
    margin: 0 0 0.2rem 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: #e5e7eb !important;
}
.course-info p {
    margin: 0;
    font-size: 0.78rem;
    color: #6b7280;
}

/* ── Roadmap Step ── */
.roadmap-step {
    display: flex;
    gap: 1rem;
    margin: 0.75rem 0;
    align-items: flex-start;
}
.step-number {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
}
.step-content {
    flex: 1;
}
.step-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e5e7eb;
}
.step-weeks {
    font-size: 0.75rem;
    color: #6b7280;
}

/* ── Tag styles ── */
.tag-easy { color: #86efac; background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25); border-radius: 6px; padding: 0.15rem 0.5rem; font-size: 0.75rem; font-weight: 600; }
.tag-medium { color: #fcd34d; background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25); border-radius: 6px; padding: 0.15rem 0.5rem; font-size: 0.75rem; font-weight: 600; }
.tag-hard { color: #fca5a5; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.25); border-radius: 6px; padding: 0.15rem 0.5rem; font-size: 0.75rem; font-weight: 600; }

/* ── Interview Question Box ── */
.question-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1));
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 16px;
    padding: 1.75rem;
    margin: 1rem 0;
}
.question-box h3 {
    color: #e5e7eb !important;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
}

/* ── Timer ── */
.timer-display {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #f472b6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

/* ── Sidebar logo ── */
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 1rem 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.sidebar-logo h2 {
    font-size: 1.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.3rem 0 0;
    color: transparent !important;
}
.sidebar-logo .logo-icon {
    font-size: 2.5rem;
}
.sidebar-version {
    font-size: 0.7rem;
    color: #4b5563 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">🚀</div>
        <h2>CareerAI Suite</h2>
        <span class="sidebar-version">v2.0 · All-in-One Platform</span>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Home",
            "📄  Resume Analyzer",
            "🧠  Interview Prep",
            "🛡️  Career Guard",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="padding: 1rem; background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.2); border-radius: 12px;">
        <p style="font-size:0.78rem; color:#6b7280; margin:0 0 0.5rem 0; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">About</p>
        <p style="font-size:0.82rem; color:#9ca3af; margin:0; line-height:1.5;">Three powerful AI tools — unified into one career acceleration platform.</p>
    </div>
    """, unsafe_allow_html=True)

# ─── HOME PAGE ────────────────────────────────────────────────────────────────
if page == "🏠  Home":
    st.markdown("""
    <div class="hero-banner">
        <h1>🚀 CareerAI Suite</h1>
        <p>Your all-in-one AI platform for resume analysis, interview prep, and career risk assessment</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:2.5rem; margin-bottom:0.75rem">📄</div>
            <h3 style="margin:0 0 0.5rem;font-size:1.1rem">Resume Analyzer</h3>
            <p style="font-size:0.85rem; color:#6b7280; margin:0; line-height:1.6">
                Upload your resume, paste a job description, and get instant ATS score, skill gap analysis, role prediction, and improvement suggestions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:2.5rem; margin-bottom:0.75rem">🧠</div>
            <h3 style="margin:0 0 0.5rem;font-size:1.1rem">Interview Prep</h3>
            <p style="font-size:0.85rem; color:#6b7280; margin:0; line-height:1.6">
                Track your DSA questions, identify weak topics, practice adaptive mock interviews with a timer, and monitor your readiness score.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:2.5rem; margin-bottom:0.75rem">🛡️</div>
            <h3 style="margin:0 0 0.5rem;font-size:1.1rem">Career Guard</h3>
            <p style="font-size:0.85rem; color:#6b7280; margin:0; line-height:1.6">
                Enter your profile, get an AI-powered placement risk score, discover weak areas, and receive a personalized roadmap with course & internship recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(168,85,247,0.08));">
        <h3 style="margin:0 0 1rem">✨ How to Get Started</h3>
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem;">
            <div>
                <div style="font-size:1.5rem">1️⃣</div>
                <p style="font-size:0.85rem; color:#9ca3af; margin:0.3rem 0 0">Pick a tool from the sidebar navigation</p>
            </div>
            <div>
                <div style="font-size:1.5rem">2️⃣</div>
                <p style="font-size:0.85rem; color:#9ca3af; margin:0.3rem 0 0">Enter your data — resume, questions, or profile</p>
            </div>
            <div>
                <div style="font-size:1.5rem">3️⃣</div>
                <p style="font-size:0.85rem; color:#9ca3af; margin:0.3rem 0 0">Get AI-powered insights and action plans instantly</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── RESUME ANALYZER ──────────────────────────────────────────────────────────
elif page == "📄  Resume Analyzer":
    st.markdown("""
    <div class="hero-banner" style="padding:1.75rem 2rem; margin-bottom:1.5rem;">
        <h1 style="font-size:1.8rem">📄 Resume Analyzer</h1>
        <p>ATS Score · Skill Gap · Role Prediction · Improvement Suggestions</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        from modules.resume.parser import extract_text_from_pdf
        from modules.resume.preprocessing import clean_text
        from modules.resume.skill_extractor import load_skills, extract_skills
        from modules.resume.similarity import calculate_similarity
        from modules.resume.skill_gap import find_missing_skills
        from modules.resume.suggestions import generate_suggestions
        from modules.resume.role_predictor import predict_role
        from modules.resume.resume_score import calculate_resume_score, get_rating
        import modules.resume.skill_category as skill_category_module

        def _resolve_categorize_skills():
            for fn_name in ("categorize_skills", "categorise_skills", "categorize_skill"):
                fn = getattr(skill_category_module, fn_name, None)
                if callable(fn):
                    return fn
            return lambda _skills: {}

        categorize_skills = _resolve_categorize_skills()
        SKILLS_PATH = os.path.join(BASE_DIR, "data", "skills.csv")

        col_upload, col_jd = st.columns([1, 1])

        with col_upload:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📎 Upload Resume")
            resume = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_jd:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📝 Job Description")
            job_desc = st.text_area("Paste the job description here...", height=120, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        if resume:
            with st.spinner("🔍 Analyzing your resume..."):
                raw_text = extract_text_from_pdf(resume)
                cleaned_text = clean_text(raw_text)

                # Load skills from correct path
                import pandas as pd_inner
                skills_df = pd_inner.read_csv(SKILLS_PATH)
                skills_list = skills_df["skill"].str.lower().tolist()

                detected_skills = extract_skills(cleaned_text, skills_list)
                predicted_role = predict_role(" ".join(detected_skills))
                category_data = categorize_skills(detected_skills)

            st.markdown("---")

            # ── Top Metrics ──
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("🎯 Skills Found", len(detected_skills))
            m2.metric("💼 Predicted Role", predicted_role)
            m3.metric("📂 Categories", len(category_data))
            m4.metric("📄 Status", "✅ Analyzed")

            # ── Skills & Categories ──
            col_skills, col_cats = st.columns(2)

            with col_skills:
                st.markdown("""
                <div class="section-header">
                    <h2>✅ Detected Skills</h2>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                if detected_skills:
                    pills = " ".join([f'<span class="skill-pill success">{s}</span>' for s in detected_skills])
                    st.markdown(pills, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-warning">⚠️ No skills detected in this resume.</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_cats:
                st.markdown("""
                <div class="section-header">
                    <h2>📊 Skill Categories</h2>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                if category_data:
                    for cat, cnt in category_data.items():
                        pct = min(cnt * 20, 100)
                        st.markdown(f"""
                        <div style="margin:0.5rem 0;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
                                <span style="font-size:0.85rem; color:#d1d5db;">{cat}</span>
                                <span style="font-size:0.8rem; color:#6b7280;">{cnt} skill(s)</span>
                            </div>
                            <div class="progress-bar-wrapper">
                                <div class="progress-bar-fill" style="width:{pct}%"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-info">ℹ️ No category data available.</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Skill Chart ──
            if detected_skills:
                st.markdown("""<div class="section-header"><h2>📈 Skill Distribution</h2></div>""", unsafe_allow_html=True)
                skill_df = pd.DataFrame(detected_skills, columns=["Skill"])
                skill_counts = skill_df.groupby("Skill").size().reset_index(name="Count")
                st.bar_chart(skill_counts.set_index("Skill"), color="#6366f1")

            # ── JD Analysis ──
            if job_desc:
                st.markdown("---")
                st.markdown("""<div class="section-header"><h2>🎯 Job Match Analysis</h2></div>""", unsafe_allow_html=True)

                with st.spinner("Calculating match..."):
                    job_skills = extract_skills(job_desc, skills_list)
                    missing_skills = find_missing_skills(detected_skills, job_skills)
                    ats_score = calculate_similarity(cleaned_text, job_desc)
                    resume_score = calculate_resume_score(ats_score, detected_skills)
                    rating = get_rating(resume_score)
                    suggestions = generate_suggestions(missing_skills)

                col_ats, col_strength = st.columns(2)

                with col_ats:
                    st.markdown('<div class="glass-card score-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-ring">{ats_score}%</div>', unsafe_allow_html=True)
                    st.markdown('<div class="score-label">ATS Match Score</div>', unsafe_allow_html=True)
                    color_class = "success" if ats_score >= 60 else "danger"
                    st.markdown(f"""
                    <div class="progress-bar-wrapper" style="margin-top:1rem">
                        <div class="progress-bar-fill {color_class}" style="width:{ats_score}%"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_strength:
                    st.markdown('<div class="glass-card score-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-ring">{resume_score}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-label">Resume Strength · {rating}</div>', unsafe_allow_html=True)
                    color_class2 = "success" if resume_score >= 60 else "danger"
                    st.markdown(f"""
                    <div class="progress-bar-wrapper" style="margin-top:1rem">
                        <div class="progress-bar-fill {color_class2}" style="width:{resume_score}%"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                col_miss, col_sugg = st.columns(2)

                with col_miss:
                    st.markdown("""<div class="section-header"><h2>❌ Missing Skills</h2></div>""", unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    if missing_skills:
                        pills = " ".join([f'<span class="skill-pill missing">{s}</span>' for s in missing_skills])
                        st.markdown(pills, unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="alert-success">🎉 Your resume covers all required skills!</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_sugg:
                    st.markdown("""<div class="section-header"><h2>💡 Suggestions</h2></div>""", unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    if suggestions:
                        for s in suggestions:
                            st.markdown(f'<div class="alert-info" style="margin:0.3rem 0; padding:0.5rem 0.75rem;">💡 {s}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="alert-success">✨ Your resume looks well-optimized!</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-info">📝 Paste a job description above to see ATS score, missing skills, and suggestions.</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:3rem;">
                <div style="font-size:3rem; margin-bottom:1rem">📄</div>
                <h3 style="color:#6b7280 !important; font-weight:500">Upload a PDF resume to begin analysis</h3>
                <p style="color:#4b5563; font-size:0.85rem">Supports all standard resume formats</p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Resume Analyzer error: {e}")
        st.exception(e)

# ─── INTERVIEW PREP ───────────────────────────────────────────────────────────
elif page == "🧠  Interview Prep":
    st.markdown("""
    <div class="hero-banner" style="padding:1.75rem 2rem; margin-bottom:1.5rem;">
        <h1 style="font-size:1.8rem">🧠 Interview Prep</h1>
        <p>Track DSA · Identify Weak Topics · Adaptive Mock Interview · Readiness Score</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        from modules.interview.analyzer import analyze_topics, get_weak_topics
        from modules.interview.recommender import recommend_topics
        from modules.interview.scorer import calculate_score, get_level
        from modules.interview.pattern_analyzer import analyze_patterns

        DATA_FILE = os.path.join(BASE_DIR, "data", "questions.csv")
        BANK_FILE = os.path.join(BASE_DIR, "data", "question_bank.csv")

        def load_data():
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
            else:
                df = pd.DataFrame(columns=["question", "topic", "difficulty", "status"])
            for col in df.columns:
                df[col] = df[col].astype(str).str.strip()
            return df

        def save_data(df):
            df.to_csv(DATA_FILE, index=False)

        df = load_data()

        # ── Session State ──
        for key, val in [
            ("current_question", None),
            ("start_time", None),
            ("interview_score", 0),
            ("questions_attempted", 0),
        ]:
            if key not in st.session_state:
                st.session_state[key] = val

        # ── Tabs ──
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Add Questions", "🎯 Mock Interview"])

        with tab1:
            if not df.empty:
                total = len(df)
                solved = len(df[df["status"].str.lower().isin(["solved", "accepted"])])
                unsolved = total - solved
                progress = solved / total if total > 0 else 0

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("📘 Total", total)
                c2.metric("✅ Solved", solved)
                c3.metric("❌ Unsolved", unsolved)
                c4.metric("📈 Progress", f"{round(progress*100,1)}%")

                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
                    <span style="font-size:0.85rem; color:#d1d5db;">Overall Progress</span>
                    <span style="font-size:0.85rem; color:#818cf8; font-weight:600;">{round(progress*100,1)}%</span>
                </div>
                <div class="progress-bar-wrapper">
                    <div class="progress-bar-fill {'success' if progress >= 0.6 else 'danger'}" style="width:{progress*100}%"></div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                topic_stats = analyze_topics(df)
                weak_topics = get_weak_topics(topic_stats)
                score = calculate_score(df, topic_stats)
                level = get_level(score)
                strong, weak, overfocus = analyze_patterns(topic_stats)

                col_l, col_r = st.columns(2)

                with col_l:
                    st.markdown("""<div class="section-header"><h2>📊 Topic Performance</h2></div>""", unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    for topic, stats in topic_stats.items():
                        pct = round(stats["accuracy"] * 100, 1)
                        color = "success" if pct >= 60 else "danger"
                        st.markdown(f"""
                        <div style="margin:0.6rem 0;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:0.2rem;">
                                <span style="font-size:0.85rem; color:#d1d5db;">{topic}</span>
                                <span style="font-size:0.78rem; color:#6b7280;">{stats['solved']}/{stats['total']} · {pct}%</span>
                            </div>
                            <div class="progress-bar-wrapper">
                                <div class="progress-bar-fill {color}" style="width:{pct}%"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_r:
                    st.markdown("""<div class="section-header"><h2>🏆 Readiness Score</h2></div>""", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="glass-card score-container">
                        <div class="score-ring">{score}</div>
                        <div class="score-label">{level}</div>
                        <div class="progress-bar-wrapper" style="margin-top:1rem">
                            <div class="progress-bar-fill {'success' if score >= 60 else 'danger'}" style="width:{score}%"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""<div class="section-header"><h2>🔍 Pattern Insights</h2></div>""", unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    if strong:
                        st.markdown(f'<div class="alert-success">💪 <strong>Strong:</strong> {", ".join(strong)}</div>', unsafe_allow_html=True)
                    if weak:
                        st.markdown(f'<div class="alert-warning">⚠️ <strong>Weak:</strong> {", ".join(weak)}</div>', unsafe_allow_html=True)
                    if overfocus:
                        st.markdown(f'<div class="alert-info">📌 <strong>Over-focused:</strong> {", ".join(overfocus)}</div>', unsafe_allow_html=True)
                    if not strong and not weak and not overfocus:
                        st.markdown('<div class="alert-success">🔥 Perfectly balanced across all topics!</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    if weak_topics:
                        recs = recommend_topics(weak_topics)
                        if recs:
                            st.markdown("""<div class="section-header"><h2>🎯 Recommendations</h2></div>""", unsafe_allow_html=True)
                            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                            for rec in recs:
                                st.markdown(f'<div class="alert-info" style="margin:0.3rem 0;">🎯 {rec}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="glass-card" style="text-align:center; padding:3rem;">
                    <div style="font-size:3rem;">📋</div>
                    <h3 style="color:#6b7280 !important; font-weight:500;">No questions yet</h3>
                    <p style="color:#4b5563; font-size:0.85rem">Head to the "Add Questions" tab to get started</p>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### ➕ Add a New Question")
            col_a, col_b = st.columns(2)
            with col_a:
                question = st.text_input("Question Name", placeholder="e.g. Two Sum")
                topic = st.selectbox("Topic", ["Array", "Linked List", "Tree", "Graph", "DP", "Stack", "Heap", "Sliding Window"])
            with col_b:
                difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
                status = st.selectbox("Status", ["Solved", "Unsolved"])

            if st.button("➕ Add Question", use_container_width=True):
                if question:
                    new_row = pd.DataFrame([[question, topic, difficulty, status]], columns=["question", "topic", "difficulty", "status"])
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.success("✅ Question added!")
                    st.rerun()
                else:
                    st.warning("Please enter a question name.")
            st.markdown('</div>', unsafe_allow_html=True)

            if not df.empty:
                st.markdown("""<div class="section-header"><h2>📋 Your Questions</h2></div>""", unsafe_allow_html=True)
                # Style the dataframe display
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "question": st.column_config.TextColumn("Question", width="large"),
                        "topic": st.column_config.TextColumn("Topic"),
                        "difficulty": st.column_config.TextColumn("Difficulty"),
                        "status": st.column_config.TextColumn("Status"),
                    }
                )

        with tab3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Adaptive Mock Interview")
            st.markdown('<p style="color:#6b7280; font-size:0.85rem;">Questions are selected from your weakest topics. 2 minute timer per question.</p>', unsafe_allow_html=True)

            if not df.empty:
                topic_stats_iv = analyze_topics(df)
                weak_topics_iv = get_weak_topics(topic_stats_iv)
                weakest = list(weak_topics_iv.keys())[0] if weak_topics_iv else random.choice(list(df["topic"].unique()))
                st.markdown(f'<div class="alert-info">🎯 Focus topic: <strong>{weakest}</strong></div>', unsafe_allow_html=True)

            if st.button("🚀 Start Next Question", use_container_width=True):
                if os.path.exists(BANK_FILE):
                    bank = pd.read_csv(BANK_FILE)
                    if not df.empty:
                        topic_stats_iv = analyze_topics(df)
                        weak_topics_iv = get_weak_topics(topic_stats_iv)
                        weakest = list(weak_topics_iv.keys())[0] if weak_topics_iv else None
                        if weakest:
                            filtered = bank[bank["topic"] == weakest]
                            if filtered.empty:
                                filtered = bank
                        else:
                            filtered = bank
                    else:
                        filtered = bank

                    if not filtered.empty:
                        q = filtered.sample(1).iloc[0].to_dict()
                        st.session_state.current_question = q
                        st.session_state.start_time = time.time()
                    else:
                        st.warning("No questions in bank.")
                else:
                    # Fallback sample question
                    sample_qs = [
                        {"question": "Given an array, find the two numbers that add to a target.", "topic": "Array", "difficulty": "Easy"},
                        {"question": "Reverse a linked list in-place.", "topic": "Linked List", "difficulty": "Medium"},
                        {"question": "Find the longest common subsequence.", "topic": "DP", "difficulty": "Hard"},
                    ]
                    st.session_state.current_question = random.choice(sample_qs)
                    st.session_state.start_time = time.time()

            st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.current_question:
                q = st.session_state.current_question
                elapsed = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
                remaining = max(0, 120 - elapsed)

                diff = q.get("difficulty", "Medium")
                diff_class = "tag-easy" if diff == "Easy" else ("tag-hard" if diff == "Hard" else "tag-medium")

                st.markdown(f"""
                <div class="question-box">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
                        <span style="font-size:0.8rem; color:#818cf8; font-weight:600; text-transform:uppercase;">📌 {q.get('topic','')}</span>
                        <span class="{diff_class}">{diff}</span>
                    </div>
                    <h3>{q.get('question','')}</h3>
                </div>
                """, unsafe_allow_html=True)

                timer_color = "#86efac" if remaining > 60 else ("#fcd34d" if remaining > 20 else "#fca5a5")
                st.markdown(f"""
                <div style="text-align:center; margin:1rem 0;">
                    <div style="font-size:3rem; font-weight:800; color:{timer_color}; line-height:1">{remaining}s</div>
                    <div style="font-size:0.8rem; color:#6b7280; margin-top:0.3rem">Time Remaining</div>
                </div>
                """, unsafe_allow_html=True)

                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button("✅ Solved!", use_container_width=True):
                        st.session_state.interview_score += 10
                        st.session_state.questions_attempted += 1
                        st.session_state.current_question = None
                        st.session_state.start_time = None
                        st.balloons()
                        st.rerun()
                with btn2:
                    if st.button("❌ Skip / Not Solved", use_container_width=True):
                        st.session_state.questions_attempted += 1
                        st.session_state.current_question = None
                        st.session_state.start_time = None
                        st.rerun()

                if remaining > 0 and st.session_state.start_time:
                    time.sleep(1)
                    st.rerun()

            # Scoreboard
            attempted = st.session_state.questions_attempted
            score_val = st.session_state.interview_score
            accuracy = round((score_val / (attempted * 10)) * 100, 1) if attempted else 0

            st.markdown("---")
            st.markdown("""<div class="section-header"><h2>📊 Session Performance</h2></div>""", unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            s1.metric("Questions Attempted", attempted)
            s2.metric("Score", score_val)
            s3.metric("Accuracy", f"{accuracy}%")

    except Exception as e:
        st.error(f"Interview Prep error: {e}")
        st.exception(e)

# ─── CAREER GUARD ─────────────────────────────────────────────────────────────
elif page == "🛡️  Career Guard":
    st.markdown("""
    <div class="hero-banner" style="padding:1.75rem 2rem; margin-bottom:1.5rem;">
        <h1 style="font-size:1.8rem">🛡️ Career Guard AI</h1>
        <p>Risk Score · Weak Areas · Personalized Roadmap · Courses & Internships</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        sys.path.insert(0, os.path.join(BASE_DIR, "ml"))
        from ml.career_logic import predict_risk, generate_roadmap, explain_risk
        from ml.live_recommender import recommend_live_courses, recommend_live_internships

        col_form, col_results = st.columns([1, 1.3], gap="large")

        with col_form:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Your Profile")

            role = st.selectbox("Target Role", ["Software Developer", "Web Developer", "Data Analyst", "ML Engineer"])

            st.markdown("---")
            st.markdown("**📊 Academic & Activity**")
            cgpa = st.slider("CGPA", 0.0, 10.0, 7.5, 0.1)
            study_hours = st.slider("Study Hours / Day", 0, 10, 3)
            dsa_count = st.number_input("DSA Problems Solved", 0, 500, 100)
            project_count = st.number_input("Projects Completed", 0, 20, 2)
            internship_attempts = st.number_input("Internship Attempts", 0, 10, 2)

            st.markdown("**🧠 Skill Levels (1–10)**")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                python_skill = st.slider("Python", 1, 10, 5)
                ml_skill = st.slider("ML", 1, 10, 4)
            with col_s2:
                web_skill = st.slider("Web Dev", 1, 10, 5)
                consistency = st.slider("Consistency", 1, 10, 5)

            c_demo, c_gen = st.columns(2)
            with c_demo:
                if st.button("⚡ Demo Data", use_container_width=True):
                    st.session_state["cg_demo"] = True
                    st.rerun()

            if st.session_state.get("cg_demo"):
                cgpa, study_hours, dsa_count = 7.5, 3, 120
                project_count, internship_attempts = 2, 3
                python_skill, ml_skill, web_skill, consistency = 6, 4, 5, 5

            with c_gen:
                generate = st.button("🚀 Analyze", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_results:
            if generate or st.session_state.get("cg_analyzed"):
                if generate:
                    st.session_state["cg_analyzed"] = True

                profile = {
                    "cgpa": cgpa, "study_hours": study_hours, "dsa_count": dsa_count,
                    "project_count": project_count, "internship_attempts": internship_attempts,
                    "python": python_skill, "ml": ml_skill, "web": web_skill,
                    "consistency": consistency, "role": role
                }

                with st.spinner("🤖 Running AI analysis..."):
                    risk_score, placement_prob, weak_areas = predict_risk(profile)
                    roadmap = generate_roadmap(weak_areas)
                    reasons = explain_risk(profile)

                # ── Score Cards ──
                r1, r2 = st.columns(2)
                with r1:
                    risk_color = "#fca5a5" if risk_score >= 60 else ("#fcd34d" if risk_score >= 30 else "#86efac")
                    st.markdown(f"""
                    <div class="glass-card score-container">
                        <div class="score-ring" style="background: linear-gradient(135deg, #ef4444, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{risk_score}%</div>
                        <div class="score-label">Career Risk Score</div>
                        <div class="progress-bar-wrapper" style="margin-top:0.75rem">
                            <div class="progress-bar-fill danger" style="width:{risk_score}%"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with r2:
                    st.markdown(f"""
                    <div class="glass-card score-container">
                        <div class="score-ring">{placement_prob}%</div>
                        <div class="score-label">Placement Probability</div>
                        <div class="progress-bar-wrapper" style="margin-top:0.75rem">
                            <div class="progress-bar-fill success" style="width:{placement_prob}%"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Verdict ──
                if risk_score < 30:
                    verdict_class, verdict_text = "alert-success", "🎉 Strong Profile — You're well-positioned for placement!"
                elif risk_score < 60:
                    verdict_class, verdict_text = "alert-warning", "⚠️ Moderate Risk — Some areas need attention."
                else:
                    verdict_class, verdict_text = "alert-danger", "🚨 High Risk — Immediate action recommended."

                st.markdown(f'<div class="{verdict_class}" style="font-weight:600">{verdict_text}</div>', unsafe_allow_html=True)

                # ── Weak Areas & Reasons ──
                col_wa, col_rr = st.columns(2)
                with col_wa:
                    st.markdown("""<div class="section-header"><h2>⚠️ Weak Areas</h2></div>""", unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    for area in weak_areas:
                        if area == "Strong Profile":
                            st.markdown(f'<div class="alert-success">✅ {area}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="alert-danger">🔸 {area}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_rr:
                    st.markdown("""<div class="section-header"><h2>📌 Risk Factors</h2></div>""", unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    for r in reasons:
                        st.markdown(f'<div class="alert-warning" style="margin:0.3rem 0; padding:0.5rem 0.75rem;">⚡ {r}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # ── Roadmap ──
                if roadmap:
                    st.markdown("""<div class="section-header"><h2>🛣️ Your Personalized Roadmap</h2></div>""", unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    for i, (area, details) in enumerate(roadmap.items()):
                        st.markdown(f"""
                        <div class="roadmap-step">
                            <div class="step-number">{i+1}</div>
                            <div class="step-content">
                                <div class="step-title">{area}</div>
                                <div class="step-weeks">⏱️ {details.get('weeks', '?')} weeks</div>
                                <div style="margin-top:0.4rem">
                                    {''.join([f'<span class="skill-pill">{t}</span>' for t in details.get('tasks',[])])}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # ── Courses ──
                st.markdown("""<div class="section-header"><h2>📚 Recommended Courses</h2></div>""", unsafe_allow_html=True)
                PROVIDER_ICONS = {
                    "coursera.org": "🎓", "udemy.com": "🎯", "nptel.ac.in": "🏛️",
                    "edx.org": "📘", "freecodecamp.org": "💻"
                }
                try:
                    courses = recommend_live_courses(weak_areas)
                    for c in courses[:4]:
                        icon = PROVIDER_ICONS.get(c.get("provider", ""), "📖")
                        url = c.get("url", "#")
                        link = f'<a href="{url}" target="_blank" style="color:#818cf8; font-size:0.75rem; text-decoration:none;">Open Course →</a>' if url != "#" else ""
                        st.markdown(f"""
                        <div class="course-card">
                            <div class="course-icon">{icon}</div>
                            <div class="course-info">
                                <h4>{c.get('name','Course')}</h4>
                                <p>{c.get('provider','').replace('www.','')} · {c.get('difficulty','')}</p>
                                {link}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    fallback_courses = [
                        {"name": "Python for Everybody", "provider": "coursera.org", "url": "https://coursera.org/specializations/python"},
                        {"name": "Data Structures & Algorithms", "provider": "udemy.com", "url": "https://udemy.com"},
                    ]
                    for c in fallback_courses:
                        st.markdown(f"""
                        <div class="course-card">
                            <div class="course-icon">🎓</div>
                            <div class="course-info">
                                <h4>{c['name']}</h4>
                                <p>{c['provider']}</p>
                                <a href="{c['url']}" target="_blank" style="color:#818cf8; font-size:0.75rem;">Open →</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # ── Internships ──
                st.markdown("""<div class="section-header"><h2>💼 Internship Opportunities</h2></div>""", unsafe_allow_html=True)
                try:
                    internships = recommend_live_internships(weak_areas)
                    for intern in internships[:3]:
                        url = intern.get("url", "#")
                        link = f'<a href="{url}" target="_blank" style="color:#818cf8; font-size:0.75rem; text-decoration:none;">Apply Here →</a>' if url != "#" else ""
                        st.markdown(f"""
                        <div class="course-card">
                            <div class="course-icon">🏢</div>
                            <div class="course-info">
                                <h4>{intern.get('title','Internship')}</h4>
                                <p>{intern.get('company','Company')} · {intern.get('domain','Tech')} · {intern.get('location','Remote')}</p>
                                {link}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    fallback_internships = [
                        {"title": "Python Developer Intern", "company": "TechStartup", "domain": "Python", "url": "https://internshala.com"},
                        {"title": "ML Research Intern", "company": "AILabs", "domain": "ML", "url": "https://internshala.com"},
                    ]
                    for i in fallback_internships:
                        st.markdown(f"""
                        <div class="course-card">
                            <div class="course-icon">🏢</div>
                            <div class="course-info">
                                <h4>{i['title']}</h4>
                                <p>{i['company']} · {i['domain']}</p>
                                <a href="{i['url']}" target="_blank" style="color:#818cf8; font-size:0.75rem;">Apply →</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="glass-card" style="text-align:center; padding:3rem; margin-top:1rem;">
                    <div style="font-size:3rem; margin-bottom:1rem">🛡️</div>
                    <h3 style="color:#6b7280 !important; font-weight:500">Fill your profile & click Analyze</h3>
                    <p style="color:#4b5563; font-size:0.85rem">Get your AI-powered career risk report in seconds</p>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Career Guard error: {e}")
        st.exception(e)
