
from uuid import uuid4


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> list[str]:

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be non-negative and smaller than chunk size."
        )

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        # Avoid cutting a word in the middle
        if end < len(text):
            space_position = text.rfind(" ", start, end)

            if space_position > start:
                end = space_position

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def create_document_chunks(
    extracted_pages: list[dict],
    document_id: str,
    filename: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> list[dict]:

    document_chunks = []

    for page in extracted_pages:

        page_chunks = chunk_text(
            text=page["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for index, chunk in enumerate(page_chunks):

            document_chunks.append({
                "chunk_id": str(uuid4()),
                "document_id": document_id,
                "filename": filename,
                "page_number": page.get("page_number"),
                "chunk_index": index,
                "text": chunk
            })

    return document_chunks
