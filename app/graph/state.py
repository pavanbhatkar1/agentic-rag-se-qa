from typing import Literal, TypedDict


class GraphState(TypedDict):
    """Shared state for the Adaptive + Corrective RAG workflow."""

    question: str
    documents: list[dict]
    web_documents: list[dict]
    answer: str

    # Adaptive RAG
    route: Literal["direct", "retrieve", "complex"]

    # Corrective RAG
    rewritten_query: str
    retrieval_score: float
    needs_retry: bool
    retry_count: int

    # Web fallback
    web_search_used: bool