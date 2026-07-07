from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever

db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

embedder = Embedder()
retriever = Retriever(db, embedder)

results = retriever.search("What is FastAPI?")

for doc in results:
    print(doc["score"])
    print(doc["metadata"])
    print(doc["content"][:200])
    print("-" * 50)