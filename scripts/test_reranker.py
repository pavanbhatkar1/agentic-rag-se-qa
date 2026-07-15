from app.retrieval.reranker import BGEReranker

retrieved_docs = [
    {
        "content": "FastAPI uses dependency injection to manage dependencies.",
        "metadata": {"source": "fastapi.md"},
    },
    {
        "content": "Qdrant is a vector database.",
        "metadata": {"source": "qdrant.md"},
    },
]

reranker = BGEReranker()

results = reranker.rerank(
    "How does FastAPI dependency injection work?",
    retrieved_docs,
)

print(results[0]["metadata"])