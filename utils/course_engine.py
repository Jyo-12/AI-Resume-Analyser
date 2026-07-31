 #==========================================================
# Course Recommendation Engine
# ==========================================================
import re
 
import pandas as pd
 
from typing import Set
 
from utils.database import load_courses
 
 
# ==========================================================
# Configuration
# ==========================================================
 
DEFAULT_TOP_N = 5
 
 
# ==========================================================
# Text Normalization
# ==========================================================
 
def normalize_text(value) -> str:
    """
    Normalize any text-like value into a clean,
    lowercase, whitespace-trimmed string.
 
    Handles None / NaN / non-string input gracefully so
    downstream comparisons never raise.
    """
 
    if value is None:
        return ""
 
    if isinstance(value, float) and pd.isna(value):
        return ""
 
    text = str(value).strip().lower()
 
    if text in ("nan", "none", "n/a", ""):
        return ""
 
    return text
 
 
# ==========================================================
# Skill Set Parsing
# ==========================================================
 
def parse_skill_set(value) -> Set[str]:
    """
    Parse a raw, comma-separated "Skill" field into a
    normalized set of individual skills.
    """
 
    text = normalize_text(value)
 
    if not text:
        return set()
 
    skills = {
        skill.strip()
        for skill in text.split(",")
        if skill.strip()
    }
 
    return skills
 
 
def validate_candidate_skills(skills) -> Set[str]:
    """
    Normalize a user-supplied collection of skills
    (set, list, tuple, or None) into a clean set of
    lowercase, trimmed skill strings.
    """
 
    if not skills:
        return set()
 
    return {
        normalize_text(skill)
        for skill in skills
        if normalize_text(skill)
    }
 
 
# ==========================================================
# Skill Comparison Helpers
# ==========================================================
 
def matched_skills(candidate_skills: Set[str], course_skills: Set[str]):
    """
    Skills the candidate already has that this course
    also covers.
    """
 
    return sorted(candidate_skills & course_skills)
 
 
def new_skills(candidate_skills: Set[str], course_skills: Set[str]):
    """
    Skills this course teaches that the candidate
    doesn't already know.
    """
 
    return sorted(course_skills - candidate_skills)
 
 
def skill_match_percentage(candidate_skills: Set[str], course_skills: Set[str]) -> float:
    """
    Percentage of the course's skills the candidate
    already knows.
    """
 
    if not course_skills:
        return 0.0
 
    overlap = len(candidate_skills & course_skills)
 
    return round((overlap / len(course_skills)) * 100, 2)
 
 
# ==========================================================
# Course Dataset
# ==========================================================
 
def build_course_dataframe() -> pd.DataFrame:
    """
    Load raw course data and enrich it with the
    normalized columns the rest of this module relies on.
    """
 
    df = load_courses()
 
    if df is None or df.empty:
        return pd.DataFrame()
 
    df = df.copy()
 
    df["skill_set"] = df["Skill"].apply(parse_skill_set)
    df["career_path_clean"] = df["Career_Path"].apply(normalize_text)
    df["difficulty_clean"] = df["Difficulty"].apply(normalize_text)
    df["platform_clean"] = df["Platform"].apply(normalize_text)
 
    return df
 
 
COURSE_DF = build_course_dataframe()
 
 
# ==========================================================
# Platform Ranking
# ==========================================================
 
PLATFORM_SCORE = {
 
    "coursera": 100,
    "edx": 98,
    "udacity": 96,
    "deeplearning.ai": 96,
    "google": 95,
    "ibm": 94,
    "microsoft": 94,
    "aws": 93,
    "oracle": 92,
    "datacamp": 91,
    "linkedin learning": 90,
    "simplilearn": 88,
    "udemy": 86,
    "great learning": 85,
    "nptel": 84,
    "youtube": 75
 
}
 
 
def platform_score(platform):
    """
    Return score based on platform quality.
    """
 
    platform = normalize_text(platform)
 
    return PLATFORM_SCORE.get(platform, 70)
 
 
# ==========================================================
# Difficulty Ranking
# ==========================================================
 
DIFFICULTY_SCORE = {
 
    "beginner": 100,
    "intermediate": 90,
    "advanced": 80,
    "expert": 70
 
}
 
 
def difficulty_score(level):
    """
    Beginner courses are recommended first.
    """
 
    level = normalize_text(level)
 
    return DIFFICULTY_SCORE.get(level, 80)
 
 
