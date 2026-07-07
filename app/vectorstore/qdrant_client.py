from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class QdrantDB:
    """Qdrant client wrapper."""

    def __init__(
        self,
        url: str,
        collection_name: str,
        embedding_dim: int = 384,
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(url=url)

        collections = self.client.get_collections().collections
        names = {collection.name for collection in collections}

        if collection_name not in names:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=embedding_dim,
                    distance=Distance.COSINE,
                ),
            )