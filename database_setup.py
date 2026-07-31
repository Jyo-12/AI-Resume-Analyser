import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# DATABASE LOCATION
# ==========================================================

DATABASE_PATH = Path("datasets/resume_analyzer.db")

# ==========================================================
# CSV FILES
# ==========================================================

csv_files = {
    "jobs": "datasets/jobs.csv",
    "skills": "datasets/skills.csv",
    "ats_keywords": "datasets/ats_keywords.csv",
    "courses": "datasets/courses.csv",
    "career_paths": "datasets/career_paths.csv",
    "certifications": "datasets/certifications.csv",
    "salary_data": "datasets/salary_data.csv",
    "interview_questions": "datasets/interview_questions.csv"
}

# ==========================================================
# CREATE DATABASE
# ==========================================================

conn = sqlite3.connect(DATABASE_PATH)

for table_name, csv_path in csv_files.items():

    print(f"Importing {table_name}...")

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"✓ {table_name}: {len(df)} rows")

conn.close()

print("\nDatabase created successfully!")
print(f"Location: {DATABASE_PATH}")