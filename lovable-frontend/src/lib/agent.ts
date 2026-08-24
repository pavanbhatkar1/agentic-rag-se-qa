export interface RetrievedDocument {
  content: string;
  metadata: {
    source: string;
    file_type?: string;
    repository?: string;
    chunk_id?: number;
    [key: string]: unknown;
  };
  score?: number;
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
  return result.route === "direct" ? 4 : 7;
}

function makePromptId(question: string): string {
  let hash = 0;
  for (let index = 0; index < question.length; index += 1) {
    hash = (hash * 31 + question.charCodeAt(index)) >>> 0;
  }
  return hash.toString(36).toUpperCase().padStart(8, "0").slice(0, 8);
}

function toParagraphs(answer: string): string[] {
  const seen = new Set<string>();

  return answer
    .split(/\n{2,}/)
    .map((part) => part.trim())
    .filter(Boolean)
    .filter((part) => {
      const key = part.replace(/\s+/g, " ").toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
}

function splitHeadline(paragraphs: string[]): { headline: string; body: string[] } {
  if (paragraphs.length === 0) {
    return { headline: "Agent response", body: [] };
  }

  const first = paragraphs[0];
  const sentenceMatch = first.match(/^(.{25,140}?[.!?])(?:\s|$)/);

  if (!sentenceMatch) {
    return { headline: "Repository-grounded answer", body: paragraphs };
  }

  const headline = sentenceMatch[1].replace(/^#+\s*/, "").trim();
  const remainder = first.slice(sentenceMatch[0].length).trim();
  const body = remainder ? [remainder, ...paragraphs.slice(1)] : paragraphs.slice(1);

  return { headline, body };
}

function routeConfidence(route: RouteDecision, question: string): number {
  const lower = question.toLowerCase();
  const explicitProjectContext = [
    "this project",
    "this repository",
    "this repo",
    "our project",
    "our codebase",
  ].some((signal) => lower.includes(signal));

  if (explicitProjectContext) return 0.95;
  if (route === "complex") return 0.9;
  if (route === "retrieve") return 0.85;
  return 0.9;
}

export async function runPipeline(rawQuestion: string): Promise<PipelineResult> {
  const question = rawQuestion.trim();
  if (!question) {
    throw new Error("Please enter a question.");
  }

  const response = await fetch("/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  const payload = (await response.json()) as {
    answer?: string;
    route?: RouteDecision;
    documents?: RetrievedDocument[];
    retrieval_score?: number;
    retry_count?: number;
    rewritten_query?: string;
    web_search_used?: boolean;
    web_documents?: WebDocument[];
    latency_ms?: number;
    detail?: string;
  };

  if (!response.ok) {
    throw new Error(payload.detail || "The FastAPI backend returned an error.");
  }

  const route: RouteDecision =
    payload.route === "complex" || payload.route === "retrieve" || payload.route === "direct"
      ? payload.route
      : "retrieve";

  const answerText = payload.answer?.trim() || "The backend returned no answer.";
  const paragraphs = toParagraphs(answerText);
  const { headline, body } = splitHeadline(paragraphs);

  return {
    route,
    routeConfidence: routeConfidence(route, question),
    retrievalScore: payload.retrieval_score ?? 0,
    retryCount: payload.retry_count ?? 0,
    webSearchUsed: Boolean(payload.web_search_used),
    documents: payload.documents ?? [],
    webDocuments: payload.web_documents ?? [],
    rewrittenQuery: payload.rewritten_query || undefined,
    answer: {
      headline,
      paragraphs: body.length > 0 ? body : paragraphs,
    },
    promptId: makePromptId(question),
    latencyMs: payload.latency_ms ?? 0,
    tokens: 0,
  };
}
