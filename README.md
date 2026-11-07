# 🚀 Career Copilot

> **Three powerful AI career tools — unified into one polished platform.**

CareerAI Suite merges three standalone projects into a single, beautifully designed Streamlit application with a modern dark glassmorphism UI.

---

## 🧩 What's Inside

| Module | Original Repo | Features |
|--------|--------------|----------|
| 📄 **Resume Analyzer** | `ai-resume-analyzer` | PDF parsing · Skill extraction · ATS score · Role prediction · Skill gap · Suggestions |
| 🧠 **Interview Prep** | `ai-interview-assistant` | DSA tracker · Weak topic detection · Pattern analysis · Adaptive mock interview · Timer |
| 🛡️ **Career Guard** | `career-guard-ai` | Risk score · Placement probability · Weak area detection · Personalized roadmap · Course & internship recommendations |

---

## 🖥️ UI Highlights

- **Dark glassmorphism** design with purple/indigo gradient theme
- **Score rings** with animated gradient text
- **Skill pills** (green = found, red = missing)
- **Animated progress bars** per category/topic
- **Card-based layout** with glass blur effect
- **Tabbed interface** for Interview Prep
- **Sidebar navigation** across all three tools
- **Streamlit native theming** via `.streamlit/config.toml`

---

## 📁 Project Structure

```
career-ai-suite/
├── app.py                    ← Main unified application
├── requirements.txt
├── .streamlit/
│   └── config.toml           ← Dark theme config
├── modules/
│   ├── resume/               ← Resume Analyzer modules
│   │   ├── parser.py
│   │   ├── preprocessing.py
│   │   ├── skill_extractor.py
│   │   ├── skill_category.py
│   │   ├── skill_gap.py
│   │   ├── suggestions.py
│   │   ├── similarity.py
│   │   ├── role_predictor.py
│   │   └── resume_score.py
│   └── interview/            ← Interview Prep modules
│       ├── analyzer.py
│       ├── scorer.py
│       ├── recommender.py
│       ├── pattern_analyzer.py
│       └── interview.py
├── ml/                       ← Career Guard AI
│   ├── career_logic.py
│   ├── live_recommender.py
│   └── risk_model.pkl
└── data/
    ├── skills.csv            ← 20 tech skills
    ├── question_bank.csv     ← 27 DSA questions
    ├── questions.csv         ← User's tracked questions (auto-saved)
    ├── courses.csv           ← Course dataset
    └── internships.csv       ← Internship dataset
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/your-username/career-ai-suite.git
cd career-ai-suite
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🔧 Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
pdfplumber>=0.10.0
scikit-learn>=1.3.0
joblib>=1.3.0
duckduckgo-search>=5.0.0
numpy>=1.24.0
```

---

## 📄 Resume Analyzer — How to Use

1. Navigate to **📄 Resume Analyzer** in the sidebar
2. Upload your resume as a **PDF**
3. (Optional) Paste a **job description** to get:
   - ATS Match Score
   - Missing skills
   - Resume Strength Score
   - Improvement suggestions

---

## 🧠 Interview Prep — How to Use

1. Navigate to **🧠 Interview Prep**
2. Go to **Add Questions** tab → add your solved/unsolved DSA problems
3. Go to **Dashboard** tab → see topic performance, readiness score, and pattern insights
4. Go to **Mock Interview** tab → start an adaptive timed interview session

---

## 🛡️ Career Guard — How to Use

1. Navigate to **🛡️ Career Guard**
2. Select your **Target Role**
3. Fill in your academic profile (CGPA, study hours, DSA count, skills)
4. Click **🚀 Analyze** to get:
   - Career Risk Score
   - Placement Probability
   - Weak areas & risk factors
   - Personalized roadmap
   - Recommended courses & internships

---

## 🤝 Credits

Built by merging three projects by [@PrateekSingh-01](https://github.com/PrateekSingh-01):
- [ai-resume-analyzer](https://github.com/PrateekSingh-01/ai-resume-analyzer)
- [ai-interview-assistant](https://github.com/PrateekSingh-01/ai-interview-assistant)
- [career-guard-ai](https://github.com/PrateekSingh-01/career-guard-ai)

---

## 📜 License

MIT License — feel free to use, modify, and distribute.
