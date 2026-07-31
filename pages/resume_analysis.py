"""
=========================================================
AI Resume Analyzer
Resume Analysis Page
=========================================================

Features
--------
✔ Resume Upload
✔ PDF/DOCX Parsing
✔ Resume Cleaning
✔ Skill Extraction
✔ Session State Integration

Author : Your Name
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import os
from pathlib import Path

import streamlit as st

# ==========================================================
# BACKEND MODULES
# ==========================================================

from utils.parser import extract_text_from_resume
from utils.cleaner import clean_resume_text
from utils.skill_extractor import (
    extract_skills,
    skill_frequency,
)

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)

# ==========================================================
# PAGE FUNCTION
# ==========================================================

def resume_analysis_page():
    """
    Resume Analysis Page
    """

    st.title("📄 Resume Analysis")

    st.markdown(
        """
Upload your resume in **PDF** or **DOCX** format.

The system will automatically:

- 📄 Parse your resume
- 🧹 Clean extracted text
- 🧠 Extract technical skills
- 📊 Generate resume statistics
- 💾 Store everything for ATS, Job Matching,
  Salary Prediction and Interview Preparation
"""
    )

    st.divider()

    # ======================================================
    # FILE UPLOADER
    # ======================================================

    uploaded_file = st.file_uploader(
        "Choose Resume",
        type=["pdf", "docx"]
    )

    if uploaded_file is None:
        st.info("Upload a resume to begin analysis.")
        return

    # ======================================================
    # SAVE FILE
    # ======================================================

    file_path = UPLOAD_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully.")

    # ======================================================
    # PARSE RESUME
    # ======================================================

    with st.spinner("Parsing resume..."):

        try:

            resume_text = extract_text_from_resume(
                str(file_path)
            )

        except Exception as e:

            st.error(f"Resume parsing failed.\n\n{e}")

            return

    # ======================================================
    # CLEAN TEXT
    # ======================================================

    with st.spinner("Cleaning resume..."):

        try:

            cleaned_text = clean_resume_text(
                resume_text
            )

        except Exception as e:

            st.error(f"Cleaning failed.\n\n{e}")

            return

    # ======================================================
    # SKILL EXTRACTION
    # ======================================================

    with st.spinner("Extracting skills..."):

        try:

            skills = extract_skills(
                cleaned_text
            )

            skill_counts = skill_frequency(
                skills
            )

        except Exception as e:

            st.error(f"Skill extraction failed.\n\n{e}")

            return

    # ======================================================
    # STORE SESSION DATA
    # ======================================================

    st.session_state["resume_text"] = resume_text

    st.session_state["clean_resume"] = cleaned_text

    st.session_state["skills"] = skills

    st.session_state["skill_frequency"] = skill_counts

    st.session_state["uploaded_resume"] = str(file_path)

    # ======================================================
    # BASIC SUMMARY
    # ======================================================

    st.success("✅ Resume processed successfully!")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Characters",
            len(cleaned_text)
        )

    with col2:

        st.metric(
            "Words",
            len(cleaned_text.split())
        )

    with col3:

        st.metric(
            "Skills",
            len(skills)
        )

    st.divider()

    # ======================================================
    # RESUME PREVIEW
    # ======================================================

    with st.expander("📄 Resume Preview", expanded=False):

        st.text_area(
            "",
            resume_text,
            height=300
        )

    # ======================================================
    # EXTRACTED SKILLS
    # ======================================================

    st.subheader("🧠 Extracted Skills")

    if len(skills) == 0:

        st.warning("No skills detected.")

    else:

        st.write(", ".join(sorted(skills)))

    st.success(
        "Resume data has been saved for ATS analysis, "
        "Job Recommendation, Salary Prediction, and "
        "Interview Preparation."
    )
    # ======================================================
    # RESUME STATISTICS
    # ======================================================

    st.divider()

    st.subheader("📊 Resume Statistics")

    total_characters = len(cleaned_text)

    total_words = len(cleaned_text.split())

    total_lines = len(resume_text.split("\n"))

    unique_skills = len(set(skills))

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Characters",
            f"{total_characters:,}"
        )

    with c2:

        st.metric(
            "Words",
            f"{total_words:,}"
        )

    with c3:

        st.metric(
            "Lines",
            total_lines
        )

    with c4:

        st.metric(
            "Skills Found",
            unique_skills
        )

    # ======================================================
    # SKILL DASHBOARD
    # ======================================================

    st.divider()

    st.subheader("🧠 Skills Dashboard")

    if len(skills) == 0:

        st.warning("No skills detected in the uploaded resume.")

    else:

        skill_cols = st.columns(4)

        for index, skill in enumerate(sorted(skills)):

            with skill_cols[index % 4]:

                st.success(skill)

    # ======================================================
    # SKILL FREQUENCY TABLE
    # ======================================================

    st.divider()

    st.subheader("📈 Skill Frequency")

    if len(skill_counts) > 0:

        import pandas as pd

        frequency_df = pd.DataFrame(

            skill_counts.items(),

            columns=[

                "Skill",

                "Frequency"

            ]

        )

        frequency_df = frequency_df.sort_values(

            by="Frequency",

            ascending=False

        )

        st.dataframe(

            frequency_df,

            use_container_width=True,

            hide_index=True

        )

    # ======================================================
    # RAW RESUME
    # ======================================================

    st.divider()

    with st.expander(

        "📄 View Extracted Resume Text",

        expanded=False

    ):

        st.text_area(

            "Resume",

            value=resume_text,

            height=350

        )

    # ======================================================
    # CLEANED TEXT
    # ======================================================

    with st.expander(

        "🧹 View Cleaned Resume",

        expanded=False

    ):

        st.text_area(

            "Clean Resume",

            value=cleaned_text,

            height=350

        )

    # ======================================================
    # DOWNLOAD CLEANED RESUME
    # ======================================================

    st.divider()

    st.download_button(

        label="⬇ Download Cleaned Resume",

        data=cleaned_text,

        file_name="clean_resume.txt",

        mime="text/plain"

    )

    # ======================================================
    # NEXT MODULES
    # ======================================================

    st.success(
        """
        ✅ Resume analysis completed successfully.

        The extracted information has been stored in the session
        and is now available for:

        • ATS Report

        • Job Recommendation

        • Course Recommendation

        • Salary Prediction

        • Interview Preparation

        • AI Career Coach
        """
    )