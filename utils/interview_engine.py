"""
==========================================================
AI Resume Analyzer
Interview Preparation Engine
Version 2.0
Part 1A
==========================================================

Dataset Columns
---------------
Question_ID
Job_Role
Skill
Difficulty
Question_Type
Question
Expected_Key_Points
Sample_Answer
==========================================================
"""

import re
import warnings
from typing import List, Set

import pandas as pd

from utils.database import load_interview_questions

warnings.filterwarnings("ignore")

# ==========================================================
# Configuration
# ==========================================================

DEFAULT_TOP_N = 10

TEXT_COLUMNS = [

    "Job_Role",

    "Skill",

    "Difficulty",

    "Question_Type",

    "Question",

    "Expected_Key_Points",

    "Sample_Answer"

]

# ==========================================================
# Load Interview Dataset
# ==========================================================

try:

    INTERVIEW_DF = load_interview_questions()

except Exception as e:

    print(f"Error loading interview dataset: {e}")

    INTERVIEW_DF = pd.DataFrame()

# ==========================================================
# Text Normalization
# ==========================================================

def normalize_text(text):
    """
    Normalize text for searching and comparison.
    """

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9+# ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ==========================================================
# Skill Parser
# ==========================================================

def split_skills(skill_string):
    """
    Convert comma-separated skills into a Python set.
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

def preprocess_interview_dataset(df):
    """
    Prepare interview dataset for searching.
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

    df["skill_set"] = (

        df["Skill"]

        .apply(split_skills)

    )

    df["job_role_clean"] = (

        df["Job_Role"]

        .apply(normalize_text)

    )

    df["skill_clean"] = (

        df["Skill"]

        .apply(normalize_text)

    )

    df["difficulty_clean"] = (

        df["Difficulty"]

        .apply(normalize_text)

    )

    df["question_type_clean"] = (

        df["Question_Type"]

        .apply(normalize_text)

    )

    return df

# ==========================================================
# Preprocess Dataset
# ==========================================================

INTERVIEW_DF = preprocess_interview_dataset(

    INTERVIEW_DF

)

# ==========================================================
# Helper Functions
# ==========================================================

def matched_skills(

    candidate_skills: Set[str],

    question_skills: Set[str]

) -> List[str]:
    """
    Return matching skills.
    """

    return sorted(

        candidate_skills & question_skills

    )


def missing_skills(

    candidate_skills: Set[str],

    question_skills: Set[str]

) -> List[str]:
    """
    Return missing skills.
    """

    return sorted(

        question_skills - candidate_skills

    )


def skill_match_percentage(

    candidate_skills: Set[str],

    question_skills: Set[str]

):
    """
    Compute percentage skill match.
    """

    if len(question_skills) == 0:

        return 0

    matched = len(

        candidate_skills & question_skills

    )

    return round(

        matched /

        len(question_skills)

        * 100,

        2

    )
# ==========================================================
# Difficulty Score
# ==========================================================

DIFFICULTY_SCORE = {

    "easy": 60,

    "medium": 80,

    "hard": 100

}


def difficulty_score(difficulty):
    """
    Convert difficulty level into a score.
    """

    difficulty = normalize_text(difficulty)

    return DIFFICULTY_SCORE.get(difficulty, 70)


# ==========================================================
# Question Type Score
# ==========================================================

QUESTION_TYPE_SCORE = {

    "technical": 100,

    "coding": 95,

    "scenario": 90,

    "behavioral": 85,

    "hr": 80,

    "aptitude": 75

}


def question_type_score(question_type):
    """
    Return score for question type.
    """

    question_type = normalize_text(question_type)

    return QUESTION_TYPE_SCORE.get(question_type, 70)


# ==========================================================
# Search by Job Role
# ==========================================================

def search_job_role(job_role):
    """
    Search interview questions by job role.
    """

    job_role = normalize_text(job_role)

    return INTERVIEW_DF[

        INTERVIEW_DF["job_role_clean"]

        .str.contains(

            job_role,

            na=False

        )

    ]


# ==========================================================
# Search by Skill
# ==========================================================

def search_skill(skill):
    """
    Search interview questions by skill.
    """

    skill = normalize_text(skill)

    return INTERVIEW_DF[

        INTERVIEW_DF["skill_clean"]

        .str.contains(

            skill,

            na=False

        )

    ]


# ==========================================================
# Search by Difficulty
# ==========================================================

def search_difficulty(level):
    """
    Search interview questions by difficulty.
    """

    level = normalize_text(level)

    return INTERVIEW_DF[

        INTERVIEW_DF["difficulty_clean"]

        .str.contains(

            level,

            na=False

        )

    ]


# ==========================================================
# Search by Question Type
# ==========================================================

def search_question_type(question_type):
    """
    Search interview questions by type.
    """

    question_type = normalize_text(question_type)

    return INTERVIEW_DF[

        INTERVIEW_DF["question_type_clean"]

        .str.contains(

            question_type,

            na=False

        )

    ]


# ==========================================================
# Filter Questions
# ==========================================================

def filter_questions(
    job_role=None,
    skill=None,
    difficulty=None,
    question_type=None
):
    """
    Filter interview questions using
    multiple conditions.
    """

    df = INTERVIEW_DF.copy()

    if job_role:

        df = df[

            df["job_role_clean"]

            .str.contains(

                normalize_text(job_role),

                na=False

            )

        ]

    if skill:

        df = df[

            df["skill_clean"]

            .str.contains(

                normalize_text(skill),

                na=False

            )

        ]

    if difficulty:

        df = df[

            df["difficulty_clean"]

            .str.contains(

                normalize_text(difficulty),

                na=False

            )

        ]

    if question_type:

        df = df[

            df["question_type_clean"]

            .str.contains(

                normalize_text(question_type),

                na=False

            )

        ]

    return df.reset_index(drop=True)


# ==========================================================
# Dataset Summary
# ==========================================================

def interview_summary():
    """
    Return interview dataset statistics.
    """

    if INTERVIEW_DF.empty:

        return {}

    return {

        "total_questions":

            len(INTERVIEW_DF),

        "job_roles":

            INTERVIEW_DF["Job_Role"]

            .nunique(),

        "skills":

            INTERVIEW_DF["Skill"]

            .nunique(),

        "difficulty_levels":

            INTERVIEW_DF["Difficulty"]

            .nunique(),

        "question_types":

            INTERVIEW_DF["Question_Type"]

            .nunique()

    }


# ==========================================================
# Helper Functions
# ==========================================================

