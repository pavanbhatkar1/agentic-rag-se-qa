import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";

import { getStepCount, runPipeline, type PipelineResult } from "@/lib/agent";
import { Sidebar } from "@/components/console/Sidebar";
import { Composer } from "@/components/console/Composer";
import { AnswerPanel, type RunStatus } from "@/components/console/AnswerPanel";
import { TraceTimeline } from "@/components/console/TraceTimeline";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Agentic RAG — Software Engineering QA Console" },
      {
        name: "description",
        content:
          "Ask software engineering questions and watch an agent route, retrieve, grade, and reason its way to an answer — with a full execution trace of every step.",
      },
      { property: "og:title", content: "Agentic RAG — Software Engineering QA Console" },
      {
        property: "og:description",
        content:
          "An agentic RAG console: query routing, vector retrieval, relevance grading, query rewriting, and web-search fallback — visualized as a live execution trace.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
  component: Index,
});

interface RunState {
  status: RunStatus;
  result: PipelineResult | null;
  question: string;
  visibleSteps: number;
}

const IDLE: RunState = { status: "idle", result: null, question: "", visibleSteps: 0 };

function Index() {
  const [run, setRun] = useState<RunState>(IDLE);
  const [prefill, setPrefill] = useState<{ question: string; nonce: number } | null>(null);
  const timerRef = useRef<number | null>(null);

  useEffect(
    () => () => {
      if (timerRef.current !== null) window.clearInterval(timerRef.current);
    },
    [],
  );

  const startRun = async (question: string) => {
    if (timerRef.current !== null) window.clearInterval(timerRef.current);

    setRun({ status: "running", result: null, question, visibleSteps: 0 });

    try {
      const result = await runPipeline(question);
      const totalSteps = getStepCount(result);
      setRun({ status: "running", result, question, visibleSteps: 0 });

      let step = 0;
      timerRef.current = window.setInterval(() => {
        step += 1;
        const done = step > totalSteps;
        setRun((previous) => {
          if (previous.question !== question) return previous;
          return {
            ...previous,
            result,
            visibleSteps: Math.min(step, totalSteps),
            status: done ? "done" : "running",
          };
        });
        if (done && timerRef.current !== null) {
          window.clearInterval(timerRef.current);
          timerRef.current = null;
        }
      }, 300);
    } catch (error) {
      setRun((previous) => ({
        ...previous,
        status: "done",
        result: {
          route: "retrieve",
          routeConfidence: 0,
          retrievalScore: 0,
          retryCount: 0,
          webSearchUsed: false,
          documents: [],
          webDocuments: [],
          answer: {
            headline: "Backend request failed",
            paragraphs: [
              error instanceof Error ? error.message : "Could not reach the FastAPI backend.",
              "Make sure FastAPI is running on http://localhost:10000 and the frontend dev server is using the configured proxy.",
            ],
          },
          promptId: "ERROR",
          latencyMs: 0,
          tokens: 0,
        },
        visibleSteps: 0,
      }));
    }
  };

  const pickExample = (question: string) => {
    setPrefill({ question, nonce: Date.now() });
    startRun(question);
  };

  return (
    <div className="flex min-h-screen bg-background font-sans text-foreground xl:h-screen xl:overflow-hidden">
      <Sidebar />

      <main className="flex min-h-screen flex-1 flex-col xl:h-screen xl:overflow-hidden">
        <Composer onSubmit={startRun} running={run.status === "running"} externalValue={prefill} />

        <div className="flex flex-1 flex-col xl:overflow-hidden xl:flex-row">
          <AnswerPanel status={run.status} result={run.result} onPickExample={pickExample} />
          <TraceTimeline
            status={run.status}
            result={run.result}
            question={run.question}
            visibleSteps={run.visibleSteps}
          />
        </div>
      </main>
    </div>
  );
}
