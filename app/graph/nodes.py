from app.graph.state import GraphState
from app.llm.ollama_client import OllamaClient
from app.rag.prompt_builder import PromptBuilder
from app.retrieval.reranker import BGEReranker
from app.vectorstore.retriever import Retriever
from app.websearch.web_searcher import WebSearcher


class GraphNodes:
    """LangGraph nodes for Adaptive + Corrective RAG."""

    def __init__(
        self,
        retriever: Retriever,
        llm: OllamaClient,
        reranker: BGEReranker | None = None,
        web_searcher: WebSearcher | None = None,
    ):
        self.retriever = retriever
        self.llm = llm
        self.reranker = reranker or BGEReranker()
        self.web_searcher = web_searcher or WebSearcher()
        self.prompt_builder = PromptBuilder()

    def retrieve_node(self, state: GraphState) -> GraphState:
        query = (
            state["rewritten_query"]
            if state["rewritten_query"]
            else state["question"]
        )

        if state["route"] == "complex":
            retrieval_k = 20
            rerank_k = 8
        else:
            retrieval_k = 10
            rerank_k = 5

        documents = self.retriever.search(
            query=query,
            top_k=retrieval_k,
        )

        documents = self.reranker.rerank(
            query=query,
            documents=documents,
            top_k=rerank_k,
        )

        return {
            **state,
            "documents": documents,
        }

    def direct_generate_node(self, state: GraphState) -> GraphState:
        """Generate an answer without repository retrieval."""

        prompt = f"""
Answer the following question using your general knowledge.

Question:
{state["question"]}

Give a concise and accurate answer.
"""

        answer = self.llm.generate(prompt)

        return {
            **state,
            "answer": answer,
        }

    def web_search_node(self, state: GraphState) -> GraphState:
        """Search the web when repository evidence is insufficient."""

        query = (
            state["rewritten_query"]
            if state["rewritten_query"]
            else state["question"]
        )

        web_documents = self.web_searcher.search(query)

        return {
            **state,
            "web_documents": web_documents,
            "web_search_used": True,
        }

    def generate_node(self, state: GraphState) -> GraphState:
        """Generate an answer using repository and/or web evidence."""

        repository_context = "\n\n".join(
            doc["content"]
            for doc in state["documents"]
        )

        web_context = "\n\n".join(
            f"Title: {doc['title']}\nURL: {doc['url']}\nContent: {doc['content']}"
            for doc in state["web_documents"]
        )

        if state["web_search_used"]:
            prompt = f"""
You are a software engineering question-answering assistant.

Answer the user's question using the retrieved evidence below.

Repository Evidence:
{repository_context}

Web Evidence:
{web_context}

Rules:
- Prefer repository evidence when it directly answers the question.
- Use web evidence when repository evidence is insufficient.
- Do not invent implementation details.
- If the evidence does not contain the requested information,
  clearly say that it could not be found.

Question:
{state["question"]}

Answer:
"""
        else:
            prompt = self.prompt_builder.build(
                question=state["question"],
                documents=state["documents"],
            )

        answer = self.llm.generate(prompt)

        return {
            **state,
            "answer": answer,
        }
