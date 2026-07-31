"""
==========================================================
AI Resume Analyzer
Database Module
==========================================================

Handles SQLite database connections and loading all tables.

Tables Supported
----------------
✓ skills
✓ jobs
✓ ats_keywords
✓ courses
✓ career_paths
✓ certifications
✓ salary_data
✓ interview_questions

Author: Your Name
==========================================================
"""

import sqlite3
from pathlib import Path
import pandas as pd


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_PATH = Path("datasets/resume_analyzer.db")


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def connect_db():
    """
    Create and return a SQLite database connection.
    """

    if not DATABASE_PATH.exists():

        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    return sqlite3.connect(DATABASE_PATH)


# ==========================================================
# GENERIC TABLE LOADER
# ==========================================================

def load_table(table_name):
    """
    Load any database table into a pandas DataFrame.
    """

    connection = connect_db()

    try:

        dataframe = pd.read_sql_query(

            f"SELECT * FROM {table_name}",

            connection

        )

    finally:

        connection.close()

    return dataframe


# ==========================================================
# LOAD SKILLS
# ==========================================================

def load_skills():

    return load_table("skills")


# ==========================================================
# LOAD JOBS
# ==========================================================

def load_jobs():

    return load_table("jobs")


# ==========================================================
# LOAD ATS KEYWORDS
# ==========================================================

def load_ats_keywords():

    return load_table("ats_keywords")


# ==========================================================
# LOAD COURSES
# ==========================================================

def load_courses():

    return load_table("courses")


# ==========================================================
# LOAD CAREER PATHS
# ==========================================================

def load_career_paths():

    return load_table("career_paths")


# ==========================================================
# LOAD CERTIFICATIONS
# ==========================================================

def load_certifications():

    return load_table("certifications")


# ==========================================================
# LOAD SALARY DATA
# ==========================================================

def load_salary_data():

    return load_table("salary_data")


# ==========================================================
# LOAD INTERVIEW QUESTIONS
# ==========================================================

def load_interview_questions():

    return load_table("interview_questions")


# ==========================================================
# DATABASE INFORMATION
# ==========================================================

def list_tables():
    """
    Return all database tables.
    """

    connection = connect_db()

    try:

        query = """

        SELECT name

        FROM sqlite_master

        WHERE type='table'

        ORDER BY name

        """

        tables = pd.read_sql_query(

            query,

            connection

        )

    finally:

        connection.close()

    return tables


# ==========================================================
# TABLE EXISTS
# ==========================================================

def table_exists(table_name):
    """
    Check if a table exists.
    """

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(

        """

        SELECT name

        FROM sqlite_master

        WHERE type='table'

        AND name=?

        """,

        (table_name,)

    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

def database_summary():
    """
    Return the number of rows in every table.
    """

    tables = [

        "skills",

        "jobs",

        "ats_keywords",

        "courses",

        "career_paths",

        "certifications",

        "salary_data",

        "interview_questions"

    ]

    summary = {}

    for table in tables:

        if table_exists(table):

            summary[table] = len(

                load_table(table)

            )

        else:

            summary[table] = "Not Found"

    return summary


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("DATABASE SUMMARY")

    print("=" * 60)

    print(database_summary())

    print("\nDATABASE TABLES")

    print("=" * 60)

    print(list_tables())