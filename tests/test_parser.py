from utils.parser import extract_resume_text
from utils.cleaner import clean_resume

resume_path = "uploads/artificial-intelligence-machine-learning-resume-example.pdf"

resume_text = extract_resume_text(resume_path)

cleaned_text = clean_resume(resume_text)

print("=" * 60)
print("ORIGINAL TEXT")
print("=" * 60)
print(resume_text[:1000])

print("\n")

print("=" * 60)
print("CLEANED TEXT")
print("=" * 60)
print(cleaned_text[:1000])