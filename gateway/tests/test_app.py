import pytest
from unittest.mock import patch, MagicMock
from app import app
import io

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("app.requests.post")
@patch("app.record_detection_metrics")
@patch("app.record_ocr_metrics")
@patch("app.record_extractor_metrics")
@patch("app.record_interaction_metrics")
def test_success_image_flow(mock_interaction_metrics, mock_extractor_metrics, mock_ocr_metrics, mock_detection_metrics, mock_post, client):
    # Mock object detection response
    detection_mock = MagicMock()
    detection_mock.status_code = 200
    detection_mock.json.return_value = {
        "predictions": [{
            "x": 100, "y": 100, "width": 50, "height": 50, "confidence": 0.9
        }]
    }

    # Mock OCR response
    ocr_mock = MagicMock()
    ocr_mock.status_code = 200
    ocr_mock.json.return_value = {"extracted_text": "Panadol"}

    # Mock drug extraction response
    extractor_mock = MagicMock()
    extractor_mock.status_code = 201
    extractor_mock.json.return_value = {"drugs_list": ["Panadol"]}

    # Mock drug interaction response
    interaction_mock = MagicMock()
    interaction_mock.status_code = 200
    interaction_mock.json.return_value = {"answer": {"content": "Panadol interaction info"}}

    mock_post.side_effect = [detection_mock, ocr_mock, extractor_mock, interaction_mock]

    # Upload fake image
    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post("/analyze", content_type='multipart/form-data', data=data)

    assert response.status_code == 200
    assert "extracted_text" in response.json
    assert "drugs_list" in response.json
    assert "interaction_result" in response.json

@patch("app.requests.post")
def test_text_input_success(mock_post, client):
    # Mock extractor response
    extractor_mock = MagicMock()
    extractor_mock.status_code = 201
    extractor_mock.json.return_value = {"drugs_list": ["Aspirin"]}

    # Mock interaction response
    interaction_mock = MagicMock()
    interaction_mock.status_code = 200
    interaction_mock.json.return_value = {"answer": {"content": "Interaction info"}}

    mock_post.side_effect = [extractor_mock, interaction_mock]

    payload = {
        "text": "I have Aspirin at home"
    }
    response = client.post("/analyze", json=payload)

    assert response.status_code == 200
    assert response.json["drugs_list"] == ["Aspirin"]

def test_invalid_input(client):
    response = client.post("/analyze", data={})
    assert response.status_code == 400
    assert "error" in response.json

@patch("app.requests.post")
def test_detection_failure(mock_post, client):
    detection_mock = MagicMock()
    detection_mock.status_code = 500

    mock_post.return_value = detection_mock

    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post("/analyze", content_type='multipart/form-data', data=data)

    assert response.status_code == 500
    assert "error" in response.json
