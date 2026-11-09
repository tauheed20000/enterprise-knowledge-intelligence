from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file_path: Path):
    reader = PdfReader(str(file_path))

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            extracted_pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    return extracted_pages


def extract_docx_text(file_path: Path):
    document = Document(str(file_path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    extracted_text = "\n".join(paragraphs)

    if not extracted_text:
        return []

    return [{
        "page_number": None,
        "text": extracted_text
    }]