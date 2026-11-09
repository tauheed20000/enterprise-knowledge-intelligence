
import pytest

from app.services.chunking_service import (
    chunk_text,
    create_document_chunks,
)


def test_chunk_text():
    text = "A" * 250

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=20
    )

    assert len(chunks) > 1
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_chunk_overlap():
    text = "A" * 250

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=20
    )

    assert chunks[0][-20:] == chunks[1][:20]


def test_empty_text():
    result = chunk_text("")

    assert result == []


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("Sample text", chunk_size=0)


def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text(
            "Sample text",
            chunk_size=100,
            chunk_overlap=100
        )


def test_document_chunk_metadata():

    extracted_pages = [
        {
            "page_number": 1,
            "text": "A" * 250
        }
    ]

    chunks = create_document_chunks(
        extracted_pages=extracted_pages,
        document_id="doc-001",
        filename="company_policy.pdf",
        chunk_size=100,
        chunk_overlap=20
    )

    assert len(chunks) > 1

    first_chunk = chunks[0]

    assert first_chunk["document_id"] == "doc-001"
    assert first_chunk["filename"] == "company_policy.pdf"
    assert first_chunk["page_number"] == 1
    assert first_chunk["chunk_index"] == 0
    assert "chunk_id" in first_chunk
    assert "text" in first_chunk
