import pytest
import io
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("app.model")
def test_detect_medicine_success(mock_yolo_model, client):
    # Mock YOLO detection output
    mock_box = MagicMock()
    mock_box.xywh = [MagicMock(cpu=lambda: MagicMock(numpy=lambda: [100, 150, 50, 50]))]
    mock_box.conf = [MagicMock(cpu=lambda: MagicMock(numpy=lambda: 0.85))]
    
    mock_result = MagicMock()
    mock_result.boxes = [mock_box]
    mock_yolo_model.return_value = [mock_result]

    # Fake image upload
    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post("/detect", content_type='multipart/form-data', data=data)

    assert response.status_code == 200
    assert "predictions" in response.json
    assert len(response.json["predictions"]) == 1
    assert response.json["predictions"][0]["class_name"] == "Medicine"

def test_no_file_uploaded(client):
    response = client.post("/detect", content_type='multipart/form-data', data={})
    assert response.status_code == 400
    assert response.json["error"] == "No file uploaded"

@patch("app.model")
def test_file_uploaded_but_empty(mock_yolo_model, client):
    data = {
        'file': (io.BytesIO(b""), '')
    }
    response = client.post("/detect", content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert response.json["error"] == "No file selected"

@patch("app.model")
def test_model_exception(mock_yolo_model, client):
    mock_yolo_model.side_effect = Exception("Model failed")
    data = {
        'file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post("/detect", content_type='multipart/form-data', data=data)
    assert response.status_code == 500
    assert "error" in response.json
