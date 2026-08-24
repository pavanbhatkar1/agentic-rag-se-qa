import argparse
from pathlib import Path

from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.file_scanner import FileScanner
from app.ingestion.github_loader import GitHubLoader
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.vector_store import VectorStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Index a GitHub or local repository into Qdrant."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--repo-url",
        help="GitHub repository URL to clone/update before indexing.",
    )
    source.add_argument(
        "--path",
        help="Local repository path to index.",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Repository label stored in Qdrant metadata.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.repo_url:
        loader = GitHubLoader()
        repo_path = loader.clone_or_update(args.repo_url)
    else:
        repo_path = Path(args.path).resolve()
        if not repo_path.exists() or not repo_path.is_dir():
            raise ValueError(f"Repository path does not exist: {repo_path}")

    scanner = FileScanner()
    files = scanner.scan(repo_path)
    print(f"Repository: {args.name}")
    print(f"Found {len(files)} source/documentation files")

    document_loader = DocumentLoader()
    documents = document_loader.load(files)

    for document in documents:
        document["metadata"]["repository"] = args.name

    print(f"Created {len(documents)} chunks")

    embedder = Embedder()
    embeddings = embedder.embed(
        [document["content"] for document in documents]
    )

    db = QdrantDB(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
    )

    store = VectorStore(db)
    store.add(documents, embeddings)

    print(
        f"Indexed {len(documents)} chunks into "
        f"'{settings.qdrant_collection}' without deleting existing data."
    )


if __name__ == "__main__":
    main()
