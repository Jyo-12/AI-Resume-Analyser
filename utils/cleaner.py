"""
==========================================================
AI Resume Analyzer
Resume Cleaning Module
==========================================================

This module handles:
1. URL Removal
2. Email & Phone Preservation
3. Special Character Removal
4. Whitespace Normalization
5. Text Normalization

Author: Your Name
==========================================================
"""

import re


# ==========================================================
# REMOVE URLS
# ==========================================================

def remove_urls(text):
    """
    Remove URLs from resume text.
    """

    if not text:
        return ""

    return re.sub(r"http\S+|www\S+", "", text)


# ==========================================================
# REMOVE SPECIAL CHARACTERS
# ==========================================================

def remove_special_characters(text):
    """
    Remove unwanted special characters while preserving
    useful resume characters.
    """

    if not text:
        return ""

    return re.sub(
        r"[^a-zA-Z0-9@.+#,\-()/\n ]",
        " ",
        text
    )


# ==========================================================
# NORMALIZE WHITESPACE
# ==========================================================

def normalize_whitespace(text):
    """
    Remove extra spaces and blank lines.
    """

    if not text:
        return ""

    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


# ==========================================================
# NORMALIZE TEXT
# ==========================================================

def normalize_text(text):
    """
    Convert text to lowercase.
    """

    if not text:
        return ""

    return text.lower()


# ==========================================================
# COMPLETE CLEANING PIPELINE
# ==========================================================

def clean_resume(text):
    """
    Perform complete resume cleaning.

    Steps
    -----
    1. Remove URLs
    2. Remove unwanted symbols
    3. Normalize whitespace
    4. Convert to lowercase

    Parameters
    ----------
    text : str

    Returns
    -------
    str
        Cleaned resume text.
    """

    if not text:
        return ""

    text = remove_urls(text)

    text = remove_special_characters(text)

    text = normalize_whitespace(text)

    text = normalize_text(text)

    return text


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def clean_resume_text(text):
    """
    Wrapper for backward compatibility.

    Older modules call:
        clean_resume_text()

    Newer modules call:
        clean_resume()
    """

    return clean_resume(text)


# ==========================================================
# ALIAS
# ==========================================================

clean_text = clean_resume


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    sample = """
    John Doe

    https://github.com/johndoe

    Email: john@gmail.com

    Phone: +91-9876543210

    Python | SQL | Machine Learning | Power BI
    """

    print("=" * 60)
    print("ORIGINAL TEXT")
    print("=" * 60)
    print(sample)

    print("\n" + "=" * 60)
    print("CLEANED TEXT")
    print("=" * 60)
    print(clean_resume(sample))