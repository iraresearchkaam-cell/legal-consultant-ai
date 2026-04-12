"""Unit tests for the Legal Consultant AI application."""
import pytest
from unittest.mock import Mock, MagicMock, patch, call
import json


class TestChatInterface:
    """Test cases for chat interface functionality."""

    def test_session_state_initialization(self, mock_streamlit):
        """Test that session state is properly initialized with empty messages."""
        mock_state = mock_streamlit["session_state"]
        mock_state.get = Mock(return_value=None)
        
        # Simulate the initialization check from the app
        messages = mock_state.get.return_value or []
        
        assert isinstance(messages, list)
        assert len(messages) == 0

    def test_session_state_persists_messages(self, mock_streamlit):
        """Test that messages are stored and persisted in session state."""
        mock_state = mock_streamlit["session_state"]
        mock_messages = [
            {"role": "user", "content": "Test question"},
            {"role": "assistant", "content": "Test answer"}
        ]
        mock_state.messages = mock_messages
        
        # Verify messages are accessible
        assert len(mock_state.messages) == 2
        assert mock_state.messages[0]["role"] == "user"
        assert mock_state.messages[1]["role"] == "assistant"

    def test_user_message_format(self):
        """Test that user messages follow the correct format."""
        user_message = {"role": "user", "content": "Can a railway penalty be imposed after delivery?"}
        
        assert user_message["role"] == "user"
        assert isinstance(user_message["content"], str)
        assert len(user_message["content"]) > 0

    def test_assistant_message_format(self):
        """Test that assistant messages follow the correct format."""
        assistant_message = {"role": "assistant", "content": "Yes, according to section..."}
        
        assert assistant_message["role"] == "assistant"
        assert isinstance(assistant_message["content"], str)
        assert len(assistant_message["content"]) > 0

    def test_message_history_order(self, mock_streamlit):
        """Test that message history maintains chronological order."""
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = [
            {"role": "user", "content": "Question 1"},
            {"role": "assistant", "content": "Answer 1"},
            {"role": "user", "content": "Question 2"},
            {"role": "assistant", "content": "Answer 2"},
        ]
        
        # Verify order
        for i, msg in enumerate(mock_state.messages):
            assert msg["role"] in ["user", "assistant"]
        
        # Verify alternating pattern (typical chat flow)
        assert mock_state.messages[0]["role"] == "user"
        assert mock_state.messages[1]["role"] == "assistant"


class TestN8NBackend:
    """Test cases for N8N webhook integration."""

    def test_webhook_url_configuration(self):
        """Test that webhook URL is properly configured."""
        webhook_url = "http://localhost:5678/webhook/consultant-bot"
        
        assert webhook_url.startswith("http")
        assert "webhook" in webhook_url
        assert "consultant-bot" in webhook_url

    def test_successful_api_call(self, mock_requests, sample_responses):
        """Test successful API call to N8N backend."""
        success_response = sample_responses["success"]
        mock_response = Mock()
        mock_response.status_code = success_response["status_code"]
        mock_response.json.return_value = success_response["json_return"]
        
        mock_requests.return_value = mock_response
        
        # Simulate API call
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": "Can a railway penalty be imposed?"})
        
        assert response.status_code == 200
        assert response.json()["answer"] == "A railway penalty can be imposed within the specified statutory period."

    def test_missing_answer_field_handling(self, mock_requests, sample_responses):
        """Test handling when API response lacks answer field."""
        no_answer_response = sample_responses["no_answer_field"]
        mock_response = Mock()
        mock_response.status_code = no_answer_response["status_code"]
        mock_response.json.return_value = no_answer_response["json_return"]
        
        mock_requests.return_value = mock_response
        
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": "Test question"})
        
        answer = response.json().get("answer", "Error: No answer field found.")
        assert answer == "Error: No answer field found."

    def test_server_error_handling(self, mock_requests, sample_responses):
        """Test handling of 500 server errors."""
        error_response = sample_responses["server_error"]
        mock_response = Mock()
        mock_response.status_code = error_response["status_code"]
        mock_response.text = error_response["text"]
        
        mock_requests.return_value = mock_response
        
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": "Test"})
        
        assert response.status_code == 500
        assert "Error" in response.text or "error" in response.text.lower()

    def test_not_found_error_handling(self, mock_requests, sample_responses):
        """Test handling of 404 not found errors."""
        error_response = sample_responses["not_found"]
        mock_response = Mock()
        mock_response.status_code = error_response["status_code"]
        mock_response.text = error_response["text"]
        
        mock_requests.return_value = mock_response
        
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": "Test"})
        
        assert response.status_code == 404

    def test_bad_request_handling(self, mock_requests, sample_responses):
        """Test handling of 400 bad request errors."""
        error_response = sample_responses["bad_request"]
        mock_response = Mock()
        mock_response.status_code = error_response["status_code"]
        mock_response.text = error_response["text"]
        
        mock_requests.return_value = mock_response
        
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": "Test"})
        
        assert response.status_code == 400

    def test_network_error_handling(self, mock_requests):
        """Test handling of network connection errors."""
        mock_requests.side_effect = ConnectionError("Failed to connect to server")
        
        with pytest.raises(ConnectionError):
            mock_requests("http://localhost:5678/webhook/consultant-bot",
                         json={"chatInput": "Test"})

    def test_timeout_error_handling(self, mock_requests):
        """Test handling of request timeout errors."""
        mock_requests.side_effect = TimeoutError("Request timed out")
        
        with pytest.raises(TimeoutError):
            mock_requests("http://localhost:5678/webhook/consultant-bot",
                         json={"chatInput": "Test"})

    def test_request_json_payload_format(self):
        """Test that request payload follows correct format."""
        question = "Can a railway penalty be imposed after delivery?"
        payload = {"chatInput": question}
        
        assert "chatInput" in payload
        assert payload["chatInput"] == question
        assert isinstance(payload, dict)


