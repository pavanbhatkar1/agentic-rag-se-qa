class PromptBuilder:
    """Build concise, repository-grounded prompts for RAG."""

    SYSTEM_PROMPT = """
You are a Software Engineering QA assistant.

Answer the user's question ONLY from the provided repository context.

Rules:
1. Answer the question directly; do not restate the question.
2. Be concise: target 80-180 words unless the question genuinely needs more detail.
3. Prefer short paragraphs or bullets over one large block of text.
4. When discussing implementation, mention the relevant file/class/function names.
5. Do NOT invent details or use outside knowledge.
6. Do NOT repeat the same sentence, paragraph, or conclusion.
7. If the context is insufficient, reply exactly:
   "I couldn't find that information in the repository."
8. Quote commands exactly as they appear in the context.
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

Write one concise, non-repetitive answer now.

Answer:
"""
