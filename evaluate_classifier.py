"""
Evaluate the CleanCity email classifier.

Reads emails_labeled.csv with columns:
    email_id, subject, body, category

Creates:
    evaluation_report.md
    confusion_matrix.png
    evaluation_predictions.csv
"""

from pathlib import Path
import time

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from classify_email import classify_email, CATEGORIES, FALLBACK


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "emails_labeled.csv"
REPORT_FILE = BASE_DIR / "evaluation_report.md"
MATRIX_FILE = BASE_DIR / "confusion_matrix.png"
PREDICTIONS_FILE = BASE_DIR / "evaluation_predictions.csv"

SUBJECT_COLUMN = "subject"
BODY_COLUMN = "body"
LABEL_COLUMN = "category"

# Delay between API calls to reduce request bursts. Set to 0 to disable.
API_DELAY_SECONDS = 0.2


# --------------------------------------------------
# 2. Load and validate the dataset
# --------------------------------------------------

def load_dataset():
    """Load the CSV, combine subject/body, and validate labels."""
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_FILE}\n"
            "Place emails_labeled.csv in the same folder as this script."
        )

    df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")

    required_columns = {SUBJECT_COLUMN, BODY_COLUMN, LABEL_COLUMN}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required CSV columns: {sorted(missing_columns)}\n"
            f"Available columns: {list(df.columns)}"
        )

    # Missing subjects are allowed; missing bodies or labels are not.
    df[SUBJECT_COLUMN] = df[SUBJECT_COLUMN].fillna("").astype(str).str.strip()
    df[BODY_COLUMN] = df[BODY_COLUMN].fillna("").astype(str).str.strip()
    df[LABEL_COLUMN] = df[LABEL_COLUMN].fillna("").astype(str).str.strip()

    df = df[
        ((df[SUBJECT_COLUMN] != "") | (df[BODY_COLUMN] != ""))
        & (df[LABEL_COLUMN] != "")
    ].copy()

    if df.empty:
        raise ValueError("The dataset contains no usable labeled emails.")

    # Make category matching tolerant of capitalization and surrounding spaces.
    category_lookup = {category.casefold(): category for category in CATEGORIES}
    normalized_labels = df[LABEL_COLUMN].map(
        lambda value: category_lookup.get(value.casefold(), value)
    )
    invalid = sorted(set(normalized_labels) - set(CATEGORIES))
    if invalid:
        raise ValueError(
            f"Labels not in CATEGORIES: {invalid}\n"
            f"Valid categories: {CATEGORIES}\n"
            "Update CATEGORIES in classify_email.py or correct the CSV labels."
        )

    df[LABEL_COLUMN] = normalized_labels
    df["email_text"] = (
        "Subject: " + df[SUBJECT_COLUMN]
        + "\nBody: " + df[BODY_COLUMN]
    ).str.strip()

    return df.reset_index(drop=True)


# --------------------------------------------------
# 3. Run the classifier on every email
# --------------------------------------------------

def predict_emails(df):
    """Classify each email and record API/runtime exceptions separately."""
    predictions = []
    errors = []
    total = len(df)

    for index, email_text in enumerate(df["email_text"], start=1):
        try:
            prediction = classify_email(email_text)

            if not isinstance(prediction, str):
                raise ValueError("Classifier returned a non-string category.")

            prediction = prediction.strip()

            # Accept only an allowed category or the configured fallback.
            valid_lookup = {category.casefold(): category for category in CATEGORIES}
            if prediction.casefold() in valid_lookup:
                prediction = valid_lookup[prediction.casefold()]
            elif prediction.casefold() == FALLBACK.casefold():
                prediction = FALLBACK
            else:
                prediction = FALLBACK

            predictions.append(prediction)
            errors.append("")

        except Exception as exc:
            # Preserve one prediction per input row if an API/runtime error occurs.
            predictions.append(FALLBACK)
            errors.append(f"{type(exc).__name__}: {exc}")
            print(f"Error on email {index}: {type(exc).__name__}: {exc}")

        if index % 10 == 0 or index == total:
            print(f"Processed {index}/{total} emails")

        if index < total and API_DELAY_SECONDS > 0:
            time.sleep(API_DELAY_SECONDS)

    return predictions, errors


# --------------------------------------------------
# 4. Calculate evaluation metrics
# --------------------------------------------------

