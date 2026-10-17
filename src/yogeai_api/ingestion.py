from io import BytesIO
from pypdf import PdfReader
from .chunking import split_text

def extract_pdf_pages(pdf_bytes: bytes) -> list[dict]:
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": page_number, "text": text})
    return pages

def make_records(document_name: str, pages: list[dict]) -> list[dict]:
    records = []
    for page in pages:
        chunks = split_text(page["text"])
        for chunk_number, chunk in enumerate(chunks, start=1):
            records.append({
                "document_name": document_name,
                "page": page["page"],
                "chunk_id": f"p{page['page']}-c{chunk_number}",
                "text": chunk,
            })
    return records
