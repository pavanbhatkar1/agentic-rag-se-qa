from app.retrieval.bm25_retriever import BM25Retriever
from app.vectorstore.retriever import Retriever


class HybridRetriever:
    """Hybrid retriever using Reciprocal Rank Fusion (RRF)."""

    def __init__(
        self,
        dense_retriever: Retriever,
        bm25_retriever: BM25Retriever,
        k: int = 60,
    ):
        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever
        self.k = k

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        dense_results = self.dense_retriever.search(query, top_k * 2)
        bm25_results = self.bm25_retriever.search(query, top_k * 2)

        fused = {}

        for rank, doc in enumerate(dense_results, start=1):
            key = (
                doc["metadata"]["source"],
                doc["metadata"].get("chunk_id", 0),
            )
            fused.setdefault(key, {"doc": doc, "score": 0.0})
            fused[key]["score"] += 1 / (self.k + rank)

        for rank, doc in enumerate(bm25_results, start=1):
            key = (
                doc["metadata"]["source"],
                doc["metadata"].get("chunk_id", 0),
            )
            fused.setdefault(key, {"doc": doc, "score": 0.0})
            fused[key]["score"] += 1 / (self.k + rank)

        ranked = sorted(
            fused.values(),
            key=lambda x: x["score"],
            reverse=True,
        )

        return [item["doc"] for item in ranked[:top_k]]