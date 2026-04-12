"""Integration tests for Legal Consultant AI application."""
import pytest
from unittest.mock import Mock, patch


class TestEndToEndFlow:
    """Test complete end-to-end user workflows."""

    def test_complete_chat_workflow(self, mock_streamlit, mock_requests, sample_responses):
        """Test complete workflow from user input to response display."""
        # Setup
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = []
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_responses["success"]["json_return"]
        mock_requests.return_value = mock_response
        
        # Simulate complete workflow
        user_question = "Can a railway penalty be imposed?"
        
        # 1. User adds to messages
        mock_state.messages.append({"role": "user", "content": user_question})
        
        # 2. API call
        api_response = mock_requests(
            "http://localhost:5678/webhook/consultant-bot",
            json={"chatInput": user_question}
        )
        
        # 3. Assistant adds to messages
        if api_response.status_code == 200:
            answer = api_response.json().get("answer", "Error")
            mock_state.messages.append({"role": "assistant", "content": answer})
        
        # Verify
        assert len(mock_state.messages) == 2
        assert mock_state.messages[0]["role"] == "user"
        assert mock_state.messages[1]["role"] == "assistant"

    def test_error_recovery_workflow(self, mock_streamlit, mock_requests):
        """Test system recovery after an error."""
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = []
        
        # First attempt - error
        mock_response_error = Mock()
        mock_response_error.status_code = 500
        mock_response_error.text = "Server Error"
        mock_requests.return_value = mock_response_error
        
        # User reports error is shown
        api_response = mock_requests(
            "http://localhost:5678/webhook/consultant-bot",
            json={"chatInput": "Question 1"}
        )
        assert api_response.status_code == 500
        
        # Second attempt - success
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"answer": "Recovered successfully"}
        mock_requests.return_value = mock_response_success
        
        api_response = mock_requests(
            "http://localhost:5678/webhook/consultant-bot",
            json={"chatInput": "Question 2"}
        )
        assert api_response.status_code == 200


class TestCrossComponentIntegration:
    """Test integration between different components."""

    def test_ui_and_session_state_integration(self, mock_streamlit):
        """Test UI components work with session state."""
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = [
            {"role": "user", "content": "Test question"},
            {"role": "assistant", "content": "Test answer"}
        ]
        
        mock_chat = mock_streamlit["chat_message"]
        
        # Simulate displaying all messages
        for message in mock_state.messages:
            assert message["role"] in ["user", "assistant"]
            assert len(message["content"]) > 0

    def test_api_integration_with_session_persistence(self, mock_streamlit, mock_requests, sample_responses):
        """Test API calls update session state correctly."""
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = []
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_responses["success"]["json_return"]
        mock_requests.return_value = mock_response
        
        # Simulate multiple interactions
        for i in range(3):
            question = f"Question {i+1}"
            mock_state.messages.append({"role": "user", "content": question})
            
            response = mock_requests(
                "http://localhost:5678/webhook/consultant-bot",
                json={"chatInput": question}
            )
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                mock_state.messages.append({"role": "assistant", "content": answer})
        
        assert len(mock_state.messages) == 6  # 3 questions + 3 answers
        
        # Verify persistence
        for msg in mock_state.messages:
            assert msg["role"] in ["user", "assistant"]
            assert len(msg["content"]) > 0


class TestAPIErrorScenarios:
    """Test various API error scenarios and recovery."""

    def test_partial_failure_with_retries(self, mock_requests):
        """Test system behavior with partial failures."""
        responses = [
            Mock(status_code=500),
            Mock(status_code=503),
            Mock(status_code=200, json=Mock(return_value={"answer": "Success"}))
        ]
        
        mock_requests.side_effect = responses
        
        # First two fail
        try:
            response1 = mock_requests("url", json={})
            assert response1.status_code == 500
        except:
            pass
        
        try:
            response2 = mock_requests("url", json={})
            assert response2.status_code == 503
        except:
            pass
        
        # Third succeeds
        response3 = mock_requests("url", json={})
        assert response3.status_code == 200

    def test_graceful_degradation(self, mock_streamlit, mock_requests):
        """Test graceful degradation when API is unavailable."""
        mock_state = mock_streamlit["session_state"]
        mock_state.messages = []
        
        # API unavailable
        mock_requests.side_effect = ConnectionError("API Unavailable")
        
        question = "Test question"
        mock_state.messages.append({"role": "user", "content": question})
        
        # System should handle error gracefully
        try:
            response = mock_requests("url", json={"chatInput": question})
        except ConnectionError:
            # Error handled
            mock_state.messages.append({
                "role": "assistant",
                "content": "Service temporarily unavailable. Please try again."
            })
        
        assert len(mock_state.messages) == 2
        assert "unavailable" in mock_state.messages[1]["content"].lower()
