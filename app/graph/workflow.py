from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.graph.nodes import GraphNodes
from app.graph.query_rewriter import QueryRewriter
from app.graph.retrieval_grader import RetrievalGrader
from app.graph.router import QueryRouter
from app.graph.state import GraphState


MAX_RETRIES = 1


class GraphWorkflow:
    """Adaptive + Corrective RAG with web-search fallback."""

    def __init__(
        self,
        nodes: GraphNodes,
        router: QueryRouter,
        grader: RetrievalGrader,
        rewriter: QueryRewriter,
    ):
        self.router = router

        graph = StateGraph(GraphState)

        # Nodes
        graph.add_node("route", self.route_node)
        graph.add_node("retrieve", nodes.retrieve_node)
        graph.add_node("direct_generate", nodes.direct_generate_node)
        graph.add_node("generate", nodes.generate_node)
        graph.add_node("grade", grader.grade)
        graph.add_node("rewrite", rewriter.rewrite)
        graph.add_node("web_search", nodes.web_search_node)

        # ---------------------------------------------------------
        # Adaptive RAG
        # ---------------------------------------------------------

        graph.add_edge(START, "route")

        graph.add_conditional_edges(
            "route",
            self._route_decision,
            {
                "direct": "direct_generate",
                "retrieve": "retrieve",
                "complex": "retrieve",
            },
        )

        graph.add_edge("direct_generate", END)

        # ---------------------------------------------------------
        # Repository Retrieval + Corrective RAG
        # ---------------------------------------------------------

        graph.add_edge("retrieve", "grade")

        graph.add_conditional_edges(
            "grade",
            self._correction_decision,
            {
                "retry": "rewrite",
                "web": "web_search",
                "generate": "generate",
            },
        )

        # Corrective retry.
        graph.add_edge("rewrite", "retrieve")

        # Web fallback.
        graph.add_edge("web_search", "generate")

        # Final generation.
        graph.add_edge("generate", END)

        self.app = graph.compile()

    def route_node(self, state: GraphState) -> GraphState:
        """Run Adaptive RAG router and store the selected route."""

        route = self.router.route(state)

        return {
            **state,
            "route": route,
        }

    @staticmethod
    def _route_decision(
        state: GraphState,
    ) -> Literal["direct", "retrieve", "complex"]:
        return state["route"]

    @staticmethod
    def _correction_decision(state: GraphState) -> str:
        """
        Decide what to do after retrieval grading.

        GOOD      ? generate
        BAD/PARTIAL + retries available ? rewrite and retry
        BAD/PARTIAL + retry exhausted ? web search
        """

        if not state["needs_retry"]:
            return "generate"

        if state["retry_count"] < MAX_RETRIES:
            return "retry"

        return "web"

    def run(self, question: str) -> dict:
        state: GraphState = {
            "question": question,
            "documents": [],
            "web_documents": [],
            "answer": "",
            "route": "direct",
            "rewritten_query": "",
            "retrieval_score": 0.0,
            "needs_retry": False,
            "retry_count": 0,
            "web_search_used": False,
        }

        return self.app.invoke(state)
