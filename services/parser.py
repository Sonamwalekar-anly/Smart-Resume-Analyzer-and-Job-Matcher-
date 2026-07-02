import json
from pathlib import Path
from typing import Any

from PyPDF2 import PdfReader
from docx import Document


def parse_job_description(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = {
            "title": path.stem,
            "description": text,
            "requirements": extract_requirements(text),
        }
    return data


def parse_resume(path: Path) -> dict[str, Any]:
    text = extract_text(path)
    return extract_resume_fields(text)


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        document = Document(path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_requirements(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return [line for line in lines if any(keyword in line.lower() for keyword in ["experience", "skill", "qualification", "degree", "certification", "responsibility"])]


def extract_resume_fields(text: str) -> dict[str, Any]:
    words = [word.strip(".,") for word in text.split()]
    skills = [word for word in words if word.istitle() and len(word) > 2][:12]
    experience = [line for line in text.splitlines() if "years" in line.lower() or "experience" in line.lower()][:5]
    education = [line for line in text.splitlines() if any(keyword in line.lower() for keyword in ["degree", "bachelor", "master", "mba", "phd", "certification"])][:4]
    return {
        "name": extract_name(text),
        "skills": skills,
        "experience": experience,
        "education": education,
        "summary": text[:600],
    }


def extract_name(text: str) -> str:
    first_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if first_lines:
        first = first_lines[0]
        if len(first.split()) <= 4:
            return first
    return "Unknown Candidate"
