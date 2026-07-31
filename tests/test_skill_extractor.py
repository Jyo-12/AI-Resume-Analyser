from utils.parser import extract_resume_text
from utils.cleaner import clean_resume
from utils.skill_extractor import extract_skills, categorize_skills

resume_path = "uploads/artificial-intelligence-machine-learning-resume-example.pdf"

resume = extract_resume_text(resume_path)

cleaned = clean_resume(resume)

skills = extract_skills(cleaned)

print("=" * 60)
print("Detected Skills")
print("=" * 60)

for skill in skills:
    print(skill)

print("\n")

print("=" * 60)
print("Skill Categories")
print("=" * 60)

categories = categorize_skills(skills)

for category, items in categories.items():

    print(f"\n{category}")

    if items:
        for item in items:
            print(f"   • {item}")