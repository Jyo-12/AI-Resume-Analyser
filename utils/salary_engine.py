"""
==========================================================
AI Resume Analyzer
Salary Prediction Engine
Version 2.0
Part 1A
==========================================================

This module predicts salary based on:

• Job Role
• Experience
• Location
• Skills
• Education
• Employment Type

Dataset Columns
---------------
Salary_ID
Job_Role
Location
Company_Type
Experience
Minimum_Salary_LPA
Maximum_Salary_LPA
Average_Salary_LPA
Required_Skills
Education
Employment_Type
==========================================================
"""

import re
import warnings
from typing import List, Set

import pandas as pd

from utils.database import load_salary_data

warnings.filterwarnings("ignore")

# ==========================================================
# Configuration
# ==========================================================

DEFAULT_TOP_N = 10

TEXT_COLUMNS = [

    "Job_Role",

    "Location",

    "Company_Type",

    "Experience",

    "Required_Skills",

    "Education",

    "Employment_Type"

]

# ==========================================================
# Load Salary Dataset
# ==========================================================

try:

    SALARY_DF = load_salary_data()

except Exception as e:

    print(f"Error loading salary dataset : {e}")

    SALARY_DF = pd.DataFrame()

# ==========================================================
# Text Normalization
# ==========================================================

def normalize_text(text):
    """
    Normalize text for comparison.
    """

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9+#, ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ==========================================================
# Skill Parser
# ==========================================================

def split_skills(skill_string):
    """
    Convert comma separated skills into a set.
    """

    if pd.isna(skill_string):

        return set()

    if not isinstance(skill_string, str):

        skill_string = str(skill_string)

    skills = re.split(r"[;,/|]", skill_string)

    parsed = set()

    for skill in skills:

        skill = normalize_text(skill)

        if skill:

            parsed.add(skill)

    return parsed

# ==========================================================
# Candidate Skill Validation
# ==========================================================

def validate_candidate_skills(skills):
    """
    Convert candidate skills into normalized set.
    """

    if skills is None:

        return set()

    if isinstance(skills, set):

        return {

            normalize_text(skill)

            for skill in skills

            if skill

        }

    if isinstance(skills, list):

        return {

            normalize_text(skill)

            for skill in skills

            if skill

        }

    return split_skills(skills)

# ==========================================================
# Dataset Preprocessing
# ==========================================================

def preprocess_salary_dataset(df):
    """
    Prepare salary dataset.
    """

    if df.empty:

        return df

    df = df.copy()

    for column in TEXT_COLUMNS:

        if column in df.columns:

            df[column] = (

                df[column]

                .fillna("")

                .astype(str)

            )

    # Salary columns

    salary_columns = [

        "Minimum_Salary_LPA",

        "Maximum_Salary_LPA",

        "Average_Salary_LPA"

    ]

    for column in salary_columns:

        if column in df.columns:

            df[column] = (

                pd.to_numeric(

                    df[column],

                    errors="coerce"

                )

                .fillna(0)

            )

    # Convert skills into Python sets

    df["skill_set"] = (

        df["Required_Skills"]

        .apply(split_skills)

    )

    # Normalized columns

    df["job_role_clean"] = (

        df["Job_Role"]

        .apply(normalize_text)

    )

    df["location_clean"] = (

        df["Location"]

        .apply(normalize_text)

    )

    df["company_type_clean"] = (

        df["Company_Type"]

        .apply(normalize_text)

    )

    df["education_clean"] = (

        df["Education"]

        .apply(normalize_text)

    )

    df["employment_type_clean"] = (

        df["Employment_Type"]

        .apply(normalize_text)

    )

    return df

# ==========================================================
# Preprocess Dataset Once
# ==========================================================

SALARY_DF = preprocess_salary_dataset(

    SALARY_DF

)

# ==========================================================
# Helper Functions
# ==========================================================

def matched_skills(

    candidate_skills: Set[str],

    required_skills: Set[str]

) -> List[str]:
    """
    Skills matching the job.
    """

    return sorted(

        candidate_skills & required_skills

    )


def missing_skills(

    candidate_skills: Set[str],

    required_skills: Set[str]

) -> List[str]:
    """
    Missing skills.
    """

    return sorted(

        required_skills - candidate_skills

    )


def skill_match_percentage(

    candidate_skills: Set[str],

    required_skills: Set[str]

):
    """
    Skill matching percentage.
    """

    if len(required_skills) == 0:

        return 0

    matched = len(

        candidate_skills & required_skills

    )

    return round(

        matched /

        len(required_skills)

        * 100,

        2

    )
