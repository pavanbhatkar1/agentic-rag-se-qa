from app.retrieval.bm25_retriever import BM25Retriever

docs = [
    {
        "content": "FastAPI uses dependency injection.",
        "metadata": {"source": "a.md"},
    },
    {
        "content": "Qdrant is a vector database.",
        "metadata": {"source": "b.md"},
    },
]

retriever = BM25Retriever(docs)

results = retriever.search("FastAPI dependency")

for r in results:
    print(r["score"], r["metadata"]["source"])