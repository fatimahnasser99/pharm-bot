import pytest
from unittest.mock import patch, MagicMock
from app import app
import io


# This is a test for the Flask app that uses Google Cloud Vision API to extract text from images.pip install pytest pytest-mock
# pip install pytest pytest-mock
# to run the test, use the command: pytest -v test_app.py


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("app.client")  # Patch the Google Vision client in app.py
def test_extract_text_success(mock_vision_client, client):
    # Mock successful text detection
    mock_response = MagicMock()
    mock_response.error.message = ""
    mock_response.full_text_annotation.text = "Detected medicine text"
    mock_vision_client.text_detection.return_value = mock_response

    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post("/extracted_text", content_type='multipart/form-data', data=data)

    assert response.status_code == 200
    assert "extracted_text" in response.json
    assert response.json["extracted_text"] == "Detected medicine text"

def test_no_file_uploaded(client):
    response = client.post("/extracted_text", content_type='multipart/form-data', data={})
    assert response.status_code == 400
    assert response.json["error"] == "No file uploaded"

@patch("app.client")
def test_file_uploaded_but_empty(mock_vision_client, client):
    data = {
        'file': (io.BytesIO(b""), '')
    }
    response = client.post("/extracted_text", content_type='multipart/form-data', data=data)

    assert response.status_code == 400
    assert response.json["error"] == "No file selected"

@patch("app.client")
def test_vision_api_error(mock_vision_client, client):
    # Simulate Vision API returning an error
    mock_response = MagicMock()
    mock_response.error.message = "API quota exceeded"
    mock_response.full_text_annotation = None
    mock_vision_client.text_detection.return_value = mock_response

    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post("/extracted_text", content_type='multipart/form-data', data=data)

    assert response.status_code == 500
    assert response.json["error"] == "API quota exceeded"
