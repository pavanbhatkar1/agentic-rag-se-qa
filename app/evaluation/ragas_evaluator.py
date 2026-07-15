from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_precision,
)


class RAGASEvaluator:
    """Evaluate a RAG pipeline using RAGAS."""

    def evaluate(
        self,
        questions: list[str],
        answers: list[str],
        contexts: list[list[str]],
        ground_truths: list[str],
    ):
        dataset = Dataset.from_dict(
            {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
                "ground_truth": ground_truths,
            }
        )

        return evaluate(
            dataset=dataset,
            metrics=[
                answer_relevancy,
                faithfulness,
                context_precision,
            ],
        )