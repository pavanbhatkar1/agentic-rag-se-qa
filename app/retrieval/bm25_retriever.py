from rank_bm25 import BM25Okapi


class BM25Retriever:
    """BM25 lexical retriever."""

    def __init__(self, documents: list[dict]):
        self.documents = documents

        self.corpus = [
            doc["content"].split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(self.corpus)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        scores = self.bm25.get_scores(query.split())

        ranked = sorted(
            zip(scores, self.documents),
            key=lambda x: x[0],
            reverse=True,
        )

        results = []

        for score, doc in ranked[:top_k]:
            results.append(
                {
                    **doc,
                    "score": float(score),
                }
            )

        return results