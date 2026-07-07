from app.graph.state import GraphState

state: GraphState = {
    "question": "",
    "documents": [],
    "answer": "",
    "route": "retrieve",
    "rewritten_query": "",
    "retrieval_score": 0.0,
    "needs_retry": False,
}

print(state)
