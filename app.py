from flask import Flask, render_template, request, jsonify, flash
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from services import parser, matcher, rag_store

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx", "txt"}
ALLOWED_JOB_EXTENSIONS = {"json", "txt"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "avi"}

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
UPLOAD_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename: str, allowed_extensions: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/jobs", methods=["GET"])
def api_jobs():
    try:
        jobs = matcher.load_all_jobs()
        return jsonify({"success": True, "jobs": jobs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/upload-job", methods=["POST"])
def api_upload_job():
    files = request.files.getlist("job_files")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"success": False, "error": "No files uploaded"}), 400

    job_data = []
    for file in files:
        if file and allowed_file(file.filename, ALLOWED_JOB_EXTENSIONS):
            filename = "job_" + secure_filename(file.filename)
            destination = UPLOAD_FOLDER / filename
            file.save(destination)
            parsed = parser.parse_job_description(destination)
            parsed["filename"] = filename
            job_data.append(parsed)

    return jsonify({"success": True, "jobs": job_data})


@app.route("/api/delete-job/<filename>", methods=["DELETE"])
def api_delete_job(filename):
    try:
        safe_filename = secure_filename(filename)
        if not safe_filename.startswith("job_"):
            return jsonify({"success": False, "error": "Invalid file format"}), 400
        
        target_file = UPLOAD_FOLDER / safe_filename
        if target_file.exists() and target_file.is_file():
            target_file.unlink()
            return jsonify({"success": True, "message": f"Job file {safe_filename} deleted"})
        else:
            return jsonify({"success": False, "error": "File not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/upload-resume", methods=["POST"])
def api_upload_resume():
    file = request.files.get("resume_file")
    if not file or file.filename == "":
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    if file and allowed_file(file.filename, ALLOWED_RESUME_EXTENSIONS):
        filename = "resume_" + secure_filename(file.filename)
        destination = UPLOAD_FOLDER / filename
        file.save(destination)
        
        resume_data = parser.parse_resume(destination)
        jobs = matcher.load_all_jobs()
        matches = matcher.match_candidate_to_jobs(resume_data, jobs)
        
        return jsonify({
            "success": True, 
            "resume": resume_data, 
            "matches": matches
        })

    return jsonify({"success": False, "error": "Unsupported file type"}), 400


@app.route("/api/upload-interview", methods=["POST"])
def api_upload_interview():
    file = request.files.get("interview_file")
    if not file or file.filename == "":
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
        filename = "interview_" + secure_filename(file.filename)
        destination = UPLOAD_FOLDER / filename
        file.save(destination)
        
        summary = rag_store.process_interview_video(destination)
        return jsonify({"success": True, "summary": summary})

    return jsonify({"success": False, "error": "Unsupported file type"}), 400


if __name__ == "__main__":
    app.run(debug=True)
