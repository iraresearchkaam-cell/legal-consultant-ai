"""Integration-style tests for the Streamlit workflow."""

from __future__ import annotations

from unittest.mock import MagicMock

import app


def test_process_prompt_persists_user_and_assistant_messages(streamlit_mocks, monkeypatch):
    app.initialize_session_state()
    submit_question = MagicMock(return_value=("Final answer", None))
    monkeypatch.setattr(app, "submit_question", submit_question)

    app.process_prompt("Summarize the judgment.")

    assert streamlit_mocks["session_state"].messages == [
        {"role": "user", "content": "Summarize the judgment."},
        {"role": "assistant", "content": "Final answer"},
    ]
    assert submit_question.call_args.args == ("Summarize the judgment.",)
    assert streamlit_mocks["chat_message"].call_args_list[0].args == ("user",)
    assert streamlit_mocks["chat_context"].markdown.call_args_list[0].args == ("Summarize the judgment.",)
    assert streamlit_mocks["spinner"].call_args.args == ("Analyzing case files...",)


def test_process_prompt_surfaces_backend_error_without_assistant_message(streamlit_mocks, monkeypatch):
    app.initialize_session_state()
    monkeypatch.setattr(app, "submit_question", MagicMock(return_value=(None, "Error 500: boom")))

    app.process_prompt("Question")

    assert streamlit_mocks["session_state"].messages == [
        {"role": "user", "content": "Question"}
    ]
    assert streamlit_mocks["error"].call_args.args == ("Error 500: boom",)


def test_process_prompt_handles_request_exception(streamlit_mocks, monkeypatch):
    app.initialize_session_state()
    monkeypatch.setattr(
        app,
        "submit_question",
        MagicMock(side_effect=app.requests.RequestException("connection reset")),
    )

    app.process_prompt("Question")

    assert streamlit_mocks["session_state"].messages == [
        {"role": "user", "content": "Question"}
    ]
    assert streamlit_mocks["error"].call_args.args == ("Connection Error: connection reset",)


def test_setup_page_renders_expected_header(streamlit_mocks):
    app.setup_page()

    assert streamlit_mocks["set_page_config"].call_args.kwargs == {
        "page_title": app.DEFAULT_PAGE_TITLE,
        "page_icon": app.DEFAULT_PAGE_ICON,
    }
    assert streamlit_mocks["title"].call_args.args == ("⚖️ AI Legal Consultant",)
    assert streamlit_mocks["markdown"].call_args.args == (
        "Ask questions about Supreme Court judgments (Workstream 2 Pilot).",
    )


def test_main_renders_history_and_processes_new_prompt(streamlit_mocks, monkeypatch):
    streamlit_mocks["session_state"].messages = [
        {"role": "assistant", "content": "Existing answer"}
    ]
    streamlit_mocks["chat_input"].return_value = "New question"
    process_prompt = MagicMock()
    monkeypatch.setattr(app, "process_prompt", process_prompt)

    app.main()

    process_prompt.assert_called_once_with("New question")
    assert streamlit_mocks["chat_message"].call_args_list[0].args == ("assistant",)
    assert streamlit_mocks["markdown"].call_args_list[0].args == (
        "Ask questions about Supreme Court judgments (Workstream 2 Pilot).",
    )


def test_main_skips_processing_when_no_prompt_is_entered(streamlit_mocks, monkeypatch):
    process_prompt = MagicMock()
    monkeypatch.setattr(app, "process_prompt", process_prompt)

    app.main()

    process_prompt.assert_not_called()
