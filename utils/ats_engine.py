"""
==========================================================
AI Resume Analyzer
ATS Scoring Engine
==========================================================

This module handles:
1. Contact Information Detection
2. Resume Section Detection
3. ATS Score Calculation (Part 1)

Author: Your Name
==========================================================
"""

import re


# ==========================================================
# EXTRACT CONTACT INFORMATION
# ==========================================================

def extract_contact_info(resume_text):
    """
    Extract email, phone number, LinkedIn and GitHub links.

    Parameters
    ----------
    resume_text : str

    Returns
    -------
    dict
    """

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    phone_pattern = r"(?:\+91[- ]?)?[6-9]\d{9}"

    linkedin_pattern = r"(linkedin\.com\/in\/[A-Za-z0-9_-]+)"

    github_pattern = r"(github\.com\/[A-Za-z0-9_-]+)"

    email = re.search(email_pattern, resume_text)

    phone = re.search(phone_pattern, resume_text)

    linkedin = re.search(linkedin_pattern, resume_text.lower())

    github = re.search(github_pattern, resume_text.lower())

    return {

        "email": email.group() if email else None,

        "phone": phone.group() if phone else None,

        "linkedin": linkedin.group() if linkedin else None,

        "github": github.group() if github else None
    }


# ==========================================================
# CONTACT INFORMATION SCORE
# ==========================================================

def score_contact_information(contact_info):
    """
    Score contact information out of 10.

    Email      = 3
    Phone      = 3
    LinkedIn   = 2
    GitHub     = 2
    """

    score = 0

    if contact_info["email"]:
        score += 3

    if contact_info["phone"]:
        score += 3

    if contact_info["linkedin"]:
        score += 2

    if contact_info["github"]:
        score += 2

    return score


# ==========================================================
# RESUME SECTION SCORE
# ==========================================================

def score_resume_sections(resume_text):
    """
    Check whether important sections exist.

    Score out of 10.
    """

    text = resume_text.lower()

    sections = {

        "education": 2,

        "experience": 2,

        "skills": 2,

        "projects": 2,

        "certifications": 2
    }

    score = 0

    found_sections = []

    for section, marks in sections.items():

        if section in text:

            score += marks

            found_sections.append(section)

    return {

        "score": score,

        "found_sections": found_sections
    }
# ==========================================================
# SKILL SCORE
# ==========================================================

from utils.skill_extractor import extract_skills
from utils.database import load_ats_keywords


def score_skills(resume_text):
    """
    Score detected technical skills.

    Maximum Score = 20
    """

    detected_skills = extract_skills(resume_text)

    skill_count = len(detected_skills)

    score = min(skill_count, 20)

    return {

        "score": score,

        "detected_skills": detected_skills,

        "skill_count": skill_count

    }


# ==========================================================
# EXPERIENCE SCORE
# ==========================================================

def score_experience(resume_text):
    """
    Estimate experience score based on
    common experience keywords.

    Maximum Score = 20
    """

    text = resume_text.lower()

    keywords = [

        "experience",

        "worked",

        "internship",

        "intern",

        "employment",

        "developer",

        "engineer",

        "analyst"

    ]

    matches = 0

    for keyword in keywords:

        if keyword in text:
            matches += 1

    score = min(matches * 2.5, 20)

    return {

        "score": round(score),

        "matches": matches

    }


# ==========================================================
# PROJECT SCORE
# ==========================================================

def score_projects(resume_text):
    """
    Score projects section.

    Maximum Score = 15
    """

    text = resume_text.lower()

    keywords = [

        "project",

        "developed",

        "built",

        "implemented",

        "designed",

        "created"

    ]

    matches = 0

    for keyword in keywords:

        if keyword in text:
            matches += 1

    score = min(matches * 3, 15)

    return {

        "score": round(score),

        "matches": matches

    }


# ==========================================================
# CERTIFICATION SCORE
# ==========================================================

def score_certifications(resume_text):
    """
    Score certifications.

    Maximum Score = 5
    """

    text = resume_text.lower()

    keywords = [

        "certification",

        "certificate",

        "certified",

        "ibm",

        "google",

        "microsoft",

        "coursera",

        "udemy"

    ]

    matches = 0

    for keyword in keywords:

        if keyword in text:
            matches += 1

    score = min(matches, 5)

    return {

        "score": score,

        "matches": matches

    }


# ==========================================================
# ATS KEYWORD SCORE
# ==========================================================

