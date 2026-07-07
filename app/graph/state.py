from typing import Literal, TypedDict


class GraphState(TypedDict):
    """Shared state for the LangGraph workflow."""

    question: str
    documents: list[dict]
    answer: str

    # Adaptive-RAG
    route: Literal["retrieve", "direct"]

    # Corrective-RAG
    rewritten_query: str
    retrieval_score: float
    needs_retry: bool