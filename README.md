## CleanCity Email Classifier

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

# Setup

```bash
git clone <your-repo-url>
cd <repo-folder>
cp .env.sample .env        # Windows: copy .env.sample .env
```

Edit `.env` and set `GEMINI_API_KEY` (free key: https://aistudio.google.com/apikey).

# Run with Docker

docker build -t email-classifier .
docker run --env-file .env -p 5000:5000 email-classifier

Open http://localhost:5000.

# Run with Docker Compose (optional)

docker compose up --build

# Run locally without Docker

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
python app.py

# Run the tests

pip install -r requirements-dev.txt
pytest

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
