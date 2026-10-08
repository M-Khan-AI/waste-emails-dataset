from unittest.mock import patch

import classify_email as ce

def test_typical_email_returns_category():
    with patch.object(
        ce,
        "_call_model",
        return_value="Missed Pickup"
    ) as mock:
        result = ce.classify_email(
            "My garbage was not collected today."
        )

    assert result == "Missed Pickup"
    mock.assert_called_once()

def test_schedule_change_returns_category():
    with patch.object(
        ce,
        "_call_model",
        return_value="Schedule Change"
    ) as mock:
        result = ce.classify_email(
            "I want to change my garbage collection day."
        )

    assert result == "Schedule Change"
    mock.assert_called_once()

def test_complaint_returns_category():
    with patch.object(
        ce,
        "_call_model",
        return_value="Complaint"
    ) as mock:
        result = ce.classify_email(
            "The garbage collection service is very poor."
        )

    assert result == "Complaint"
    mock.assert_called_once()

def test_other_returns_category():
    with patch.object(
        ce,
        "_call_model",
        return_value="Other"
    ) as mock:
        result = ce.classify_email(
            "I would like some general information."
        )

    assert result == "Other"
    mock.assert_called_once()


def test_ambiguous_email_returns_fallback():
    with patch.object(
        ce,
        "_call_model",
        return_value="I don't know"
    ):
        assert (
            ce.classify_email("Hmm, maybe, not sure.")
            == "I don't know"
        )

def test_empty_input_returns_fallback_without_api_call():
    with patch.object(ce, "_call_model") as mock:
        assert ce.classify_email("") == "I don't know"
        assert ce.classify_email("   \n ") == "I don't know"

    mock.assert_not_called()

def test_reply_is_normalized():
    with patch.object(
        ce,
        "_call_model",
        return_value=" complaint. "
    ):
        assert (
            ce.classify_email(
                "The garbage service was very poor."
            )
            == "Complaint"
        )

def test_unexpected_reply_returns_fallback():
    with patch.object(
        ce,
        "_call_model",
        return_value="Spam"
    ):
        assert (
            ce.classify_email("Win a prize!")
            == "I don't know"
        )

def test_prompt_lists_all_categories_and_fallback():
    for category in ce.CATEGORIES:
        assert category in ce.SYSTEM_PROMPT

    assert ce.FALLBACK in ce.SYSTEM_PROMPT
    