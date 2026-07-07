from app.ingestion.chunker import Chunker

documents = [
    {
        "content": "A" * 1200,
        "metadata": {"source": "test.py"},
    }
]

chunker = Chunker(chunk_size=500, chunk_overlap=100)

chunks = chunker.chunk(documents)

print(f"Chunks: {len(chunks)}")

for chunk in chunks:
    print(
        chunk["metadata"]["chunk_id"],
        len(chunk["content"]),
    )
    