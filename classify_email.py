
"""Email classifier that uses Gemini to select one of four categories."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

CATEGORIES = [
    "Missed Pickup",
    "Schedule Change",
    "Complaint",
    "Other",
]

FALLBACK = "I don't know"

SYSTEM_PROMPT_TEMPLATE = (
    "You are an email classifier. Classify the user's email into exactly "
    "one of these categories:\n{categories}\n\n"
    "Reply with the exact category name and nothing else. "
    'If you are not certain which category fits, reply exactly: "{fallback}".'
)

SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.format(
    categories="\n".join(f"- {category}" for category in CATEGORIES),
    fallback=FALLBACK,
)


def _call_model(text: str) -> str:
    """Send the email to Gemini and return its raw response."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from the environment.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL,
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )

    return response.text or ""


def classify_email(text: str) -> str:
    """Return a valid category or the fallback label."""

    if not text or not text.strip():
        return FALLBACK

    reply = _call_model(text).strip().strip("\"'.").strip()

    for category in CATEGORIES:
        if reply.casefold() == category.casefold():
            return category

    return FALLBACK
