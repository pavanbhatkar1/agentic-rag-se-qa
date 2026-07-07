from app.llm.ollama_client import OllamaClient
from app.graph.router import QueryRouter

router = QueryRouter(OllamaClient())

print(router.route({
    "question": "Hi",
    "documents": [],
    "answer": "",
}))

print(router.route({
    "question": "How does FastAPI dependency injection work?",
    "documents": [],
    "answer": "",
}))