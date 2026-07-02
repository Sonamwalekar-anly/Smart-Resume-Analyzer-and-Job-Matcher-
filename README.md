# Smart-Resume-Analyzer-and-Job-Matcher-
# Resume Analyzer by Description

An AI-powered Resume Analyzer that evaluates resumes against job descriptions and interview transcripts using **Retrieval-Augmented Generation (RAG)**. The application extracts key information, matches candidate skills with job requirements, and provides intelligent insights through a simple web interface.

---

## Features

- 📄 Upload and analyze resumes (PDF)
- 📋 Upload job descriptions (TXT/PDF)
- 🎤 Upload interview transcripts
- 🤖 AI-powered resume-job matching
- 🔍 Semantic search using RAG
- 📊 Match score and relevant insights
- 🌐 User-friendly Flask web interface

---

## Project Structure

```text
resume_analyser_by_description/
│
├── app.py
├── README.md
├── .gitignore
│
├── services/
│   ├── __init__.py
│   ├── parser.py
│   ├── matcher.py
│   └── rag_store.py
│
├── templates/
│   ├── index.html
│   ├── upload_resume.html
│   ├── upload_job.html
│   ├── upload_interview.html
│   ├── resume_results.html
│   ├── job_results.html
│   └── interview_results.html
│
├── static/
│   └── styles.css
│
├── uploads/
│   ├── resumes/
│   ├── job_descriptions/
│   └── interview_files/
│
├── vector_store/
│   ├── interview.index
│   └── interview_meta.json
│
└── requirements.txt
```

---

## Tech Stack

- Python
- Flask
- LangChain
- ChromaDB / FAISS
- Google Gemini / OpenAI
- HuggingFace Embeddings
- PyPDF
- HTML
- CSS

---

## Workflow

1. Upload a resume.
2. Upload a job description or interview transcript.
3. Extract and preprocess text.
4. Generate vector embeddings.
5. Store embeddings in the vector database.
6. Retrieve relevant information using RAG.
7. Compare resume with job requirements or interview responses.
8. Display AI-generated analysis and matching results.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/resume_analyser_by_description.git
cd resume_analyser_by_description
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Example Use Cases

- Analyze a resume against a job description.
- Measure candidate-job compatibility.
- Evaluate interview transcripts.
- Identify missing skills.
- Generate AI-powered hiring insights.

---

## Future Enhancements

- ATS Resume Scoring
- Skill Gap Analysis
- Resume Recommendations
- Multi-Resume Comparison
- Dashboard with Analytics
- Export Reports (PDF)

---

