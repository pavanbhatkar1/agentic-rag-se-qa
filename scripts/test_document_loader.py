from pathlib import Path

from app.ingestion.document_loader import DocumentLoader

loader = DocumentLoader()

files = [
    Path("README.md"),
    Path("main.py"),
]

documents = loader.load(files)

print(f"Loaded: {len(documents)} documents")

for doc in documents:
    print(doc["metadata"])
    print(doc["content"][:100])
    print("-" * 40)
    