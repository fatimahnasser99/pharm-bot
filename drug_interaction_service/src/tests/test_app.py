import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

# pip install pytest pytest-mock fastapi httpx

client = TestClient(app)

@patch("app.process_zip_of_json")
@patch("app.embed_and_store")
def test_embed_and_store_success(mock_embed_and_store, mock_process_zip):
    mock_process_zip.return_value = [{"content": "dummy chunk"}]
    
    with open("tests/assets/fake.zip", "wb") as f:
        f.write(b"Fake zip content")

    with open("tests/assets/fake.zip", "rb") as fake_file:
        response = client.post("/chunk_embed_and_store/", files={"uploaded_file": ("fake.zip", fake_file, "application/zip")})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "Data embedded and stored" in response.json()["message"]

@patch("app.process_zip_of_json")
def test_embed_and_store_no_chunks(mock_process_zip):
    mock_process_zip.return_value = []

    with open("tests/assets/fake.zip", "wb") as f:
        f.write(b"Fake zip content")

    with open("tests/assets/fake.zip", "rb") as fake_file:
        response = client.post("/chunk_embed_and_store/", files={"uploaded_file": ("fake.zip", fake_file, "application/zip")})

    assert response.status_code == 200
    assert response.json()["status"] == "error"

@patch("app.perform_rag_query")
def test_rag_query_success(mock_rag_query):
    mock_rag_query.return_value = {"answer": "This is a test answer"}

    query_payload = {
        "query": "What is RAG?",
        "top_k": 3
    }

    response = client.post("/rag/", json=query_payload)

    assert response.status_code == 200
    assert response.json()["answer"] == "This is a test answer"
