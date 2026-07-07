from langgraph.graph import END, START, StateGraph

from app.graph.nodes import GraphNodes
from app.graph.query_rewriter import QueryRewriter
from app.graph.retrieval_grader import RetrievalGrader
from app.graph.router import QueryRouter
from app.graph.state import GraphState


class GraphWorkflow:
    """Adaptive + Corrective RAG workflow."""

    def __init__(
        self,
        nodes: GraphNodes,
        router: QueryRouter,
        grader: RetrievalGrader,
        rewriter: QueryRewriter,
    ):
        graph = StateGraph(GraphState)

        graph.add_node("retrieve", nodes.retrieve_node)
        graph.add_node("generate", nodes.generate_node)
        graph.add_node("grade", grader.grade)
        graph.add_node("rewrite", rewriter.rewrite)

        graph.add_conditional_edges(
            START,
            router.route,
            {
                "retrieve": "retrieve",
                "direct": "generate",
            },
        )

        graph.add_edge("retrieve", "grade")

        graph.add_conditional_edges(
            "grade",
            lambda state: "rewrite" if state["needs_retry"] else "generate",
            {
                "rewrite": "rewrite",
                "generate": "generate",
            },
        )

        graph.add_edge("rewrite", "retrieve")
        graph.add_edge("generate", END)

        self.app = graph.compile()

    def run(self, question: str) -> dict:
        state: GraphState = {
            "question": question,
            "documents": [],
            "answer": "",
            "route": "retrieve",
            "rewritten_query": "",
            "retrieval_score": 0.0,
            "needs_retry": False,
        }

        return self.app.invoke(state)