import joblib
import numpy as np
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Load Model Safely
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "risk_model.pkl")

model = joblib.load(MODEL_PATH)

# -------------------------------
# 1️⃣ Predict Career Risk
# -------------------------------
def predict_risk(profile):
    # Extract values
    cgpa = profile.get("cgpa", 0)
    study_hours = profile.get("study_hours", 0)
    dsa = profile.get("dsa_count", 0)
    projects = profile.get("project_count", 0)
    internships = profile.get("internship_attempts", 0)
    python = profile.get("python", 0)
    ml = profile.get("ml", 0)
    web = profile.get("web", 0)
    consistency = profile.get("consistency", 0)
    role = profile.get("role", "Software Developer")

    # -------------------------
    # ROLE BASED WEIGHTING
    # -------------------------
    if role == "ML Engineer":
        score = (
            python * 2 +
            ml * 3 +
            dsa * 0.05 +
            projects * 1.5 +
            consistency * 2 +
            study_hours * 1.5 +
            cgpa * 1.2
        )

    elif role == "Web Developer":
        score = (
            web * 3 +
            projects * 2 +
            dsa * 0.03 +
            consistency * 2 +
            study_hours * 1.5 +
            cgpa * 1.2
        )

    elif role == "Data Analyst":
        score = (
            python * 2 +
            ml * 1.5 +
            projects * 1.5 +
            consistency * 2 +
            study_hours * 1.5 +
            cgpa * 1.2
        )

    else:  # Software Developer
        score = (
            dsa * 0.06 +
            projects * 2 +
            consistency * 2 +
            study_hours * 1.5 +
            cgpa * 1.2 +
            python * 1.5
        )

    # Normalize score
    risk_score = max(0, 100 - int(score))
    placement_probability = 100 - risk_score

    # -------------------------
    # WEAK AREAS
    # -------------------------
    weak_areas = []

    if dsa < 100:
        weak_areas.append("DSA")
    if projects < 3:
        weak_areas.append("Projects")
    if consistency < 5:
        weak_areas.append("Consistency")
    if role == "ML Engineer" and ml < 5:
        weak_areas.append("Machine Learning")
    if role == "Web Developer" and web < 5:
        weak_areas.append("Web Development")

    if not weak_areas:
        weak_areas = ["Strong Profile"]

    return risk_score, placement_probability, weak_areas


# -------------------------------
# 2️⃣ Weak Area Detection
# -------------------------------
def find_weak_areas(profile):
    weak = []

    if profile["dsa_count"] < 100:
        weak.append("DSA")
    if profile["project_count"] < 2:
        weak.append("Projects")
    if profile["python"] < 5:
        weak.append("Python")
    if profile["ml"] < 5:
        weak.append("ML")
    if profile["web"] < 5:
        weak.append("Web")
    if profile["consistency"] < 5:
        weak.append("Consistency")

    if not weak:
        weak.append("None - Strong Profile")

    return weak


# -------------------------------
# 3️⃣ Roadmap Generator
# -------------------------------
def generate_roadmap(weak_areas):
    roadmap = {}

    if "None - Strong Profile" in weak_areas:
        roadmap["Career Growth"] = {
            "weeks": 6,
            "tasks": [
                "Advanced DSA",
                "System Design Basics",
                "Advanced ML Project",
                "Open Source Contribution"
            ],
            "courses": []
        }
        return roadmap

    if "DSA" in weak_areas:
        roadmap["DSA"] = {
            "weeks": 4,
            "tasks": ["Arrays", "Strings", "Linked List", "Stacks", "Queues"],
            "courses": []
        }

    if "Python" in weak_areas:
        roadmap["Python"] = {
            "weeks": 3,
            "tasks": ["Basics", "Functions", "OOP", "File Handling"],
            "courses": []
        }

    if "ML" in weak_areas:
        roadmap["ML"] = {
            "weeks": 6,
            "tasks": ["NumPy", "Pandas", "ML Basics", "Projects"],
            "courses": []
        }

    if "Web" in weak_areas:
        roadmap["Web"] = {
            "weeks": 5,
            "tasks": ["HTML", "CSS", "JavaScript", "React"],
            "courses": []
        }

    if "Projects" in weak_areas:
        roadmap["Projects"] = {
            "weeks": 4,
            "tasks": ["Mini Project", "API Project", "ML Project"],
            "courses": []
        }

    if "Consistency" in weak_areas:
        roadmap["Consistency"] = {
            "weeks": 2,
            "tasks": ["Daily Study Habit", "Pomodoro", "Weekly Review"],
            "courses": []
        }

    return roadmap


# -------------------------------
# 4️⃣ Internship Recommendation
# -------------------------------
def recommend_internships(user_profile):
    csv_path = os.path.join(BASE_DIR, "datasets", "internships.csv")
    df = pd.read_csv(csv_path)

    goal_domain = "ML" if user_profile["ml"] >= user_profile["web"] else "Web"
    df = df[df["domain"] == goal_domain]

    df["trust_score"] = 100
    df.loc[df["salary"] > 60000, "trust_score"] -= 30
    df.loc[df["company_age"] < 1, "trust_score"] -= 20
    df.loc[df["has_website"] == False, "trust_score"] -= 20

    df = df[df["trust_score"] >= 60]

    return df[["title", "company", "domain", "salary", "trust_score"]] \
             .head(5).to_dict(orient="records")


# -------------------------------
# 5️⃣ Explainable AI
# -------------------------------
def explain_risk(profile):
    reasons = []

    if profile["dsa_count"] < 100:
        reasons.append("Low DSA practice")
    if profile["project_count"] < 2:
        reasons.append("Not enough projects")
    if profile["consistency"] < 5:
        reasons.append("Low study consistency")
    if profile["ml"] < 5:
        reasons.append("Weak ML fundamentals")
    if profile["python"] < 5:
        reasons.append("Weak Python fundamentals")

    if not reasons:
        reasons.append("Strong overall profile")

    return reasons


# -------------------------------
# 6️⃣ AI Course Recommender
# -------------------------------
def recommend_courses(weak_areas):
    try:
        csv_path = os.path.join(BASE_DIR, "datasets", "courses.csv")
        df = pd.read_csv(csv_path)

        if df.empty:
            return []

        user_skills = " ".join(weak_areas).lower()
        course_skills = df["skills"].fillna("").str.lower().tolist()

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(course_skills + [user_skills])

        user_vector = vectors[-1]
        course_vectors = vectors[:-1]

        similarities = cosine_similarity(user_vector, course_vectors)[0]
        df["score"] = similarities

        top_courses = df.sort_values(by="score", ascending=False).head(3)

        return top_courses[["name", "provider", "difficulty", "score"]] \
               .to_dict(orient="records")

    except Exception as e:
        print("⚠️ Course recommender failed:", str(e))
        return []
