from langchain_ollama import ChatOllama

from app.core.config import settings


class OllamaClient:
    """Simple wrapper around Ollama."""

    def __init__(
        self,
        model: str = "mistral:7b",
        temperature: float = 0.0,
    ):
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            base_url=settings.ollama_base_url,
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content