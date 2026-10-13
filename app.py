"""Flask web app: paste an email, see its predicted category."""

from flask import Flask, render_template, request

from classify_email import ClassificationError, classify_email

app = Flask(__name__)

MAX_EMAIL_CHARS = 8000


@app.route("/", methods=["GET", "POST"])
def index():
    category = None
    error = None
    email_text = ""

    if request.method == "POST":
        email_text = request.form.get("email_text", "").strip()

        if not email_text:
            error = "Please paste an email before submitting."
        elif len(email_text) > MAX_EMAIL_CHARS:
            error = f"The email is too long (maximum {MAX_EMAIL_CHARS} characters)."
        else:
            try:
                category = classify_email(email_text)
            except ClassificationError as exc:
                error = str(exc)
            except Exception:
                app.logger.exception("Unexpected error during classification")
                error = "Something went wrong. Please try again."

    return render_template(
        "index.html", category=category, error=error, email_text=email_text
    )


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
