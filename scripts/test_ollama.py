from app.llm.ollama_client import OllamaClient

llm = OllamaClient()

response = llm.generate(
    "What is FastAPI? Answer in one sentence."
)

print(response)
