# Architecture

## Components
- Streamlit frontend: file upload and question interface.
- FastAPI backend: `/health`, `/documents`, and `/ask`.
- Ingestion: PDF text extraction retaining original page numbers.
- Chunking: approximately 900 characters per chunk, with 150 characters of overlap.
- Embeddings: local `sentence-transformers/all-MiniLM-L6-v2`.
- Vector store: FAISS inner-product similarity over normalized embeddings.
- Generation: Azure OpenAI chat deployment, or OpenAI API as a fallback provider.
- Evaluation data: synthetic questions with expected evidence and answerability labels.

## Data flow
1. User uploads a PDF.
2. API validates extension and size.
3. PDF pages are extracted.
4. Each page is split into chunks; document name, page number, and chunk ID are retained.
5. Chunks are embedded and added to an in-memory FAISS index.
6. User question is embedded and top-k chunks are retrieved.
7. The LLM answers using only retrieved context and labels its sources.
8. API returns the answer and retrieved source metadata.

## API
- `GET /health`: health and indexed chunk count.
- `POST /documents`: multipart PDF upload and indexing.
- `POST /ask`: JSON `{ "question": "...", "top_k": 4 }`.

## Production requirements not yet implemented
Persistent multi-tenant storage, document access controls, authentication, malware scanning, OCR, hybrid search, citation validation, rate limits, deletion/retention workflows, structured telemetry, and deployment hardening.
