from fastapi import APIRouter

from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.llm.ollama_client import OllamaClient
from app.rag.rag_pipeline import RAGPipeline
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever

router = APIRouter()

# Initialize once
db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

embedder = Embedder()
retriever = Retriever(db, embedder)
llm = OllamaClient(model=settings.llm_model)

pipeline = RAGPipeline(
    retriever=retriever,
    llm=llm,
)


@router.post("/query")
def query(request: dict):
    return pipeline.run(request["question"])