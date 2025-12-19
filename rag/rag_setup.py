import chromadb
from sentence_transformers import SentenceTransformer


def setup_rag():
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="role_expectations")

    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    with open("rag_data/role_expectations.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = [line for line in text.split("\n") if line.strip()]
    embeddings = embedder.encode(chunks).tolist()

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[str(i)],
        )

    return collection
