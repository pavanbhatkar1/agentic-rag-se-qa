from app.core.config import settings
from app.vectorstore.qdrant_client import QdrantDB

db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

print(db.client.get_collections())