def calculate_metrics(actual, predicted):
    """Calculate accuracy, per-category metrics, and confusion matrix."""
    # Include fallback as a prediction column/row so uncertain results are visible.
    labels = list(CATEGORIES)
    if FALLBACK not in labels:
        labels.append(FALLBACK)

    accuracy = accuracy_score(actual, predicted)
    metrics = classification_report(
        actual,
        predicted,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(actual, predicted, labels=labels)
    return labels, accuracy, metrics, matrix


# --------------------------------------------------
# 5. Save confusion matrix image
# --------------------------------------------------

def save_confusion_matrix(labels, matrix):
    """Create and save a labeled confusion matrix image."""
    figure_size = max(8, len(labels) * 1.5)
    fig, ax = plt.subplots(figsize=(figure_size, figure_size * 0.8))

    image = ax.imshow(matrix, cmap="Blues")
    fig.colorbar(image, ax=ax, label="Number of emails")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Actual label")
    ax.set_title("CleanCity Email Classification Confusion Matrix")

    threshold = matrix.max() / 2 if matrix.size and matrix.max() else 0
    for row in range(len(labels)):
        for col in range(len(labels)):
            color = "white" if matrix[row, col] > threshold else "black"
            ax.text(
                col, row, str(matrix[row, col]),
                ha="center", va="center", color=color,
            )

    fig.tight_layout()
    fig.savefig(MATRIX_FILE, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Confusion matrix saved: {MATRIX_FILE.name}")


# --------------------------------------------------
# 6. Generate Markdown evaluation report
# --------------------------------------------------

def generate_report(df, predictions, errors, labels, accuracy, metrics):
    """Write evaluation results to a Markdown report."""
    total = len(df)
    error_count = sum(bool(error) for error in errors)
    fallback_count = sum(prediction == FALLBACK for prediction in predictions)

    report = [
        "# CleanCity Email Classifier Evaluation Report",
        "",
        "## 1. Overview",
        "",
        "This report compares classifier predictions with the ground-truth labels.",
        "",
        "## 2. Dataset Summary",
        "",
        f"- Dataset: `{CSV_FILE.name}`",
        f"- Emails evaluated: {total}",
        f"- Runtime/API exceptions: {error_count}",
        f"- Fallback (`{FALLBACK}`) predictions: {fallback_count}",
        f"- Categories shown (including fallback): {len(labels)}",
        "",
        "## 3. Overall Performance",
        "",
        f"- **Accuracy:** {accuracy:.2%}",
        f"- **Macro precision:** {metrics['macro avg']['precision']:.2%}",
        f"- **Macro recall:** {metrics['macro avg']['recall']:.2%}",
        f"- **Macro F1-score:** {metrics['macro avg']['f1-score']:.2%}",
        f"- **Weighted precision:** {metrics['weighted avg']['precision']:.2%}",
        f"- **Weighted recall:** {metrics['weighted avg']['recall']:.2%}",
        f"- **Weighted F1-score:** {metrics['weighted avg']['f1-score']:.2%}",
        "",
        "## 4. Per-Category Metrics",
        "",
        "| Category | Precision | Recall | F1-score | Support |",
        "|---|---:|---:|---:|---:|",
    ]

    for label in labels:
        result = metrics[label]
        report.append(
            f"| {label} | {result['precision']:.2%} "
            f"| {result['recall']:.2%} | {result['f1-score']:.2%} "
            f"| {int(result['support'])} |"
        )

    report.extend([
        "",
        "## 5. Confusion Matrix",
        "",
        "Rows represent actual labels; columns represent predicted labels.",
        "",
        "![Confusion Matrix](confusion_matrix.png)",
        "",
        "## 6. Prediction Results",
        "",
        f"Detailed predictions and error details are saved in `{PREDICTIONS_FILE.name}`.",
        "",
        "## 7. Error Analysis",
        "",
    ])

    if error_count:
        report.append(
            f"The evaluation script encountered runtime/API exceptions for "
            f"{error_count} email(s). Those rows were assigned `{FALLBACK}`. "
            "Review the `evaluation_error` column in the predictions CSV."
        )
    else:
        report.append(
            "No runtime/API exceptions were recorded by the evaluation script. "
            "This does not guarantee that every prediction was correct."
        )

    report.extend([
        "",
        "Fallback predictions may indicate uncertainty or invalid model output. "
        "They are counted as incorrect unless the ground-truth label matches the fallback.",
        "",
        "## 8. Conclusion",
        "",
        f"Overall accuracy on this dataset was {accuracy:.2%}. "
        "Use the per-category metrics and prediction CSV to investigate errors. "
        "Results on this dataset do not guarantee performance on new emails.",
        "",
    ])

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")
    print(f"Markdown report saved: {REPORT_FILE.name}")


# --------------------------------------------------
# 7. Main workflow
# --------------------------------------------------

def main():
    """Run the complete evaluation workflow."""
    print("=" * 55)
    print("CleanCity Email Classifier Evaluation")
    print("=" * 55)

    df = load_dataset()
    print(f"Loaded {len(df)} labeled emails.")

    predictions, errors = predict_emails(df)
    actual = df[LABEL_COLUMN].tolist()

    labels, accuracy, metrics, matrix = calculate_metrics(actual, predictions)

    results_df = df.copy()
    results_df["predicted_label"] = predictions
    results_df["correct"] = [
        true_label == predicted_label
        for true_label, predicted_label in zip(actual, predictions)
    ]
    results_df["evaluation_error"] = errors
    results_df.to_csv(PREDICTIONS_FILE, index=False, encoding="utf-8-sig")

    save_confusion_matrix(labels, matrix)
    generate_report(df, predictions, errors, labels, accuracy, metrics)

    print()
    print(f"Overall accuracy: {accuracy:.2%}")
    print(f"Runtime/API exceptions: {sum(bool(error) for error in errors)}")
    print(f"Fallback predictions: {sum(p == FALLBACK for p in predictions)}")
    print(f"Predictions saved: {PREDICTIONS_FILE.name}")
    print(f"Report saved: {REPORT_FILE.name}")
    print("Evaluation completed.")


if __name__ == "__main__":
    main()
