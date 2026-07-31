"""
=========================================================
AI Resume Analyzer
Salary Engine Test File
=========================================================
"""

from utils.salary_engine import (

    salary_summary,

    salary_statistics,

    search_job_role,

    search_location,

    predict_salary,

    predict_best_salary,

    generate_salary_report,

    print_salary_report,

    estimate_growth,

    salary_insights,

    compare_locations,

    compare_company_types,

    top_paying_roles,

    top_paying_locations,

    top_company_types

)

# ==========================================================
# Test Candidate
# ==========================================================

candidate_skills = [

    "Python",

    "Machine Learning",

    "Deep Learning",

    "SQL",

    "Pandas",

    "NumPy",

    "Scikit-learn",

    "Power BI"

]

job_role = "Data Scientist"

experience = "2 Years"

education = "B.Tech"

# ==========================================================
# Dataset Summary
# ==========================================================

print("\n" + "=" * 70)

print("DATASET SUMMARY")

print("=" * 70)

print(

    salary_summary()

)

# ==========================================================
# Dataset Statistics
# ==========================================================

print("\n" + "=" * 70)

print("DATASET STATISTICS")

print("=" * 70)

print(

    salary_statistics()

)

# ==========================================================
# Search Job Role
# ==========================================================

print("\n" + "=" * 70)

print("SEARCH JOB ROLE")

print("=" * 70)

jobs = search_job_role(job_role)

print(

    jobs.head()

)

# ==========================================================
# Search Location
# ==========================================================

print("\n" + "=" * 70)

print("SEARCH LOCATION : Bangalore")

print("=" * 70)

locations = search_location("Bangalore")

print(

    locations.head()

)

# ==========================================================
# Salary Prediction
# ==========================================================

print("\n" + "=" * 70)

print("TOP SALARY PREDICTIONS")

print("=" * 70)

predictions = predict_salary(

    job_role=job_role,

    candidate_skills=candidate_skills,

    experience=experience,

    education=education,

    top_n=5

)

print(predictions)

# ==========================================================
# Best Salary Match
# ==========================================================

print("\n" + "=" * 70)

print("BEST SALARY MATCH")

print("=" * 70)

best = predict_best_salary(

    job_role,

    candidate_skills,

    experience,

    education

)

print(best)

# ==========================================================
# Salary Report
# ==========================================================

print("\n" + "=" * 70)

print("SALARY REPORT")

print("=" * 70)

report = generate_salary_report(

    job_role,

    candidate_skills,

    experience,

    education

)

print_salary_report(report)

# ==========================================================
# Career Growth
# ==========================================================

print("\n" + "=" * 70)

print("CAREER GROWTH")

print("=" * 70)

growth = estimate_growth(report)

print(growth)

# ==========================================================
# Salary Insights
# ==========================================================

print("\n" + "=" * 70)

print("SALARY INSIGHTS")

print("=" * 70)

insights = salary_insights(report)

for item in insights:

    print("•", item)

# ==========================================================
# Compare Locations
# ==========================================================

print("\n" + "=" * 70)

print("LOCATION COMPARISON")

print("=" * 70)

print(

    compare_locations(job_role)

)

# ==========================================================
# Compare Company Types
# ==========================================================

print("\n" + "=" * 70)

print("COMPANY TYPE COMPARISON")

print("=" * 70)

print(

    compare_company_types(job_role)

)

# ==========================================================
# Top Paying Roles
# ==========================================================

print("\n" + "=" * 70)

print("TOP PAYING ROLES")

print("=" * 70)

print(

    top_paying_roles(10)

)

# ==========================================================
# Top Paying Locations
# ==========================================================

print("\n" + "=" * 70)

print("TOP PAYING LOCATIONS")

print("=" * 70)

print(

    top_paying_locations()

)

# ==========================================================
# Top Paying Company Types
# ==========================================================

print("\n" + "=" * 70)

print("TOP PAYING COMPANY TYPES")

print("=" * 70)

print(

    top_company_types()

)

print("\n" + "=" * 70)

print("ALL TESTS COMPLETED SUCCESSFULLY")

print("=" * 70)