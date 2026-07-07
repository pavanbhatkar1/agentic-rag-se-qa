import uuid

from qdrant_client.models import PointStruct

from app.vectorstore.qdrant_client import QdrantDB


class VectorStore:
    """Store and retrieve vectors from Qdrant."""

    def __init__(self, db: QdrantDB):
        self.db = db

    def add(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must have the same length.")

        points = []

        for chunk, embedding in zip(chunks, embeddings):
            payload = {
                "content": chunk["content"],
                **chunk["metadata"],
            }

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload,
                )
            )

        self.db.client.upsert(
            collection_name=self.db.collection_name,
            points=points,
        )