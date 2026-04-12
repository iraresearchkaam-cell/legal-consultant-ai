"""Pytest configuration and shared fixtures."""
import pytest
import sys
from unittest.mock import Mock, patch
from pathlib import Path

# Add parent directory to path to allow imports from app module
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_streamlit():
    """Mock streamlit module for testing."""
    with patch("streamlit.set_page_config") as mock_config, \
         patch("streamlit.title") as mock_title, \
         patch("streamlit.markdown") as mock_markdown, \
         patch("streamlit.chat_message") as mock_chat, \
         patch("streamlit.chat_input") as mock_input, \
         patch("streamlit.spinner") as mock_spinner, \
         patch("streamlit.error") as mock_error, \
         patch("streamlit.session_state", new_callable=lambda: Mock()) as mock_state:
        
        mock_spinner.return_value.__enter__ = Mock()
        mock_spinner.return_value.__exit__ = Mock()
        
        yield {
            "set_page_config": mock_config,
            "title": mock_title,
            "markdown": mock_markdown,
            "chat_message": mock_chat,
            "chat_input": mock_input,
            "spinner": mock_spinner,
            "error": mock_error,
            "session_state": mock_state,
        }


@pytest.fixture
def mock_requests():
    """Mock requests module for testing."""
    with patch("requests.post") as mock_post:
        yield mock_post


@pytest.fixture
def sample_responses():
    """Provide sample API responses for testing."""
    return {
        "success": {
            "status_code": 200,
            "json_return": {"answer": "A railway penalty can be imposed within the specified statutory period."}
        },
        "no_answer_field": {
            "status_code": 200,
            "json_return": {"data": "Some data without answer field"}
        },
        "server_error": {
            "status_code": 500,
            "text": "Internal Server Error"
        },
        "not_found": {
            "status_code": 404,
            "text": "Not Found"
        },
        "bad_request": {
            "status_code": 400,
            "text": "Bad Request"
        }
    }
