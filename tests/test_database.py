from utils.database import (
    load_skills,
    load_jobs,
    load_courses,
    load_ats_keywords
)

skills = load_skills()
jobs = load_jobs()
courses = load_courses()
ats = load_ats_keywords()

print("=" * 50)
print("Database Connected Successfully")
print("=" * 50)

print(f"Skills: {len(skills)}")
print(f"Jobs: {len(jobs)}")
print(f"Courses: {len(courses)}")
print(f"ATS Keywords: {len(ats)}")