# ==========================================================
# Certificate Score
# ==========================================================
 
CERTIFICATE_SCORE = {
 
    "yes": 100,
    "available": 100,
    "true": 100,
    "certificate": 100,
 
    "no": 50,
    "false": 50
 
}
 
 
def certificate_score(value):
    """
    Give preference to certified courses.
    """
 
    value = normalize_text(value)
 
    return CERTIFICATE_SCORE.get(value, 75)
 
 
# ==========================================================
# Duration Conversion
# ==========================================================
 
def duration_hours(duration):
    """
    Convert duration to approximate hours.
 
    Examples
 
    8 Hours
    5 Weeks
    2 Months
    """
 
    if duration is None or (isinstance(duration, float) and pd.isna(duration)):
        return 0
 
    duration = normalize_text(duration)
 
    numbers = re.findall(r"\d+\.?\d*", duration)
 
    if len(numbers) == 0:
        return 0
 
    value = float(numbers[0])
 
    if "hour" in duration:
        return value
 
    elif "day" in duration:
        return value * 8
 
    elif "week" in duration:
        return value * 40
 
    elif "month" in duration:
        return value * 160
 
    return value
 
 
# ==========================================================
# Duration Score
# ==========================================================
 
def duration_score(duration):
    """
    Shorter courses receive higher scores.
    """
 
    hrs = duration_hours(duration)
 
    if hrs <= 10:
        return 100
 
    elif hrs <= 20:
        return 95
 
    elif hrs <= 40:
        return 90
 
    elif hrs <= 80:
        return 85
 
    elif hrs <= 160:
        return 75
 
    return 65
 
 
# ==========================================================
# Career Path Similarity
# ==========================================================
 
def career_path_score(
    desired_path,
    course_path
):
    """
    Compare candidate career path
    with course career path.
    """
 
    desired = normalize_text(desired_path)
 
    course = normalize_text(course_path)
 
    if desired == "" or course == "":
        return 60
 
    if desired == course:
        return 100
 
    if desired in course:
        return 90
 
    if course in desired:
        return 90
 
    desired_words = set(desired.split())
 
    course_words = set(course.split())
 
    if not course_words:
        return 50
 
    overlap = len(
        desired_words &
        course_words
    )
 
    if overlap == 0:
        return 50
 
    return round(
 
        (overlap / len(course_words)) * 100,
 
        2
 
    )
 
 
# ==========================================================
# Search Courses by Skill
# ==========================================================
 
def search_courses_by_skill(skill):
    """
    Return all courses teaching
    a particular skill.
    """
 
    skill = normalize_text(skill)
 
    if COURSE_DF.empty:
        return pd.DataFrame()
 
    return COURSE_DF[
 
        COURSE_DF["skill_set"].apply(
 
            lambda x: skill in x
 
        )
 
    ]
 
 
# ==========================================================
# Search Courses by Career Path
# ==========================================================
 
def search_courses_by_career(career):
    """
    Return courses matching
    career path.
    """
 
    career = normalize_text(career)
 
    if COURSE_DF.empty:
        return pd.DataFrame()
 
    return COURSE_DF[
 
        COURSE_DF["career_path_clean"].str.contains(
 
            career,
 
            na=False
 
        )
 
    ]
 
 
# ==========================================================
# Filter Courses
# ==========================================================
 
def filter_courses(
 
    difficulty=None,
 
    platform=None,
 
    certificate=None
 
):
    """
    Filter course dataset.
    """
 
    df = COURSE_DF.copy()
 
    if difficulty:
 
        df = df[
 
            df["difficulty_clean"] ==
 
            normalize_text(difficulty)
 
        ]
 
    if platform:
 
        df = df[
 
            df["platform_clean"] ==
 
            normalize_text(platform)
 
        ]
 
    if certificate:
 
        df = df[
 
            df["Certificate"]
 
            .apply(normalize_text)
 
            .eq(
 
                normalize_text(certificate)
 
            )
 
        ]
 
    return df.reset_index(drop=True)
 
 
# ==========================================================
# Dataset Summary
# ==========================================================
 
