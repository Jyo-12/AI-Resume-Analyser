"""
==========================================================
AI Resume Analyzer
Resume Parsing Module
==========================================================

This module handles:
1. PDF Resume Parsing
2. DOCX Resume Parsing
3. Automatic Resume Text Extraction

Author: Your Name
==========================================================
"""

from pathlib import Path
from pypdf import PdfReader
from docx import Document


# ==========================================================
# PDF PARSER
# ==========================================================

def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF resume.

    Parameters
    ----------
    pdf_path : str or Path
        Path to the PDF file.

    Returns
    -------
    str
        Extracted text.
    """

    try:

        text = ""

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:

        raise Exception(
            f"Error reading PDF file: {e}"
        )


# ==========================================================
# DOCX PARSER
# ==========================================================

def extract_docx_text(docx_path):
    """
    Extract text from a DOCX resume.
    """

    try:

        document = Document(docx_path)

        text = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)

    except Exception as e:

        raise Exception(
            f"Error reading DOCX file: {e}"
        )


# ==========================================================
# AUTO DETECT FILE TYPE
# ==========================================================

def extract_resume_text(file_path):
    """
    Automatically detect the resume type
    and extract text.

    Supported formats:
        • PDF
        • DOCX
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        return extract_pdf_text(file_path)

    elif extension == ".docx":

        return extract_docx_text(file_path)

    else:

        raise ValueError(
            "Unsupported file format. Please upload a PDF or DOCX file."
        )


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def extract_text_from_resume(file_path):
    """
    Backward-compatible wrapper.

    Older modules use:
        extract_text_from_resume()

    New modules use:
        extract_resume_text()

    Both now work.
    """

    return extract_resume_text(file_path)


# ==========================================================
# FILE VALIDATION
# ==========================================================

def validate_resume(file_path):
    """
    Validate uploaded resume file.

    Returns
    -------
    bool
        True if supported.
    """

    allowed_extensions = [".pdf", ".docx"]

    file_path = Path(file_path)

    return file_path.suffix.lower() in allowed_extensions


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Resume Parser Loaded Successfully")
    print("=" * 60)