def get_unique_job_roles():
    """
    Return sorted job roles.
    """

    return sorted(

        INTERVIEW_DF["Job_Role"]

        .dropna()

        .unique()

    )


def get_unique_skills():
    """
    Return sorted skills.
    """

    skills = set()

    for skill_set in INTERVIEW_DF["skill_set"]:

        skills.update(skill_set)

    return sorted(skills)


def get_unique_difficulties():
    """
    Return difficulty levels.
    """

    return sorted(

        INTERVIEW_DF["Difficulty"]

        .dropna()

        .unique()

    )


def get_unique_question_types():
    """
    Return question types.
    """

    return sorted(

        INTERVIEW_DF["Question_Type"]

        .dropna()

        .unique()

    )


# ==========================================================
# End of Part 1
# ==========================================================
# ==========================================================
# Interview Recommendation Engine
# Part 2A-1
# ==========================================================

def question_relevance_score(
    candidate_skills,
    question_skills,
    difficulty,
    question_type
):
    """
    Calculate the relevance score for an interview question.
    """

    skill_score = skill_match_percentage(
        candidate_skills,
        question_skills
    )

    diff_score = difficulty_score(
        difficulty
    )

    type_score = question_type_score(
        question_type
    )

    overall = (

        skill_score * 0.60 +

        diff_score * 0.20 +

        type_score * 0.20

    )

    return round(overall, 2)


# ==========================================================
# Overall Recommendation Score
# ==========================================================

def recommendation_score(
    row,
    candidate_skills
):
    """
    Compute recommendation score for a question.
    """

    return question_relevance_score(

        candidate_skills,

        row["skill_set"],

        row["Difficulty"],

        row["Question_Type"]

    )


# ==========================================================
# Recommend Interview Questions
# ==========================================================

def recommend_interview_questions(
    job_role,
    candidate_skills,
    difficulty=None,
    question_type=None,
    top_n=DEFAULT_TOP_N
):
    """
    Recommend personalized interview questions.
    """

    candidate_skills = validate_candidate_skills(
        candidate_skills
    )

    questions = filter_questions(
        job_role=job_role,
        difficulty=difficulty,
        question_type=question_type
    )

    if questions.empty:
        return pd.DataFrame()

    recommendations = []

    for _, row in questions.iterrows():

        score = recommendation_score(
            row,
            candidate_skills
        )

        recommendations.append({

            "Question_ID":
                row["Question_ID"],

            "Job_Role":
                row["Job_Role"],

            "Skill":
                row["Skill"],

            "Difficulty":
                row["Difficulty"],

            "Question_Type":
                row["Question_Type"],

            "Question":
                row["Question"],

            "Expected_Key_Points":
                row["Expected_Key_Points"],

            "Sample_Answer":
                row["Sample_Answer"],

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

            "Skill_Match_%"

        ],

        ascending=False

    )

    return recommendations.head(
        top_n
    )


# ==========================================================
# End of Part 2A-1
# ==========================================================
# ==========================================================
# Best Question Recommendations
# Part 2A-2
# ==========================================================

def recommend_best_questions(
    job_role,
    candidate_skills,
    top_n=5
):
    """
    Return the best interview questions.
    """

    recommendations = recommend_interview_questions(
        job_role=job_role,
        candidate_skills=candidate_skills,
        top_n=top_n
    )

    return recommendations


# ==========================================================
# Recommend Questions by Skill
# ==========================================================

def recommend_questions_by_skill(
    skill,
    difficulty=None,
    top_n=DEFAULT_TOP_N
):
    """
    Recommend interview questions for a skill.
    """

    questions = filter_questions(
        skill=skill,
        difficulty=difficulty
    )

    if questions.empty:
        return pd.DataFrame()

    questions = questions.copy()

    questions["Difficulty_Score"] = (
        questions["Difficulty"]
        .apply(difficulty_score)
    )

    questions = questions.sort_values(
        by="Difficulty_Score",
        ascending=False
    )

    return questions.head(top_n).reset_index(drop=True)


# ==========================================================
# Recommend Questions by Difficulty
# ==========================================================

def recommend_questions_by_difficulty(
    difficulty,
    top_n=DEFAULT_TOP_N
):
    """
    Return questions of a specific difficulty.
    """

    questions = search_difficulty(
        difficulty
    )

    if questions.empty:
        return pd.DataFrame()

    return questions.head(top_n).reset_index(drop=True)


# ==========================================================
# Recommend Questions by Type
# ==========================================================

def recommend_questions_by_type(
    question_type,
    difficulty=None,
    top_n=DEFAULT_TOP_N
):
    """
    Recommend questions by question type.
    """

    questions = filter_questions(
        question_type=question_type,
        difficulty=difficulty
    )

    if questions.empty:
        return pd.DataFrame()

    questions = questions.copy()

    questions["Type_Score"] = (
        questions["Question_Type"]
        .apply(question_type_score)
    )

    questions = questions.sort_values(
        by="Type_Score",
        ascending=False
    )

    return questions.head(top_n).reset_index(drop=True)


# ==========================================================
# Random Mock Interview Set
# ==========================================================

def random_mock_interview(
    job_role,
    n_questions=10
):
    """
    Generate a random interview set.
    """

    questions = search_job_role(job_role)

    if questions.empty:
        return pd.DataFrame()

    n_questions = min(
        n_questions,
        len(questions)
    )

    return (
        questions
        .sample(
            n=n_questions,
            random_state=42
        )
        .reset_index(drop=True)
    )


# ==========================================================
# Frequently Asked Questions
# ==========================================================

def frequently_asked_questions(
    job_role,
    top_n=10
):
    """
    Return the top interview questions
    for a job role.
    """

    questions = search_job_role(
        job_role
    )

    if questions.empty:
        return pd.DataFrame()

    return (
        questions
        .head(top_n)
        .reset_index(drop=True)
    )


# ==========================================================
# End of Part 2A
# ==========================================================
# ==========================================================
# Interview Readiness Score
# Part 2B-1A
# ==========================================================

def interview_readiness_score(
    job_role,
    candidate_skills,
    difficulty=None
):
    """
    Calculate interview readiness score based on
    recommended interview questions.
    """

    recommendations = recommend_interview_questions(
        job_role=job_role,
        candidate_skills=candidate_skills,
        difficulty=difficulty,
        top_n=20
    )

    if recommendations.empty:
        return 0.0

    readiness = recommendations[
        "Recommendation_Score"
    ].mean()

    return round(float(readiness), 2)


