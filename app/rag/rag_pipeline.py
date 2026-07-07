from app.llm.ollama_client import OllamaClient
from app.rag.prompt_builder import PromptBuilder
from app.vectorstore.retriever import Retriever


class RAGPipeline:
    """End-to-end RAG pipeline."""

    def __init__(
        self,
        retriever: Retriever,
        llm: OllamaClient,
    ):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm = llm

    def run(self, question: str, top_k: int = 5) -> dict:
        documents = self.retriever.search(
            query=question,
            top_k=top_k,
        )

        prompt = self.prompt_builder.build(
            question=question,
            documents=documents,
        )

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "documents": documents,
        }