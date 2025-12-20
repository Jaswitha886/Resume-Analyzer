# rag/rag_setup.py

from sentence_transformers import SentenceTransformer
import numpy as np

class SimpleRAG:
    def __init__(self, role_file_path: str):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = self._load_documents(role_file_path)
        self.embeddings = self.model.encode(self.documents)

    def _load_documents(self, path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return [chunk.strip() for chunk in text.split("\n") if chunk.strip()]

    def retrieve(self, query: str, top_k: int = 5):
        query_emb = self.model.encode([query])[0]
        scores = np.dot(self.embeddings, query_emb)
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [self.documents[i] for i in top_indices]
