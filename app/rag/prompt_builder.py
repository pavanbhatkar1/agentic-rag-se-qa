class PromptBuilder:
    """Build prompts for RAG."""

    SYSTEM_PROMPT = """
You are a Software Engineering QA assistant.

Rules:
1. Answer ONLY from the provided repository context.
2. Do NOT use your own knowledge.
3. Do NOT make assumptions.
4. If the context is insufficient, reply exactly:
   "I couldn't find that information in the repository."
5. Quote commands exactly as they appear in the context.
"""

    def build(self, question: str, documents: list[dict]) -> str:
        context = "\n\n".join(
            doc["content"] for doc in documents
        )

        return f"""{self.SYSTEM_PROMPT}

Repository Context:
==================
{context}
==================

Question:
{question}

Answer:
"""