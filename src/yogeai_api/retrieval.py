import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model

class InMemoryVectorStore:
    def __init__(self):
        self.records = []
        self.index = None

    def add_records(self, records: list[dict]):
        if not records:
            return
        model = get_embedding_model()
        vectors = model.encode(
            [r["text"] for r in records],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")
        if self.index is None:
            self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)
        self.records.extend(records)

    def search(self, question: str, top_k: int = 4) -> list[dict]:
        if self.index is None or not self.records:
            return []
        vector = get_embedding_model().encode(
            [question], convert_to_numpy=True, normalize_embeddings=True
        ).astype("float32")
        k = min(top_k, len(self.records))
        scores, ids = self.index.search(vector, k)
        found = []
        for score, idx in zip(scores[0], ids[0]):
            if idx >= 0:
                record = dict(self.records[int(idx)])
                record["score"] = float(score)
                found.append(record)
        return found

# In-memory, process-wide store for this local prototype only.
# Production must use a durable index with document-level authorization.
vector_store = InMemoryVectorStore()