def course_summary():
    """
    Quick statistics of
    course database.
    """
 
    if COURSE_DF.empty:
        return {}
 
    return {
 
        "total_courses":
 
            len(COURSE_DF),
 
        "platforms":
 
            COURSE_DF["Platform"]
 
            .nunique(),
 
        "career_paths":
 
            COURSE_DF["Career_Path"]
 
            .nunique(),
 
        "skills":
 
            len(
 
                set().union(
 
                    *COURSE_DF["skill_set"]
 
                )
 
            )
 
    }
 
 
# ==========================================================
# Course Skill Relevance
# ==========================================================
 
def relevance_score(
    candidate_skills: Set[str],
    missing_skills: Set[str],
    course_skills: Set[str]
) -> float:
    """
    Calculate how relevant a course is based on
    the candidate's missing skills.
    """
 
    if len(course_skills) == 0:
        return 0.0
 
    missing_match = len(course_skills & missing_skills)
    known_match = len(course_skills & candidate_skills)
 
    score = (
        (missing_match * 3) +
        (known_match * 1)
    ) / len(course_skills)
 
    # Cap at 100 so the final recommendation_score stays a
    # sane percentage instead of exceeding 100% when a course
    # is made up mostly of missing (x3-weighted) skills.
    return round(min(score * 100, 100.0), 2)
 
 
# ==========================================================
# Overall Recommendation Score
# ==========================================================
 
def recommendation_score(
    candidate_skills: Set[str],
    missing_skills: Set[str],
    desired_career: str,
    course: pd.Series
) -> float:
    """
    Calculate final recommendation score.
    """
 
    course_skills = course["skill_set"]
 
    relevance = relevance_score(
        candidate_skills,
        missing_skills,
        course_skills
    )
 
    platform = platform_score(
        course["Platform"]
    )
 
    difficulty = difficulty_score(
        course["Difficulty"]
    )
 
    duration = duration_score(
        course["Duration"]
    )
 
    certificate = certificate_score(
        course["Certificate"]
    )
 
    career = career_path_score(
        desired_career,
        course["Career_Path"]
    )
 
    score = (
 
        relevance * 0.45 +
 
        career * 0.20 +
 
        platform * 0.15 +
 
        difficulty * 0.10 +
 
        duration * 0.05 +
 
        certificate * 0.05
 
    )
 
    return round(score, 2)
 
 
# ==========================================================
# Recommendation Explanation
# ==========================================================
 
def recommendation_reason(
    candidate_skills: Set[str],
    missing_skills: Set[str],
    course: pd.Series
):
    """
    Generate recommendation explanation.
    """
 
    reasons = []
 
    learnable = sorted(
        course["skill_set"] &
        missing_skills
    )
 
    if learnable:
 
        reasons.append(
            "Teaches: " +
            ", ".join(learnable)
        )
 
    if normalize_text(course["Certificate"]) in [
        "yes",
        "available",
        "true",
        "certificate"
    ]:
 
        reasons.append(
            "Provides certificate."
        )
 
    reasons.append(
        f"Platform: {course['Platform']}"
    )
 
    reasons.append(
        f"Difficulty: {course['Difficulty']}"
    )
 
    reasons.append(
        f"Duration: {course['Duration']}"
    )
 
    return reasons
 
 
# ==========================================================
# Recommend Courses
# ==========================================================
 
def recommend_courses(
 
    candidate_skills,
 
    missing_skills,
 
    desired_career="",
 
    top_n=DEFAULT_TOP_N
 
):
    """
    Generate top course recommendations.
    """
 
    candidate_skills = validate_candidate_skills(
        candidate_skills
    )
 
    missing_skills = validate_candidate_skills(
        missing_skills
    )
 
    if COURSE_DF.empty:
        return []
 
    recommendations = []
 
    for _, course in COURSE_DF.iterrows():
 
        score = recommendation_score(
 
            candidate_skills,
 
            missing_skills,
 
            desired_career,
 
            course
 
        )
 
        recommendations.append({
 
            "course_id":
                course["Course_ID"],
 
            "course_name":
                course["Course_Name"],
 
            "platform":
                course["Platform"],
 
            "skill":
                course["Skill"],
 
            "difficulty":
                course["Difficulty"],
 
            "duration":
                course["Duration"],
 
            "certificate":
                course["Certificate"],
 
            "career_path":
                course["Career_Path"],
 
            "course_url":
                course["Course_URL"],
 
            "recommendation_score":
                score,
 
            "matched_skills":
                matched_skills(
                    candidate_skills,
                    course["skill_set"]
                ),
 
            "new_skills":
                new_skills(
                    candidate_skills,
                    course["skill_set"]
                ),
 
            "skill_match_percentage":
                skill_match_percentage(
                    candidate_skills,
                    course["skill_set"]
                ),
 
            "reason":
                recommendation_reason(
                    candidate_skills,
                    missing_skills,
                    course
                )
 
        })
 
    recommendations.sort(
 
        key=lambda x:
        x["recommendation_score"],
 
        reverse=True
 
    )
 
    return recommendations[:top_n]
 
 