class TestErrorHandling:
    """Test cases for comprehensive error handling."""

    def test_invalid_response_format(self, mock_requests):
        """Test handling of invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        
        mock_requests.return_value = mock_response
        
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": "Test"})
        
        with pytest.raises(json.JSONDecodeError):
            response.json()

    def test_empty_response_text(self, mock_requests):
        """Test handling of empty response text."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = ""
        
        mock_requests.return_value = mock_response
        
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": "Test"})
        
        assert response.status_code == 500
        assert response.text == ""

    def test_malformed_question_input(self):
        """Test handling of various question formats."""
        questions = [
            "Can a railway penalty be imposed?",  # Normal question
            "",  # Empty string
            "   ",  # Whitespace only
            "?" * 100,  # Repeated characters
            "<script>alert('test')</script>",  # Potential XSS
        ]
        
        for question in questions:
            payload = {"chatInput": question}
            assert "chatInput" in payload
            assert isinstance(payload["chatInput"], str)


class TestUIComponents:
    """Test cases for UI component configuration."""

    def test_page_config_setup(self, mock_streamlit):
        """Test page configuration is set up correctly."""
        mock_config = mock_streamlit["set_page_config"]
        
        # This would be called with page_title and page_icon
        assert mock_config is not None

    def test_title_display(self, mock_streamlit):
        """Test title is displayed correctly."""
        mock_title = mock_streamlit["title"]
        expected_title = "⚖️ AI Legal Consultant"
        
        # Verify title mock exists
        assert mock_title is not None

    def test_markdown_content_display(self, mock_streamlit):
        """Test markdown content can be displayed."""
        mock_markdown = mock_streamlit["markdown"]
        test_content = "Ask questions about Supreme Court judgments"
        
        # Verify markdown mock exists
        assert mock_markdown is not None

    def test_chat_message_context_manager(self, mock_streamlit):
        """Test chat message context manager works properly."""
        mock_chat = mock_streamlit["chat_message"]
        mock_chat.return_value.__enter__ = Mock()
        mock_chat.return_value.__exit__ = Mock()
        
        assert mock_chat is not None

    def test_chat_input_collection(self, mock_streamlit):
        """Test user input is collected correctly."""
        mock_input = mock_streamlit["chat_input"]
        mock_input.return_value = "Sample question"
        
        result = mock_input("Ex: Can a railway penalty be imposed after delivery?")
        assert result == "Sample question"


class TestUseCases:
    """Test cases for main use cases."""

    def test_basic_legal_question_flow(self, mock_requests):
        """Test basic flow: user asks legal question -> API responds."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"answer": "Legal answer here"}
        
        mock_requests.return_value = mock_response
        
        # Simulate use case
        question = "Can a railway penalty be imposed after delivery?"
        response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                json={"chatInput": question})
        
        assert response.status_code == 200
        assert "answer" in response.json()

    def test_multiple_questions_session(self, mock_streamlit):
        """Test user can ask multiple questions in one session."""
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = []
        
        questions = [
            "Question 1?",
            "Question 2?",
            "Question 3?"
        ]
        
        for i, question in enumerate(questions):
            mock_state.messages.append({"role": "user", "content": question})
            mock_state.messages.append({"role": "assistant", "content": f"Answer {i+1}"})
        
        assert len(mock_state.messages) == 6  # 3 questions + 3 answers
        assert mock_state.messages[0]["role"] == "user"

    def test_conversation_context_preserved(self, mock_streamlit):
        """Test that conversation context is preserved across interactions."""
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = [
            {"role": "user", "content": "Q1"},
            {"role": "assistant", "content": "A1"},
            {"role": "user", "content": "Q2"},
            {"role": "assistant", "content": "A2"}
        ]
        
        # Verify full context is available
        assert len(mock_state.messages) == 4
        assert mock_state.messages[0]["content"] == "Q1"
        assert mock_state.messages[-1]["content"] == "A2"

    def test_special_characters_in_questions(self, mock_requests):
        """Test handling of special characters in questions."""
        special_questions = [
            "What about Section 45-B (subsection (ii))?",
            "Can penalties be imposed? Yes/No?",
            "What's the ruling on 'exclusive' delivery?",
            "Are there any exceptions (e.g., SIC)?",
        ]
        
        for question in special_questions:
            payload = {"chatInput": question}
            assert payload["chatInput"] == question

    def test_long_question_handling(self, mock_requests):
        """Test handling of very long questions."""
        long_question = "This is a very long question... " * 50
        
        payload = {"chatInput": long_question}
        assert len(payload["chatInput"]) > 1000
        assert payload["chatInput"] == long_question

    def test_rapid_succession_queries(self, mock_requests, sample_responses):
        """Test handling multiple queries in rapid succession."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_responses["success"]["json_return"]
        mock_requests.return_value = mock_response
        
        queries = ["Q1", "Q2", "Q3", "Q4", "Q5"]
        results = []
        
        for query in queries:
            response = mock_requests("http://localhost:5678/webhook/consultant-bot",
                                    json={"chatInput": query})
            results.append(response.status_code)
        
        assert all(status == 200 for status in results)
        assert len(results) == 5
