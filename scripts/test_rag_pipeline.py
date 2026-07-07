from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.llm.ollama_client import OllamaClient
from app.rag.rag_pipeline import RAGPipeline
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever

db = QdrantDB(
    url=settings.qdrant_url,
    collection_name=settings.qdrant_collection,
)

embedder = Embedder()
retriever = Retriever(db, embedder)
llm = OllamaClient()

pipeline = RAGPipeline(
    retriever=retriever,
    llm=llm,
)

result = pipeline.run(
    "How do I start the FastAPI server?"
)

print(result["answer"])