# ==========================================================
# Readiness Level
# ==========================================================

def readiness_level(score):
    """
    Convert readiness score into a level.
    """

    if score >= 90:
        return "Excellent"

    elif score >= 80:
        return "Very Good"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Average"

    return "Needs Improvement"


# ==========================================================
# Weak Skill Identification
# ==========================================================

def identify_weak_skills(
    job_role,
    candidate_skills,
    top_n=10
):
    """
    Identify skills that frequently appear
    in interview questions but are missing
    from the candidate profile.
    """

    candidate_skills = validate_candidate_skills(
        candidate_skills
    )

    questions = search_job_role(
        job_role
    )

    if questions.empty:
        return []

    skill_frequency = {}

    for _, row in questions.iterrows():

        missing = row["skill_set"] - candidate_skills

        for skill in missing:

            skill_frequency[skill] = (

                skill_frequency.get(skill, 0) + 1

            )

    weak_skills = sorted(

        skill_frequency.items(),

        key=lambda x: x[1],

        reverse=True

    )

    return weak_skills[:top_n]


# ==========================================================
# Strong Skill Identification
# ==========================================================

def identify_strong_skills(
    job_role,
    candidate_skills,
    top_n=10
):
    """
    Identify the candidate's strongest
    interview skills.
    """

    candidate_skills = validate_candidate_skills(
        candidate_skills
    )

    questions = search_job_role(
        job_role
    )

    if questions.empty:
        return []

    skill_frequency = {}

    for _, row in questions.iterrows():

        matched = row["skill_set"] & candidate_skills

        for skill in matched:

            skill_frequency[skill] = (

                skill_frequency.get(skill, 0) + 1

            )

    strong_skills = sorted(

        skill_frequency.items(),

        key=lambda x: x[1],

        reverse=True

    )

    return strong_skills[:top_n]


# ==========================================================
# Skill Coverage
# ==========================================================

def interview_skill_coverage(
    job_role,
    candidate_skills
):
    """
    Calculate interview skill coverage.
    """

    candidate_skills = validate_candidate_skills(
        candidate_skills
    )

    questions = search_job_role(
        job_role
    )

    if questions.empty:
        return 0.0

    required_skills = set()

    for skill_set in questions["skill_set"]:

        required_skills.update(skill_set)

    if len(required_skills) == 0:
        return 0.0

    matched = len(

        required_skills & candidate_skills

    )

    coverage = (

        matched /

        len(required_skills)

    ) * 100

    return round(coverage, 2)


# ==========================================================
# End of Part 2B-1A
# ==========================================================
# ==========================================================
# Interview Skill Gap Analysis
# Part 2B-1B(1A)
# ==========================================================

def interview_skill_gap_analysis(
    job_role,
    candidate_skills
):
    """
    Perform interview skill gap analysis by comparing
    candidate skills against the required interview
    skills for the selected job role.
    """

    candidate_skills = validate_candidate_skills(
        candidate_skills
    )

    questions = search_job_role(
        job_role
    )

    if questions.empty:

        return {

            "Required_Skills": [],

            "Candidate_Skills": sorted(
                candidate_skills
            ),

            "Matched_Skills": [],

            "Missing_Skills": [],

            "Coverage": 0.0,

            "Gap": 100.0

        }

    required_skills = set()

    for skill_set in questions["skill_set"]:

        required_skills.update(
            skill_set
        )

    matched = sorted(

        required_skills &
        candidate_skills

    )

    missing = sorted(

        required_skills -
        candidate_skills

    )

    if len(required_skills) == 0:

        coverage = 0.0

    else:

        coverage = round(

            (
                len(matched)
                /
                len(required_skills)
            ) * 100,

            2

        )

    gap = round(

        100 - coverage,

        2

    )

    return {

        "Required_Skills":

            sorted(
                required_skills
            ),

        "Candidate_Skills":

            sorted(
                candidate_skills
            ),

        "Matched_Skills":

            matched,

        "Missing_Skills":

            missing,

        "Coverage":

            coverage,

        "Gap":

            gap

    }


# ==========================================================
# Missing Skill Percentage
# ==========================================================

def missing_skill_percentage(
    job_role,
    candidate_skills
):
    """
    Calculate the percentage of interview
    skills missing from the candidate profile.
    """

    gap_analysis = interview_skill_gap_analysis(

        job_role,

        candidate_skills

    )

    return gap_analysis["Gap"]


# ==========================================================
# Candidate Skill Percentage
# ==========================================================

def candidate_skill_percentage(
    job_role,
    candidate_skills
):
    """
    Calculate the percentage of required interview
    skills already possessed by the candidate.
    """

    gap_analysis = interview_skill_gap_analysis(

        job_role,

        candidate_skills

    )

    return gap_analysis["Coverage"]


# ==========================================================
# Missing Skill Count
# ==========================================================

def missing_skill_count(
    job_role,
    candidate_skills
):
    """
    Return the total number of interview
    skills missing from the candidate profile.
    """

    gap_analysis = interview_skill_gap_analysis(

        job_role,

        candidate_skills

    )

    return len(

        gap_analysis["Missing_Skills"]

    )


# ==========================================================
# Matched Skill Count
# ==========================================================

def matched_skill_count(
    job_role,
    candidate_skills
):
    """
    Return the total number of interview
    skills matched by the candidate.
    """

    gap_analysis = interview_skill_gap_analysis(

        job_role,

        candidate_skills

    )

    return len(

        gap_analysis["Matched_Skills"]

    )


# ==========================================================
# End of Part 2B-1B(1A)
# ==========================================================
# ==========================================================
# Interview Preparation Roadmap
# Part 2B-1B(1B)
# ==========================================================

def interview_preparation_roadmap(
    job_role,
    candidate_skills
):
    """
    Generate a personalized interview preparation
    roadmap based on the candidate's missing skills.
    """

    gap_analysis = interview_skill_gap_analysis(

        job_role,

        candidate_skills

    )

    roadmap = []

    for index, skill in enumerate(

        gap_analysis["Missing_Skills"],

        start=1

    ):

        roadmap.append({

            "Priority":

                index,

            "Skill":

                skill,

            "Action":

                (
                    f"Study {skill} concepts, "
                    f"practice interview questions, "
                    f"and implement at least one project."
                )

        })

    return roadmap


# ==========================================================
# Recommended Learning Order
# ==========================================================

