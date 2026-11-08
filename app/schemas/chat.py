from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=3)
    session_id: str
    top_k: int = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    document_name: str
    page_number: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    session_id: str