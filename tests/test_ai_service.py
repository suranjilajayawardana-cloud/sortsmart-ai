"""
Unit tests for the SortSmart AI Service layer.
These tests verify that the service layer correctly handles edge cases, 
formats the RAG prompt, and maps low-level model exceptions to user-friendly messages.
"""

import pytest
from unittest.mock import MagicMock, patch
from src.services.ai_service import AIService, generate_response
from src.models.model_client import OllamaConnectionError, ModelNotFoundError


def test_service_initialization():
    """Verify service initializes with a default client if none provided."""
    service = AIService()
    assert service.model_client is None
    client = service._get_client()
    assert client is not None


def test_empty_input_validation():
    """Verify that empty inputs are rejected gracefully without invoking the RAG pipeline."""
    mock_client = MagicMock()
    service = AIService(model_client=mock_client)
    
    response_empty = service.process_message("")
    assert response_empty.success is False
    assert "Please enter a waste item" in response_empty.content
    
    response_whitespace = service.process_message("   \n   ")
    assert response_whitespace.success is False
    
    # Model should NOT be called if input is empty
    mock_client.generate.assert_not_called()


@patch("src.services.ai_service.build_rag_prompt")
def test_successful_response_generation(mock_build_rag_prompt):
    """Verify valid input triggers the RAG pipeline and returns the model string."""
    
    # Mock the RAG prompt builder so we don't need to load the actual JSON in tests
    mock_build_rag_prompt.return_value = "MOCKED_RAG_PROMPT"
    
    mock_client = MagicMock()
    mock_client.generate.return_value = "It belongs in Plastic Packaging."
    service = AIService(model_client=mock_client)
    
    result_text = generate_response("plastic bottle", service=service)
    
    assert result_text == "It belongs in Plastic Packaging."
    # Assert the model was called with the assembled RAG prompt, not just the raw user input
    mock_client.generate.assert_called_once_with("MOCKED_RAG_PROMPT")


def test_connection_error_handling():
    """Verify Ollama connection errors are caught and converted to friendly messages."""
    mock_client = MagicMock()
    mock_client.generate.side_effect = OllamaConnectionError("Connection Refused")
    service = AIService(model_client=mock_client)
    
    response = service.process_message("test item")
    
    assert response.success is False
    assert "Could not connect to Ollama" in response.content


def test_model_not_found_handling():
    """Verify missing model errors are caught and converted to friendly messages."""
    mock_client = MagicMock()
    mock_client.generate.side_effect = ModelNotFoundError("llama3.2 not found")
    service = AIService(model_client=mock_client)
    
    response = service.process_message("test item")
    
    assert response.success is False
    assert "configured AI model is unavailable" in response.content