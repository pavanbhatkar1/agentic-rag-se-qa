from sentence_transformers import CrossEncoder


class BGEReranker:
    """Rerank retrieved documents using a BGE CrossEncoder."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:
        if not documents:
            return []

        pairs = [
            (query, doc["content"])
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(scores, documents),
            key=lambda x: x[0],
            reverse=True,
        )

        return [doc for _, doc in ranked[:top_k]]