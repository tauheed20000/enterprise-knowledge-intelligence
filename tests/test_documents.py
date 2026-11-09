
from fastapi.testclient import TestClient
import app.api.routes as document_routes

from app.main import app

client = TestClient(app)


def test_pdf_upload(tmp_path, monkeypatch):

    monkeypatch.setattr(
        document_routes, "DOCUMENT_DIR", tmp_path
    )

    monkeypatch.setattr(
        document_routes,
        "extract_pdf_text",
        lambda path: [
            {"page_number": 1, "text": "Sample PDF content"}
        ]
    )

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("policy.pdf", b"fake pdf content", "application/pdf")}
    )

    assert response.status_code == 200
    assert response.json()["file_type"] == "pdf"


def test_docx_upload(tmp_path, monkeypatch):

    monkeypatch.setattr(
        document_routes, "DOCUMENT_DIR", tmp_path
    )

    monkeypatch.setattr(
        document_routes,
        "extract_docx_text",
        lambda path: [
            {"page_number": None, "text": "Sample DOCX content"}
        ]
    )

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("policy.docx", b"fake docx content",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )

    assert response.status_code == 200
    assert response.json()["file_type"] == "docx"


def test_invalid_file_type():

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("notes.txt", b"Hello", "text/plain")}
    )

    assert response.status_code == 400


def test_large_file():

    large_content = b"x" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("large.pdf", large_content, "application/pdf")}
    )

    assert response.status_code == 413
