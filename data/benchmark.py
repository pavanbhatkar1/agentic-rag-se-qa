import json
import time
from pathlib import Path
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

def build_pipeline():
    db = QdrantDB(url=settings.qdrant_url, collection_name=settings.qdrant_collection)
    embedder = Embedder()
    retriever = Retriever(db, embedder)
    reranker = BGEReranker()
    llm = OllamaClient(model=settings.ollama_model)
    nodes = GraphNodes(retriever=retriever, llm=llm, reranker=reranker)
    router = QueryRouter(llm)
    grader = RetrievalGrader(llm)
    rewriter = QueryRewriter(llm)
    workflow = GraphWorkflow(nodes=nodes, router=router, grader=grader, rewriter=rewriter)
    return RAGPipeline(workflow)

def main():
    benchmark_path = Path("data/benchmark.json")
    data = json.loads(benchmark_path.read_text(encoding="utf-8"))
    limit = int(__import__("os").environ.get("BENCHMARK_LIMIT", str(len(data))))
    data = data[:limit]
    pipeline = build_pipeline()
    results, latencies = [], []
    for i, item in enumerate(data, start=1):
        start = time.perf_counter()
        result = pipeline.run(item["question"])
        latency = time.perf_counter() - start
        latencies.append(latency)
        results.append({
            "question": item["question"],
            "ground_truth": item["ground_truth"],
            "difficulty": item.get("difficulty"),
            "answer": result["answer"],
            "contexts": [doc["content"] for doc in result["documents"]],
            "route": result.get("route"),
            "retrieval_score": result.get("retrieval_score"),
            "retry_count": result.get("retry_count"),
            "web_search_used": result.get("web_search_used"),
            "latency_ms": round(latency * 1000, 2),
        })
        print(f"{i}/{len(data)} - {latency * 1000:.2f} ms - {item.get('difficulty','')}")
    avg = sum(latencies) / len(latencies) if latencies else 0
    output = {"average_latency_ms": round(avg * 1000, 2), "count": len(results), "results": results}
    Path("data/benchmark_results.json").write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nAverage latency: {avg * 1000:.2f} ms")
if __name__ == "__main__":
    main()
