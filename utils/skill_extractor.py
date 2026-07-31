"""
==========================================================
AI Resume Analyzer
Skill Extraction Module
==========================================================

This module handles:
1. Loading Skills Database
2. Resume Skill Extraction
3. Skill Categorization
4. Skill Frequency Analysis

Author: Your Name
==========================================================
"""

import re
from collections import Counter

from utils.database import load_skills


# ==========================================================
# LOAD SKILLS DATABASE
# ==========================================================

def load_skill_database():
    """
    Load skills from the SQLite database.
    """

    skills_df = load_skills()

    if skills_df.empty:
        return []

    if "Skill_Name" not in skills_df.columns:
        raise ValueError(
            "Database must contain a 'Skill_Name' column."
        )

    return (
        skills_df["Skill_Name"]
        .dropna()
        .astype(str)
        .str.lower()
        .unique()
        .tolist()
    )


# ==========================================================
# EXTRACT SKILLS
# ==========================================================

def extract_skills(resume_text):
    """
    Extract skills from resume text.
    """

    if not resume_text:
        return []

    resume_text = resume_text.lower()

    database = load_skill_database()

    detected = set()

    for skill in database:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, resume_text):

            detected.add(skill)

    return sorted(detected)


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def extract_resume_skills(resume_text):
    """
    Wrapper for older modules.
    """

    return extract_skills(resume_text)


# ==========================================================
# SKILL FREQUENCY
# ==========================================================

def skill_frequency(skills):
    """
    Return frequency of detected skills.

    Parameters
    ----------
    skills : list

    Returns
    -------
    dict
    """

    if not skills:
        return {}

    return dict(Counter(skills))


# ==========================================================
# CATEGORIZE SKILLS
# ==========================================================

def categorize_skills(skills):
    """
    Categorize skills into domains.
    """

    categories = {

        "Programming": [
            "python",
            "java",
            "c",
            "c++",
            "r",
            "sql"
        ],

        "Machine Learning": [
            "machine learning",
            "deep learning",
            "tensorflow",
            "keras",
            "pytorch",
            "scikit-learn",
            "xgboost"
        ],

        "Data Analysis": [
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "statistics",
            "excel",
            "power bi",
            "tableau"
        ],

        "Database": [
            "mysql",
            "postgresql",
            "sqlite",
            "mongodb"
        ],

        "Cloud": [
            "aws",
            "azure",
            "gcp"
        ]

    }

    categorized = {}

    for category, skill_list in categories.items():

        categorized[category] = [

            skill

            for skill in skills

            if skill in skill_list

        ]

    return categorized


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    sample = """
    Python SQL Machine Learning
    Pandas Python Tableau
    """

    skills = extract_skills(sample)

    print("=" * 60)

    print("Detected Skills")

    print(skills)

    print("=" * 60)

    print("Frequency")

    print(skill_frequency(skills))

    print("=" * 60)

    print("Categories")

    print(categorize_skills(skills))