# ==========================================================
# Best Recommended Course
# ==========================================================
 
def recommend_best_course(
 
    candidate_skills,
 
    missing_skills,
 
    desired_career=""
 
):
    """
    Return the highest ranked course.
    """
 
    courses = recommend_courses(
 
        candidate_skills,
 
        missing_skills,
 
        desired_career,
 
        top_n=1
 
    )
 
    if len(courses) == 0:
        return None
 
    return courses[0]
 
 
# ==========================================================
# Learning Path Generator
# ==========================================================
 
def generate_learning_path(
    recommendations
):
    """
    Arrange recommended courses from
    Beginner -> Intermediate -> Advanced.
    """
 
    if not recommendations:
        return []
 
    difficulty_order = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
        "expert": 4
    }
 
    ordered = sorted(
 
        recommendations,
 
        key=lambda x: (
 
            difficulty_order.get(
 
                normalize_text(
 
                    x["difficulty"]
 
                ),
 
                99
 
            ),
 
            -x["recommendation_score"]
 
        )
 
    )
 
    learning_path = []
 
    for index, course in enumerate(ordered, start=1):
 
        learning_path.append({
 
            "step": index,
 
            "course_name": course["course_name"],
 
            "platform": course["platform"],
 
            "difficulty": course["difficulty"],
 
            "duration": course["duration"],
 
            "career_path": course["career_path"],
 
            "course_url": course["course_url"]
 
        })
 
    return learning_path
 
 
# ==========================================================
# Weekly Study Plan
# ==========================================================
 
def generate_weekly_plan(
    learning_path
):
    """
    Create a simple weekly roadmap.
    """
 
    plan = []
 
    for week, course in enumerate(
        learning_path,
        start=1
    ):
 
        plan.append({
 
            "week": week,
 
            "course": course["course_name"],
 
            "goal": f"Complete {course['course_name']}",
 
            "platform": course["platform"]
 
        })
 
    return plan
 
 
# ==========================================================
# Estimated Completion Time
# ==========================================================
 
def estimated_completion_time(
    recommendations
):
    """
    Estimate total learning hours.
    """
 
    total_hours = 0
 
    for course in recommendations:
 
        total_hours += duration_hours(
            course["duration"]
        )
 
    return round(total_hours, 2)
 
 
# ==========================================================
# Skill Gap Summary
# ==========================================================
 
def learning_statistics(
    recommendations
):
    """
    Generate recommendation statistics.
    """
 
    if not recommendations:
        return {}
 
    scores = [
 
        course["recommendation_score"]
 
        for course in recommendations
 
    ]
 
    return {
 
        "total_courses":
 
            len(recommendations),
 
        "average_score":
 
            round(
 
                sum(scores) / len(scores),
 
                2
 
            ),
 
        "highest_score":
 
            max(scores),
 
        "lowest_score":
 
            min(scores)
 
    }
 
 
# ==========================================================
# Course Recommendation Report
# ==========================================================
 
def generate_course_report(
 
    candidate_skills,
 
    missing_skills,
 
    desired_career="",
 
    top_n=DEFAULT_TOP_N
 
):
    """
    Complete course recommendation report.
    """
 
    recommendations = recommend_courses(
 
        candidate_skills,
 
        missing_skills,
 
        desired_career,
 
        top_n
 
    )
 
    learning_path = generate_learning_path(
        recommendations
    )
 
    weekly_plan = generate_weekly_plan(
        learning_path
    )
 
    total_hours = estimated_completion_time(
        recommendations
    )
 
    statistics = learning_statistics(
        recommendations
    )
 
    best_course = (
 
        recommendations[0]
 
        if recommendations
 
        else None
 
    )
 
    return {
 
        "best_course":
 
            best_course,
 
        "recommendations":
 
            recommendations,
 
        "learning_path":
 
            learning_path,
 
        "weekly_plan":
 
            weekly_plan,
 
        "estimated_hours":
 
            total_hours,
 
        "statistics":
 
            statistics
 
    }
 
 
