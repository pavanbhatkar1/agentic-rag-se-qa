from fastapi import APIRouter

from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.graph.nodes import GraphNodes
from app.graph.query_rewriter import QueryRewriter
from app.graph.retrieval_grader import RetrievalGrader
from app.graph.router import QueryRouter
from app.graph.workflow import GraphWorkflow
from app.llm.ollama_client import OllamaClient
from app.rag.rag_pipeline import RAGPipeline
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever

router = APIRouter()

db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

embedder = Embedder()
retriever = Retriever(db, embedder)
llm = OllamaClient(model=settings.ollama_model)

nodes = GraphNodes(retriever, llm)
query_router = QueryRouter(llm)
grader = RetrievalGrader(llm)
rewriter = QueryRewriter(llm)

workflow = GraphWorkflow(
    nodes=nodes,
    router=query_router,
    grader=grader,
    rewriter=rewriter,
)

pipeline = RAGPipeline(workflow)


@router.post("/query")
def query(request: dict):
    return pipeline.run(request["question"])