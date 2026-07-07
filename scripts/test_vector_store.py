from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.vector_store import VectorStore

chunks = [
    {
        "content": "FastAPI is a modern Python web framework.",
        "metadata": {
            "source": "test.py",
            "file_type": ".py",
            "chunk_id": 0,
        },
    }
]

embedder = Embedder()
embeddings = embedder.embed([chunk["content"] for chunk in chunks])

db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

store = VectorStore(db)
store.add(chunks, embeddings)

print("Stored successfully!")