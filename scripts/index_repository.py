from pathlib import Path
from unittest import loader

from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.file_scanner import FileScanner
from app.ingestion.github_loader import GitHubLoader
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.vector_store import VectorStore


def main():
    # Clone/download repository

    
    
    loader = GitHubLoader()

    repo_path = loader.clone_or_update(
    "https://github.com/fastapi/fastapi.git"
    )

    # Scan files
    scanner = FileScanner()
    files = scanner.scan(repo_path)

    print(f"Found {len(files)} files")

    # Parse + Chunk
    document_loader = DocumentLoader()
    documents = document_loader.load(files)

    print(f"Created {len(documents)} chunks")

    # Embed
    embedder = Embedder()
    embeddings = embedder.embed(
        [doc["content"] for doc in documents]
    )

    # Store
    db = QdrantDB(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
    )

    store = VectorStore(db)
    store.add(documents, embeddings)

    print("Repository indexed successfully!")


if __name__ == "__main__":
    main()
