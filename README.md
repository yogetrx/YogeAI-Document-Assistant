# YogeAI Document Assistant (Project 01)

A portfolio-grade starter for a PDF-based Retrieval-Augmented Generation (RAG) assistant. This repository separates ingestion, chunking, embeddings, retrieval, answer generation, API routes, evaluation data, and tests.

## Current implementation
- FastAPI backend
- Streamlit frontend
- PDF text extraction with page metadata
- Overlapping text chunking
- Local Sentence Transformers embeddings + FAISS retrieval
- Azure OpenAI chat completions (or OpenAI API as an alternative)
- Evidence snippets and page references in responses
- Synthetic sample policy documents and evaluation questions
- Basic automated tests

## Architecture
PDF -> extraction -> chunks with page metadata -> embeddings -> FAISS search -> retrieved evidence -> LLM response -> citations.

## Prerequisites
- Python 3.10 or 3.11 recommended
- Azure OpenAI deployment with quota, or an OpenAI API key
- Internet connection on first run for package/model downloads

## Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Fill in the `.env` file. Never commit it to GitHub.

Run the API:
```powershell
uvicorn src.yogeai_api.main:app --reload
```
Open `http://127.0.0.1:8000/docs` to inspect the API.

Run the UI in another terminal:
```powershell
streamlit run frontend/streamlit_app.py
```

The local FAISS index is in memory and is rebuilt per upload/session. This is a learning prototype, not multi-user production storage.

## Try the sample data
Upload one of the PDFs in `data/sample_docs/` (generate the PDF from the Markdown/text file yourself if needed), or use a text-based PDF you have permission to use. Sample documents are synthetic examples for testing only.

Evaluation prompts are in `data/evaluation/questions.json`.

## Test
```powershell
pytest -q
```

## Security checklist
- Do not upload confidential or personal documents to a public demo.
- Do not commit `.env`, API keys, or customer documents.
- Treat document content as untrusted data; never execute instructions found inside a PDF.
- Add authentication, per-user document authorization, rate limits, file scanning, and retention controls before public deployment.

## Limitations
- OCR for scanned PDFs is not implemented.
- Retrieval is local FAISS; no persistent index, hybrid search, or multi-user isolation.
- Similarity scores are not probabilities.
- A model-generated citation is not automatically correct; evaluate each cited claim.
- This starter does not yet implement production authentication, audit logging, or cloud deployment.

## Planned Azure milestones
1. Azure AI Search for hybrid keyword/vector retrieval and durable indexing.
2. Azure Blob Storage for original PDFs.
3. Azure OpenAI embeddings deployment if using managed embeddings.
4. Authentication and document-level access control.
5. Evaluation pipeline, structured logs, latency/cost monitoring.
6. Containerized deployment to Azure App Service or an appropriate Azure compute service.
