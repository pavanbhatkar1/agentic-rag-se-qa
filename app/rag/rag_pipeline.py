from app.graph.workflow import GraphWorkflow


class RAGPipeline:
    """Entry point for the Agentic RAG system."""

    def __init__(self, workflow: GraphWorkflow):
        self.workflow = workflow

    def run(self, question: str) -> dict:
        state = self.workflow.run(question)

        return {
            "answer": state["answer"],
            "route": state["route"],
            "documents": state["documents"],
            "retrieval_score": state["retrieval_score"],
            "needs_retry": state["needs_retry"],
            "retry_count": state["retry_count"],
            "rewritten_query": state["rewritten_query"],
            "web_search_used": state["web_search_used"],
            "web_documents": state["web_documents"],
        }