# ==========================================================
# Experience Parsing
# ==========================================================

def extract_experience(experience):
    """
    Convert experience text into years.

    Examples:
        Fresher -> 0
        2 Years -> 2
        3-5 Years -> 4
        5+ Years -> 5
    """

    if pd.isna(experience):
        return 0

    experience = normalize_text(experience)

    if "fresher" in experience:
        return 0

    numbers = re.findall(r"\d+", experience)

    if len(numbers) == 0:
        return 0

    numbers = [int(x) for x in numbers]

    if len(numbers) == 1:
        return numbers[0]

    return round(sum(numbers) / len(numbers), 1)


# ==========================================================
# Experience Score
# ==========================================================

def experience_score(candidate_exp, required_exp):
    """
    Compare candidate experience
    with required experience.
    """

    candidate = extract_experience(candidate_exp)
    required = extract_experience(required_exp)

    if candidate >= required:
        return 100

    if required == 0:
        return 100

    score = (candidate / required) * 100

    return round(score, 2)


# ==========================================================
# Company Type Score
# ==========================================================

COMPANY_SCORE = {

    "mnc": 100,

    "multinational": 100,

    "product": 95,

    "startup": 90,

    "government": 90,

    "service": 85,

    "consulting": 85

}


def company_score(company_type):
    """
    Return score based on company type.
    """

    company_type = normalize_text(company_type)

    return COMPANY_SCORE.get(company_type, 80)


# ==========================================================
# Location Score
# ==========================================================

LOCATION_SCORE = {

    "bangalore": 100,

    "bengaluru": 100,

    "hyderabad": 98,

    "pune": 96,

    "chennai": 94,

    "mumbai": 94,

    "gurgaon": 92,

    "gurugram": 92,

    "delhi": 90,

    "noida": 90,

    "kolkata": 88,

    "coimbatore": 86,

    "mysore": 85,

    "mysuru": 85,

    "kochi": 84,

    "remote": 90

}


def location_score(location):
    """
    Score based on hiring market.
    """

    location = normalize_text(location)

    return LOCATION_SCORE.get(location, 80)


# ==========================================================
# Education Score
# ==========================================================

EDUCATION_SCORE = {

    "phd": 100,

    "doctorate": 100,

    "mtech": 95,

    "masters": 95,

    "msc": 92,

    "btech": 90,

    "be": 90,

    "bachelor": 88,

    "bsc": 85,

    "diploma": 75

}


def education_score(education):
    """
    Convert education level into score.
    """

    education = normalize_text(education)

    for key, value in EDUCATION_SCORE.items():

        if key in education:

            return value

    return 70


# ==========================================================
# Employment Type Score
# ==========================================================

EMPLOYMENT_SCORE = {

    "full time": 100,

    "permanent": 100,

    "contract": 90,

    "internship": 80,

    "part time": 75,

    "freelance": 70

}


def employment_score(employment):
    """
    Employment type score.
    """

    employment = normalize_text(employment)

    return EMPLOYMENT_SCORE.get(employment, 80)


# ==========================================================
# Salary Range Helper
# ==========================================================

def salary_range(row):
    """
    Return salary range as tuple.
    """

    return (

        row["Minimum_Salary_LPA"],

        row["Maximum_Salary_LPA"]

    )


# ==========================================================
# Average Salary Helper
# ==========================================================

def average_salary(row):
    """
    Return average salary.
    """

    return float(

        row["Average_Salary_LPA"]

    )


# ==========================================================
# Search Salary by Job Role
# ==========================================================

def search_job_role(job_role):
    """
    Search salary dataset
    using job role.
    """

    job_role = normalize_text(job_role)

    return SALARY_DF[

        SALARY_DF["job_role_clean"]

        .str.contains(

            job_role,

            na=False

        )

    ]


# ==========================================================
# Search Salary by Location
# ==========================================================

def search_location(location):
    """
    Search salary records
    by location.
    """

    location = normalize_text(location)

    return SALARY_DF[

        SALARY_DF["location_clean"]

        .str.contains(

            location,

            na=False

        )

    ]


# ==========================================================
# Dataset Summary
# ==========================================================

def salary_summary():
    """
    Salary dataset statistics.
    """

    if SALARY_DF.empty:

        return {}

    return {

        "total_jobs":

            len(SALARY_DF),

        "locations":

            SALARY_DF["Location"]

            .nunique(),

        "company_types":

            SALARY_DF["Company_Type"]

            .nunique(),

        "job_roles":

            SALARY_DF["Job_Role"]

            .nunique()

    }


