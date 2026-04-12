"""Streamlit frontend for the Legal Consultant AI assistant."""

from __future__ import annotations

import json
import os
from typing import Optional, Tuple

import requests
import streamlit as st

DEFAULT_WEBHOOK_URL = "http://localhost:5678/webhook/consultant-bot"
DEFAULT_PAGE_TITLE = "Legal Mind AI"
DEFAULT_PAGE_ICON = "⚖️"
DEFAULT_REQUEST_TIMEOUT = 30
ERROR_NO_ANSWER = "Error: No answer field found."


def get_webhook_url() -> str:
    """Return the configured backend webhook URL."""
    return os.getenv("N8N_WEBHOOK_URL", DEFAULT_WEBHOOK_URL)


def initialize_session_state() -> None:
    """Ensure chat history exists in the Streamlit session."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def append_message(role: str, content: str) -> None:
    """Persist a chat message in session state."""
    st.session_state.messages.append({"role": role, "content": content})


def render_chat_history() -> None:
    """Render all persisted messages in chronological order."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def submit_question(
    prompt: str,
    webhook_url: Optional[str] = None,
    timeout: int = DEFAULT_REQUEST_TIMEOUT,
) -> Tuple[Optional[str], Optional[str]]:
    """Send the user's question to the backend and normalize the result."""
    response = requests.post(
        webhook_url or get_webhook_url(),
        json={"chatInput": prompt},
        timeout=timeout,
    )

    if response.status_code != 200:
        return None, f"Error {response.status_code}: {response.text}"

    try:
        payload = response.json()
    except json.JSONDecodeError as exc:
        return None, f"Invalid response format: {exc}"

    answer = payload.get("answer")
    if answer is None:
        answer = ERROR_NO_ANSWER

    return answer, None


def process_prompt(prompt: str) -> None:
    """Handle a new user message and render the assistant response."""
    st.chat_message("user").markdown(prompt)
    append_message("user", prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing case files..."):
            try:
                ai_answer, error_message = submit_question(prompt)
            except requests.RequestException as exc:
                st.error(f"Connection Error: {exc}")
                return

            if error_message:
                st.error(error_message)
                return

            st.markdown(ai_answer)
            append_message("assistant", ai_answer)


def setup_page() -> None:
    """Render the static page configuration and header."""
    st.set_page_config(page_title=DEFAULT_PAGE_TITLE, page_icon=DEFAULT_PAGE_ICON)
    st.title("⚖️ AI Legal Consultant")
    st.markdown("Ask questions about Supreme Court judgments (Workstream 2 Pilot).")


def main() -> None:
    """Run the Streamlit application."""
    setup_page()
    initialize_session_state()
    render_chat_history()

    prompt = st.chat_input("Ex: Can a railway penalty be imposed after delivery?")
    if prompt:
        process_prompt(prompt)


if __name__ == "__main__":
    main()
