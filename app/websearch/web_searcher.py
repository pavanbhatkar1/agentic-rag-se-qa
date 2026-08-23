from tavily import TavilyClient

from app.core.config import settings


class WebSearcher:
    """Search the web for external information using Tavily."""

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

        if not settings.tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not configured.")

        self.client = TavilyClient(
            api_key=settings.tavily_api_key,
        )

    def search(self, query: str) -> list[dict]:
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=self.max_results,
            include_answer=False,
        )

        results = []

        for result in response.get("results", []):
            results.append(
                {
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", ""),
                }
            )

        return results