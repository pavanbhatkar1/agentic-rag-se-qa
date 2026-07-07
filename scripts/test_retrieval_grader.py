from app.graph.retrieval_grader import RetrievalGrader
from app.llm.ollama_client import OllamaClient

grader = RetrievalGrader(OllamaClient())

state = {
    "question": "How do I start FastAPI?",
    "documents": [
        {"content": "Run uvicorn app.main:app --reload"}
    ],
    "answer": "",
    "route": "retrieve",
    "rewritten_query": "",
    "retrieval_score": 0.0,
    "needs_retry": False,
}

result = grader.grade(state)

print(result["needs_retry"])
print(result["retrieval_score"])
