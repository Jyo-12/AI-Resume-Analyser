"""
=========================================================
AI Resume Analyzer & Career Guidance System
=========================================================

Main Streamlit Application

Features
--------
✔ Resume Analysis
✔ ATS Score
✔ Job Recommendation
✔ Course Recommendation
✔ Salary Prediction
✔ Interview Preparation
✔ AI Career Coach

Author : Your Name
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import os
from pathlib import Path

import streamlit as st

# ----------------------------------------------------------
# Page Imports
# ----------------------------------------------------------

from pages.resume_analysis import resume_analysis_page
from pages.ats_report import ats_report_page
from pages.job_recommendation import job_recommendation_page
from pages.course_recommendation import course_recommendation_page
from pages.salary_prediction import salary_prediction_page
from pages.interview_preparation import interview_preparation_page


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(

    page_title="AI Resume Analyzer",

    page_icon="📄",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploads"

REPORT_DIR = BASE_DIR / "reports"

ASSET_DIR = BASE_DIR / "assets"

DATASET_DIR = BASE_DIR / "datasets"

# ==========================================================
# CREATE DIRECTORIES
# ==========================================================

for folder in [

    UPLOAD_DIR,

    REPORT_DIR,

]:

    folder.mkdir(

        exist_ok=True

    )

# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULT_SESSION = {

    "resume_text": "",

    "resume_data": {},

    "skills": [],

    "ats_score": 0,

    "job_recommendations": None,

    "course_recommendations": None,

    "salary_prediction": None,

    "interview_questions": None,

    "career_chat": []

}

for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================================
# LOAD CUSTOM CSS
# ==========================================================

css_file = ASSET_DIR / "styles.css"

if css_file.exists():

    with open(css_file, "r", encoding="utf-8") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True

        )
# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style='text-align:center;color:#4CAF50;'>
            📄 AI Resume Analyzer
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    selected_page = st.radio(

        "Navigation",

        [

            "🏠 Home",

            "📄 Resume Analysis",

            "🎯 ATS Report",

            "💼 Job Recommendations",

            "📚 Course Recommendations",

            "💰 Salary Prediction",

            "🎤 Interview Preparation",

            "🤖 AI Career Coach"

        ]

    )

    st.markdown("---")

    st.caption("Version 1.0")

    st.caption("Built using Streamlit + SQLite + AI")

# ==========================================================
# HOME PAGE
# ==========================================================

if selected_page == "🏠 Home":

    st.title("🚀 AI Resume Analyzer & Career Guidance System")

    st.markdown(
        """
        Welcome to your **AI-powered career assistant**.

        This platform helps you analyze your resume,
        improve your ATS score, discover suitable jobs,
        predict salary, prepare for interviews,
        and receive personalized career guidance.
        """
    )

    st.divider()

    # ------------------------------------------------------
    # Statistics Cards
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Skills Extracted",

            len(st.session_state["skills"])

        )

    with col2:

        st.metric(

            "ATS Score",

            f'{st.session_state["ats_score"]}%'

        )

    with col3:

        jobs = st.session_state["job_recommendations"]

        total_jobs = 0 if jobs is None else len(jobs)

        st.metric(

            "Recommended Jobs",

            total_jobs

        )

    with col4:

        courses = st.session_state["course_recommendations"]

        total_courses = 0 if courses is None else len(courses)

        st.metric(

            "Courses",

            total_courses

        )

    st.divider()

    # ------------------------------------------------------
    # Features
    # ------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            """
            ### 📄 Resume Analysis

            • Resume Parsing

            • Skill Extraction

            • Contact Information

            • Education Detection

            • Experience Extraction
            """
        )

        st.success(
            """
            ### 🎯 ATS Report

            • ATS Score

            • Missing Keywords

            • Resume Suggestions

            • Improvement Tips
            """
        )

        st.warning(
            """
            ### 💼 Job Recommendation

            • AI Matching

            • Skill Match %

            • Missing Skills

            • Experience Match
            """
        )

    with c2:

        st.info(
            """
            ### 📚 Course Recommendation

            • Personalized Courses

            • Learning Roadmap

            • Certifications

            • Skill Development
            """
        )

        st.success(
            """
            ### 💰 Salary Prediction

            • Salary Estimation

            • Salary Growth

            • Location Comparison

            • Company Analysis
            """
        )

        st.warning(
            """
            ### 🎤 Interview Preparation

            • Mock Interview

            • Technical Questions

            • Readiness Score

            • Weak Skill Detection
            """
        )

    st.divider()

    st.subheader("🤖 AI Career Coach")

    st.write(

        "Receive personalized career guidance, resume feedback, "
        "learning roadmap, interview strategies, and job recommendations "
        "using Artificial Intelligence."

    )

    st.success("Upload your resume from the Resume Analysis page to begin.")
# ==========================================================
# PAGE ROUTING
# ==========================================================

elif selected_page == "📄 Resume Analysis":

    resume_analysis_page()

elif selected_page == "🎯 ATS Report":

    ats_report_page()

elif selected_page == "💼 Job Recommendations":

    job_recommendation_page()

elif selected_page == "📚 Course Recommendations":

    course_recommendation_page()

elif selected_page == "💰 Salary Prediction":

    salary_prediction_page()

elif selected_page == "🎤 Interview Preparation":

    interview_preparation_page()

