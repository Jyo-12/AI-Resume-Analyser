"""
==============================================================
AI Resume Analyzer
Job Recommendation Engine (Version 2.0)

Author : Your Name

Description
-----------
This module provides an intelligent job recommendation engine.

Features
--------
✓ Load Jobs Database
✓ Text Normalization
✓ Skill Preprocessing
✓ Smart Skill Matching
✓ Weighted Recommendation Engine
✓ Experience Matching
✓ Education Matching
✓ Recommendation Ranking
✓ Career Advice Generator

==============================================================
"""

import re
from typing import List, Dict, Tuple

import pandas as pd

from utils.database import load_jobs
from utils.skill_extractor import extract_skills


# ==========================================================
# CONFIGURATION
# ==========================================================

REQUIRED_SKILL_WEIGHT = 0.80
PREFERRED_SKILL_WEIGHT = 0.20

EXPERIENCE_BONUS = 5
EDUCATION_BONUS = 5
DESCRIPTION_BONUS = 5

MAX_MATCH_SCORE = 100


# ==========================================================
# LOAD JOB DATABASE
# ==========================================================

_jobs_cache = None


def load_job_database() -> pd.DataFrame:
    """
    Load the jobs database only once.

    Returns
    -------
    pandas.DataFrame
    """

    global _jobs_cache

    if _jobs_cache is None:
        _jobs_cache = load_jobs()

    return _jobs_cache.copy()


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(text: str) -> str:
    """
    Normalize text for comparisons.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# PREPROCESS SKILLS
# ==========================================================

def preprocess_job_skills(skill_text) -> List[str]:
    """
    Convert skills into a clean list.

    Supports separators:
        ,
        ;
        |
        /
        newline

    Example

    Python; SQL | Machine Learning

    becomes

    [
        "python",
        "sql",
        "machine learning"
    ]
    """

    if pd.isna(skill_text):
        return []

    skill_text = normalize_text(skill_text)

    skill_text = re.sub(r"[;|/\n]", ",", skill_text)

    skills = []

    for skill in skill_text.split(","):

        skill = skill.strip()

        if skill:

            skills.append(skill)

    return sorted(list(set(skills)))


# ==========================================================
# JOB DESCRIPTION SKILLS
# ==========================================================

def extract_description_skills(description: str) -> List[str]:
    """
    Extract skills from job description.

    Uses the same NLP skill extractor
    used for resumes.
    """

    if pd.isna(description):
        return []

    return extract_skills(str(description))


# ==========================================================
# SET OPERATIONS
# ==========================================================

def matched_skills(
    candidate_skills: List[str],
    job_skills: List[str]
) -> List[str]:
    """
    Return matched skills.
    """

    candidate = {

        normalize_text(skill)

        for skill in candidate_skills

    }

    job = {

        normalize_text(skill)

        for skill in job_skills

    }

    return sorted(candidate.intersection(job))


def missing_skills(
    candidate_skills: List[str],
    job_skills: List[str]
) -> List[str]:
    """
    Return missing skills.
    """

    candidate = {

        normalize_text(skill)

        for skill in candidate_skills

    }

    job = {

        normalize_text(skill)

        for skill in job_skills

    }

    return sorted(job.difference(candidate))


# ==========================================================
# BASIC MATCH SCORE
# ==========================================================

def skill_match_percentage(
    candidate_skills: List[str],
    job_skills: List[str]
) -> float:
    """
    Calculate percentage of matched skills.
    """

    if len(job_skills) == 0:
        return 0.0

    matched = matched_skills(
        candidate_skills,
        job_skills
    )

    percentage = (

        len(matched)

        / len(job_skills)

    ) * 100

    return round(percentage, 2)


# ==========================================================
# CONFIDENCE LEVEL
# ==========================================================

def confidence_level(score: float) -> str:
    """
    Convert score into confidence label.
    """

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Strong"

    if score >= 60:
        return "Moderate"

    if score >= 40:
        return "Weak"

    return "Poor"
# ==========================================================
# REQUIRED SKILL MATCH
# ==========================================================

def required_skill_score(
    candidate_skills: List[str],
    required_skills: List[str]
) -> float:
    """
    Calculate required skill score.
    """

    return skill_match_percentage(
        candidate_skills,
        required_skills
    )


# ==========================================================
# PREFERRED SKILL MATCH
# ==========================================================

def preferred_skill_score(
    candidate_skills: List[str],
    preferred_skills: List[str]
) -> float:
    """
    Calculate preferred skill score.
    """

    return skill_match_percentage(
        candidate_skills,
        preferred_skills
    )


# ==========================================================
# EXPERIENCE MATCH
# ==========================================================

def experience_score(
    candidate_experience: int,
    required_experience
) -> int:
    """
    Compare candidate experience with
    job experience requirement.

    Returns
    -------
    Bonus score
    """

    if pd.isna(required_experience):
        return EXPERIENCE_BONUS

    text = normalize_text(required_experience)

    numbers = re.findall(r"\d+", text)

    if len(numbers) == 0:
        return EXPERIENCE_BONUS

    required_years = int(numbers[0])

    if candidate_experience >= required_years:
        return EXPERIENCE_BONUS

    if candidate_experience >= max(required_years - 1, 0):
        return EXPERIENCE_BONUS // 2

    return 0


# ==========================================================
# EDUCATION MATCH
# ==========================================================

def education_score(
    candidate_education: str,
    required_education: str
) -> int:
    """
    Compare education levels.
    """

    if not candidate_education:
        return 0

    if pd.isna(required_education):
        return EDUCATION_BONUS

    candidate = normalize_text(candidate_education)

    required = normalize_text(required_education)

    if candidate in required:

        return EDUCATION_BONUS

    if required in candidate:

        return EDUCATION_BONUS

    return 0


# ==========================================================
# DESCRIPTION BONUS
# ==========================================================

def description_bonus(
    candidate_skills: List[str],
    description: str
) -> int:
    """
    Give bonus if resume skills
    appear inside the job description.
    """

    description_skills = extract_description_skills(
        description
    )

    score = skill_match_percentage(
        candidate_skills,
        description_skills
    )

    if score >= 80:
        return DESCRIPTION_BONUS

    if score >= 50:
        return DESCRIPTION_BONUS // 2

    return 0


# ==========================================================
# WEIGHTED MATCH SCORE
# ==========================================================

def weighted_match_score(
    candidate_skills: List[str],
    required_skills: List[str],
    preferred_skills: List[str],
    candidate_experience: int = 0,
    required_experience=None,
    candidate_education: str = "",
    required_education: str = "",
    job_description: str = ""
) -> Dict:
    """
    Calculate overall job match score.
    """

    required_score = required_skill_score(
        candidate_skills,
        required_skills
    )

    preferred_score = preferred_skill_score(
        candidate_skills,
        preferred_skills
    )

    weighted_score = (

        required_score * REQUIRED_SKILL_WEIGHT

        +

        preferred_score * PREFERRED_SKILL_WEIGHT

    )

    exp_bonus = experience_score(
        candidate_experience,
        required_experience
    )

    edu_bonus = education_score(
        candidate_education,
        required_education
    )

    desc_bonus = description_bonus(
        candidate_skills,
        job_description
    )

    final_score = (

        weighted_score

        + exp_bonus

        + edu_bonus

        + desc_bonus

    )

    final_score = min(
        MAX_MATCH_SCORE,
        round(final_score, 2)
    )

    return {

        "required_score": round(required_score, 2),

        "preferred_score": round(preferred_score, 2),

        "experience_bonus": exp_bonus,

        "education_bonus": edu_bonus,

        "description_bonus": desc_bonus,

        "overall_score": final_score,

        "confidence": confidence_level(final_score)

    }


# ==========================================================
# RECOMMENDATION REASON
# ==========================================================

def recommendation_reason(
    matched_required: List[str],
    matched_preferred: List[str],
    missing_required: List[str]
) -> List[str]:
    """
    Generate human-readable reasons
    for recommendation.
    """

    reasons = []

    if matched_required:

        reasons.append(
            f"Matched {len(matched_required)} required skills."
        )

    if matched_preferred:

        reasons.append(
            f"Matched {len(matched_preferred)} preferred skills."
        )

    if missing_required:

        reasons.append(
            f"{len(missing_required)} required skills can still be improved."
        )

    if len(reasons) == 0:

        reasons.append(
            "Limited skill overlap with this role."
        )

    return reasons
# ==========================================================
# RECOMMEND JOBS
# ==========================================================

def recommend_jobs(
    candidate_skills: List[str],
    candidate_experience: int = 0,
    candidate_education: str = "",
    top_n: int = 10
) -> List[Dict]:
    """
    Recommend the best matching jobs.
    """

    jobs_df = load_job_database()

    recommendations = []

    for _, row in jobs_df.iterrows():

        required_skills = preprocess_job_skills(
            row["Required_Skills"]
        )

        preferred_skills = preprocess_job_skills(
            row["Preferred_Skills"]
        )

        score = weighted_match_score(
            candidate_skills=candidate_skills,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            candidate_experience=candidate_experience,
            required_experience=row["Experience"],
            candidate_education=candidate_education,
            required_education=row["Education"],
            job_description=row["Job_Description"]
        )

        matched_required = matched_skills(
            candidate_skills,
            required_skills
        )

        matched_preferred = matched_skills(
            candidate_skills,
            preferred_skills
        )

        missing_required = missing_skills(
            candidate_skills,
            required_skills
        )

        missing_preferred = missing_skills(
            candidate_skills,
            preferred_skills
        )

        recommendations.append({

            "job_id": row["Job_ID"],

            "job_title": row["Job_Title"],

            "company": row["Company"],

            "location": row["Location"],

            "salary": row["Salary"],

            "experience": row["Experience"],

            "education": row["Education"],

            "employment_type": row["Employment_Type"],

            "overall_score": score["overall_score"],

            "confidence": score["confidence"],

            "required_score": score["required_score"],

            "preferred_score": score["preferred_score"],

            "experience_bonus": score["experience_bonus"],

            "education_bonus": score["education_bonus"],

            "description_bonus": score["description_bonus"],

            "matched_required": matched_required,

            "matched_preferred": matched_preferred,

            "missing_required": missing_required,

            "missing_preferred": missing_preferred,

            "recommendation_reason": recommendation_reason(
                matched_required,
                matched_preferred,
                missing_required
            )

        })

    recommendations = sorted(
        recommendations,
        key=lambda x: x["overall_score"],
        reverse=True
    )

    return recommendations[:top_n]


# ==========================================================
# BEST JOB
# ==========================================================

def recommend_best_job(
    candidate_skills: List[str],
    candidate_experience: int = 0,
    candidate_education: str = ""
):
    """
    Return the highest-ranked job.
    """

    jobs = recommend_jobs(
        candidate_skills,
        candidate_experience,
        candidate_education,
        top_n=1
    )

    if jobs:
        return jobs[0]

    return None


from typing import Dict, List, Optional


def generate_career_advice(
    job: Optional[Dict] = None,
    *args,
    **kwargs
) -> List[str]:
    """
    Generate personalized career advice.

    Compatible with both old and new versions.
    """

    advice = []

    if job is None:

        return [
            "Generate job recommendations first to receive personalized career advice."
        ]

    score = job.get("overall_score", 0)

    if score >= 90:

        advice.append(
            "Excellent profile! You are highly suitable for this role."
        )

    elif score >= 75:

        advice.append(
            "You are a strong candidate. A few improvements can make your resume even stronger."
        )

    elif score >= 60:

        advice.append(
            "You have a good foundation, but should strengthen a few key skills."
        )

    else:

        advice.append(
            "Consider building more skills before applying for similar roles."
        )

    required = job.get("missing_required", [])

    if required:

        advice.append(
            "Focus on learning these required skills:"
        )

        for skill in required:

            advice.append(f"• {skill}")

    preferred = job.get("missing_preferred", [])

    if preferred:

        advice.append(
            "Preferred skills that will improve your profile:"
        )

        for skill in preferred:

            advice.append(f"• {skill}")

    advice.append(
        "Build portfolio projects demonstrating these skills."
    )

    advice.append(
        "Earn relevant certifications to improve ATS performance."
    )

    return advice

# ==========================================================
# GENERATE JOB REPORT
# ==========================================================

def generate_job_report(
    candidate_skills: List[str],
    candidate_experience: int = 0,
    candidate_education: str = "",
    top_n: int = 10
) -> Dict:
    """
    Generate complete recommendation report.
    """

    recommendations = recommend_jobs(
        candidate_skills,
        candidate_experience,
        candidate_education,
        top_n
    )

    best_job = recommendations[0] if recommendations else None

    return {

        "recommended_jobs": recommendations,

        "best_job": best_job,

        "career_advice": generate_career_advice(best_job),

        "total_recommendations": len(recommendations)

    }


# ==========================================================
# SEARCH JOBS
# ==========================================================

def search_jobs(
    keyword: str,
    jobs: List[Dict]
) -> List[Dict]:
    """
    Search recommended jobs by keyword.
    """

    keyword = normalize_text(keyword)

    results = []

    for job in jobs:

        if (

            keyword in normalize_text(job["job_title"])

            or

            keyword in normalize_text(job["company"])

            or

            keyword in normalize_text(job["location"])

        ):

            results.append(job)

    return results
# ==========================================================
# SKILL GAP ANALYSIS
# ==========================================================

def skill_gap_analysis(job: Dict) -> Dict:
    """
    Analyze skill gaps for the selected job.
    """

    if job is None:

        return {
            "matched": [],
            "missing_required": [],
            "missing_preferred": [],
            "completion_percentage": 0
        }

    total = (
        len(job["matched_required"])
        + len(job["missing_required"])
    )

    completion = 100

    if total > 0:
        completion = round(
            (len(job["matched_required"]) / total) * 100,
            2
        )

    return {

        "matched": sorted(
            job["matched_required"] +
            job["matched_preferred"]
        ),

        "missing_required":
            job["missing_required"],

        "missing_preferred":
            job["missing_preferred"],

        "completion_percentage":
            completion

    }


# ==========================================================
# IMPROVEMENT ROADMAP
# ==========================================================

def improvement_roadmap(job: Dict) -> List[str]:
    """
    Generate an improvement roadmap.
    """

    roadmap = []

    if job is None:
        return roadmap

    roadmap.append("Step 1 : Master all required skills.")

    for skill in job["missing_required"]:
        roadmap.append(f"Learn {skill}")

    roadmap.append("Step 2 : Learn preferred skills.")

    for skill in job["missing_preferred"]:
        roadmap.append(f"Learn {skill}")

    roadmap.append("Step 3 : Build portfolio projects.")

    roadmap.append("Step 4 : Earn certifications.")

    roadmap.append("Step 5 : Update resume and LinkedIn.")

    roadmap.append("Step 6 : Start applying for jobs.")

    return roadmap


# ==========================================================
# RECOMMENDATION STATISTICS
# ==========================================================

def recommendation_statistics(
    recommendations: List[Dict]
) -> Dict:
    """
    Generate summary statistics.
    """

    if not recommendations:

        return {

            "average_score": 0,

            "highest_score": 0,

            "lowest_score": 0,

            "excellent": 0,

            "strong": 0,

            "moderate": 0,

            "weak": 0,

            "poor": 0

        }

    scores = [

        job["overall_score"]

        for job in recommendations

    ]

    stats = {

        "average_score": round(

            sum(scores) / len(scores),

            2

        ),

        "highest_score": max(scores),

        "lowest_score": min(scores),

        "excellent": 0,

        "strong": 0,

        "moderate": 0,

        "weak": 0,

        "poor": 0

    }

    for job in recommendations:

        label = job["confidence"].lower()

        if label in stats:
            stats[label] += 1

    return stats


# ==========================================================
# REPORT FORMATTER
# ==========================================================

def format_job_report(report: Dict) -> Dict:
    """
    Create a dashboard-friendly report.
    """

    recommendations = report["recommended_jobs"]

    stats = recommendation_statistics(
        recommendations
    )

    best_job = report["best_job"]

    return {

        "summary": {

            "total_jobs":
                report["total_recommendations"],

            "average_score":
                stats["average_score"],

            "highest_score":
                stats["highest_score"]

        },

        "best_job":
            best_job,

        "statistics":
            stats,

        "career_advice":
            report["career_advice"],

        "skill_gap":
            skill_gap_analysis(best_job),

        "roadmap":
            improvement_roadmap(best_job),

        "recommendations":
            recommendations

    }


# ==========================================================
# PRINT REPORT
# ==========================================================

def print_job_report(report: Dict):
    """
    Pretty-print the job report.
    """

    formatted = format_job_report(report)

    print("\n" + "=" * 80)
    print("JOB RECOMMENDATION REPORT")
    print("=" * 80)

    summary = formatted["summary"]

    print(f"Total Jobs          : {summary['total_jobs']}")
    print(f"Average Match Score : {summary['average_score']} %")
    print(f"Highest Score       : {summary['highest_score']} %")

    best = formatted["best_job"]

    if best:

        print("\nBEST MATCH")
        print("-" * 80)

        print(f"Job Title : {best['job_title']}")
        print(f"Company   : {best['company']}")
        print(f"Location  : {best['location']}")
        print(f"Match     : {best['overall_score']} %")
        print(f"Confidence: {best['confidence']}")

    print("\nCAREER ADVICE")

    for advice in formatted["career_advice"]:

        print(f"• {advice}")

    print("\nROADMAP")

    for step in formatted["roadmap"]:

        print(f"✓ {step}")

    print("\nTOP JOBS")

    for i, job in enumerate(
        formatted["recommendations"],
        start=1
    ):

        print(
            f"{i}. {job['job_title']} | "
            f"{job['company']} | "
            f"{job['overall_score']}%"
        )

    print("=" * 80)


# ==========================================================
# MODULE COMPLETE
# ==========================================================