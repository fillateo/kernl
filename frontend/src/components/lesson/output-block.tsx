import { CornerDownLeft } from "lucide-react";

export function OutputBlock({ text, label }: { text: string; label?: string }) {
  return (
    <div className="border-line bg-paper overflow-hidden rounded-2xl border">
      <div className="border-line/80 bg-cream/60 flex items-center justify-between border-b px-4 py-2.5">
        <span className="text-muted inline-flex items-center gap-2 font-mono text-[9px] tracking-[0.14em] uppercase">
          <CornerDownLeft className="size-3" />
          {label ?? "Command output"}
        </span>
        <span className="border-line bg-paper text-muted rounded-full border px-2 py-0.5 font-mono text-[8px] tracking-[0.12em] uppercase">
          stdout
        </span>
      </div>
      <pre className="text-ink/70 overflow-x-auto px-4 py-4 font-mono text-[11px] leading-6 sm:text-[12px]">
        <code>{text}</code>
      </pre>
    </div>
  );
}
