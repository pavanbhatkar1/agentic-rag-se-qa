import json
from pathlib import Path
from app.evaluation.ragas_evaluator import RAGASEvaluator

def main():
    p = Path("data/benchmark_results.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    results = data["results"]
    evaluator = RAGASEvaluator()
    score = evaluator.evaluate(
        questions=[r["question"] for r in results],
        answers=[r["answer"] for r in results],
        contexts=[r["contexts"] for r in results],
        ground_truths=[r["ground_truth"] for r in results],
    )
    print(score)
    print("\nRAGAS scores:")
    try:
        print(score.to_pandas().to_string(index=False))
    except Exception:
        pass

if __name__ == "__main__":
    main()