# ==========================================================
# Format Course Report
# ==========================================================
 
def format_course_report(report):
    """
    Format the generated report into a cleaner structure.
    """
 
    if not report:
        return {}
 
    return {
 
        "best_course":
            report.get("best_course"),
 
        "recommendations":
            report.get("recommendations", []),
 
        "learning_path":
            report.get("learning_path", []),
 
        "weekly_plan":
            report.get("weekly_plan", []),
 
        "estimated_hours":
            report.get("estimated_hours", 0),
 
        "statistics":
            report.get("statistics", {})
 
    }
 
 
# ==========================================================
# Print Complete Report
# ==========================================================
 
def print_course_report(report):
    """
    Pretty-print the recommendation report.
    """
 
    report = format_course_report(report)
 
    print("\n" + "=" * 80)
    print("COURSE RECOMMENDATION REPORT")
    print("=" * 80)
 
    # ------------------------------------------------------
 
    best = report["best_course"]
 
    if best:
 
        print("\nBEST COURSE\n")
 
        print(f"Course Name      : {best['course_name']}")
        print(f"Platform         : {best['platform']}")
        print(f"Skill            : {best['skill']}")
        print(f"Difficulty       : {best['difficulty']}")
        print(f"Duration         : {best['duration']}")
        print(f"Certificate      : {best['certificate']}")
        print(f"Career Path      : {best['career_path']}")
        print(f"Recommendation   : {best['recommendation_score']} %")
        print(f"Course URL       : {best['course_url']}")
 
        print("\nRecommendation Reason")
 
        for reason in best["reason"]:
            print(f"✓ {reason}")
 
    # ------------------------------------------------------
 
    print("\n" + "=" * 80)
    print("TOP COURSE RECOMMENDATIONS")
    print("=" * 80)
 
    for index, course in enumerate(
            report["recommendations"],
            start=1):
 
        print(f"\nRank #{index}")
 
        print(f"Course      : {course['course_name']}")
        print(f"Platform    : {course['platform']}")
        print(f"Difficulty  : {course['difficulty']}")
        print(f"Duration    : {course['duration']}")
        print(f"Score       : {course['recommendation_score']} %")
 
    # ------------------------------------------------------
 
    print("\n" + "=" * 80)
    print("LEARNING PATH")
    print("=" * 80)
 
    for step in report["learning_path"]:
 
        print(
 
            f"Step {step['step']} : "
 
            f"{step['course_name']} "
 
            f"({step['difficulty']})"
 
        )
 
    # ------------------------------------------------------
 
    print("\n" + "=" * 80)
    print("WEEKLY PLAN")
    print("=" * 80)
 
    for week in report["weekly_plan"]:
 
        print(
 
            f"Week {week['week']} : "
 
            f"{week['goal']}"
 
        )
 
    # ------------------------------------------------------
 
    stats = report["statistics"]
 
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
 
    if stats:
 
        print(f"Total Courses    : {stats['total_courses']}")
        print(f"Average Score    : {stats['average_score']} %")
        print(f"Highest Score    : {stats['highest_score']} %")
        print(f"Lowest Score     : {stats['lowest_score']} %")
 
    print(f"\nEstimated Study Time : {report['estimated_hours']} Hours")
 
    print("\n" + "=" * 80)
    print("END OF REPORT")
    print("=" * 80)
 
 
# ==========================================================
# Module Test
# ==========================================================
 
if __name__ == "__main__":
 
    sample_candidate_skills = {
        "python",
        "sql",
        "excel",
        "power bi"
    }
 
    sample_missing_skills = {
        "machine learning",
        "tensorflow",
        "docker",
        "aws"
    }
 
    report = generate_course_report(
 
        candidate_skills=sample_candidate_skills,
 
        missing_skills=sample_missing_skills,
 
        desired_career="Data Scientist",
 
        top_n=5
 
    )
 
    print_course_report(report)
 