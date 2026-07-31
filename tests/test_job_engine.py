from utils.parser import extract_resume_text
from utils.cleaner import clean_resume
from utils.skill_extractor import extract_skills
from utils.job_engine import (
    generate_job_report,
    format_job_report,
    print_job_report
)

# ==========================================================
# UPDATE YOUR RESUME PATH
# ==========================================================

resume_path = "uploads/artificial-intelligence-machine-learning-resume-example.pdf"   # Change to your resume filename

# ==========================================================
# STEP 1 : PARSE RESUME
# ==========================================================

resume_text = extract_resume_text(resume_path)

# ==========================================================
# STEP 2 : CLEAN RESUME
# ==========================================================

cleaned_resume = clean_resume(resume_text)

# ==========================================================
# STEP 3 : EXTRACT SKILLS
# ==========================================================

candidate_skills = extract_skills(cleaned_resume)

# ==========================================================
# OPTIONAL INFORMATION
# ==========================================================

candidate_experience = 0          # Change if required
candidate_education = ""          # Example: "Bachelor"

# ==========================================================
# STEP 4 : GENERATE REPORT
# ==========================================================

report = generate_job_report(
    candidate_skills=candidate_skills,
    candidate_experience=candidate_experience,
    candidate_education=candidate_education,
    top_n=10
)

formatted_report = format_job_report(report)

# ==========================================================
# DISPLAY DETECTED SKILLS
# ==========================================================

print("\n" + "=" * 80)
print("AI RESUME ANALYZER")
print("=" * 80)

print("\nDetected Skills\n")

for skill in sorted(candidate_skills):
    print(f"✓ {skill}")

# ==========================================================
# BEST JOB
# ==========================================================

best_job = formatted_report["best_job"]

print("\n" + "=" * 80)
print("BEST JOB MATCH")
print("=" * 80)

if best_job:

    print(f"Job Title        : {best_job['job_title']}")
    print(f"Company          : {best_job['company']}")
    print(f"Location         : {best_job['location']}")
    print(f"Salary           : {best_job['salary']}")
    print(f"Experience       : {best_job['experience']}")
    print(f"Education        : {best_job['education']}")
    print(f"Employment Type  : {best_job['employment_type']}")
    print(f"Overall Score    : {best_job['overall_score']} %")
    print(f"Confidence       : {best_job['confidence']}")

    print("\nRequired Skill Score :",
          best_job["required_score"])

    print("Preferred Skill Score:",
          best_job["preferred_score"])

    print("\nMatched Required Skills")

    if best_job["matched_required"]:

        for skill in best_job["matched_required"]:
            print(f"✓ {skill}")

    else:
        print("None")

    print("\nMatched Preferred Skills")

    if best_job["matched_preferred"]:

        for skill in best_job["matched_preferred"]:
            print(f"✓ {skill}")

    else:
        print("None")

    print("\nMissing Required Skills")

    if best_job["missing_required"]:

        for skill in best_job["missing_required"]:
            print(f"• {skill}")

    else:
        print("None")

    print("\nMissing Preferred Skills")

    if best_job["missing_preferred"]:

        for skill in best_job["missing_preferred"]:
            print(f"• {skill}")

    else:
        print("None")

    print("\nRecommendation Reasons")

    for reason in best_job["recommendation_reason"]:
        print(f"✓ {reason}")

# ==========================================================
# STATISTICS
# ==========================================================

stats = formatted_report["statistics"]

print("\n" + "=" * 80)
print("RECOMMENDATION STATISTICS")
print("=" * 80)

print(f"Average Score : {stats['average_score']} %")
print(f"Highest Score : {stats['highest_score']} %")
print(f"Lowest Score  : {stats['lowest_score']} %")

print("\nConfidence Distribution")

print(f"Excellent : {stats['excellent']}")
print(f"Strong    : {stats['strong']}")
print(f"Moderate  : {stats['moderate']}")
print(f"Weak      : {stats['weak']}")
print(f"Poor      : {stats['poor']}")

# ==========================================================
# TOP JOBS
# ==========================================================

print("\n" + "=" * 80)
print("TOP JOB RECOMMENDATIONS")
print("=" * 80)

for index, job in enumerate(
        formatted_report["recommendations"],
        start=1):

    print(f"\nRank #{index}")

    print(f"Job Title : {job['job_title']}")
    print(f"Company   : {job['company']}")
    print(f"Location  : {job['location']}")
    print(f"Salary    : {job['salary']}")
    print(f"Score     : {job['overall_score']} %")
    print(f"Confidence: {job['confidence']}")

# ==========================================================
# CAREER ADVICE
# ==========================================================

print("\n" + "=" * 80)
print("CAREER ADVICE")
print("=" * 80)

for advice in formatted_report["career_advice"]:
    print(f"• {advice}")

# ==========================================================
# SKILL GAP
# ==========================================================

gap = formatted_report["skill_gap"]

print("\n" + "=" * 80)
print("SKILL GAP ANALYSIS")
print("=" * 80)

print(f"Completion : {gap['completion_percentage']} %")

print("\nMissing Required Skills")

if gap["missing_required"]:

    for skill in gap["missing_required"]:
        print(f"• {skill}")

else:
    print("None")

print("\nMissing Preferred Skills")

if gap["missing_preferred"]:

    for skill in gap["missing_preferred"]:
        print(f"• {skill}")

else:
    print("None")

# ==========================================================
# IMPROVEMENT ROADMAP
# ==========================================================

print("\n" + "=" * 80)
print("IMPROVEMENT ROADMAP")
print("=" * 80)

for step in formatted_report["roadmap"]:
    print(f"✓ {step}")

# ==========================================================
# PRINT COMPLETE REPORT
# ==========================================================

print("\n" + "=" * 80)
print("COMPLETE REPORT")
print("=" * 80)

print_job_report(report)

print("\nJob Engine Version 2.0 Tested Successfully!")