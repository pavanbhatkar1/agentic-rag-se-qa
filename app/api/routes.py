import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.embeddings.embedder import Embedder
from app.graph.nodes import GraphNodes
from app.graph.query_rewriter import QueryRewriter
from app.graph.retrieval_grader import RetrievalGrader
from app.graph.router import QueryRouter
from app.graph.workflow import GraphWorkflow
from app.llm.ollama_client import OllamaClient
from app.rag.rag_pipeline import RAGPipeline
from app.retrieval.reranker import BGEReranker
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever


router = APIRouter()


def build_pipeline() -> RAGPipeline:
    """Build the Agentic RAG pipeline."""

    db = QdrantDB(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
    )

    embedder = Embedder()

    retriever = Retriever(
        db=db,
        embedder=embedder,
    )

    reranker = BGEReranker()

    llm = OllamaClient(
        model=settings.ollama_model,
    )

    nodes = GraphNodes(
        retriever=retriever,
        llm=llm,
        reranker=reranker,
    )

    query_router = QueryRouter(llm)
    grader = RetrievalGrader(llm)
    rewriter = QueryRewriter(llm)

    workflow = GraphWorkflow(
        nodes=nodes,
        router=query_router,
        grader=grader,
        rewriter=rewriter,
    )

    return RAGPipeline(workflow)


pipeline: RAGPipeline | None = None


def get_pipeline() -> RAGPipeline:
    """Create the pipeline lazily when first needed."""

    global pipeline

    if pipeline is None:
        pipeline = build_pipeline()

    return pipeline


@router.post("/query")
def query(request: dict):
    """Run the Agentic RAG pipeline and return the full UI trace payload."""

    question = request.get("question", "").strip()
    if not question:
        return JSONResponse(
            status_code=400,
            content={"detail": "question is required"},
        )

    started = time.perf_counter()

    try:
        result = get_pipeline().run(question)
    except Exception as exc:
        # Always return JSON so the frontend can display a useful error
        # instead of failing while parsing FastAPI's plain-text 500 page.
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Pipeline execution failed: {exc}",
            },
        )

    latency_ms = round((time.perf_counter() - started) * 1000, 2)

    return {
        "answer": result["answer"],
        "route": result["route"],
        "documents": result["documents"],
        "retrieval_score": result["retrieval_score"],
        "needs_retry": result["needs_retry"],
        "retry_count": result["retry_count"],
        "rewritten_query": result["rewritten_query"],
        "web_search_used": result["web_search_used"],
        "web_documents": result["web_documents"],
        "latency_ms": latency_ms,
    }
