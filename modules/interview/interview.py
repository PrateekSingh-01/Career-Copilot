import pandas as pd
import random
import os

def get_question(topic=None, difficulty=None):

    df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "question_bank.csv"))

    if topic:
        df = df[df["topic"] == topic]

    if difficulty:
        df = df[df["difficulty"] == difficulty]

    if df.empty:
        return None

    return df.sample(1).iloc[0].to_dict()