import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("app.extract_drugs_from_text")
def test_extract_success(mock_extractor, client):
    mock_extractor.return_value = ["Panadol", "Ibuprofen"]

    response = client.post("/extract", json={
        "text": "I have Panadol and Ibuprofen at home"
    })

    assert response.status_code == 201
    assert "drugs_list" in response.json
    assert response.json["drugs_list"] == ["Panadol", "Ibuprofen"]

def test_missing_text_field(client):
    response = client.post("/extract", json={})
    assert response.status_code == 400
    assert response.json["error"] == "Missing 'text' field"

@patch("app.extract_drugs_from_text")
def test_extraction_exception(mock_extractor, client):
    mock_extractor.side_effect = Exception("Extraction failed")

    response = client.post("/extract", json={
        "text": "Something strange"
    })

    assert response.status_code == 500
    assert "error" in response.json
