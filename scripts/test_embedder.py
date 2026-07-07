from app.embeddings.embedder import Embedder

embedder = Embedder()

texts = [
    "FastAPI is a Python web framework.",
    "Qdrant is a vector database.",
]

vectors = embedder.embed(texts)

print(len(vectors))
print(len(vectors[0]))