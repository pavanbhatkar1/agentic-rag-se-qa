from app.rag.prompt_builder import PromptBuilder

builder = PromptBuilder()

docs = [
    {"content": "FastAPI uses dependency injection."},
    {"content": "Routes are defined using decorators."},
]

prompt = builder.build(
    "How does FastAPI define routes?",
    docs,
)

print(prompt)
