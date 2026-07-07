from app.graph.query_rewriter import QueryRewriter
from app.llm.ollama_client import OllamaClient

rewriter = QueryRewriter(OllamaClient())

state = {
    "question": "How start server?",
    "documents": [],
    "answer": "",
    "route": "retrieve",
    "rewritten_query": "",
    "retrieval_score": 0.0,
    "needs_retry": False,
}

result = rewriter.rewrite(state)

print(result["rewritten_query"])