from typing import Any
from pathlib import Path
from services import parser



def load_sample_jobs() -> list[dict[str, Any]]:
    return [
        {
            "title": "Software Engineer",
            "description": "Build backend services, integrate AI tools, and manage APIs.",
            "requirements": [
                "3+ years of software development experience",
                "Python, Flask, REST APIs",
                "Experience with NLP or machine learning",
            ],
            "skills": ["Python", "Flask", "API", "NLP", "Machine Learning"],
        },
        {
            "title": "Talent Acquisition Specialist",
            "description": "Manage candidate sourcing, evaluate resumes, and support hiring managers.",
            "requirements": [
                "Experience with recruitment workflows",
                "Strong communication and interviewing skills",
                "Comfortable using analytics and hiring platforms",
            ],
            "skills": ["Recruiting", "Communication", "Analytics", "Interviewing"],
        },
    ]


def match_candidate_to_jobs(candidate: dict[str, Any], jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidate_text = " ".join([candidate.get("name", ""), " ".join(candidate.get("skills", [])), " ".join(candidate.get("experience", [])), " ".join(candidate.get("education", []))]).lower()
    results = []

    for job in jobs:
        skill_hits = sum(1 for skill in job.get("skills", []) if skill.lower() in candidate_text)
        requirement_hits = sum(1 for requirement in job.get("requirements", []) if any(term in candidate_text for term in requirement.lower().split()))
        total_points = skill_hits * 2 + requirement_hits
        score = round(min(100, total_points * 10), 1)
        results.append(
            {
                "title": job["title"],
                "description": job["description"],
                "score": score,
                "skill_match": skill_hits,
                "experience_match": requirement_hits,
                "matched_skills": [skill for skill in job.get("skills", []) if skill.lower() in candidate_text],
                "missing_skills": [skill for skill in job.get("skills", []) if skill.lower() not in candidate_text],
            }
        )

    return sorted(results, key=lambda item: item["score"], reverse=True)


def load_all_jobs() -> list[dict[str, Any]]:
    jobs = load_sample_jobs()
    base_dir = Path(__file__).resolve().parent.parent
    upload_dir = base_dir / "uploads"
    if not upload_dir.exists():
        return jobs

    for path in upload_dir.glob("job_*"):
        if path.is_file() and path.suffix.lower() in [".json", ".txt"]:
            try:
                parsed = parser.parse_job_description(path)
                job_entry = {
                    "title": parsed.get("title", path.stem.replace("job_", "")),
                    "description": parsed.get("description", ""),
                    "requirements": parsed.get("requirements", []),
                    "skills": parsed.get("skills", []),
                    "filename": path.name
                }
                if not job_entry["skills"]:
                    words = [w.strip(".,()[]{}") for w in job_entry["description"].split()]
                    job_entry["skills"] = list(set([w for w in words if w.istitle() and len(w) > 2]))[:8]
                jobs.append(job_entry)
            except Exception:
                pass
    return jobs

