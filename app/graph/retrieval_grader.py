from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient


class RetrievalGrader:
    """Strict evaluator for repository retrieval quality."""

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

        context = "\n\n".join(
            f"Document {i + 1}:\n{doc['content']}"
            for i, doc in enumerate(documents)
        )

        prompt = f"""
You are a STRICT retrieval evaluator for a software engineering RAG system.

Question:
{state["question"]}

Retrieved Repository Context:
{context}

Your task is to determine whether the repository context contains enough
EXPLICIT evidence to answer the EXACT question.

Return ONLY:

GOOD
PARTIAL
BAD

Rules:

GOOD:
The retrieved context explicitly contains the information needed to answer
the question.

PARTIAL:
The context is related to the question but some requested information
is missing.

BAD:
The context is irrelevant or does not contain enough evidence.

IMPORTANT:

- Do NOT use your general knowledge.
- Do NOT infer missing implementation details.
- Do NOT assume that two documents are related just because they mention
  the same technology.
- If the question asks for a specific algorithm, function, class,
  filename, implementation detail, or exact behavior, that information
  must be explicitly present in the retrieved context.
- A generic WebSocket documentation page is NOT enough to answer a
  question about an internal compression algorithm.
- A file such as applications.py or __init__.py is NOT evidence for
  WebSocket compression unless the relevant implementation is actually
  present in the retrieved content.
- If you are uncertain, choose PARTIAL or BAD rather than GOOD.

Question:
{state["question"]}

Label:
"""

        response = self.llm.generate(prompt).strip().upper()

        if response == "GOOD":
            return {
                **state,
                "retrieval_score": 1.0,
                "needs_retry": False,
            }

        if response == "PARTIAL":
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