def recommended_learning_order(
    job_role,
    candidate_skills
):
    """
    Return an ordered list of skills that
    should be learned before interviews.
    """

    roadmap = interview_preparation_roadmap(

        job_role,

        candidate_skills

    )

    return [

        item["Skill"]

        for item in roadmap

    ]


# ==========================================================
# Preparation Progress
# ==========================================================

def preparation_progress(
    job_role,
    candidate_skills
):
    """
    Return the current interview preparation
    progress percentage.
    """

    return candidate_skill_percentage(

        job_role,

        candidate_skills

    )


# ==========================================================
# Preparation Status
# ==========================================================

def preparation_status(
    job_role,
    candidate_skills
):
    """
    Convert preparation percentage into
    an easy-to-understand status.
    """

    progress = preparation_progress(

        job_role,

        candidate_skills

    )

    if progress >= 90:

        return "Interview Ready"

    elif progress >= 75:

        return "Almost Ready"

    elif progress >= 60:

        return "Preparing Well"

    elif progress >= 40:

        return "Needs More Practice"

    return "Begin Preparation"


# ==========================================================
# Interview Preparation Summary
# ==========================================================

def interview_preparation_summary(
    job_role,
    candidate_skills
):
    """
    Return a summarized preparation report.
    """

    gap = interview_skill_gap_analysis(

        job_role,

        candidate_skills

    )

    return {

        "Job_Role":

            job_role,

        "Coverage":

            gap["Coverage"],

        "Gap":

            gap["Gap"],

        "Matched_Skills":

            len(
                gap["Matched_Skills"]
            ),

        "Missing_Skills":

            len(
                gap["Missing_Skills"]
            ),

        "Preparation_Status":

            preparation_status(

                job_role,

                candidate_skills

            ),

        "Readiness_Level":

            readiness_level(

                interview_readiness_score(

                    job_role,

                    candidate_skills

                )

            )

    }


# ==========================================================
# End of Part 2B-1B(1B)
# ==========================================================
# ==========================================================
# Mock Interview Planner
# Part 2B-1B(2A)
# ==========================================================

def create_mock_interview_plan(
    job_role,
    candidate_skills,
    total_questions=20
):
    """
    Create a structured mock interview plan
    based on the candidate profile.
    """

    recommendations = recommend_interview_questions(

        job_role=job_role,

        candidate_skills=candidate_skills,

        top_n=total_questions

    )

    if recommendations.empty:

        return pd.DataFrame()

    plan = recommendations.copy()

    plan.insert(

        0,

        "Question_Number",

        range(

            1,

            len(plan) + 1

        )

    )

    plan["Status"] = "Not Attempted"

    plan["Candidate_Score"] = 0

    plan["Max_Score"] = 10

    return plan.reset_index(drop=True)


# ==========================================================
# Technical Interview Plan
# ==========================================================

def technical_mock_interview(
    job_role,
    candidate_skills,
    total_questions=10
):
    """
    Generate a technical mock interview.
    """

    return recommend_interview_questions(

        job_role=job_role,

        candidate_skills=candidate_skills,

        question_type="Technical",

        top_n=total_questions

    )


# ==========================================================
# HR Interview Plan
# ==========================================================

def hr_mock_interview(
    job_role,
    candidate_skills,
    total_questions=10
):
    """
    Generate HR interview questions.
    """

    return recommend_interview_questions(

        job_role=job_role,

        candidate_skills=candidate_skills,

        question_type="HR",

        top_n=total_questions

    )


# ==========================================================
# Behavioral Interview Plan
# ==========================================================

def behavioral_mock_interview(
    job_role,
    candidate_skills,
    total_questions=10
):
    """
    Generate behavioral interview questions.
    """

    return recommend_interview_questions(

        job_role=job_role,

        candidate_skills=candidate_skills,

        question_type="Behavioral",

        top_n=total_questions

    )


# ==========================================================
# Scenario-Based Interview Plan
# ==========================================================

def scenario_mock_interview(
    job_role,
    candidate_skills,
    total_questions=10
):
    """
    Generate scenario-based interview questions.
    """

    return recommend_interview_questions(

        job_role=job_role,

        candidate_skills=candidate_skills,

        question_type="Scenario",

        top_n=total_questions

    )


# ==========================================================
# Coding Interview Plan
# ==========================================================

def coding_mock_interview(
    job_role,
    candidate_skills,
    total_questions=10
):
    """
    Generate coding interview questions.
    """

    return recommend_interview_questions(

        job_role=job_role,

        candidate_skills=candidate_skills,

        question_type="Coding",

        top_n=total_questions

    )


# ==========================================================
# End of Part 2B-1B(2A)
# ==========================================================
# ==========================================================
# Mock Interview Evaluation
# Part 2B-1B(2B)
# ==========================================================

def calculate_mock_interview_score(
    mock_interview_df
):
    """
    Calculate the overall score obtained in
    a completed mock interview.
    """

    if mock_interview_df.empty:

        return {

            "Obtained_Score": 0,

            "Maximum_Score": 0,

            "Percentage": 0.0

        }

    obtained_score = float(

        mock_interview_df["Candidate_Score"].sum()

    )

    maximum_score = float(

        mock_interview_df["Max_Score"].sum()

    )

    if maximum_score == 0:

        percentage = 0.0

    else:

        percentage = round(

            (

                obtained_score /

                maximum_score

            ) * 100,

            2

        )

    return {

        "Obtained_Score":

            obtained_score,

        "Maximum_Score":

            maximum_score,

        "Percentage":

            percentage

    }


# ==========================================================
# Mock Interview Result
# ==========================================================

def mock_interview_result(
    percentage
):
    """
    Convert interview score into
    an evaluation result.
    """

    if percentage >= 90:

        return "Outstanding"

    elif percentage >= 80:

        return "Excellent"

    elif percentage >= 70:

        return "Good"

    elif percentage >= 60:

        return "Average"

    elif percentage >= 50:

        return "Needs Improvement"

    return "Poor"


# ==========================================================
# Question-wise Performance
# ==========================================================

def question_performance(
    mock_interview_df
):
    """
    Return question-wise interview
    performance.
    """

    if mock_interview_df.empty:

        return pd.DataFrame()

    performance = mock_interview_df.copy()

    performance["Score_%"] = (

        performance["Candidate_Score"] /

        performance["Max_Score"]

    ) * 100

    performance["Score_%"] = (

        performance["Score_%"]

        .round(2)

    )

    return performance


# ==========================================================
# Weak Interview Areas
# ==========================================================