# ==========================================================
# End of Part 1
# ==========================================================
# ==========================================================
# Salary Prediction Engine
# Part 2A
# ==========================================================

def recommendation_score(
    candidate_skills,
    required_skills,
    candidate_experience,
    required_experience,
    education,
    company_type,
    location
):
    """
    Calculate overall salary recommendation score.
    """

    skill_score = skill_match_percentage(
        candidate_skills,
        required_skills
    )

    exp_score = experience_score(
        candidate_experience,
        required_experience
    )

    edu_score = education_score(
        education
    )

    comp_score = company_score(
        company_type
    )

    loc_score = location_score(
        location
    )

    overall = (

        skill_score * 0.40 +

        exp_score * 0.25 +

        edu_score * 0.15 +

        comp_score * 0.10 +

        loc_score * 0.10

    )

    return round(overall, 2)


# ==========================================================
# Salary Estimate
# ==========================================================

def estimate_salary(
    row,
    candidate_skills,
    candidate_experience,
    education
):
    """
    Estimate expected salary
    based on recommendation score.
    """

    score = recommendation_score(

        candidate_skills,

        row["skill_set"],

        candidate_experience,

        row["Experience"],

        education,

        row["Company_Type"],

        row["Location"]

    )

    minimum = row["Minimum_Salary_LPA"]

    maximum = row["Maximum_Salary_LPA"]

    average = row["Average_Salary_LPA"]

    if score >= 90:

        predicted = maximum

    elif score >= 80:

        predicted = average + (

            (maximum - average) * 0.50

        )

    elif score >= 70:

        predicted = average

    elif score >= 60:

        predicted = (

            minimum + average

        ) / 2

    else:

        predicted = minimum

    predicted = round(

        predicted,

        2

    )

    return predicted, score


# ==========================================================
# Salary Prediction
# ==========================================================

def predict_salary(
    job_role,
    candidate_skills,
    experience,
    education,
    top_n=DEFAULT_TOP_N
):
    """
    Predict salary for a job role.
    """

    candidate_skills = validate_candidate_skills(
        candidate_skills
    )

    jobs = search_job_role(
        job_role
    )

    if jobs.empty:

        return pd.DataFrame()

    recommendations = []

    for _, row in jobs.iterrows():

        predicted_salary, score = estimate_salary(

            row,

            candidate_skills,

            experience,

            education

        )

        recommendations.append({

            "Job_Role":

                row["Job_Role"],

            "Location":

                row["Location"],

            "Company_Type":

                row["Company_Type"],

            "Employment_Type":

                row["Employment_Type"],

            "Experience":

                row["Experience"],

            "Education":

                row["Education"],

            "Predicted_Salary_LPA":

                predicted_salary,

            "Average_Salary_LPA":

                row["Average_Salary_LPA"],

            "Minimum_Salary_LPA":

                row["Minimum_Salary_LPA"],

            "Maximum_Salary_LPA":

                row["Maximum_Salary_LPA"],

            "Matched_Skills":

                matched_skills(
                    candidate_skills,
                    row["skill_set"]
                ),

            "Missing_Skills":

                missing_skills(
                    candidate_skills,
                    row["skill_set"]
                ),

            "Skill_Match_%":

                skill_match_percentage(
                    candidate_skills,
                    row["skill_set"]
                ),

            "Recommendation_Score":

                score

        })

    recommendations = pd.DataFrame(
        recommendations
    )

    recommendations = recommendations.sort_values(

        by=[

            "Recommendation_Score",

            "Predicted_Salary_LPA"

        ],

        ascending=False

    )

    return recommendations.head(
        top_n
    )


# ==========================================================
# Best Salary Match
# ==========================================================

def predict_best_salary(
    job_role,
    candidate_skills,
    experience,
    education
):
    """
    Return the highest ranked
    salary prediction.
    """

    predictions = predict_salary(

        job_role,

        candidate_skills,

        experience,

        education,

        top_n=1

    )

    if predictions.empty:

        return None

    return predictions.iloc[0]


# ==========================================================
# Salary Category
# ==========================================================

def salary_category(predicted_salary):
    """
    Categorize predicted salary.
    """

    if predicted_salary >= 25:

        return "Excellent"

    elif predicted_salary >= 15:

        return "High"

    elif predicted_salary >= 8:

        return "Good"

    elif predicted_salary >= 5:

        return "Average"

    return "Entry Level"


# ==========================================================
# Recommendation Reason
# ==========================================================

