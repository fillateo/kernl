"use client";

import { Check, Copy, Play, TerminalSquare } from "lucide-react";
import { useState } from "react";

export function CommandBlock({
  command,
  label,
  onRun,
}: {
  command: string;
  label?: string;
  onRun: (command: string) => void;
}) {
  const [copied, setCopied] = useState(false);

  async function copyCommand() {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div className="group border-ink/10 bg-terminal relative overflow-hidden rounded-2xl border shadow-[0_14px_30px_-22px_rgb(23_23_44_/_0.8)]">
      <div className="border-terminal-line flex items-center justify-between gap-3 border-b px-4 py-2.5">
        <span className="text-terminal-muted inline-flex items-center gap-2 font-mono text-[9px] tracking-[0.14em] uppercase">
          <TerminalSquare className="text-lime/80 size-3" />
          {label ?? "Try this command"}
        </span>
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={copyCommand}
            className="text-terminal-muted hover:text-paper grid size-7 place-items-center rounded-md transition-colors hover:bg-white/5"
            aria-label={copied ? "Command copied" : "Copy command"}
            title={copied ? "Copied" : "Copy command"}
          >
            {copied ? (
              <Check className="text-lime size-3.5" />
            ) : (
              <Copy className="size-3.5" />
            )}
          </button>
          <button
            type="button"
            onClick={() => onRun(command)}
            className="border-lime/30 bg-lime/10 text-lime hover:bg-lime/20 inline-flex h-7 items-center gap-1.5 rounded-md border px-2.5 font-mono text-[9px] font-semibold tracking-[0.1em] uppercase transition-colors"
            title="Run this command in the terminal"
          >
            <Play className="size-3 fill-current" />
            Run
          </button>
        </div>
      </div>
      <pre className="overflow-x-auto px-5 py-4 font-mono text-[12px] leading-6 text-[#e7e7f5] sm:text-[13px]">
        <code>
          <span className="text-lime pr-2 select-none">$</span>
          {command}
        </code>
      </pre>
    </div>
  );
}
