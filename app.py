
from flask import Flask, render_template, request, jsonify
from scanner import analyze_logs
from pathlib import Path
import json
from datetime import datetime, timezone

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB limit

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "online",
        "project": "LogSentry AI",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/api/scan", methods=["POST"])
def scan_logs():
    if "logfile" not in request.files:
        return jsonify({"error": "Please upload a log file."}), 400

    file = request.files["logfile"]

    if not file.filename:
        return jsonify({"error": "No file selected."}), 400

    if Path(file.filename).suffix.lower() not in {".log", ".txt"}:
        return jsonify({"error": "Only .log and .txt files are allowed."}), 400

    try:
        content = file.read().decode("utf-8", errors="replace")
        results = analyze_logs(content)

        report = {
            "filename": Path(file.filename).name,
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "total_events": results["total_events"],
            "errors": results["errors"],
            "warnings": results["warnings"],
            "suspicious_events": results["suspicious_events"],
            "findings": results["findings"]
        }

        report_path = REPORT_DIR / "latest-report.json"
        report_path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8"
        )

        return jsonify(report)

    except Exception:
        app.logger.exception("Log scan failed")
        return jsonify({"error": "Unable to analyze this log file."}), 500


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"error": "File exceeds the 2 MB limit."}), 413


if __name__ == "__main__":
    app.run(debug=True, port=5000)
