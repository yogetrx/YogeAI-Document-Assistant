from fastapi import FastAPI, File, HTTPException, UploadFile
from .config import MAX_UPLOAD_MB, TOP_K_DEFAULT
from .generation import answer_question
from .ingestion import extract_pdf_pages, make_records
from .retrieval import vector_store
from .schemas import AskRequest, AskResponse, IngestResponse, Source
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="YogeAI Document Assistant API",
    version="0.1.0",
    description="PDF ingestion and evidence-grounded RAG question answering.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "indexed_chunks": len(vector_store.records)}

@app.post("/documents", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    content = await file.read()
    if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {MAX_UPLOAD_MB} MB limit.")
    try:
        pages = extract_pdf_pages(content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}")
    if not pages:
        raise HTTPException(
            status_code=422,
            detail="No selectable text found. Scanned PDFs require OCR, which is not included yet.",
        )
    records = make_records(file.filename, pages)
    if not records:
        raise HTTPException(status_code=422, detail="No text chunks were created.")
    try:
        vector_store.add_records(records)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {exc}")
    return IngestResponse(
        document_name=file.filename,
        pages_with_text=len(pages),
        chunks_indexed=len(records),
        status="indexed",
    )

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be blank.")
    top_k = request.top_k or TOP_K_DEFAULT
    retrieved = vector_store.search(question, top_k=top_k)
    try:
        answer = answer_question(question, retrieved)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Answer generation failed: {exc}")
    sources = [
        Source(
            document_name=r["document_name"],
            page=r["page"],
            chunk_id=r["chunk_id"],
            text=r["text"],
            score=r.get("score"),
        )
        for r in retrieved
    ]
    return AskResponse(answer=answer, sources=sources, retrieval_count=len(sources))
