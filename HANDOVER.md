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