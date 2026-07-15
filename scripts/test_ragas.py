from app.evaluation.ragas_evaluator import RAGASEvaluator

questions = [
    "What is FastAPI?"
]

answers = [
    "FastAPI is a modern Python web framework."
]

contexts = [
    ["FastAPI is a modern Python web framework used to build APIs."]
]

ground_truths = [
    "FastAPI is a Python web framework."
]

evaluator = RAGASEvaluator()

result = evaluator.evaluate(
    questions,
    answers,
    contexts,
    ground_truths,
)

print(result)