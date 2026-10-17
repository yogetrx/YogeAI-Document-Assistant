from pydantic import BaseModel, Field

class Source(BaseModel):
    document_name: str
    page: int
    chunk_id: str
    text: str
    score: float | None = None

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=4, ge=1, le=8)

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    retrieval_count: int

class IngestResponse(BaseModel):
    document_name: str
    pages_with_text: int
    chunks_indexed: int
    status: str
