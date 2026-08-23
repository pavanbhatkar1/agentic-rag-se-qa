from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient


class QueryRewriter:
    """Rewrite queries when retrieved evidence is insufficient."""

    def __init__(self, llm: OllamaClient):
        self.llm = llm

    def rewrite(self, state: GraphState) -> GraphState:
        documents = state["documents"]

        context = "\n\n".join(
            f"Document {i + 1}:\n{doc['content']}"
            for i, doc in enumerate(documents)
        )

        prompt = f"""
You are improving a software engineering retrieval query.

Original question:
{state["question"]}

Current retrieval quality:
{state["retrieval_score"]}

Retrieved evidence:
{context}

The retrieved evidence was insufficient.

Rewrite the original question into a more precise search query.
Use useful technical terms from the retrieved evidence when appropriate.
Focus on relevant APIs, classes, functions, configuration, implementation
details, filenames, or error messages.

Do not change the user's intent.
Do not answer the question.
Return ONLY the rewritten retrieval query.

Rewritten query:
"""

        rewritten_query = self.llm.generate(prompt).strip()

        # Fallback if the LLM returns an empty response.
        if not rewritten_query:
            rewritten_query = state["question"]

        return {
            **state,
            "rewritten_query": rewritten_query,
            "retry_count": state["retry_count"] + 1,
        }
