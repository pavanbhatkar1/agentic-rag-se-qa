from tavily import TavilyClient

from app.core.config import settings


class WebSearcher:
    """Search the web for external information using Tavily."""

    MAX_QUERY_LENGTH = 1200

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

        if not settings.tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not configured.")

        self.client = TavilyClient(
            api_key=settings.tavily_api_key,
        )

    def search(self, query: str) -> list[dict]:
        # Tavily rejects queries longer than 1500 characters. LLM-generated
        # rewrites can occasionally become verbose, so keep the external
        # search query safely below that limit.
        query = " ".join(query.split())[: self.MAX_QUERY_LENGTH].strip()

        if not query:
            return []

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
