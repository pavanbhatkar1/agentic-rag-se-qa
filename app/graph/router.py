from typing import Literal

from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient


Route = Literal["direct", "retrieve", "complex"]


class QueryRouter:
    """Adaptive RAG query router."""

    REPOSITORY_SIGNALS = (
        "repository",
        "repo",
        "source code",
        "codebase",
        "implementation",
        "implemented",
        "function",
        "class",
        "module",
        "file",
        "endpoint",
        "route",
        "configuration",
        "config",
        "error",
        "exception",
        "bug",
        "fastapi",
        "qdrant",
        "langgraph",
        "ollama",
    )

    def __init__(self, llm: OllamaClient):
        self.llm = llm

    def route(self, state: GraphState) -> Route:
        question = state["question"].strip()
        question_lower = question.lower()

        # Obvious general-knowledge questions do not need repository retrieval.
        if not any(
            signal in question_lower
            for signal in self.REPOSITORY_SIGNALS
        ):
            return "direct"

        prompt = f"""
You are the routing controller for a software engineering RAG system.

Classify the user's question into exactly ONE category.

DIRECT:
The question can be answered using general knowledge and does not
require information from the indexed software repository.

RETRIEVE:
The question requires information from the indexed repository,
documentation, source code, APIs, classes, functions, configuration,
or implementation.

COMPLEX:
The question requires deeper repository investigation, such as tracing
multiple components, understanding an internal workflow, comparing
implementations, or connecting several pieces of source code.

Return ONLY one label:

DIRECT
RETRIEVE
COMPLEX

Question:
{question}

Label:
"""

        decision = self.llm.generate(prompt).strip().upper()

        if decision == "DIRECT":
            return "direct"

        if decision == "COMPLEX":
            return "complex"

        return "retrieve"