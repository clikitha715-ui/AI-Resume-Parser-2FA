
import re
import pdfplumber
from docx import Document
from io import BytesIO


def extract_text(file_bytes: bytes, filename: str) -> str:

    if filename.lower().endswith(".pdf"):
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

    elif filename.lower().endswith(".docx"):
        document = Document(BytesIO(file_bytes))
        text = "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    else:
        raise ValueError("Only PDF and DOCX files are supported")

    return text


def parse_resume(text: str) -> dict:

    email = re.search(
        r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', text
    )

    phone = re.search(
        r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)', text
    )

    skills_list = [
        "Python", "Java", "SQL", "FastAPI", "Django",
        "Machine Learning", "Deep Learning",
        "HTML", "CSS", "JavaScript", "React",
        "Figma", "PostgreSQL", "AWS"
    ]

    found_skills = [
        skill for skill in skills_list
        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text,
            re.IGNORECASE
        )
    ]

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return {
        "name": lines[0] if lines else None,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "skills": found_skills,
        "experience": None
    }
