from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.graph.nodes import GraphNodes
from app.llm.ollama_client import OllamaClient
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever

db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

embedder = Embedder()
retriever = Retriever(db, embedder)
llm = OllamaClient()

nodes = GraphNodes(retriever, llm)

state = {
    "question": "How start server?",
    "documents": [],
    "answer": "",
    "route": "retrieve",
    "rewritten_query": "How do I start the FastAPI server?",
    "retrieval_score": 0.0,
    "needs_retry": False,
}

result = nodes.retrieve_node(state)

print(len(result["documents"]))