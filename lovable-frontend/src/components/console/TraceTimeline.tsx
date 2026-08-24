import { useState, type ReactNode } from "react";
import type { PipelineResult } from "@/lib/agent";
import type { RunStatus } from "./AnswerPanel";

function TraceNode({
  n,
  title,
  active = false,
  dimmed = false,
  children,
}: {
  n: number;
  title: string;
  active?: boolean;
  dimmed?: boolean;
  children?: ReactNode;
}) {
  return (
    <div className={`relative animate-fade-in pl-8 ${dimmed ? "opacity-40" : ""}`}>
      <div
        className={`absolute left-0 top-1 flex size-3.5 items-center justify-center rounded-full border ring-4 ring-background ${
          active ? "border-accent bg-primary-deep" : "border-edge bg-background"
        }`}
      >
        <span className={`font-mono text-[8px] ${active ? "text-primary-bright" : "text-foreground-subtle"}`}>
          {n}
        </span>
      </div>
      <div
        className={`text-xs font-medium ${
          active ? "text-primary-bright" : dimmed ? "text-foreground" : "text-foreground-strong"
        } ${children ? "mb-1" : ""}`}
      >
        {title}
      </div>
      {children}
    </div>
  );
}

function Collapsible({ label, children }: { label: string; children: ReactNode }) {
  return (
    <details className="group">
      <summary className="flex list-none cursor-pointer items-center justify-between font-mono text-[10px] uppercase tracking-widest text-foreground-subtle [&::-webkit-details-marker]:hidden">
        <span>{label}</span>
        <span className="transition-transform group-open:rotate-180">↓</span>
      </summary>
      <div className="mt-2">{children}</div>
    </details>
  );
}

function truncate(text: string, max = 42): string {
  return text.length > max ? `${text.slice(0, max).trimEnd()}...` : text;
}

interface TraceTimelineProps {
  status: RunStatus;
  result: PipelineResult | null;
  question: string;
  visibleSteps: number;
}

