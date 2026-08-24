function StatusRow({
  label,
  state,
  live = true,
}: {
  label: string;
  state?: string;
  live?: boolean;
}) {
  return (
    <div className="flex items-center gap-3">
      <div
        className={`size-1.5 rounded-full ${
          live
            ? "bg-accent shadow-[0_0_8px_color-mix(in_oklab,var(--accent)_40%,transparent)]"
            : "bg-edge"
        }`}
      />
      <span className={`text-sm font-medium ${live ? "text-foreground-strong" : "text-foreground-subtle"}`}>
        {label}
      </span>
      {state ? (
        <span className={`ml-auto font-mono text-[10px] ${live ? "text-foreground-subtle" : "text-foreground-faint"}`}>
          {state}
        </span>
      ) : null}
    </div>
  );
}

function ConfigCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-card/50 p-3 ring-1 ring-background/50">
      <div className="mb-1 font-mono text-[10px] uppercase text-foreground-subtle">{label}</div>
      <div className="text-sm font-medium text-foreground-strong">{value}</div>
    </div>
  );
}

export function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col gap-8 border-r border-border p-6 lg:flex">
      <div>
        <div className="text-sm font-semibold tracking-tight text-foreground-strong">Agentic RAG</div>
        <div className="mt-0.5 text-[11px] text-foreground-subtle">Software Engineering QA</div>
      </div>

      <div>
        <h2 className="mb-4 text-[10px] font-medium uppercase tracking-[0.2em] text-foreground-subtle">
          System Architecture
        </h2>
        <div className="space-y-3">
          <StatusRow label="Agent Engine" state="READY" />
          <StatusRow label="FastAPI Gateway" />
          <StatusRow label="Qdrant Cluster" />
          <StatusRow label="Ollama Instance" state="IDLE" live={false} />
        </div>
      </div>

      <div>
        <h2 className="mb-4 text-[10px] font-medium uppercase tracking-[0.2em] text-foreground-subtle">
          Configuration
        </h2>
        <div className="space-y-4">
          <ConfigCard label="Model" value="Mistral 7B Instruct" />
          <ConfigCard label="Retriever" value="Dense Vector / HNSW" />
        </div>
      </div>

      <p className="mt-auto text-[11px] leading-relaxed text-foreground-faint">
        Routes questions, retrieves repository context, evaluates relevance, and falls back to web
        search when needed.
      </p>
    </aside>
  );
}
