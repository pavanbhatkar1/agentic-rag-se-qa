from langchain_ollama import ChatOllama


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
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content