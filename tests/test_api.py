from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200


def test_chat_endpoint():
    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What is RAG?",
            "session_id": "session-001",
            "top_k": 5
        }
    )

    assert response.status_code == 200
    assert response.json()["session_id"] == "session-001"


def test_invalid_top_k():
    response = client.post(
        "/api/v1/chat",
        json={
            "question": "What is RAG?",
            "session_id": "session-001",
            "top_k": 25
        }
    )

    assert response.status_code == 422