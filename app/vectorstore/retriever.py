from app.embeddings.embedder import Embedder
from app.vectorstore.qdrant_client import QdrantDB


class Retriever:
    """Retrieve relevant chunks from Qdrant."""

    def __init__(self, db: QdrantDB, embedder: Embedder):
        self.db = db
        self.embedder = embedder

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_vector = self.embedder.embed([query])[0]

        results = self.db.client.query_points(
            collection_name=self.db.collection_name,
            query=query_vector,
            limit=top_k,
        ).points

        documents = []

        for result in results:
            documents.append(
                {
                    "content": result.payload["content"],
                    "metadata": {
                        k: v
                        for k, v in result.payload.items()
                        if k != "content"
                    },
                    "score": result.score,
                }
            )

        return documents