def recommendation_reason(score):
    """
    Human-readable explanation.
    """

    if score >= 90:

        return "Excellent profile match."

    elif score >= 80:

        return "Very strong candidate."

    elif score >= 70:

        return "Good salary potential."

    elif score >= 60:

        return "Average salary expectation."

    return "Improve skills and experience to increase salary."
# ==========================================================
# Salary Report Generator
# Part 2B
# ==========================================================

def generate_salary_report(
    job_role,
    candidate_skills,
    experience,
    education
):
    """
    Generate a complete salary report for a candidate.
    """

    predictions = predict_salary(
        job_role,
        candidate_skills,
        experience,
        education
    )

    if predictions.empty:
        return {}

    best = predictions.iloc[0]

    report = {

        "job_role":
            best["Job_Role"],

        "location":
            best["Location"],

        "company_type":
            best["Company_Type"],

        "employment_type":
            best["Employment_Type"],

        "experience":
            best["Experience"],

        "education":
            best["Education"],

        "predicted_salary_lpa":
            best["Predicted_Salary_LPA"],

        "minimum_salary_lpa":
            best["Minimum_Salary_LPA"],

        "average_salary_lpa":
            best["Average_Salary_LPA"],

        "maximum_salary_lpa":
            best["Maximum_Salary_LPA"],

        "salary_category":
            salary_category(
                best["Predicted_Salary_LPA"]
            ),

        "recommendation_score":
            best["Recommendation_Score"],

        "skill_match":
            best["Skill_Match_%"],

        "matched_skills":
            best["Matched_Skills"],

        "missing_skills":
            best["Missing_Skills"],

        "recommendation":
            recommendation_reason(
                best["Recommendation_Score"]
            )

    }

    return report


# ==========================================================
# Career Growth Estimator
# ==========================================================

def estimate_growth(report):
    """
    Estimate future salary growth.
    """

    current = report["predicted_salary_lpa"]

    return {

        "Current":
            round(current, 2),

        "After_2_Years":
            round(current * 1.25, 2),

        "After_5_Years":
            round(current * 1.70, 2),

        "After_10_Years":
            round(current * 2.50, 2)

    }


# ==========================================================
# Salary Insights
# ==========================================================

def salary_insights(report):
    """
    Generate salary insights.
    """

    insights = []

    if report["recommendation_score"] >= 90:
        insights.append(
            "Excellent overall profile."
        )

    elif report["recommendation_score"] >= 75:
        insights.append(
            "Strong profile with good salary prospects."
        )

    else:
        insights.append(
            "Upskilling can significantly improve salary."
        )

    if report["missing_skills"]:

        insights.append(

            "Consider learning: "

            + ", ".join(
                report["missing_skills"][:5]
            )

        )

    insights.append(

        f"Expected salary category: {report['salary_category']}."

    )

    return insights


# ==========================================================
# Compare Multiple Locations
# ==========================================================

def compare_locations(job_role):
    """
    Compare salaries for the same role
    across different locations.
    """

    jobs = search_job_role(job_role)

    if jobs.empty:

        return pd.DataFrame()

    comparison = jobs[

        [

            "Location",

            "Minimum_Salary_LPA",

            "Average_Salary_LPA",

            "Maximum_Salary_LPA"

        ]

    ].copy()

    comparison = comparison.sort_values(

        by="Average_Salary_LPA",

        ascending=False

    )

    return comparison.reset_index(drop=True)


# ==========================================================
# Compare Company Types
# ==========================================================

def compare_company_types(job_role):
    """
    Compare salaries across company types.
    """

    jobs = search_job_role(job_role)

    if jobs.empty:

        return pd.DataFrame()

    comparison = jobs.groupby(

        "Company_Type",

        as_index=False

    )["Average_Salary_LPA"].mean()

    comparison = comparison.sort_values(

        by="Average_Salary_LPA",

        ascending=False

    )

    return comparison


# ==========================================================
# Salary Statistics
# ==========================================================

def salary_statistics():
    """
    Dataset statistics.
    """

    if SALARY_DF.empty:

        return {}

    return {

        "total_records":
            len(SALARY_DF),

        "unique_job_roles":
            SALARY_DF["Job_Role"].nunique(),

        "unique_locations":
            SALARY_DF["Location"].nunique(),

        "average_salary":
            round(
                SALARY_DF["Average_Salary_LPA"].mean(),
                2
            ),

        "highest_salary":
            round(
                SALARY_DF["Maximum_Salary_LPA"].max(),
                2
            ),

        "lowest_salary":
            round(
                SALARY_DF["Minimum_Salary_LPA"].min(),
                2
            )

    }


# ==========================================================
# End of Part 2
# ==========================================================
# ==========================================================
# Salary Report Formatter
# ==========================================================

