from langgraph.graph import END, START, StateGraph

from app.graph.nodes import GraphNodes
from app.graph.router import QueryRouter
from app.graph.state import GraphState


class GraphWorkflow:
    """Adaptive-RAG workflow."""

    def __init__(
        self,
        nodes: GraphNodes,
        router: QueryRouter,
    ):
        graph = StateGraph(GraphState)

        graph.add_node("retrieve", nodes.retrieve_node)
        graph.add_node("generate", nodes.generate_node)

        graph.add_conditional_edges(
            START,
            router.route,
            {
                "retrieve": "retrieve",
                "direct": "generate",
            },
        )

        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)

        self.app = graph.compile()

    def run(self, question: str) -> dict:
        state: GraphState = {
            "question": question,
            "documents": [],
            "answer": "",
        }

        return self.app.invoke(state)