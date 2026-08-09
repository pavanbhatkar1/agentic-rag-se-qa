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
from app.vectorstore.qdrant_client import QdrantDB
from app.vectorstore.retriever import Retriever


def build_pipeline():
    db = QdrantDB(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
    )

    embedder = Embedder()
    retriever = Retriever(db, embedder)
    llm = OllamaClient(model=settings.ollama_model)

    nodes = GraphNodes(retriever, llm)
    router = QueryRouter(llm)
    grader = RetrievalGrader(llm)
    rewriter = QueryRewriter(llm)

    workflow = GraphWorkflow(
        nodes=nodes,
        router=router,
        grader=grader,
        rewriter=rewriter,
    )

    return RAGPipeline(workflow)


def main():
    benchmark_path = Path("data/benchmark.json")
    data = json.loads(benchmark_path.read_text(encoding="utf-8"))

    pipeline = build_pipeline()
    results = []
    latencies = []

    for i, item in enumerate(data, start=1):
        start = time.perf_counter()

        result = pipeline.run(item["question"])

        latency = time.perf_counter() - start
        latencies.append(latency)

        results.append(
            {
                "question": item["question"],
                "ground_truth": item["ground_truth"],
                "answer": result["answer"],
                "contexts": [
                    doc["content"]
                    for doc in result["documents"]
                ],
                "latency_ms": round(latency * 1000, 2),
            }
        )

        print(f"{i}/{len(data)} - {latency * 1000:.2f} ms")

    average_latency = sum(latencies) / len(latencies)

    output = {
        "average_latency_ms": round(
            average_latency * 1000, 2
        ),
        "results": results,
    }

    Path("data/benchmark_results.json").write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print(
        f"\nAverage latency: "
        f"{average_latency * 1000:.2f} ms"
    )


if __name__ == "__main__":
    main()