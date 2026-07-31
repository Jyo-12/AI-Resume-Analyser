"""
=========================================================
AI Resume Analyzer
Interview Engine Test File
=========================================================
"""

from utils.interview_engine import (

    interview_summary,

    search_job_role,

    search_skill,

    search_difficulty,

    search_question_type,

    recommend_interview_questions,

    recommend_best_questions,

    recommend_questions_by_skill,

    recommend_questions_by_difficulty,

    recommend_questions_by_type,

    random_mock_interview,

    frequently_asked_questions,

    interview_readiness_score,

    readiness_level,

    identify_weak_skills,

    identify_strong_skills,

    interview_skill_coverage

)

# ==========================================================
# Test Candidate
# ==========================================================

candidate_skills = [

    "Python",

    "Machine Learning",

    "SQL",

    "Pandas",

    "Statistics",

    "Scikit-learn"

]

job_role = "Data Scientist"

difficulty = "Medium"

question_type = "Technical"

# ==========================================================
# Dataset Summary
# ==========================================================

print("\n" + "=" * 70)
print("INTERVIEW DATASET SUMMARY")
print("=" * 70)

print(
    interview_summary()
)

# ==========================================================
# Search by Job Role
# ==========================================================

print("\n" + "=" * 70)
print("SEARCH JOB ROLE")
print("=" * 70)

print(
    search_job_role(job_role).head()
)

# ==========================================================
# Search by Skill
# ==========================================================

print("\n" + "=" * 70)
print("SEARCH BY SKILL")
print("=" * 70)

print(
    search_skill("Python").head()
)

# ==========================================================
# Search by Difficulty
# ==========================================================

print("\n" + "=" * 70)
print("SEARCH BY DIFFICULTY")
print("=" * 70)

print(
    search_difficulty("Medium").head()
)

# ==========================================================
# Search by Question Type
# ==========================================================

print("\n" + "=" * 70)
print("SEARCH BY QUESTION TYPE")
print("=" * 70)

print(
    search_question_type("Technical").head()
)

# ==========================================================
# Personalized Recommendations
# ==========================================================

print("\n" + "=" * 70)
print("RECOMMENDED QUESTIONS")
print("=" * 70)

recommendations = recommend_interview_questions(

    job_role=job_role,

    candidate_skills=candidate_skills,

    difficulty=difficulty,

    question_type=question_type,

    top_n=5

)

print(recommendations)

# ==========================================================
# Best Questions
# ==========================================================

print("\n" + "=" * 70)
print("BEST QUESTIONS")
print("=" * 70)

print(

    recommend_best_questions(

        job_role,

        candidate_skills,

        top_n=5

    )

)

# ==========================================================
# Questions by Skill
# ==========================================================

print("\n" + "=" * 70)
print("QUESTIONS BY SKILL")
print("=" * 70)

print(

    recommend_questions_by_skill(

        "Python",

        top_n=5

    )

)

# ==========================================================
# Questions by Difficulty
# ==========================================================

print("\n" + "=" * 70)
print("QUESTIONS BY DIFFICULTY")
print("=" * 70)

print(

    recommend_questions_by_difficulty(

        "Hard",

        top_n=5

    )

)

# ==========================================================
# Questions by Type
# ==========================================================

print("\n" + "=" * 70)
print("QUESTIONS BY TYPE")
print("=" * 70)

print(

    recommend_questions_by_type(

        "Technical",

        top_n=5

    )

)

# ==========================================================
# Mock Interview
# ==========================================================

print("\n" + "=" * 70)
print("MOCK INTERVIEW")
print("=" * 70)

print(

    random_mock_interview(

        job_role,

        n_questions=5

    )

)

# ==========================================================
# Frequently Asked Questions
# ==========================================================

print("\n" + "=" * 70)
print("FREQUENTLY ASKED QUESTIONS")
print("=" * 70)

print(

    frequently_asked_questions(

        job_role,

        top_n=5

    )

)

# ==========================================================
# Readiness Score
# ==========================================================

print("\n" + "=" * 70)
print("INTERVIEW READINESS")
print("=" * 70)

score = interview_readiness_score(

    job_role,

    candidate_skills,

    difficulty

)

print("Score :", score)

print("Level :", readiness_level(score))

# ==========================================================
# Skill Coverage
# ==========================================================

print("\n" + "=" * 70)
print("SKILL COVERAGE")
print("=" * 70)

coverage = interview_skill_coverage(

    job_role,

    candidate_skills

)

print("Coverage :", coverage, "%")

# ==========================================================
# Strong Skills
# ==========================================================

print("\n" + "=" * 70)
print("STRONG SKILLS")
print("=" * 70)

for skill, count in identify_strong_skills(

    job_role,

    candidate_skills

):

    print(f"{skill:<25} {count}")

# ==========================================================
# Weak Skills
# ==========================================================

print("\n" + "=" * 70)
print("WEAK SKILLS")
print("=" * 70)

for skill, count in identify_weak_skills(

    job_role,

    candidate_skills

):

    print(f"{skill:<25} {count}")

print("\n" + "=" * 70)
print("INTERVIEW ENGINE TEST COMPLETED")
print("=" * 70)