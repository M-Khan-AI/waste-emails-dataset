"""Email classifier that asks an LLM to pick one of four categories."""

CATEGORIES = ["Missed Pickup", "Schedule Change", "Complaint", "Other"]
FALLBACK = "I don't know"
MODEL = "gpt-4o-mini"

# System prompt template.
# - {categories} is filled with the bulleted list of valid categories.
# - {fallback} is the exact string the model must return when uncertain.
# The model is told to answer with the category name only, so the reply
# can be matched directly against CATEGORIES without parsing.
SYSTEM_PROMPT_TEMPLATE = (
    "You are an email classifier. Classify the user's email into exactly one "
    "of these categories:\n{categories}\n\n"
    "Reply with the exact category name and nothing else. "
    'If you are not certain which category fits, reply exactly: "{fallback}".'
)

SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.format(
    categories="\n".join(f"- {c}" for c in CATEGORIES),
    fallback=FALLBACK,
)


def _call_model(text: str) -> str:
    """Send the email to the OpenAI API and return the raw reply text.

    Kept separate so tests can mock it without touching the network.
    """
    from openai import OpenAI  # imported lazily so tests don't need the package

    client = OpenAI()  # reads OPENAI_API_KEY from the environment
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""


def classify_email(text: str) -> str:
    """Return one of CATEGORIES, or "I don't know" if uncertain or invalid."""
    if not text or not text.strip():
        return FALLBACK  # nothing to classify; skip the API call

    reply = _call_model(text).strip().strip("\"'.").strip()

    for category in CATEGORIES:
        if reply.lower() == category.lower():
            return category
    return FALLBACK  # covers "I don't know" and any unexpected output