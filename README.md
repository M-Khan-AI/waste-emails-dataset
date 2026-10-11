# Email Classifier

A small Python module that uses an LLM ("GEMINI_MODEL", gemini-2.5-flash)to sort an email into one of four categories. If the model is unsure, or returns anything unexpected, the classifier returns `"I don't know"`.

## Categories

| Category | Typical email |
|---|---|
| `Missed Pickup` | "My garbage was not collected today." |
| `Schedule Change` | "I want to change my collection day." |
| `Complaint` | "The service is very poor." |
| `Other` | "I would like some general information." |
| `I don't know` (fallback) | Empty input, ambiguous email, or invalid model output |

## Project structure
waste-email-dataset
|
├── evaluate_classifier.py     # The it classifies the categories
├── evaluation_predicions.csv  # Actual and predicted labels
├── evaluation_report.md       # Shows metrics, category-wise results, errors, and limitations.
├── confusion_matrix.png       # Shows the data in a graph
├── requirements.txt           # Stores python libraries and packages to run
└── README.md                  # Complete detail about the project

## Requirements

- Python 3.8+
- pandas
- matplotlib
- scikit-learn
- gemini-2.5-flash
- python-dotenv

## Setup

```bash
pip install pandas
pip install matplotlib
pip install scikit-learn
pip install-genai
```
## API Key Setup
1. create api key in google ai studio
2. create .env file in root
3.  copy api key and paste in .env

export GEMINI_API_KEY="your-api-key-here"      # macOS / Linux
       GEMINI_MODEL=gemini-2.5-flash
setx GEMINI_MODEL="your-api-key-here"      # Windows

## Usage

**Run the script:**

```bash
python evaluate_classifier.py
```

**Generated files:**
- `evaluation_report.md` — Detailed performance report.
- `confusion_matrix.png` — Visual representation of classification results.
- `evaluation_predictions.csv` — Actual and predicted labels for each email.

**Note:** Configure the Gemini API key and install the required dependencies before running the script.

## How it works

1. **Empty check:** blank or whitespace-only input returns `"I don't know"` immediately, with no API call.
2. **Ask the model:** the email is sent to `gemini-2.5-flash` with a system prompt that lists the valid categories and asks for the exact category name only. `temperature=0` keeps answers consistent.
3. **Clean the reply:** surrounding whitespace, quotes, and periods are stripped.
4. **Validate:** the cleaned reply is compared (case-insensitive) against the category list. A match returns the official spelling. Anything else returns `"I don't know"`.

The model's output is never trusted blindly, so the function can only return a value from the approved list or the fallback.

## Configuration

All settings are constants at the top of `classify_email.py`:

| Constant | Purpose | Default |
|---|---|---|
| `CATEGORIES` | Valid categories | `["Missed Pickup", "Schedule Change", "Complaint", "Other"]` |
| `FALLBACK` | Returned when uncertain or invalid | `"I don't know"` |
| `MODEL` | gemini model used | `"gemini-2.5-flash"` |

To add a category, append it to `CATEGORIES`. The system prompt is rebuilt from that list automatically.

## Evaluation Report

For detailed performance metrics and classification results, see the
[Evaluation Report](evaluation_report.md).

## Author:
Muhammad Khan