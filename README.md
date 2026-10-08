# Email Classifier

A small Python module that uses an LLM (OpenAI `gpt-4o-mini`) to sort an email into one of four categories. If the model is unsure, or returns anything unexpected, the classifier returns `"I don't know"`.

## Categories

| Category | Typical email |
|---|---|
| `Missed Pickup` | "My garbage was not collected today." |
| `Schedule Change` | "I want to change my collection day." |
| `Complaint` | "The service is very poor." |
| `Other` | "I would like some general information." |
| `I don't know` (fallback) | Empty input, ambiguous email, or invalid model output |

## Project structure
.
├── classify_email.py        # The classifier
├── test_classify_email.py   # Unit tests (no network needed)
└── README.md

## Requirements

- Python 3.8+
- An OpenAI API key (only needed to classify real emails, not to run the tests)
- The `openai` package (only needed for real use)
- `pytest` (for running the tests)

## Setup

```bash
pip install openai pytest
export OPENAI_API_KEY="your-api-key-here"      # macOS / Linux
# setx OPENAI_API_KEY "your-api-key-here"      # Windows
```

## Usage

```python
from classify_email import classify_email

print(classify_email("You missed my bin again today!"))
# Missed Pickup

print(classify_email("Can we move my pickup to Friday?"))
# Schedule Change

print(classify_email(""))
# I don't know
```

`classify_email(text)` always returns one of five strings: the four categories above or `"I don't know"`.

## How it works

1. **Empty check:** blank or whitespace-only input returns `"I don't know"` immediately, with no API call.
2. **Ask the model:** the email is sent to `gpt-4o-mini` with a system prompt that lists the valid categories and asks for the exact category name only. `temperature=0` keeps answers consistent.
3. **Clean the reply:** surrounding whitespace, quotes, and periods are stripped.
4. **Validate:** the cleaned reply is compared (case-insensitive) against the category list. A match returns the official spelling. Anything else returns `"I don't know"`.

The model's output is never trusted blindly, so the function can only return a value from the approved list or the fallback.

## Configuration

All settings are constants at the top of `classify_email.py`:

| Constant | Purpose | Default |
|---|---|---|
| `CATEGORIES` | Valid categories | `["Missed Pickup", "Schedule Change", "Complaint", "Other"]` |
| `FALLBACK` | Returned when uncertain or invalid | `"I don't know"` |
| `MODEL` | OpenAI model used | `"gpt-4o-mini"` |

To add a category, append it to `CATEGORIES`. The system prompt is rebuilt from that list automatically.

## Running the tests

pytest

The tests replace `_call_model` with a mock using `unittest.mock.patch`, so they run instantly, cost nothing, and need no API key or internet connection.

| Test | What it checks |
|---|---|
| `test_typical_email_returns_category` | "Missed Pickup" reply is returned correctly |
| `test_schedule_change_returns_category` | "Schedule Change" reply is returned correctly |
| `test_complaint_returns_category` | "Complaint" reply is returned correctly |
| `test_other_returns_category` | "Other" reply is returned correctly |
| `test_ambiguous_email_returns_fallback` | Model says "I don't know" → fallback |
| `test_empty_input_returns_fallback_without_api_call` | Empty or blank input skips the API |
| `test_reply_is_normalized` | `" complaint. "` becomes `"Complaint"` |
| `test_unexpected_reply_returns_fallback` | Invalid reply like `"Spam"` → fallback |
| `test_prompt_lists_all_categories_and_fallback` | System prompt contains every category and the fallback |

## Limitations

The tests do not call the real OpenAI API, so `_call_model` itself is not covered. Run the function manually once with a real key to verify it.
Each call classifies a single email and makes one API request. There is no retry or error handling for network or API failures.
Classification quality depends on the model. Ambiguous emails may fall back to `"I don't know"`.