from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient


class QueryRewriter:
    """Rewrite queries for better retrieval."""

    def __init__(self, llm: OllamaClient):
        self.llm = llm

    def rewrite(self, state: GraphState) -> GraphState:
        prompt = f"""
Rewrite the following software engineering question to improve retrieval.

Keep the meaning unchanged.
Return ONLY the rewritten question.

Question:
{state["question"]}
"""

        rewritten_query = self.llm.generate(prompt).strip()

        return {
            **state,
            "rewritten_query": rewritten_query,
        }