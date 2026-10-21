# Hand-over summary (for the client)

## 1. Project Overview

The CleanCity Email Classifier is a single-page Flask web application that uses Google Gemini to classify incoming CleanCity service emails into the supported categories:

- Missed Pickup
- Schedule Change
- Complaint
- Other

When the model cannot confidently provide a valid category, the application displays `I don't know`.

## 2. How to Use the Application

1. Start the application using the local, Docker, or Docker Compose instructions above.
2. Open the application URL in a web browser.
3. Paste the email text into the input field.
4. Click **Classify**.
5. Review the predicted category.
6. If an error appears, follow the troubleshooting instructions in this README.

## 3. How to Maintain the Application

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

## 4. Troubleshooting

- **API key error:** Check that `GEMINI_API_KEY` is configured correctly.
- **Rate limit error:** Wait before retrying and check the Gemini API quota.
- **Network error:** Check the internet connection and hosting platform status.
- **Application unavailable:** Check the container status and server logs.
- **Unexpected category:** Review the prompt and evaluation results before changing the classifier.

## 5. Known Limitations

- The application does not provide user authentication.
- Request rate limiting, a database, and classification history are not included.
- Gemini API limits may restrict usage.
- AI predictions can be incorrect and should be reviewed where necessary.
- Classification quality depends on the prompt, model, and evaluation dataset.

## 6. Recommended Future Improvements

- Add authentication and request rate limiting.
- Monitor API usage and configure appropriate quotas.
- Add optional prediction logging with suitable privacy controls.
- Improve the evaluation dataset and re-evaluate the model after changes.

## 7. Handover Checklist

Before handing over the application to CleanCity Services, confirm that:

- [ ] The application starts successfully.
- [ ] The health endpoint responds correctly.
- [ ] The automated tests pass.
- [ ] The API key is configured securely.
- [ ] The deployment instructions match the chosen hosting platform.
- [ ] The latest evaluation report is available, if evaluation has been completed.
- [ ] The client understands how to start, stop, and troubleshoot the application.
