from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.graph.nodes import GraphNodes
from app.graph.router import QueryRouter
from app.graph.workflow import GraphWorkflow
from app.llm.ollama_client import OllamaClient
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever

db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

embedder = Embedder()
retriever = Retriever(db, embedder)
llm = OllamaClient(model=settings.ollama_model)

nodes = GraphNodes(retriever, llm)
router = QueryRouter(llm)          # <-- Add this
workflow = GraphWorkflow(nodes, router)   # <-- Change this

result = workflow.run("Hi")
print(result["answer"])

result = workflow.run("How does FastAPI dependency injection work?")
print(result["answer"])