def score_keywords(resume_text):
    """
    Compare resume against ATS keyword database.

    Maximum Score = 10
    """

    ats_df = load_ats_keywords()

    # Change column name if required
    keyword_column = "Keyword"

    keywords = (

        ats_df[keyword_column]

        .dropna()

        .astype(str)

        .str.lower()

        .tolist()

    )

    matched_keywords = []

    text = resume_text.lower()

    for keyword in keywords:

        if keyword in text:
            matched_keywords.append(keyword)

    total_keywords = len(keywords)

    matched = len(matched_keywords)

    score = round((matched / total_keywords) * 10) if total_keywords else 0

    return {

        "score": score,

        "matched_keywords": matched_keywords,

        "matched_count": matched,

        "total_keywords": total_keywords

    }
# ==========================================================
# GENERATE STRENGTHS
# ==========================================================

def generate_strengths(report):
    """
    Generate resume strengths based on ATS scores.
    """

    strengths = []

    if report["contact_score"] >= 8:
        strengths.append("Complete contact information.")

    if report["skill_score"] >= 15:
        strengths.append("Strong technical skill set.")

    if report["experience_score"] >= 15:
        strengths.append("Good experience profile.")

    if report["project_score"] >= 10:
        strengths.append("Projects strengthen the resume.")

    if report["certification_score"] >= 3:
        strengths.append("Relevant certifications included.")

    if report["keyword_score"] >= 7:
        strengths.append("Good ATS keyword optimization.")

    if report["section_score"] >= 8:
        strengths.append("Resume contains all major sections.")

    if not strengths:
        strengths.append("Resume has a good foundation for improvement.")

    return strengths


# ==========================================================
# GENERATE IMPROVEMENTS
# ==========================================================

def generate_improvement_suggestions(report):
    """
    Generate improvement suggestions.
    """

    suggestions = []

    if report["contact_score"] < 10:
        suggestions.append(
            "Add missing contact details such as LinkedIn or GitHub."
        )

    if report["section_score"] < 10:
        suggestions.append(
            "Include all standard resume sections."
        )

    if report["skill_score"] < 15:
        suggestions.append(
            "Add more relevant technical skills."
        )

    if report["experience_score"] < 15:
        suggestions.append(
            "Describe work experience with measurable achievements."
        )

    if report["project_score"] < 10:
        suggestions.append(
            "Include more practical or impactful projects."
        )

    if report["certification_score"] < 3:
        suggestions.append(
            "Add industry-recognized certifications."
        )

    if report["keyword_score"] < 7:
        suggestions.append(
            "Increase ATS keywords related to your target role."
        )

    return suggestions


# ==========================================================
# CALCULATE ATS SCORE
# ==========================================================

def calculate_ats_score(resume_text):
    """
    Calculate complete ATS score.

    Returns
    -------
    dict
    """

    contact_info = extract_contact_info(resume_text)

    contact_score = score_contact_information(contact_info)

    section_result = score_resume_sections(resume_text)

    skill_result = score_skills(resume_text)

    experience_result = score_experience(resume_text)

    project_result = score_projects(resume_text)

    certification_result = score_certifications(resume_text)

    keyword_result = score_keywords(resume_text)

    # Education score (derived from section detection)
    education_score = (
        10 if "education" in section_result["found_sections"] else 0
    )

    overall_score = (

        contact_score +

        section_result["score"] +

        skill_result["score"] +

        experience_result["score"] +

        project_result["score"] +

        education_score +

        certification_result["score"] +

        keyword_result["score"]

    )

    overall_score = min(round(overall_score), 100)

    report = {

        "overall_score": overall_score,

        "contact_score": contact_score,

        "section_score": section_result["score"],

        "education_score": education_score,

        "skill_score": skill_result["score"],

        "experience_score": experience_result["score"],

        "project_score": project_result["score"],

        "certification_score": certification_result["score"],

        "keyword_score": keyword_result["score"],

        "contact_info": contact_info,

        "found_sections": section_result["found_sections"],

        "detected_skills": skill_result["detected_skills"],

        "matched_keywords": keyword_result["matched_keywords"]

    }

    report["strengths"] = generate_strengths(report)

    report["improvements"] = generate_improvement_suggestions(report)

    return report


# ==========================================================
# GENERATE ATS REPORT
# ==========================================================

def generate_ats_report(resume_text):
    """
    Generate complete ATS report.
    """

    return calculate_ats_score(resume_text)