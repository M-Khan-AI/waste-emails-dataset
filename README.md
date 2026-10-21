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


## Manual Setup

### Prerequisites

Before running the application, install:

- Python 3.10 or newer
- Docker Desktop (if using Docker)
- Git
- A Gemini API key from https://aistudio.google.com/apikey

### Option A: Run Locally

**Step 1: Clone the repository**

```bash
git clone <your-repo-url>
cd <repo-folder>
```

Replace `<your-repo-url>` and `<repo-folder>` with your actual repository URL and folder name.

**Step 2: Create a virtual environment**

```bash
python -m venv venv
```

**Step 3: Activate the virtual environment**

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows Git Bash:

```bash
source venv/Scripts/activate
```

Linux or macOS:

```bash
source venv/bin/activate
```

**Step 4: Install dependencies**

```bash
pip install -r requirements-dev.txt
```

**Step 5: Configure the API key**

Create a `.env` file in the project root using `.env.sample` as a template, if that sample file exists.

Add your key:

```text
GEMINI_API_KEY=your_actual_api_key
```

Never commit your real API key to GitHub.

**Step 6: Start the application**

```bash
python app.py
```

**Step 7: Open the application**

Visit http://localhost:5000 in your browser.

**Step 8: Verify the application**

Open http://localhost:5000/health. A successful health check should return:

```json
{"status": "ok"}
```

### Option B: Run with Docker

**Step 1:** Configure `GEMINI_API_KEY` in your `.env` file.

**Step 2: Build the Docker image**

```bash
docker build -t email-classifier .
```

**Step 3: Start the container**

```bash
docker run --env-file .env -p 5000:5000 email-classifier
```

**Step 4:** Open http://localhost:5000 in your browser.

**Step 5:** Verify the health endpoint at http://localhost:5000/health.

To stop the container, press `Ctrl+C` in the terminal running it.

### Option C: Run with Docker Compose

**Step 1:** Make sure Docker Desktop is running and the `.env` file contains your API key.

**Step 2: Start the application**

```bash
docker compose up --build
```

**Step 3:** Open http://localhost:5000.

**Step 4: Stop the application**

```bash
docker compose down
```

### Run Automated Tests

Install the development dependencies if you have not already done so:

```bash
pip install -r requirements-dev.txt
```

Run the tests:

```bash
pytest
```

### Evaluate the Classifier (Optional)

Validate the dataset:

```bash
python validate_csv.py
```

Evaluate the classifier:

```bash
python evaluate_classifier.py
```

The evaluation script requires a valid Gemini API key. Review `evaluation_report.md` for the measured results, if the evaluation has been completed successfully.

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

## Deployment Guide

The application can be deployed to a container hosting platform that supports Docker, such as Render, Railway, Fly.io, Google Cloud Run, AWS ECS, or a VPS.

### Deployment Steps

1. **Prepare the application:** Confirm that the Dockerfile builds successfully on your local machine.
2. **Prepare the API key:** Obtain a valid Gemini API key and configure it as the `GEMINI_API_KEY` environment variable in the hosting platform's environment-variable or secrets settings.
3. **Deploy the application:** Connect the repository or upload the container image according to the selected platform's deployment process.
4. **Configure the port:** Ensure the platform routes HTTP traffic to the application's configured listening port, which is 5000 for this project unless the deployment configuration specifies otherwise.
5. **Configure HTTPS:** Use the hosting platform's HTTPS support or a reverse proxy with a valid TLS certificate.
6. **Verify deployment:** Visit the deployed application's URL and check its `/health` endpoint. A successful health check should return `{"status": "ok"}`.
7. **Check logs:** If classification fails, review the hosting platform's logs for server-side errors.

### Security and Operations

- Never commit `.env` or expose the Gemini API key in source code, logs, or public documentation.
- Keep secrets in the hosting platform's secret manager or environment-variable settings.
- Set appropriate API quotas and monitor usage.
- Use authentication or rate limiting before exposing the application to unrestricted public traffic.
- Review application logs and re-run classifier evaluation after changing the prompt, categories, or model.
- Check the container size with `docker images email-classifier`.

The actual deployment steps, port configuration, and environment-variable settings depend on the selected hosting platform. Follow that platform's documentation before deploying to production.

## Hand-over summary (for the client)

### 1. Project Overview

The CleanCity Email Classifier is a single-page Flask web application that uses Google Gemini to classify incoming CleanCity service emails into the supported categories:

- Missed Pickup
- Schedule Change
- Complaint
- Other

When the model cannot confidently provide a valid category, the application displays `I don't know`.

### 2. How to Use the Application

1. Start the application using the local, Docker, or Docker Compose instructions above.
2. Open the application URL in a web browser.
3. Paste the email text into the input field.
4. Click **Classify**.
5. Review the predicted category.
6. If an error appears, follow the troubleshooting instructions in this README.

### 3. How to Maintain the Application

**Update the API key:** Change `GEMINI_API_KEY` in the local `.env` file or hosting platform's secret settings. Restart or redeploy the application if required.

**Change the Gemini model:** Update `GEMINI_MODEL` if this setting is supported by the classifier configuration. Confirm that the selected model is available for the configured API key.

**Change categories:** Update the category definitions and classification prompt in the classifier code. Update `emails_labeled.csv`, dataset validation rules, tests, and evaluation logic to match. Run the tests and evaluate the classifier before releasing changes.

**Run tests:**

```bash
pytest
```

**Evaluate performance:**

```bash
python validate_csv.py
python evaluate_classifier.py
```

Review `evaluation_report.md` after a successful evaluation.

### 4. Troubleshooting

- **API key error:** Check that `GEMINI_API_KEY` is configured correctly.
- **Rate limit error:** Wait before retrying and check the Gemini API quota.
- **Network error:** Check the internet connection and hosting platform status.
- **Application unavailable:** Check the container status and server logs.
- **Unexpected category:** Review the prompt and evaluation results before changing the classifier.

### 5. Known Limitations

- The application does not provide user authentication.
- Request rate limiting, a database, and classification history are not included.
- Gemini API limits may restrict usage.
- AI predictions can be incorrect and should be reviewed where necessary.
- Classification quality depends on the prompt, model, and evaluation dataset.

### 6. Recommended Future Improvements

- Add authentication and request rate limiting.
- Monitor API usage and configure appropriate quotas.
- Add optional prediction logging with suitable privacy controls.
- Improve the evaluation dataset and re-evaluate the model after changes.
