from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient


class RetrievalGrader:
    """Evaluate whether retrieved repository context is sufficient."""

    def __init__(self, llm: OllamaClient):
        self.llm = llm

    def grade(self, state: GraphState) -> GraphState:
        documents = state["documents"]

        if not documents:
            return {
                **state,
                "retrieval_score": 0.0,
                "needs_retry": True,
            }

        # Keep the grading prompt small. The reranker has already selected
        # the most relevant documents, so grading does not need full chunks.
        context_parts = []
        for i, doc in enumerate(documents[:8]):
            content = str(doc.get("content", ""))[:1800]
            context_parts.append(f"Document {i + 1}:\n{content}")
        context = "\n\n".join(context_parts)

        prompt = f"""
You are a retrieval quality grader for a software-engineering RAG system.

Question:
{state["question"]}

Repository evidence:
{context}

Decide whether the evidence is sufficient to answer the question.

GOOD = the evidence directly contains the implementation or facts needed.
PARTIAL = the evidence is relevant but some requested details are missing.
BAD = the evidence is irrelevant or does not support the answer.

Return exactly one word: GOOD, PARTIAL, or BAD.
Do not explain your decision.

Label:
"""

        response = self.llm.generate(prompt).strip().upper()

        # Mistral may add punctuation or a short explanation even when asked
        # for one word. Parse the first valid label instead of treating that
        # normal LLM behavior as a retrieval failure.
        label = None
        for candidate in ("GOOD", "PARTIAL", "BAD"):
            if response.startswith(candidate):
                label = candidate
                break

        if label == "GOOD":
            return {
                **state,
                "retrieval_score": 1.0,
                "needs_retry": False,
            }

        if label == "PARTIAL":
            return {
                **state,
                "retrieval_score": 0.5,
                "needs_retry": True,
            }

        return {
            **state,
            "retrieval_score": 0.0,
            "needs_retry": True,
        }
