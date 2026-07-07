from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient
from app.rag.prompt_builder import PromptBuilder
from app.vectorstore.retriever import Retriever


class GraphNodes:
    """LangGraph nodes."""

    def __init__(
        self,
        retriever: Retriever,
        llm: OllamaClient,
    ):
        self.retriever = retriever
        self.llm = llm
        self.prompt_builder = PromptBuilder()

    def retrieve_node(self, state: GraphState) -> GraphState:
        query = (
            state["rewritten_query"]
            if state["rewritten_query"]
            else state["question"]
        )

        documents = self.retriever.search(
            query=query,
            top_k=5,
        )

        return {
            **state,
            "documents": documents,
        }

    def generate_node(self, state: GraphState) -> GraphState:
        prompt = self.prompt_builder.build(
            question=state["question"],
            documents=state["documents"],
        )

        answer = self.llm.generate(prompt)

        return {
            **state,
            "answer": answer,
        }