from app.graph.workflow import GraphWorkflow


class RAGPipeline:
    """Entry point for the RAG system."""

    def __init__(self, workflow: GraphWorkflow):
        self.workflow = workflow

    def run(self, question: str) -> dict:
        state = self.workflow.run(question)

        return {
            "answer": state["answer"],
            "documents": state["documents"],
        }