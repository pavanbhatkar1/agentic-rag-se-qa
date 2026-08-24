# Benchmark setup

This package adapts the supplied Easy/Medium/Hard dataset to the project's existing benchmark schema.

Files:
- `benchmark.json` -> copy to `data/benchmark.json`
- `benchmark.py` -> replace `app/evaluation/benchmark.py`
- `run_ragas.py` -> copy to `scripts/run_ragas.py`

The included benchmark contains 15 deterministic examples: 5 Easy, 5 Medium, 5 Hard.

Run:
1. Copy `benchmark.json` to `data/benchmark.json`
2. Replace `app/evaluation/benchmark.py`
3. Run: `python app/evaluation/benchmark.py`
   Optional quick run: `$env:BENCHMARK_LIMIT="3"; python app/evaluation/benchmark.py`
4. Copy `run_ragas.py` to `scripts/run_ragas.py`
5. Run: `python scripts/run_ragas.py`

Do not commit generated `data/benchmark_results.json`; it is already ignored by the project's `.gitignore`.