def weak_interview_areas(
    mock_interview_df,
    threshold=60
):
    """
    Identify weak interview areas based
    on the obtained score.
    """

    if mock_interview_df.empty:

        return pd.DataFrame()

    performance = question_performance(

        mock_interview_df

    )

    weak = performance[

        performance["Score_%"] < threshold

    ]

    return weak.reset_index(

        drop=True

    )


# ==========================================================
# Strong Interview Areas
# ==========================================================

def strong_interview_areas(
    mock_interview_df,
    threshold=80
):
    """
    Identify strong interview areas.
    """

    if mock_interview_df.empty:

        return pd.DataFrame()

    performance = question_performance(

        mock_interview_df

    )

    strong = performance[

        performance["Score_%"] >= threshold

    ]

    return strong.reset_index(

        drop=True

    )


# ==========================================================
# Overall Mock Interview Report
# ==========================================================

def mock_interview_report(
    mock_interview_df
):
    """
    Generate a complete mock interview
    performance report.
    """

    score = calculate_mock_interview_score(

        mock_interview_df

    )

    return {

        "Obtained_Score":

            score["Obtained_Score"],

        "Maximum_Score":

            score["Maximum_Score"],

        "Percentage":

            score["Percentage"],

        "Result":

            mock_interview_result(

                score["Percentage"]

            ),

        "Weak_Questions":

            len(

                weak_interview_areas(

                    mock_interview_df

                )

            ),

        "Strong_Questions":

            len(

                strong_interview_areas(

                    mock_interview_df

                )

            )

    }


# ==========================================================
# End of Part 2B-1B(2B)
# ==========================================================
# ==========================================================
# AI Interview Feedback Engine
# Part 2B-2A
# ==========================================================

def generate_question_feedback(
    obtained_score,
    max_score=10
):
    """
    Generate AI feedback for an interview answer
    based on the obtained score.
    """

    if max_score <= 0:

        return "Invalid score."

    percentage = (

        obtained_score /

        max_score

    ) * 100

    if percentage >= 90:

        return (
            "Outstanding answer. The response demonstrates "
            "excellent technical understanding, confidence, "
            "clarity, and communication."
        )

    elif percentage >= 80:

        return (
            "Very good answer. Minor improvements in depth "
            "or examples would make the response stronger."
        )

    elif percentage >= 70:

        return (
            "Good answer. The fundamentals are correct, "
            "but additional technical explanation would help."
        )

    elif percentage >= 60:

        return (
            "Average answer. Review the topic again and "
            "practice explaining concepts with examples."
        )

    elif percentage >= 40:

        return (
            "Weak answer. Significant improvement is needed "
            "before attending interviews."
        )

    return (
        "Poor answer. Learn the concept from scratch "
        "and practice multiple interview questions."
    )


# ==========================================================
# Evaluate Individual Answers
# ==========================================================

def evaluate_mock_answers(
    mock_interview_df
):
    """
    Generate AI feedback for every
    interview question.
    """

    if mock_interview_df.empty:

        return pd.DataFrame()

    evaluation = mock_interview_df.copy()

    evaluation["Feedback"] = evaluation.apply(

        lambda row:

        generate_question_feedback(

            row["Candidate_Score"],

            row["Max_Score"]

        ),

        axis=1

    )

    return evaluation


# ==========================================================
# Overall Interview Feedback
# ==========================================================

def overall_interview_feedback(
    percentage
):
    """
    Generate overall interview feedback.
    """

    if percentage >= 90:

        return (
            "You are interview-ready. Continue practicing "
            "advanced questions and company-specific rounds."
        )

    elif percentage >= 80:

        return (
            "Your interview preparation is strong. Focus on "
            "improving communication and problem-solving speed."
        )

    elif percentage >= 70:

        return (
            "Good preparation. Revise weak concepts and "
            "practice additional mock interviews."
        )

    elif percentage >= 60:

        return (
            "You have a reasonable foundation but should "
            "strengthen technical knowledge before interviews."
        )

    elif percentage >= 40:

        return (
            "Your preparation requires significant effort. "
            "Create a structured learning plan and practice daily."
        )

    return (
        "Interview readiness is currently low. Begin with "
        "core concepts and gradually progress to mock interviews."
    )


# ==========================================================
# AI Performance Summary
# ==========================================================

def interview_performance_summary(
    mock_interview_df
):
    """
    Generate an AI summary of the mock interview.
    """

    report = mock_interview_report(

        mock_interview_df

    )

    return {

        **report,

        "AI_Feedback":

            overall_interview_feedback(

                report["Percentage"]

            )

    }


# ==========================================================
# Performance Improvement Suggestions
# ==========================================================

def improvement_suggestions(
    mock_interview_df
):
    """
    Generate improvement suggestions based
    on weak interview performance.
    """

    weak = weak_interview_areas(

        mock_interview_df

    )

    if weak.empty:

        return [

            "Continue solving advanced interview questions.",

            "Participate in company-specific mock interviews.",

            "Improve communication and presentation skills."

        ]

    suggestions = []

    for _, row in weak.iterrows():

        suggestions.append(

            f"Improve {row['Skill']} by practicing "
            f"more {row['Question_Type']} interview questions."

        )

    return suggestions


# ==========================================================
# End of Part 2B-2A
# ==========================================================
# ==========================================================
# AI Interview Coach
# Part 2B-2B
# ==========================================================

def interview_confidence_score(
    mock_interview_df
):
    """
    Estimate interview confidence based on
    mock interview performance.
    """

    if mock_interview_df.empty:

        return 0.0

    report = mock_interview_report(

        mock_interview_df

    )

    confidence = report["Percentage"]

    return round(

        confidence,

        2

    )


# ==========================================================
# Confidence Level
# ==========================================================

def confidence_level(
    confidence_score
):
    """
    Convert confidence score into
    a confidence level.
    """

    if confidence_score >= 90:

        return "Very High"

    elif confidence_score >= 80:

        return "High"

    elif confidence_score >= 70:

        return "Moderate"

    elif confidence_score >= 60:

        return "Low"

    return "Very Low"


# ==========================================================
# Interview Coaching Tips
# ==========================================================

