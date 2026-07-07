from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient


class RetrievalGrader:
    """Evaluate retrieved documents."""

    def __init__(self, llm: OllamaClient):
        self.llm = llm

    def grade(self, state: GraphState) -> GraphState:
        context = "\n\n".join(
            doc["content"] for doc in state["documents"]
        )

        prompt = f"""
You are evaluating retrieved documents for a RAG system.

Question:
{state["question"]}

Retrieved Context:
{context}

Can the question be answered using ONLY this context?

Respond with ONLY:
yes
or
no
"""

        response = self.llm.generate(prompt).strip().lower()

        needs_retry = response != "yes"

        return {
            **state,
            "retrieval_score": 1.0 if not needs_retry else 0.0,
            "needs_retry": needs_retry,
        }