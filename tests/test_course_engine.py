"""
==========================================================
Test Course Recommendation Engine
==========================================================
"""



from utils.course_engine import (
    generate_course_report,
    print_course_report,
    course_summary,
    search_courses_by_skill,
    search_courses_by_career
)

# ==========================================================
# SAMPLE CANDIDATE
# ==========================================================

candidate_skills = {
    "python",
    "sql",
    "excel",
    "power bi",
    "pandas"
}

missing_skills = {
    "machine learning",
    "deep learning",
    "tensorflow",
    "docker",
    "aws",
    "nlp"
}

desired_career = "Data Scientist"

# ==========================================================
# DATASET SUMMARY
# ==========================================================

print("\n" + "=" * 80)
print("COURSE DATASET SUMMARY")
print("=" * 80)

summary = course_summary()

for key, value in summary.items():
    print(f"{key:20}: {value}")

# ==========================================================
# SEARCH BY SKILL
# ==========================================================

print("\n" + "=" * 80)
print("SEARCH : MACHINE LEARNING")
print("=" * 80)

ml_courses = search_courses_by_skill(
    "machine learning"
)

if len(ml_courses):

    print(

        ml_courses[
            [
                "Course_Name",
                "Platform",
                "Difficulty"
            ]
        ]

    )

else:

    print("No matching courses found.")

# ==========================================================
# SEARCH BY CAREER
# ==========================================================

print("\n" + "=" * 80)
print("SEARCH : DATA SCIENTIST")
print("=" * 80)

career_courses = search_courses_by_career(
    desired_career
)

if len(career_courses):

    print(

        career_courses[
            [
                "Course_Name",
                "Platform",
                "Career_Path"
            ]
        ]

    )

else:

    print("No career specific courses found.")

# ==========================================================
# GENERATE REPORT
# ==========================================================

report = generate_course_report(

    candidate_skills=candidate_skills,

    missing_skills=missing_skills,

    desired_career=desired_career,

    top_n=10

)

# ==========================================================
# PRINT REPORT
# ==========================================================

print_course_report(report)

# ==========================================================
# BEST COURSE
# ==========================================================

best = report["best_course"]

if best:

    print("\n" + "=" * 80)
    print("BEST COURSE")
    print("=" * 80)

    print(f"Course Name           : {best['course_name']}")
    print(f"Platform              : {best['platform']}")
    print(f"Difficulty            : {best['difficulty']}")
    print(f"Duration              : {best['duration']}")
    print(f"Recommendation Score  : {best['recommendation_score']} %")
    print(f"Certificate           : {best['certificate']}")
    print(f"Career Path           : {best['career_path']}")
    print(f"Course URL            : {best['course_url']}")

# ==========================================================
# TOP RECOMMENDATIONS
# ==========================================================

print("\n" + "=" * 80)
print("TOP COURSE RECOMMENDATIONS")
print("=" * 80)

for i, course in enumerate(

    report["recommendations"],

    start=1

):

    print(f"\nRank #{i}")

    print(f"Course       : {course['course_name']}")
    print(f"Platform     : {course['platform']}")
    print(f"Difficulty   : {course['difficulty']}")
    print(f"Duration     : {course['duration']}")
    print(f"Score        : {course['recommendation_score']} %")

# ==========================================================
# LEARNING PATH
# ==========================================================

print("\n" + "=" * 80)
print("LEARNING PATH")
print("=" * 80)

for step in report["learning_path"]:

    print(

        f"Step {step['step']} : "

        f"{step['course_name']} "

        f"({step['difficulty']})"

    )

# ==========================================================
# WEEKLY PLAN
# ==========================================================

print("\n" + "=" * 80)
print("WEEKLY STUDY PLAN")
print("=" * 80)

for week in report["weekly_plan"]:

    print(

        f"Week {week['week']}"

        f" -> {week['goal']}"

    )

# ==========================================================
# STATISTICS
# ==========================================================

stats = report["statistics"]

print("\n" + "=" * 80)
print("STATISTICS")
print("=" * 80)

print(f"Total Courses     : {stats['total_courses']}")
print(f"Average Score     : {stats['average_score']}")
print(f"Highest Score     : {stats['highest_score']}")
print(f"Lowest Score      : {stats['lowest_score']}")
print(f"Estimated Hours   : {report['estimated_hours']}")

print("\n")
print("=" * 80)
print("Course Engine Version 2.0 Tested Successfully!")
print("=" * 80)