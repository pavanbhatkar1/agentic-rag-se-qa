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
        "retriever",
        "reranker",
        "query router",
        "queryrouter",
        "rag pipeline",
        "workflow",
    )

    PROJECT_CONTEXT_SIGNALS = (
        "this project",
        "this repository",
        "this repo",
        "our project",
        "our code",
        "our codebase",
        "in the project",
        "in this codebase",
        "in this repository",
    )

    COMPLEX_SIGNALS = (
        "architecture",
        "workflow",
        "pipeline",
        "end-to-end",
        "trace",
        "how do these components",
        "how do the components",
        "how does .* connect",
        "compare",
    )

    def __init__(self, llm: OllamaClient):
        self.llm = llm

    def route(self, state: GraphState) -> Route:
        question = state["question"].strip()
        question_lower = question.lower()

        has_project_context = any(
            signal in question_lower
            for signal in self.PROJECT_CONTEXT_SIGNALS
        )
        has_repository_signal = any(
            signal in question_lower
            for signal in self.REPOSITORY_SIGNALS
        )

        # Explicit project/repository questions must use local evidence.
        if has_project_context:
            if any(signal in question_lower for signal in self.COMPLEX_SIGNALS):
                return "complex"
            return "retrieve"

        # General-knowledge questions do not need repository retrieval.
        if not has_repository_signal:
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
