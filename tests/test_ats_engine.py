from utils.parser import extract_resume_text
from utils.cleaner import clean_resume
from utils.ats_engine import generate_ats_report

# Replace with your uploaded resume filename
resume_path = "uploads/artificial-intelligence-machine-learning-resume-example.pdf"

# Step 1 - Parse
resume_text = extract_resume_text(resume_path)

# Step 2 - Clean
cleaned_text = clean_resume(resume_text)

# Step 3 - ATS Analysis
report = generate_ats_report(cleaned_text)

print("=" * 70)
print("AI RESUME ANALYZER - ATS REPORT")
print("=" * 70)

print(f"\nOverall ATS Score : {report['overall_score']}/100")

print("\nSECTION SCORES")
print("-" * 40)

print(f"Contact Information : {report['contact_score']}/10")
print(f"Resume Sections     : {report['section_score']}/10")
print(f"Education           : {report['education_score']}/10")
print(f"Skills              : {report['skill_score']}/20")
print(f"Experience          : {report['experience_score']}/20")
print(f"Projects            : {report['project_score']}/15")
print(f"Certifications      : {report['certification_score']}/5")
print(f"ATS Keywords        : {report['keyword_score']}/10")

print("\nDETECTED SKILLS")
print("-" * 40)

for skill in report["detected_skills"]:
    print(f"✓ {skill}")

print("\nFOUND SECTIONS")
print("-" * 40)

for section in report["found_sections"]:
    print(f"✓ {section}")

print("\nMATCHED ATS KEYWORDS")
print("-" * 40)

for keyword in report["matched_keywords"]:
    print(f"✓ {keyword}")

print("\nSTRENGTHS")
print("-" * 40)

for strength in report["strengths"]:
    print(f"✅ {strength}")

print("\nIMPROVEMENT SUGGESTIONS")
print("-" * 40)

for suggestion in report["improvements"]:
    print(f"• {suggestion}")

print("\n" + "=" * 70)
print("ATS Analysis Completed Successfully!")
print("=" * 70)