def interview_coaching_tips(
    confidence_score
):
    """
    Return coaching tips based on
    interview confidence.
    """

    if confidence_score >= 90:

        return [

            "Maintain consistency in mock interviews.",

            "Focus on company-specific interview rounds.",

            "Revise important projects before interviews.",

            "Practice leadership and behavioral questions."

        ]

    elif confidence_score >= 80:

        return [

            "Strengthen system design and scenario questions.",

            "Improve response structure using STAR method.",

            "Practice explaining technical concepts clearly.",

            "Revise important algorithms and SQL."

        ]

    elif confidence_score >= 70:

        return [

            "Practice one mock interview daily.",

            "Improve coding speed.",

            "Review weak technical topics.",

            "Prepare project explanations."

        ]

    elif confidence_score >= 60:

        return [

            "Study missing interview skills.",

            "Solve beginner and intermediate questions.",

            "Improve communication skills.",

            "Practice HR interview questions."

        ]

    return [

        "Build strong technical fundamentals.",

        "Complete beginner interview preparation.",

        "Watch interview demonstrations.",

        "Take regular mock interviews.",

        "Revise resume projects thoroughly."

    ]


# ==========================================================
# Personalized Weekly Plan
# ==========================================================

def weekly_interview_plan(
    job_role,
    candidate_skills
):
    """
    Generate a personalized seven-day
    interview preparation schedule.
    """

    roadmap = interview_preparation_roadmap(

        job_role,

        candidate_skills

    )

    days = [

        "Day 1",

        "Day 2",

        "Day 3",

        "Day 4",

        "Day 5",

        "Day 6",

        "Day 7"

    ]

    schedule = []

    for index, day in enumerate(days):

        if index < len(roadmap):

            task = roadmap[index]["Skill"]

        else:

            task = "Mock Interview Practice"

        schedule.append({

            "Day":

                day,

            "Focus":

                task

        })

    return pd.DataFrame(

        schedule

    )


# ==========================================================
# Final AI Coaching Report
# ==========================================================

def ai_interview_coach(
    job_role,
    candidate_skills,
    mock_interview_df
):
    """
    Generate a complete AI interview
    coaching report.
    """

    report = interview_performance_summary(

        mock_interview_df

    )

    confidence = interview_confidence_score(

        mock_interview_df

    )

    return {

        "Interview_Readiness":

            readiness_level(

                interview_readiness_score(

                    job_role,

                    candidate_skills

                )

            ),

        "Confidence_Score":

            confidence,

        "Confidence_Level":

            confidence_level(

                confidence

            ),

        "Performance":

            report,

        "Improvement_Suggestions":

            improvement_suggestions(

                mock_interview_df

            ),

        "Coaching_Tips":

            interview_coaching_tips(

                confidence

            ),

        "Weekly_Plan":

            weekly_interview_plan(

                job_role,

                candidate_skills

            )

    }


# ==========================================================
# End of Part 2B-2B
# ==========================================================
import json
from pathlib import Path


# ==========================================================
# Format Interview Report
# ==========================================================

def format_interview_report(
    job_role,
    candidate_skills,
    mock_interview_df
):
    """
    Generate a comprehensive interview report.

    Returns
    -------
    dict
        Complete interview report.
    """

    readiness_score = interview_readiness_score(

        job_role,

        candidate_skills

    )

    readiness = readiness_level(

        readiness_score

    )

    skill_gap = interview_skill_gap_analysis(

        job_role,

        candidate_skills

    )

    preparation = interview_preparation_summary(

        job_role,

        candidate_skills

    )

    coach = ai_interview_coach(

        job_role,

        candidate_skills,

        mock_interview_df

    )

    mock_report = mock_interview_report(

        mock_interview_df

    )

    statistics = interview_statistics()

    report = {

        "Candidate_Profile": {

            "Job_Role":

                job_role,

            "Candidate_Skills":

                sorted(

                    validate_candidate_skills(

                        candidate_skills

                    )

                )

        },

        "Interview_Readiness": {

            "Readiness_Score":

                readiness_score,

            "Readiness_Level":

                readiness

        },

        "Skill_Gap_Analysis":

            skill_gap,

        "Preparation_Summary":

            preparation,

        "Mock_Interview_Report":

            mock_report,

        "AI_Coaching":

            coach,

        "Interview_Statistics":

            statistics

    }

    return report


# ==========================================================
# Report Summary
# ==========================================================

def interview_report_summary(
    report
):
    """
    Return a concise report summary.
    """

    return {

        "Job_Role":

            report["Candidate_Profile"]["Job_Role"],

        "Readiness":

            report["Interview_Readiness"]["Readiness_Level"],

        "Coverage":

            report["Skill_Gap_Analysis"]["Coverage"],

        "Missing_Skills":

            len(

                report["Skill_Gap_Analysis"][
                    "Missing_Skills"
                ]

            ),

        "Interview_Percentage":

            report[
                "Mock_Interview_Report"
            ][
                "Percentage"
            ]

    }


# ==========================================================
# Report Validation
# ==========================================================

def validate_interview_report(
    report
):
    """
    Validate generated report.
    """

    required_sections = [

        "Candidate_Profile",

        "Interview_Readiness",

        "Skill_Gap_Analysis",

        "Preparation_Summary",

        "Mock_Interview_Report",

        "AI_Coaching",

        "Interview_Statistics"

    ]

    missing = [

        item

        for item in required_sections

        if item not in report

    ]

    return {

        "Valid":

            len(

                missing

            ) == 0,

        "Missing_Sections":

            missing

    }


# ==========================================================
# End Part 3A-1
# ==========================================================
# ==========================================================
# Print Interview Report
# Part 3A-2
# ==========================================================

