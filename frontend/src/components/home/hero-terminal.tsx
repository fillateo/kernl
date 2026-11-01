import { Check, ShieldCheck } from "lucide-react";

const SCREEN_LINES = [
  { prompt: true, text: "ls" },
  { prompt: false, text: "README.md   projects   welcome.txt" },
  { prompt: true, text: 'echo "Hello world"' },
  { prompt: false, text: "Hello world" },
  { prompt: true, text: "pwd" },
  { prompt: false, text: "/home/learner" },
];

export function HeroTerminal() {
  return (
    <div className="relative mx-auto w-full max-w-[560px] lg:mr-0">
      <div
        className="bg-lime/50 absolute -inset-8 rounded-[38px] blur-2xl"
        aria-hidden
      />
      <div
        className="border-terminal-line bg-terminal relative rounded-[24px] border p-2 shadow-[0_35px_90px_-30px_rgb(23_23_44_/_0.65)]"
        aria-hidden="true"
      >
        <div className="border-terminal-line flex items-center gap-2 border-b px-3 py-2.5">
          <span className="size-2.5 rounded-full bg-[#ff6b5f]" />
          <span className="size-2.5 rounded-full bg-[#ffc857]" />
          <span className="size-2.5 rounded-full bg-[#6ee7a8]" />
          <span className="text-terminal-muted ml-3 font-mono text-[10px] tracking-wide">
            learner@kernl — bash
          </span>
          <span className="border-terminal-line text-terminal-muted ml-auto rounded-full border px-2 py-0.5 font-mono text-[8px] tracking-[0.12em] uppercase">
            sandbox
          </span>
        </div>

        <div className="px-5 pt-5 pb-9 font-mono text-[12.5px] leading-[2] text-[#e7e7f5] sm:text-[13px]">
          {SCREEN_LINES.map((line, index) => (
            <div key={`${line.text}-${index}`} className="whitespace-pre">
              {line.prompt ? (
                <>
                  <span className="text-lime">learner</span>
                  <span className="text-terminal-muted">@</span>
                  <span className="text-[#9ad9ff]">kernl</span>
                  <span className="text-terminal-muted">:</span>
                  <span className="text-[#ffd479]">~</span>
                  <span className="text-terminal-muted">$ </span>
                  <span>{line.text}</span>
                </>
              ) : (
                <span className="text-[#a9aac5]">{line.text}</span>
              )}
            </div>
          ))}
          <div className="whitespace-pre">
            <span className="text-lime">learner</span>
            <span className="text-terminal-muted">@</span>
            <span className="text-[#9ad9ff]">kernl</span>
            <span className="text-terminal-muted">:</span>
            <span className="text-[#ffd479]">~</span>
            <span className="text-terminal-muted">$ </span>
            <span className="animate-blink bg-lime inline-block h-[15px] w-[7px] translate-y-[2px]" />
          </div>
        </div>

        <div className="border-terminal-line text-terminal-muted flex items-center justify-between border-t px-4 py-2.5 font-mono text-[9px] tracking-[0.12em] uppercase">
          <span>UTF-8</span>
          <span className="flex items-center gap-1.5">
            <span className="size-1.5 rounded-full bg-emerald-400" />
            ephemeral session
          </span>
        </div>
      </div>

      <div className="border-line bg-paper shadow-float absolute top-16 -right-3 flex rotate-2 items-center gap-2 rounded-xl border px-3.5 py-2.5 sm:-right-8">
        <span className="grid size-7 place-items-center rounded-full bg-emerald-100 text-emerald-700">
          <Check className="size-4" strokeWidth={3} />
        </span>
        <div>
          <p className="text-[10px] leading-tight font-semibold">Command passed</p>
          <p className="text-muted font-mono text-[8px] tracking-[0.1em] uppercase">
            lesson 01 · ls
          </p>
        </div>
      </div>

      <div className="border-line bg-paper shadow-float absolute -bottom-5 left-3 flex -rotate-1 items-center gap-2 rounded-xl border px-3.5 py-2.5 sm:-left-6">
        <ShieldCheck className="text-violet size-4" />
        <div>
          <p className="text-[10px] leading-tight font-semibold">Isolated shell</p>
          <p className="text-muted font-mono text-[8px] tracking-[0.1em] uppercase">
            no network · resets on exit
          </p>
        </div>
      </div>
    </div>
  );
}