export function TraceTimeline({ status, result, question, visibleSteps }: TraceTimelineProps) {
  const [showJson, setShowJson] = useState(false);

  const nodes: ReactNode[] = [];

  if (result) {
    let step = 0;
    const next = () => {
      step += 1;
      return step;
    };

    nodes.push(
      <TraceNode key="query" n={next()} title="User Query Received">
        <div className="font-mono text-[11px] italic text-foreground-subtle">
          &ldquo;{truncate(question)}&rdquo;
        </div>
      </TraceNode>,
    );

    const routeDecision =
      result.route === "complex"
        ? "COMPLEX_RETRIEVAL"
        : result.route === "retrieve"
          ? "RETRIEVE"
          : "DIRECT";
    nodes.push(
      <TraceNode key="router" n={next()} title="Query Router">
        <div className="mt-1 rounded-md border border-border-strong bg-card p-2 text-[10px]">
          <div className="mb-1 flex justify-between text-foreground-subtle">
            <span>Decision:</span>
            <span className="text-accent">{routeDecision}</span>
          </div>
          <div className="flex justify-between text-foreground-faint">
            <span>Confidence:</span>
            <span className="font-mono">{result.routeConfidence.toFixed(2)}</span>
          </div>
        </div>
      </TraceNode>,
    );

    if (result.route !== "direct") {
      const topDoc = result.documents[0];
      nodes.push(
        <TraceNode key="retrieval" n={next()} title="Vector Retrieval">
          <div className="mt-1 space-y-2">
            {result.documents.length > 0 ? (
              <>
                <div className="flex flex-wrap gap-1.5">
                  {result.documents.map((doc) => (
                    <span
                      key={doc.metadata.source}
                      className="rounded border border-edge bg-raised px-1.5 py-0.5 font-mono text-[9px] text-foreground-subtle"
                    >
                      {doc.metadata.source}
                    </span>
                  ))}
                </div>
                {topDoc ? (
                  <div className="rounded border border-border-strong/50 bg-card/50 p-2 text-[10px] text-foreground-subtle">
                    <div className="mb-1 text-foreground">Top Context:</div>
                    <p className="leading-relaxed">&ldquo;{truncate(topDoc.content, 90)}&rdquo;</p>
                  </div>
                ) : null}
                <Collapsible label="View retrieved context">
                  <div className="space-y-2">
                    {result.documents.map((doc, index) => (
                      <div key={doc.metadata.source}>
                        <div className="mb-0.5 font-mono text-[9px] text-foreground-faint">
                          Document {index + 1}
                          {doc.metadata.file_type ? ` · ${doc.metadata.file_type}` : ""}
                        </div>
                        <pre className="overflow-x-auto whitespace-pre-wrap rounded border border-border-strong/50 bg-background/60 p-2 font-mono text-[10px] leading-relaxed text-foreground-subtle">
                          {doc.content}
                        </pre>
                      </div>
                    ))}
                  </div>
                </Collapsible>
              </>
            ) : (
              <div className="text-[10px] text-warning">No repository documents were retrieved.</div>
            )}
          </div>
        </TraceNode>,
      );

      const score = result.retrievalScore;
      const strong = score >= 0.75;
      nodes.push(
        <TraceNode key="grader" n={next()} title="Retrieval Grader">
          <div className="mt-1 flex items-center gap-2">
            <div className="h-1 flex-1 overflow-hidden rounded-full bg-raised">
              <div
                className={`h-full ${strong ? "bg-accent" : "bg-warning"}`}
                style={{ width: `${Math.round(score * 100)}%` }}
              />
            </div>
            <span className="font-mono text-[10px] text-foreground-subtle">{score.toFixed(2)}</span>
          </div>
          <div className={`mt-1 text-[10px] ${strong ? "text-accent" : "text-warning"}`}>
            {strong ? "Relevant context found" : "Low relevance — rewrite triggered"}
          </div>
        </TraceNode>,
      );

      if (result.retryCount > 0) {
        nodes.push(
          <TraceNode key="rewrite" n={next()} title="Query Rewrite / Retry">
            <div className="mt-1 text-[10px] text-warning">
              {result.retryCount} retrieval retry(s) performed.
            </div>
            {result.rewrittenQuery ? (
              <div className="mt-2">
                <Collapsible label="View rewritten query">
                  <div className="space-y-2">
                    <div>
                      <div className="mb-0.5 font-mono text-[9px] text-foreground-faint">Original</div>
                      <pre className="overflow-x-auto whitespace-pre-wrap rounded border border-border-strong/50 bg-background/60 p-2 font-mono text-[10px] text-foreground-subtle">
                        {question}
                      </pre>
                    </div>
                    <div>
                      <div className="mb-0.5 font-mono text-[9px] text-foreground-faint">Rewritten</div>
                      <pre className="overflow-x-auto whitespace-pre-wrap rounded border border-border-strong/50 bg-background/60 p-2 font-mono text-[10px] text-foreground-subtle">
                        {result.rewrittenQuery}
                      </pre>
                    </div>
                  </div>
                </Collapsible>
              </div>
            ) : null}
          </TraceNode>,
        );
      } else {
        nodes.push(
          <TraceNode key="rewrite" n={next()} title="Query Rewrite" dimmed>
            <div className="font-mono text-[10px] italic">SKIPPED: Confidence &gt; 0.85</div>
          </TraceNode>,
        );
      }

      if (result.webSearchUsed) {
        nodes.push(
          <TraceNode key="web" n={next()} title="Web Search">
            <div className="mt-1 text-[10px] text-accent">
              Triggered — {result.webDocuments.length} result(s).
            </div>
            {result.webDocuments.length > 0 ? (
              <div className="mt-2">
                <Collapsible label="View web sources">
                  <div className="space-y-2">
                    {result.webDocuments.map((doc, index) => (
                      <div
                        key={doc.title}
                        className="rounded border border-border-strong/50 bg-card/50 p-2"
                      >
                        <div className="text-[10px] font-medium text-foreground">
                          {index + 1}. {doc.title}
                        </div>
                        {doc.url ? (
                          <div className="mt-0.5 truncate font-mono text-[9px] text-foreground-faint">
                            {doc.url}
                          </div>
                        ) : null}
                        <p className="mt-1 text-[10px] leading-relaxed text-foreground-subtle">
                          {doc.content}
                        </p>
                      </div>
                    ))}
                  </div>
                </Collapsible>
              </div>
            ) : null}
          </TraceNode>,
        );
      } else {
        nodes.push(
          <TraceNode key="web" n={next()} title="Web Search">
            <div className="mt-1 text-[10px] text-foreground-faint">
              BYPASSED - LOCAL CONTEXT SUFFICIENT
            </div>
          </TraceNode>,
        );
      }
    } else {
      nodes.push(
        <TraceNode key="skipped" n={next()} title="Retrieval Pipeline" dimmed>
          <div className="font-mono text-[10px] italic">
            SKIPPED — router selected the DIRECT path.
          </div>
        </TraceNode>,
      );
    }

    nodes.push(
      <TraceNode key="generation" n={next()} title="Final Generation" active>
        <div className="text-[10px] text-foreground-subtle">
          Mistral-7B / Tokens: {result.tokens} / Temp: 0.1
        </div>
      </TraceNode>,
    );
  }

  const developerDetails = result
    ? JSON.stringify(
        {
          route: result.route,
          retrieval_score: result.retrievalScore,
          retry_count: result.retryCount,
          web_search_used: result.webSearchUsed,
          documents_retrieved: result.documents.length,
          web_documents_retrieved: result.webDocuments.length,
          rewritten_query: result.rewrittenQuery ?? null,
        },
        null,
        2,
      )
    : "";

  return (
    <div className="shrink-0 border-t border-border bg-card/20 p-6 xl:w-[420px] xl:overflow-y-auto xl:border-l xl:border-t-0">
      <div className="mb-8 flex items-center justify-between">
        <h3 className="text-xs font-medium uppercase tracking-[0.1em] text-foreground-subtle">
          Trace Timeline
        </h3>
        {result ? (
          <button
            type="button"
            onClick={() => setShowJson((value) => !value)}
            className="font-mono text-[10px] text-foreground-faint transition-colors hover:text-foreground-subtle"
          >
            {showJson ? "HIDE JSON" : "VIEW JSON"}
          </button>
        ) : null}
      </div>

      {!result ? (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="size-1.5 rounded-full bg-edge" />
          <p className="max-w-[28ch] text-[11px] leading-relaxed text-foreground-faint">
            Run a query to populate the execution trace step by step.
          </p>
        </div>
      ) : (
        <>
          <div className="relative ml-2 space-y-8">
            <div className="absolute left-[7px] top-2 bottom-2 w-px bg-border-strong" />
            {nodes.slice(0, visibleSteps)}
            {status === "running" && visibleSteps < nodes.length ? (
              <div className="relative pl-8">
                <div className="absolute left-0 top-1 flex size-3.5 items-center justify-center rounded-full border border-accent bg-background ring-4 ring-background">
                  <span className="size-1 animate-pulse-soft rounded-full bg-accent" />
                </div>
                <div className="font-mono text-[10px] text-foreground-faint">Awaiting next step...</div>
              </div>
            ) : null}
          </div>

          <div className="mt-12 border-t border-border-strong pt-6">
            <button
              type="button"
              onClick={() => setShowJson((value) => !value)}
              className="flex w-full cursor-pointer items-center justify-between font-mono text-[10px] uppercase tracking-widest text-foreground-subtle transition-colors hover:text-foreground"
            >
              <span>Raw Data Objects</span>
              <span className={`transition-transform ${showJson ? "rotate-180" : ""}`}>↓</span>
            </button>
            {showJson ? (
              <pre className="mt-4 animate-fade-in overflow-x-auto rounded bg-background/60 p-4 font-mono text-[10px] leading-relaxed text-foreground-faint">
                {developerDetails}
              </pre>
            ) : null}
          </div>
        </>
      )}
    </div>
  );
}
