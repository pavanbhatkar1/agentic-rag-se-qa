class PromptBuilder:
    """Build prompts for RAG."""

    SYSTEM_PROMPT = (
        "You are a Software Engineering assistant.\n"
        "Answer ONLY using the provided context.\n"
        "If the answer cannot be found in the context, say:\n"
        "\"I couldn't find that information in the repository.\""
    )

    def build(self, question: str, documents: list[dict]) -> str:
        context = "\n\n".join(
            doc["content"] for doc in documents
        )

        return f"""{self.SYSTEM_PROMPT}

Context:
---------
{context}
---------

Question:
{question}

Answer:
"""