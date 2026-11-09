
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.document_service import (
    extract_pdf_text,
    extract_docx_text,
)

router = APIRouter()

DOCUMENT_DIR = Path("data/documents")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    # 1. Validate file extension
    original_filename = Path(file.filename or "uploaded_file").name
    file_extension = Path(original_filename).suffix.lower()

    if file_extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # 2. Read and validate file size
    file_content = await file.read(MAX_FILE_SIZE + 1)

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 10 MB limit."
        )

    # 3. Create unique document ID
    document_id = str(uuid4())

    DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)

    saved_file_path = DOCUMENT_DIR / f"{document_id}{file_extension}"

    try:
        # 4. Save uploaded document
        saved_file_path.write_bytes(file_content)

        # 5. Extract document text
        if file_extension == ".pdf":
            extracted_pages = extract_pdf_text(saved_file_path)
        else:
            extracted_pages = extract_docx_text(saved_file_path)

        if not extracted_pages:
            raise HTTPException(
                status_code=422,
                detail="No readable text found in the document."
            )

        # 6. Return document information
        return {
            "document_id": document_id,
            "filename": original_filename,
            "file_type": file_extension.lstrip("."),
            "total_pages": len(extracted_pages) if file_extension == ".pdf" else None,
            "extracted_pages": extracted_pages
        }

    except HTTPException:
        saved_file_path.unlink(missing_ok=True)
        raise

    except Exception as error:
        saved_file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail="Unable to process this document. Check whether the file is valid."
        ) from error


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return ChatResponse(
        answer=f"You asked: {request.question}",
        sources=[],
        session_id=request.session_id
    )