def print_interview_report(
    report
):
    """
    Pretty print the complete interview report.
    """

    print("\n" + "=" * 70)
    print("AI RESUME ANALYZER - INTERVIEW REPORT")
    print("=" * 70)

    print("\nCandidate Profile")
    print("-" * 70)

    profile = report["Candidate_Profile"]

    print(
        f"Target Job Role : {profile['Job_Role']}"
    )

    print(
        "Candidate Skills : "
    )

    for skill in profile["Candidate_Skills"]:

        print(f"  • {skill}")

    print("\nInterview Readiness")
    print("-" * 70)

    readiness = report["Interview_Readiness"]

    print(

        f"Readiness Score : "
        f"{readiness['Readiness_Score']}"

    )

    print(

        f"Readiness Level : "
        f"{readiness['Readiness_Level']}"

    )

    print("\nSkill Gap Analysis")
    print("-" * 70)

    gap = report["Skill_Gap_Analysis"]

    print(

        f"Coverage : "
        f"{gap['Coverage']} %"

    )

    print(

        f"Gap : "
        f"{gap['Gap']} %"

    )

    print(

        f"Matched Skills : "
        f"{len(gap['Matched_Skills'])}"

    )

    print(

        f"Missing Skills : "
        f"{len(gap['Missing_Skills'])}"

    )

    if gap["Missing_Skills"]:

        print("\nMissing Skills")

        for skill in gap["Missing_Skills"]:

            print(

                f"   - {skill}"

            )

    print("\nPreparation Summary")
    print("-" * 70)

    prep = report["Preparation_Summary"]

    print(

        f"Preparation Status : "
        f"{prep['Preparation_Status']}"

    )

    print(

        f"Coverage : "
        f"{prep['Coverage']} %"

    )

    print(

        f"Readiness Level : "
        f"{prep['Readiness_Level']}"

    )

    print("\nMock Interview")
    print("-" * 70)

    mock = report["Mock_Interview_Report"]

    print(

        f"Obtained Score : "
        f"{mock['Obtained_Score']}"

    )

    print(

        f"Maximum Score : "
        f"{mock['Maximum_Score']}"

    )

    print(

        f"Percentage : "
        f"{mock['Percentage']} %"

    )

    print(

        f"Result : "
        f"{mock['Result']}"

    )

    print("\nAI Coaching")
    print("-" * 70)

    coach = report["AI_Coaching"]

    print(

        f"Confidence Score : "
        f"{coach['Confidence_Score']}"

    )

    print(

        f"Confidence Level : "
        f"{coach['Confidence_Level']}"

    )

    print("\nImprovement Suggestions")

    for suggestion in coach["Improvement_Suggestions"]:

        print(

            f"  • {suggestion}"

        )

    print("\nCoaching Tips")

    for tip in coach["Coaching_Tips"]:

        print(

            f"  • {tip}"

        )

    print("\nDataset Statistics")
    print("-" * 70)

    stats = report["Interview_Statistics"]

    for key, value in stats.items():

        print(

            f"{key.replace('_', ' ')} : {value}"

        )

    print("\n" + "=" * 70)
    print("End of Interview Report")
    print("=" * 70)


# ==========================================================
# Export Interview Report (JSON)
# ==========================================================

def export_interview_report(
    report,
    output_dir="reports",
    filename="interview_report.json"
):
    """
    Export interview report as JSON.
    """

    output_dir = Path(

        output_dir

    )

    output_dir.mkdir(

        parents=True,

        exist_ok=True

    )

    file_path = output_dir / filename

    with open(

        file_path,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            report,

            file,

            indent=4,

            ensure_ascii=False,

            default=str

        )

    return str(

        file_path

    )


# ==========================================================
# Export Summary Report
# ==========================================================

def export_interview_summary(
    report,
    output_dir="reports",
    filename="interview_summary.json"
):
    """
    Export summarized interview report.
    """

    summary = interview_report_summary(

        report

    )

    output_dir = Path(

        output_dir

    )

    output_dir.mkdir(

        parents=True,

        exist_ok=True

    )

    file_path = output_dir / filename

    with open(

        file_path,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            summary,

            file,

            indent=4,

            ensure_ascii=False

        )

    return str(

        file_path

    )


# ==========================================================
# End of Part 3A-2
# ==========================================================
# ==========================================================
# Interview Analytics
# Part 3B-1
# ==========================================================

def interview_statistics():
    """
    Return overall interview dataset statistics.
    """

    if INTERVIEW_DF.empty:

        return {}

    return {

        "Total_Questions":

            int(

                len(INTERVIEW_DF)

            ),

        "Total_Job_Roles":

            int(

                INTERVIEW_DF[
                    "Job_Role"
                ].nunique()

            ),

        "Total_Skills":

            int(

                len(

                    get_unique_skills()

                )

            ),

        "Difficulty_Levels":

            int(

                INTERVIEW_DF[
                    "Difficulty"
                ].nunique()

            ),

        "Question_Types":

            int(

                INTERVIEW_DF[
                    "Question_Type"
                ].nunique()

            )

    }


# ==========================================================
# Top Interview Skills
# ==========================================================

def top_interview_skills(
    top_n=20
):
    """
    Return the most frequently occurring
    interview skills.
    """

    if INTERVIEW_DF.empty:

        return pd.DataFrame()

    skill_frequency = {}

    for skill_set in INTERVIEW_DF["skill_set"]:

        for skill in skill_set:

            skill_frequency[skill] = (

                skill_frequency.get(

                    skill,

                    0

                ) + 1

            )

    ranking = (

        pd.DataFrame(

            {

                "Skill":

                    list(

                        skill_frequency.keys()

                    ),

                "Frequency":

                    list(

                        skill_frequency.values()

                    )

            }

        )

        .sort_values(

            by="Frequency",

            ascending=False

        )

        .head(top_n)

        .reset_index(

            drop=True

        )

    )

    return ranking


# ==========================================================
# Top Job Roles
# ==========================================================

def top_job_roles(
    top_n=20
):
    """
    Return job roles having the
    highest number of interview
    questions.
    """

    if INTERVIEW_DF.empty:

        return pd.DataFrame()

    ranking = (

        INTERVIEW_DF

        .groupby(

            "Job_Role"

        )

        .size()

        .reset_index(

            name="Questions"

        )

        .sort_values(

            by="Questions",

            ascending=False

        )

        .head(

            top_n

        )

        .reset_index(

            drop=True

        )

    )

    return ranking


# ==========================================================
# Job Role Coverage
# ==========================================================

def job_role_question_count():
    """
    Return question count
    for every job role.
    """

    if INTERVIEW_DF.empty:

        return pd.DataFrame()

    return (

        INTERVIEW_DF

        .groupby(

            "Job_Role"

        )

        .size()

        .reset_index(

            name="Question_Count"

        )

        .sort_values(

            by="Question_Count",

            ascending=False

        )

        .reset_index(

            drop=True

        )

    )


# ==========================================================
# Skill Frequency Dictionary
# ==========================================================

def skill_frequency_dictionary():
    """
    Return skill frequencies
    as a dictionary.
    """

    frequency = {}

    if INTERVIEW_DF.empty:

        return frequency

    for skill_set in INTERVIEW_DF["skill_set"]:

        for skill in skill_set:

            frequency[skill] = (

                frequency.get(

                    skill,

                    0

                ) + 1

            )

    return dict(

        sorted(

            frequency.items(),

            key=lambda item: item[1],

            reverse=True

        )

    )


