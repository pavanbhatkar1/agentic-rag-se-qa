from typing import Literal

from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient


class QueryRouter:
    """Route user queries for Adaptive-RAG."""

    def __init__(self, llm: OllamaClient):
        self.llm = llm

    def route(self, state: GraphState) -> Literal["retrieve", "direct"]:
        prompt = f"""
You are a query router.

Decide whether the user's question requires retrieving information from a software repository.

Return ONLY one word:
- retrieve
- direct

Question:
{state["question"]}
"""

        decision = self.llm.generate(prompt).strip().lower()

        if decision == "direct":
            return "direct"

        return "retrieve"