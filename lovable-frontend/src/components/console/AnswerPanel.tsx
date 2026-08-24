import type { ReactNode } from "react";
import type { PipelineResult } from "@/lib/agent";

export type RunStatus = "idle" | "running" | "done";

function renderInline(text: string): ReactNode[] {
  return text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g).map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return (
        <strong key={index} className="font-semibold text-foreground-strong">
          {part.slice(2, -2)}
        </strong>
      );
    }

    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={index}
          className="rounded border border-border-strong bg-card px-1.5 py-0.5 font-mono text-[0.9em] text-accent"
        >
          {part.slice(1, -1)}
        </code>
      );
    }

    return <span key={index}>{part}</span>;
  });
}

function renderMarkdown(text: string): ReactNode[] {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const blocks: ReactNode[] = [];
  let paragraph: string[] = [];
  let codeLines: string[] = [];
  let codeLanguage = "";
  let inCode = false;

  const flushParagraph = () => {
    const content = paragraph.join(" ").trim();
    if (content) {
      blocks.push(
        <p key={`p-${blocks.length}`} className="text-pretty">
          {renderInline(content)}
        </p>,
      );
    }
    paragraph = [];
  };

  const flushCode = () => {
    blocks.push(
      <pre
        key={`code-${blocks.length}`}
        className="overflow-x-auto rounded-lg border border-border-strong bg-card px-4 py-3 font-mono text-[13px] leading-6 text-foreground"
      >
        <code data-language={codeLanguage || undefined}>{codeLines.join("\n")}</code>
      </pre>,
    );
    codeLines = [];
    codeLanguage = "";
  };

  lines.forEach((line) => {
    const fence = line.match(/^\s*```(\w+)?\s*$/);

    if (fence) {
      if (inCode) {
        flushCode();
        inCode = false;
      } else {
        flushParagraph();
        inCode = true;
        codeLanguage = fence[1] || "";
      }
      return;
    }

    if (inCode) {
      codeLines.push(line);
      return;
    }

    if (!line.trim()) {
      flushParagraph();
      return;
    }

    paragraph.push(line.trim());
  });

  if (inCode) flushCode();
  flushParagraph();

  return blocks;
}

function Metric({ label, value, tone }: { label: string; value: string; tone?: "accent" | "faint" | undefined }) {
  return (
    <div className="flex min-w-[90px] flex-col gap-1">
      <span className="text-[10px] uppercase tracking-wider text-foreground-faint">{label}</span>
      <span
        className={`font-mono text-xs ${
          tone === "accent"
            ? "text-accent"
            : tone === "faint"
              ? "text-foreground-faint"
              : "text-foreground-subtle"
        }`}
      >
        {value}
      </span>
    </div>
  );
}

const EXAMPLES = [
  "Explain the architecture of this project and how the RAG workflow works.",
  "How is the QueryRouter class implemented in this project?",
  "How does FastAPI define an API route?",
];

interface AnswerPanelProps {
  status: RunStatus;
  result: PipelineResult | null;
  onPickExample: (question: string) => void;
}

export function AnswerPanel({ status, result, onPickExample }: AnswerPanelProps) {
  if (status === "idle" || !result) {
    return (
      <div className="flex flex-1 flex-col overflow-y-visible p-6 sm:p-8 xl:overflow-y-auto xl:border-r xl:border-border">
        <div className="m-auto flex max-w-md flex-col items-center text-center">
          <div className="mb-4 size-2 rounded-full bg-edge" />
          <h2 className="text-lg font-medium text-foreground-strong">Ask the agent a question</h2>
          <p className="mt-2 text-sm leading-relaxed text-foreground-subtle">
            The agent routes your question, retrieves repository context, grades relevance,
            and generates an answer with a live execution trace.
          </p>
          <div className="mt-8 flex flex-col items-stretch gap-2">
            {EXAMPLES.map((example) => (
              <button
                key={example}
                type="button"
                onClick={() => onPickExample(example)}
                className="rounded-lg border border-border-strong bg-card/50 px-4 py-2.5 text-left font-mono text-[11px] text-foreground-subtle transition-colors hover:border-edge hover:text-foreground"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (status === "running") {
    return (
      <div className="flex flex-1 flex-col overflow-y-visible p-6 sm:p-8 xl:overflow-y-auto xl:border-r xl:border-border">
        <div className="m-auto flex items-center gap-3 text-foreground-subtle">
          <span className="size-2 animate-pulse-soft rounded-full bg-accent" />
          <span className="font-mono text-xs">Agent is routing, retrieving and reasoning...</span>
        </div>
      </div>
    );
  }

  const { answer } = result;
  const routeLabel =
    result.route === "complex"
      ? "Vector > Multi_Node"
      : result.route === "retrieve"
        ? "Vector > Single_Pass"
        : "Direct > LLM";

  return (
    <div className="flex-1 overflow-y-visible p-6 sm:p-8 xl:overflow-y-auto xl:border-r xl:border-border">
      <div className="mx-auto max-w-[72ch] animate-fade-in">
        <div className="mb-6 flex flex-wrap items-center gap-3">
          <span className="rounded border border-border-strong bg-card px-2 py-0.5 font-mono text-[10px] text-foreground-subtle">
            PROMPT_ID: {result.promptId}
          </span>
          <span className="font-mono text-[10px] text-foreground-subtle">
            LATENCY: {(result.latencyMs / 1000).toFixed(2)}s
          </span>
        </div>

        <div className="mb-6 border-l-2 border-accent pl-4">
          <div className="mb-1 text-[10px] font-medium uppercase tracking-[0.16em] text-accent">
            Answer
          </div>
          <h1 className="text-balance text-xl font-semibold leading-snug text-foreground-strong sm:text-2xl">
            {answer.headline}
          </h1>
        </div>

        <div className="space-y-4 text-[15px] leading-7 text-foreground">
          {answer.paragraphs.map((paragraph, index) => (
            <div key={index} className="space-y-3 text-pretty">
              {renderMarkdown(paragraph)}
            </div>
          ))}
          {answer.bullets ? (
            <ul className="space-y-3 border-l border-border-strong pl-5 pt-2">
              {answer.bullets.map((bullet) => (
                <li key={bullet.title} className="text-sm leading-6">
                  <span className="mb-1 block font-medium text-foreground-strong">{bullet.title}</span>
                  {renderMarkdown(bullet.body)}
                </li>
              ))}
            </ul>
          ) : null}
        </div>

        <div className="mt-10 grid grid-cols-2 gap-5 border-t border-border py-4 sm:grid-cols-4">
          <Metric label="Routing Path" value={routeLabel} />
          <Metric label="Documents" value={`${result.documents.length} Retrieved`} />
          <Metric
            label="Retries"
            value={result.retryCount === 0 ? "0 (Optimal)" : `${result.retryCount} (Rewritten)`}
            tone={result.retryCount === 0 ? "accent" : undefined}
          />
          <Metric
            label="Web Search"
            value={result.webSearchUsed ? "TRIGGERED" : "SKIPPED"}
            tone={result.webSearchUsed ? undefined : "faint"}
          />
        </div>
      </div>
    </div>
  );
}
