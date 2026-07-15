import uuid

from qdrant_client.models import PointStruct

from app.vectorstore.qdrant_client import QdrantDB


class VectorStore:
    """Store and retrieve vectors from Qdrant."""

    def __init__(self, db: QdrantDB):
        self.db = db

    def add(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        batch_size: int = 256,
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunks and embeddings must have the same length."
            )

        total = len(chunks)

        for start in range(0, total, batch_size):
            end = min(start + batch_size, total)

            points = []

            for chunk, embedding in zip(
                chunks[start:end],
                embeddings[start:end],
            ):
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

            print(f"Indexed {end}/{total} chunks")