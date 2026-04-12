"""Unit tests for core application helpers."""

from __future__ import annotations

import app


def test_get_webhook_url_uses_default_when_env_is_missing(monkeypatch):
    monkeypatch.delenv("N8N_WEBHOOK_URL", raising=False)

    assert app.get_webhook_url() == app.DEFAULT_WEBHOOK_URL


def test_get_webhook_url_uses_environment_override(monkeypatch):
    custom_url = "https://example.com/legal-consultant"
    monkeypatch.setenv("N8N_WEBHOOK_URL", custom_url)

    assert app.get_webhook_url() == custom_url


def test_initialize_session_state_creates_messages_list(streamlit_mocks):
    app.initialize_session_state()

    assert streamlit_mocks["session_state"].messages == []


def test_initialize_session_state_preserves_existing_messages(streamlit_mocks):
    existing_messages = [{"role": "user", "content": "Existing question"}]
    streamlit_mocks["session_state"].messages = existing_messages.copy()

    app.initialize_session_state()

    assert streamlit_mocks["session_state"].messages == existing_messages


def test_append_message_adds_message_to_history(streamlit_mocks):
    app.initialize_session_state()

    app.append_message("assistant", "Here is the legal summary.")

    assert streamlit_mocks["session_state"].messages == [
        {"role": "assistant", "content": "Here is the legal summary."}
    ]


def test_render_chat_history_renders_each_saved_message(streamlit_mocks):
    streamlit_mocks["session_state"].messages = [
        {"role": "user", "content": "Question one"},
        {"role": "assistant", "content": "Answer one"},
    ]

    app.render_chat_history()

    assert streamlit_mocks["chat_message"].call_count == 2
    assert streamlit_mocks["chat_message"].call_args_list[0].args == ("user",)
    assert streamlit_mocks["chat_message"].call_args_list[1].args == ("assistant",)
    assert streamlit_mocks["markdown"].call_args_list[0].args == ("Question one",)
    assert streamlit_mocks["markdown"].call_args_list[1].args == ("Answer one",)


def test_submit_question_returns_answer_on_success(mock_post, make_response):
    mock_post.return_value = make_response(payload={"answer": "The appeal is maintainable."})

    answer, error = app.submit_question("Can I file an appeal?")

    assert answer == "The appeal is maintainable."
    assert error is None
    assert mock_post.call_args.kwargs["json"] == {"chatInput": "Can I file an appeal?"}
    assert mock_post.call_args.kwargs["timeout"] == app.DEFAULT_REQUEST_TIMEOUT


def test_submit_question_falls_back_when_answer_field_is_missing(mock_post, make_response):
    mock_post.return_value = make_response(payload={"status": "ok"})

    answer, error = app.submit_question("Question")

    assert answer == app.ERROR_NO_ANSWER
    assert error is None


def test_submit_question_returns_http_error_message(mock_post, make_response):
    mock_post.return_value = make_response(status_code=503, text="Backend unavailable")

    answer, error = app.submit_question("Question")

    assert answer is None
    assert error == "Error 503: Backend unavailable"


def test_submit_question_returns_invalid_json_error(mock_post, make_response, invalid_json_error):
    mock_post.return_value = make_response(json_error=invalid_json_error)

    answer, error = app.submit_question("Question")

    assert answer is None
    assert error.startswith("Invalid response format:")


def test_submit_question_preserves_empty_string_answer(mock_post, make_response):
    mock_post.return_value = make_response(payload={"answer": ""})

    answer, error = app.submit_question("Question")

    assert answer == ""
    assert error is None