# ==========================================================
# End of Part 3B-1
# ==========================================================
# ==========================================================
# Difficulty Distribution
# Part 3B-2
# ==========================================================

def difficulty_distribution():
    """
    Return the distribution of interview
    question difficulty levels.
    """

    if INTERVIEW_DF.empty:

        return pd.DataFrame()

    distribution = (

        INTERVIEW_DF

        .groupby(

            "Difficulty"

        )

        .size()

        .reset_index(

            name="Count"

        )

        .sort_values(

            by="Count",

            ascending=False

        )

        .reset_index(

            drop=True

        )

    )

    total = distribution["Count"].sum()

    distribution["Percentage"] = (

        distribution["Count"]

        / total

        * 100

    ).round(2)

    return distribution


# ==========================================================
# Question Type Distribution
# ==========================================================

def question_type_distribution():
    """
    Return the distribution of interview
    question types.
    """

    if INTERVIEW_DF.empty:

        return pd.DataFrame()

    distribution = (

        INTERVIEW_DF

        .groupby(

            "Question_Type"

        )

        .size()

        .reset_index(

            name="Count"

        )

        .sort_values(

            by="Count",

            ascending=False

        )

        .reset_index(

            drop=True

        )

    )

    total = distribution["Count"].sum()

    distribution["Percentage"] = (

        distribution["Count"]

        / total

        * 100

    ).round(2)

    return distribution


# ==========================================================
# Job Role Distribution
# ==========================================================

def job_role_distribution():
    """
    Return the distribution of
    interview questions by job role.
    """

    if INTERVIEW_DF.empty:

        return pd.DataFrame()

    distribution = (

        INTERVIEW_DF

        .groupby(

            "Job_Role"

        )

        .size()

        .reset_index(

            name="Count"

        )

        .sort_values(

            by="Count",

            ascending=False

        )

        .reset_index(

            drop=True

        )

    )

    total = distribution["Count"].sum()

    distribution["Percentage"] = (

        distribution["Count"]

        / total

        * 100

    ).round(2)

    return distribution


# ==========================================================
# Skill Distribution
# ==========================================================

def skill_distribution():
    """
    Return interview skill
    frequency distribution.
    """

    if INTERVIEW_DF.empty:

        return pd.DataFrame()

    frequency = skill_frequency_dictionary()

    distribution = pd.DataFrame(

        {

            "Skill":

                list(

                    frequency.keys()

                ),

            "Count":

                list(

                    frequency.values()

                )

        }

    )

    total = distribution["Count"].sum()

    distribution["Percentage"] = (

        distribution["Count"]

        / total

        * 100

    ).round(2)

    return distribution.reset_index(

        drop=True

    )


# ==========================================================
# Complete Dataset Analytics
# ==========================================================

def interview_dataset_analytics():
    """
    Generate complete analytics for the
    interview dataset.
    """

    return {

        "Statistics":

            interview_statistics(),

        "Top_Skills":

            top_interview_skills(),

        "Top_Job_Roles":

            top_job_roles(),

        "Difficulty_Distribution":

            difficulty_distribution(),

        "Question_Type_Distribution":

            question_type_distribution(),

        "Job_Role_Distribution":

            job_role_distribution(),

        "Skill_Distribution":

            skill_distribution()

    }


# ==========================================================
# End of Part 3B-2
# ==========================================================
# ==========================================================
# Engine Validation
# Part 3C
# ==========================================================

def validate_interview_engine():
    """
    Validate the interview engine configuration.
    """

    validation = {

        "Dataset_Loaded": not INTERVIEW_DF.empty,

        "Dataset_Rows": len(INTERVIEW_DF),

        "Dataset_Columns": list(INTERVIEW_DF.columns),

        "Total_Job_Roles": len(get_unique_job_roles()),

        "Total_Skills": len(get_unique_skills()),

        "Total_Difficulty_Levels": len(
            get_unique_difficulties()
        ),

        "Total_Question_Types": len(
            get_unique_question_types()
        )

    }

    return validation


# ==========================================================
# Smoke Test
# ==========================================================

def run_interview_engine_tests():
    """
    Execute production smoke tests.
    """

    print("\n" + "=" * 70)
    print("Running Interview Engine Validation")
    print("=" * 70)

    validation = validate_interview_engine()

    for key, value in validation.items():

        print(

            f"{key:<30}: {value}"

        )

    assert validation["Dataset_Loaded"], \
        "Interview dataset failed to load."

    assert validation["Dataset_Rows"] > 0, \
        "Dataset is empty."

    print("\nEngine validation completed successfully.")

    return True


# ==========================================================
# Sample Execution
# ==========================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("AI Resume Analyzer")
    print("Interview Preparation Engine")
    print("=" * 70)

    run_interview_engine_tests()

    sample_job_role = "Data Scientist"

    sample_candidate_skills = [

        "Python",

        "SQL",

        "Machine Learning",

        "Pandas",

        "NumPy",

        "Statistics"

    ]

    print("\nGenerating Interview Recommendations...")

    recommendations = recommend_interview_questions(

        job_role=sample_job_role,

        candidate_skills=sample_candidate_skills,

        top_n=10

    )

    print(

        f"Questions Recommended : "

        f"{len(recommendations)}"

    )

    readiness = interview_readiness_score(

        sample_job_role,

        sample_candidate_skills

    )

    print(

        f"Interview Readiness : "

        f"{readiness}"

    )

    mock_plan = create_mock_interview_plan(

        sample_job_role,

        sample_candidate_skills,

        total_questions=10

    )

    if not mock_plan.empty:

        mock_plan["Candidate_Score"] = 8

        report = format_interview_report(

            sample_job_role,

            sample_candidate_skills,

            mock_plan

        )

        print_interview_report(

            report

        )

        report_path = export_interview_report(

            report

        )

        summary_path = export_interview_summary(

            report

        )

        print(

            "\nInterview report saved to:",

            report_path

        )

        print(

            "Interview summary saved to:",

            summary_path

        )

    print("\nTop Interview Skills")

    print(

        top_interview_skills()

    )

    print("\nTop Job Roles")

    print(

        top_job_roles()

    )

    print("\nDifficulty Distribution")

    print(

        difficulty_distribution()

    )

    print("\nQuestion Type Distribution")

    print(

        question_type_distribution()

    )

    print("\nDataset Statistics")

    print(

        interview_statistics()

    )

    print("\n" + "=" * 70)
    print("Interview Engine Completed Successfully")
    print("Version 2.0")
    print("=" * 70)