def format_salary_report(report):
    """
    Format the salary report into a readable string.
    """

    if not report:
        return "No salary prediction available."

    lines = []

    lines.append("=" * 60)
    lines.append("AI RESUME ANALYZER - SALARY REPORT")
    lines.append("=" * 60)

    lines.append(f"Job Role            : {report['job_role']}")
    lines.append(f"Location            : {report['location']}")
    lines.append(f"Company Type        : {report['company_type']}")
    lines.append(f"Employment Type     : {report['employment_type']}")
    lines.append(f"Experience          : {report['experience']}")
    lines.append(f"Education           : {report['education']}")

    lines.append("")

    lines.append(
        f"Predicted Salary    : ₹{report['predicted_salary_lpa']:.2f} LPA"
    )

    lines.append(
        f"Salary Range        : ₹{report['minimum_salary_lpa']:.2f}"
        f" - ₹{report['maximum_salary_lpa']:.2f} LPA"
    )

    lines.append(
        f"Average Salary      : ₹{report['average_salary_lpa']:.2f} LPA"
    )

    lines.append(
        f"Recommendation Score: {report['recommendation_score']:.2f}"
    )

    lines.append(
        f"Skill Match         : {report['skill_match']:.2f}%"
    )

    lines.append(
        f"Salary Category     : {report['salary_category']}"
    )

    lines.append("")

    lines.append("Matched Skills")

    if report["matched_skills"]:

        for skill in report["matched_skills"]:
            lines.append(f"  ✓ {skill}")

    else:
        lines.append("  None")

    lines.append("")

    lines.append("Missing Skills")

    if report["missing_skills"]:

        for skill in report["missing_skills"]:
            lines.append(f"  • {skill}")

    else:
        lines.append("  None")

    lines.append("")

    lines.append("Recommendation")

    lines.append(report["recommendation"])

    lines.append("=" * 60)

    return "\n".join(lines)


# ==========================================================
# Print Salary Report
# ==========================================================

def print_salary_report(report):
    """
    Print formatted salary report.
    """

    print(
        format_salary_report(report)
    )


# ==========================================================
# Export Report
# ==========================================================

def export_salary_report(report):
    """
    Return report as dictionary.
    """

    if not report:
        return {}

    return dict(report)


# ==========================================================
# Top Paying Roles
# ==========================================================

def top_paying_roles(top_n=10):
    """
    Return highest-paying job roles.
    """

    if SALARY_DF.empty:
        return pd.DataFrame()

    result = SALARY_DF.sort_values(
        by="Average_Salary_LPA",
        ascending=False
    )

    return result.head(top_n)


# ==========================================================
# Top Paying Locations
# ==========================================================

def top_paying_locations():
    """
    Average salary by location.
    """

    if SALARY_DF.empty:
        return pd.DataFrame()

    result = (
        SALARY_DF
        .groupby("Location", as_index=False)
        ["Average_Salary_LPA"]
        .mean()
        .sort_values(
            by="Average_Salary_LPA",
            ascending=False
        )
    )

    return result


# ==========================================================
# Top Company Types
# ==========================================================

def top_company_types():
    """
    Average salary by company type.
    """

    if SALARY_DF.empty:
        return pd.DataFrame()

    result = (
        SALARY_DF
        .groupby("Company_Type", as_index=False)
        ["Average_Salary_LPA"]
        .mean()
        .sort_values(
            by="Average_Salary_LPA",
            ascending=False
        )
    )

    return result


# ==========================================================
# Main Testing
# ==========================================================

if __name__ == "__main__":

    candidate_skills = [

        "Python",

        "Machine Learning",

        "SQL",

        "Pandas",

        "Power BI"

    ]

    report = generate_salary_report(

        job_role="Data Scientist",

        candidate_skills=candidate_skills,

        experience="2 Years",

        education="B.Tech"

    )

    print_salary_report(report)

    print("\nSalary Statistics")
    print("------------------------------")
    print(salary_statistics())

    print("\nCareer Growth")
    print("------------------------------")
    print(estimate_growth(report))

    print("\nSalary Insights")
    print("------------------------------")

    for item in salary_insights(report):
        print("-", item)

    print("\nTop Paying Roles")
    print("------------------------------")
    print(
        top_paying_roles(5)[
            [
                "Job_Role",
                "Average_Salary_LPA"
            ]
        ]
    )

    print("\nTop Paying Locations")
    print("------------------------------")
    print(top_paying_locations().head())

    print("\nTop Company Types")
    print("------------------------------")
    print(top_company_types().head())