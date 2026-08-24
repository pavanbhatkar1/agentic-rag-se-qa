/*
 * Simulated agentic RAG pipeline.
 *
 * Mirrors the response shape of the FastAPI backend (app.api.routes
 * get_pipeline().run(question)) so the console can be wired to the real
 * endpoint later by swapping `runPipeline` for a fetch call.
 */

export interface RetrievedDocument {
  content: string;
  metadata: {
    source: string;
    file_type?: string;
  };
}

export interface WebDocument {
  title: string;
  url?: string;
  content: string;
}

export interface AnswerBullet {
  title: string;
  body: string;
}

export interface AgentAnswer {
  headline: string;
  paragraphs: string[];
  bullets?: AnswerBullet[];
}

export type RouteDecision = "direct" | "retrieve" | "complex";

export interface PipelineResult {
  route: RouteDecision;
  routeConfidence: number;
  retrievalScore: number;
  retryCount: number;
  webSearchUsed: boolean;
  documents: RetrievedDocument[];
  webDocuments: WebDocument[];
  rewrittenQuery?: string;
  answer: AgentAnswer;
  promptId: string;
  latencyMs: number;
  tokens: number;
}

export function getStepCount(result: PipelineResult): number {
  // direct: query, router, retrieval-skipped, generation
  // otherwise: query, router, retrieval, grader, rewrite, web search, generation
  return result.route === "direct" ? 4 : 7;
}

function hashQuestion(question: string): number {
  let hash = 0;
  for (let i = 0; i < question.length; i += 1) {
    hash = (hash * 31 + question.charCodeAt(i)) >>> 0;
  }
  return hash;
}

const ARCHITECTURE_ANSWER: AgentAnswer = {
  headline:
    "Multi-agent RAG routing facilitates specialized retrieval through a tree-based decision structure.",
  paragraphs: [
    "A hierarchical multi-agent RAG system utilizes a central router agent to categorize incoming user queries before dispatching them to specialized sub-agents. This avoids the noise associated with broad-spectrum retrieval by ensuring only relevant vector namespaces are queried.",
    "The primary architecture consists of three layers: the **Intent Orchestrator**, the **Domain Retrievers**, and the **Synthesis Engine**. When a query is identified as complex, it is decomposed into sub-tasks that are executed in parallel across the specific node experts.",
  ],
  bullets: [
    {
      title: "Level 1: Semantic Routing",
      body: "Directs the query based on high-level intent (e.g., technical docs vs. API reference).",
    },
    {
      title: "Level 2: Contextual Retrieval",
      body: "Sub-agents perform specific K-neighbor searches within isolated indices.",
    },
  ],
};

const FASTAPI_ANSWER: AgentAnswer = {
  headline:
    "FastAPI defines API routes by decorating path operation functions on an APIRouter or application instance.",
  paragraphs: [
    "A route is declared by applying a decorator such as **@app.get** or **@router.post** to an async function. The decorator registers the path, HTTP method, and response model, while the function signature declares path parameters, query parameters, and the request body through type-annotated arguments.",
    "Because routes are plain Python functions, dependencies declared with **Depends()** are resolved automatically per request, and the return value is validated against the declared response model before serialization.",
  ],
  bullets: [
    {
      title: "Decorator registration",
      body: "@app.get('/items/{item_id}') binds the path and method to the handler.",
    },
    {
      title: "Typed signature",
      body: "Path, query, and body parameters come from type annotations and Pydantic models.",
    },
  ],
};

const DIRECT_ANSWER: AgentAnswer = {
  headline:
    "This is a general knowledge question, so the agent answered directly from the model without repository retrieval.",
  paragraphs: [
    "The query router classified this prompt as **DIRECT** — it does not depend on private repository context, so vector retrieval was skipped entirely. The answer is generated straight from the language model's pretrained knowledge.",
    "Questions about concepts, definitions, or well-known libraries typically take this path, which keeps latency low and avoids polluting the context window with irrelevant documents.",
  ],
};

const FALLBACK_ANSWER: AgentAnswer = {
  headline:
    "The agent combined repository context with web results to synthesize this answer after one retrieval retry.",
  paragraphs: [
    "The initial retrieval pass returned documents below the relevance threshold, so the agent **rewrote the query** and searched again. The second pass recovered useful repository context, and a web search supplemented gaps that the local index could not cover.",
    "This retry-then-escalate pattern is what makes the pipeline agentic: the grader's relevance score decides whether the agent accepts the context, rewrites the query, or falls back to the open web before generating the final answer.",
  ],
  bullets: [
    {
      title: "Retry loop",
      body: "Low grader scores trigger a query rewrite and a second retrieval pass.",
    },
    {
      title: "Web fallback",
      body: "When the repository cannot support an answer, external sources are merged in.",
    },
  ],
};

export async function runPipeline(rawQuestion: string): Promise<PipelineResult> {
  const question = rawQuestion.trim();

  const response = await fetch("/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  const payload = (await response.json()) as {
    answer?: string;
    route?: RouteDecision;
    retrieval_score?: number;
    web_search_used?: boolean;
    retry_count?: number;
    detail?: string;
  };

  if (!response.ok) {
    throw new Error(payload.detail || "The FastAPI backend returned an error.");
  }

  const route: RouteDecision =
    payload.route === "complex" || payload.route === "retrieve" || payload.route === "direct"
      ? payload.route
      : "retrieve";

  const answerText = payload.answer || "The backend returned no answer.";
  const paragraphs = answerText
    .split(/\n{2,}/)
    .map((part) => part.trim())
    .filter(Boolean);

  return {
    route,
    routeConfidence: 0,
    retrievalScore: payload.retrieval_score ?? 0,
    retryCount: payload.retry_count ?? 0,
    webSearchUsed: Boolean(payload.web_search_used),
    documents: [],
    webDocuments: [],
    answer: {
      headline: paragraphs[0] || "Agent response",
      paragraphs: paragraphs.length > 1 ? paragraphs.slice(1) : [answerText],
    },
    promptId: `${Date.now().toString(36).toUpperCase()}`,
    latencyMs: 0,
    tokens: 0,
  };
}
