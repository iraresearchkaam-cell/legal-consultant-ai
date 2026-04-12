"""Edge case coverage for application behavior."""

from __future__ import annotations

import app


def test_submit_question_uses_explicit_webhook_url_and_timeout(mock_post, make_response):
    mock_post.return_value = make_response(payload={"answer": "ok"})

    answer, error = app.submit_question(
        "Question",
        webhook_url="https://example.com/webhook",
        timeout=10,
    )

    assert answer == "ok"
    assert error is None
    assert mock_post.call_args.args[0] == "https://example.com/webhook"
    assert mock_post.call_args.kwargs["timeout"] == 10


def test_render_chat_history_handles_empty_history(streamlit_mocks):
    app.initialize_session_state()

    app.render_chat_history()

    streamlit_mocks["chat_message"].assert_not_called()
    streamlit_mocks["markdown"].assert_not_called()


def test_process_prompt_keeps_whitespace_only_message_as_entered(streamlit_mocks, monkeypatch):
    app.initialize_session_state()
    monkeypatch.setattr(app, "submit_question", lambda prompt: ("Acknowledged", None))

    app.process_prompt("   ")

    assert streamlit_mocks["session_state"].messages[0] == {
        "role": "user",
        "content": "   ",
    }


def test_process_prompt_handles_missing_answer_response(streamlit_mocks, monkeypatch):
    app.initialize_session_state()
    monkeypatch.setattr(app, "submit_question", lambda prompt: (app.ERROR_NO_ANSWER, None))

    app.process_prompt("Question")

    assert streamlit_mocks["session_state"].messages[-1] == {
        "role": "assistant",
        "content": app.ERROR_NO_ANSWER,
    }


def test_process_prompt_supports_unicode_content(streamlit_mocks, monkeypatch):
    app.initialize_session_state()
    unicode_prompt = "क्या रेलवे दंड लागू किया जा सकता है?"
    unicode_answer = "हाँ, प्रासंगिक वैधानिक अवधि के भीतर."
    monkeypatch.setattr(app, "submit_question", lambda prompt: (unicode_answer, None))

    app.process_prompt(unicode_prompt)

    assert streamlit_mocks["session_state"].messages == [
        {"role": "user", "content": unicode_prompt},
        {"role": "assistant", "content": unicode_answer},
    ]
