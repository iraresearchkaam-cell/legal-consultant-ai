"""Pytest fixtures shared across the test suite."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

import app


class SessionState(dict):
    """Dictionary-backed session state with attribute access."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


@pytest.fixture
def streamlit_mocks(monkeypatch):
    """Patch Streamlit entry points used by the application."""
    session_state = SessionState()
    set_page_config = MagicMock()
    title = MagicMock()
    markdown = MagicMock()
    error = MagicMock()
    chat_input = MagicMock(return_value=None)

    chat_context = MagicMock()
    chat_context.__enter__.return_value = None
    chat_context.__exit__.return_value = None
    chat_context.markdown = MagicMock()
    chat_message = MagicMock(return_value=chat_context)

    spinner_context = MagicMock()
    spinner_context.__enter__.return_value = None
    spinner_context.__exit__.return_value = None
    spinner = MagicMock(return_value=spinner_context)

    monkeypatch.setattr(app.st, "session_state", session_state)
    monkeypatch.setattr(app.st, "set_page_config", set_page_config)
    monkeypatch.setattr(app.st, "title", title)
    monkeypatch.setattr(app.st, "markdown", markdown)
    monkeypatch.setattr(app.st, "error", error)
    monkeypatch.setattr(app.st, "chat_input", chat_input)
    monkeypatch.setattr(app.st, "chat_message", chat_message)
    monkeypatch.setattr(app.st, "spinner", spinner)

    return {
        "session_state": session_state,
        "set_page_config": set_page_config,
        "title": title,
        "markdown": markdown,
        "error": error,
        "chat_input": chat_input,
        "chat_message": chat_message,
        "chat_context": chat_context,
        "spinner": spinner,
    }


@pytest.fixture
def mock_post(monkeypatch):
    """Patch the outgoing POST request used by the application."""
    post = MagicMock()
    monkeypatch.setattr(app.requests, "post", post)
    return post


@pytest.fixture
def make_response():
    """Create a lightweight response object for request tests."""

    def _make_response(status_code=200, payload=None, text="", json_error=None):
        response = MagicMock()
        response.status_code = status_code
        response.text = text
        if json_error is not None:
            response.json.side_effect = json_error
        else:
            response.json.return_value = payload or {}
        return response

    return _make_response


@pytest.fixture
def invalid_json_error():
    """Provide a representative JSON decode failure."""
    return json.JSONDecodeError("Expecting value", "not-json", 0)
