# CleanCity Email Classifier

A minimal Flask web app. Paste an email, click **Classify**, and see its predicted
category: **Missed Pickup**, **Schedule Change**, **Complaint**, or **Other**. If the
model is unsure, the app shows **I don't know**. Classification uses Google Gemini.

# Project structure

| File | Purpose |
|---|---|
| `app.py` | Flask routes and input validation |
| `classify_email.py` | Classification logic and API error handling |
| `templates/index.html` | The single web page |
| `Dockerfile` | Slim production image (Gunicorn) |
| `docker-compose.yml` | Optional one-command startup |
| `evaluate_classifier.py`, `validate_csv.py` | Dataset validation and accuracy evaluation |
| `test_classify_email.py`, `test_app.py` | Automated tests (no API key needed) |


## Setup

## Prerequisites

- Git
- Python 3.10+ (for local run)
- Docker Desktop (for Docker run)
- A Gemini API key (free): https://aistudio.google.com/apikey

## Quick setup (one script)

```bash
git clone <your-repo-url>
cd <repo-folder>
chmod +x setup.sh
./setup.sh            # local: venv + dependencies + tests + start app
./setup.sh docker     # build the Docker image and run it
./setup.sh compose    # docker compose up --build
```

Open http://localhost:5000.

On Windows, run `setup.sh` from Git Bash or WSL. If port 5000 is busy, run `PORT=5001 ./setup.sh docker`.

The script creates `.env`, asks for your `GEMINI_API_KEY`, adds `.env` to `.gitignore`, and then runs the mode you chose.

## Manual setup

### 1. Clone and configure

git clone <your-repo-url>
cd <repo-folder>
cp .env.sample .env        # Windows: copy .env.sample .env

Edit `.env` and set `GEMINI_API_KEY`.

### 2a. Run with Docker

docker build -t email-classifier .

### 2b. Run with Docker Compose

docker compose up --build

### 2c. Run locally without Docker

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
python app.py

## Verify

curl http://localhost:5000/health
# {"status": "ok"}

Open http://localhost:5000, paste an email, and click **Classify**.

## Run the tests

pip install -r requirements-dev.txt
pytest

## Evaluate accuracy (optional)

```bash
python validate_csv.py
python evaluate_classifier.py      # requires a valid GEMINI_API_KEY
```

# Troubleshooting

| Problem | Fix |
|---|---|
| "Contact the administrator" message | `GEMINI_API_KEY` is missing or invalid. Check `.env` and restart. |
| "Too many requests" | Free-tier rate limit reached. Wait a minute and retry. |
| Port 5000 already in use | Use `-p 5001:5000` and open http://localhost:5001. |
| `.env` changes not applied | Restart the app or container. |

# Error handling

| Situation | What the user sees |
|---|---|
| Empty input | "Please paste an email before submitting." |
| Email over 8,000 characters | "The email is too long..." |
| Missing or invalid API key | A message asking them to contact the administrator |
| Rate limit (HTTP 429) | "Too many requests. Please wait a minute and try again." |
| Network error or timeout | "Could not reach the classification service..." |
| Any other failure | "Something went wrong. Please try again." (logged on the server) |

# Deployment notes

- The container runs Gunicorn on port 5000 as a non-root user.
- The API key is supplied at runtime (`--env-file` or the host's secret manager) and is
  never baked into the image, because `.env` is excluded by `.dockerignore`.
- Works on any container host (Render, Railway, Fly.io, Google Cloud Run, AWS ECS, a VPS).
  Set `GEMINI_API_KEY` as an environment variable on the platform.
- Serve over HTTPS using the platform's load balancer or a reverse proxy.
- `GET /health` returns `{"status": "ok"}` for health checks.
- Check the image size with `docker images email-classifier` (target: under 200 MB).

## Hand-over summary (for the client)

**What was built:** A single-page web app that sorts CleanCity emails into four
categories using Gemini.

**How it works:** The browser posts the email text to Flask. `app.py` validates it and
calls `classify_email.py`, which sends it to Gemini with a prompt that allows only the
four categories or "I don't know". Anything outside that list becomes "I don't know".

**Common changes:**
- Categories: edit `CATEGORIES` in `classify_email.py`, and update `emails_labeled.csv` and `validate_csv.py` to match.
- Model: set `GEMINI_MODEL` in `.env`.

**Known limitations:**
- No login: anyone with the URL can use the app and consume your API quota.
- No rate limiting, database, or stored history.
- The free Gemini tier has low request limits, so heavy use may return "Too many requests".
- Predictions come from an AI model and can be wrong; check `evaluation_report.md` for measured accuracy.
**Suggested next steps:** add authentication or rate limiting, set a spending/quota
cap on the API key, log predictions for review, and re-run `evaluate_classifier.py`
after any prompt or category change.