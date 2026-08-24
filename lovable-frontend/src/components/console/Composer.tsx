import { useState } from "react";

interface ComposerProps {
  onSubmit: (question: string) => void;
  running: boolean;
  externalValue?: { question: string; nonce: number } | null;
}

export function Composer({ onSubmit, running, externalValue }: ComposerProps) {
  const [value, setValue] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [lastNonce, setLastNonce] = useState(0);

  if (externalValue && externalValue.nonce !== lastNonce) {
    setLastNonce(externalValue.nonce);
    setValue(externalValue.question);
    setError(null);
  }

  const submit = () => {
    const question = value.trim();
    if (!question) {
      setError("Please enter a question.");
      return;
    }
    if (running) return;
    setError(null);
    onSubmit(question);
  };

  return (
    <div className="sticky top-0 z-20 border-b border-border bg-background/60 p-4 backdrop-blur-sm sm:p-8">
      <div className="mx-auto w-full max-w-5xl">
        <div className="relative flex items-center">
          <input
            type="text"
            value={value}
            onChange={(event) => {
              setValue(event.target.value);
              if (error) setError(null);
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter") submit();
            }}
            placeholder="e.g. How does FastAPI define an API route?"
            aria-label="Ask a question"
            className="w-full rounded-xl border border-border-strong bg-card py-4 pl-5 pr-32 text-foreground transition-all placeholder:text-foreground-faint focus:outline-none focus:ring-2 focus:ring-ring/20"
          />
          <button
            type="button"
            onClick={submit}
            disabled={running}
            className="absolute right-2 top-2 bottom-2 rounded-lg bg-primary px-5 text-sm font-medium text-primary-foreground ring-1 ring-accent transition-transform hover:bg-accent active:scale-95 disabled:cursor-not-allowed disabled:opacity-70 disabled:active:scale-100"
          >
            {running ? (
              <span className="flex items-center gap-2">
                <span className="size-1.5 animate-pulse-soft rounded-full bg-primary-foreground" />
                Analyzing
              </span>
            ) : (
              "Analyze"
            )}
          </button>
        </div>
        {error ? <p className="mt-3 font-mono text-[11px] text-warning">{error}</p> : null}
      </div>
    </div>
  );
}
