import { ArrowLeft, Command, Terminal } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";

import { TerminalPanel } from "@/components/lesson/terminal-panel";
import { AppHeader } from "@/components/site/app-header";

export const metadata: Metadata = {
  title: "Terminal playground",
  description: "A free local Linux sandbox with no lesson attached.",
};

const QUICK_COMMANDS = [
  { command: "pwd", note: "see where you are" },
  { command: "ls -la", note: "list everything" },
  { command: "echo hello", note: "make output" },
  { command: "mkdir notes", note: "create a directory" },
];

export default function PlaygroundPage() {
  return (
    <div className="bg-cream flex min-h-dvh flex-col">
      <AppHeader title="Terminal playground" />
      <main className="grid flex-1 lg:h-[calc(100dvh-4rem)] lg:grid-cols-[360px_minmax(0,1fr)]">
        <aside className="border-line bg-cream/70 flex flex-col border-r p-6 lg:p-8">
          <span className="eyebrow text-violet">
            <Terminal className="size-3.5" />
            Free practice
          </span>
          <h1 className="display mt-4 text-[36px] leading-[0.98] font-bold tracking-[-0.055em]">
            Terminal playground
          </h1>
          <p className="text-muted mt-4 text-[13px] leading-6">
            A clean sandbox with no lesson attached. Use it to practice the commands you
            have learned, or break something without consequences.
          </p>

          <div className="border-line bg-paper mt-7 rounded-2xl border p-4">
            <p className="eyebrow text-muted">Starting points</p>
            <ul className="mt-3 space-y-2.5">
              {QUICK_COMMANDS.map((item) => (
                <li
                  key={item.command}
                  className="flex items-center justify-between gap-3"
                >
                  <code className="text-ink bg-ink/5 rounded px-2 py-1 font-mono text-[10px]">
                    {item.command}
                  </code>
                  <span className="text-muted text-right text-[10px]">{item.note}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-auto space-y-3 pt-8">
            <Link
              href="/"
              className="text-muted hover:text-ink inline-flex items-center gap-2 text-[11px] font-medium"
            >
              <ArrowLeft className="size-3.5" />
              Back to Git Essentials
            </Link>
            <div className="text-muted flex items-center gap-2 font-mono text-[9px] tracking-[0.12em] uppercase">
              <Command className="size-3" />
              ephemeral · no network
            </div>
          </div>
        </aside>

        <div className="h-[70vh] min-h-[480px] lg:h-full lg:min-h-0">
          <TerminalPanel className="h-full" />
        </div>
      </main>
    </div>
  );
}
