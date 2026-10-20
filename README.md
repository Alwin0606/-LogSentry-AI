# LogSentry AI

AI-powered log analysis and suspicious activity detection built with Python and Flask.

## Features
- Upload `.log` and `.txt` files
- Analyze log events
- Count errors and warnings
- Detect suspicious activity
- Display scan findings on a web dashboard
- Export scan reports as JSON
- Maximum upload size: 2 MB

## Tech Stack
- Python
- Flask
- HTML
- CSS
- JavaScript

## Setup

Create and activate a virtual environment on Windows:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Project Structure

```text
LogSentry-AI/
├── app.py
├── scanner.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Disclaimer

This project is intended for educational and defensive log analysis. Findings should be verified before taking security actions.

