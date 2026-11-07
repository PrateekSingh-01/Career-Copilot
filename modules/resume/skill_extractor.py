import pandas as pd
import os

def load_skills(skills_path=None):
    if skills_path is None:
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        skills_path = os.path.join(base, "data", "skills.csv")
    skills = pd.read_csv(skills_path)
    return skills["skill"].str.lower().tolist()


def extract_skills(text, skills_list):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))