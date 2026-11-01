import { Circle } from "lucide-react";

import { Logo } from "@/components/site/logo";

export function AppHeader({ courseTitle }: { courseTitle: string }) {
  return (
    <header className="border-line/80 bg-cream/90 sticky top-0 z-50 border-b backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between gap-4 px-4 md:px-6">
        <div className="flex min-w-0 items-center gap-4">
          <Logo />
          <span className="bg-line-strong hidden h-5 w-px sm:block" />
          <div className="hidden min-w-0 items-center gap-2 sm:flex">
            <span className="eyebrow text-muted text-[10px]!">Learning workspace</span>
            <span className="border-line-strong bg-paper text-ink max-w-[220px] truncate rounded-full border px-2.5 py-1 font-mono text-[10px] font-medium">
              {courseTitle}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-muted hidden items-center gap-1.5 font-mono text-[10px] tracking-[0.14em] uppercase lg:inline-flex">
            <Circle
              className="size-2 fill-emerald-500 text-emerald-500"
              strokeWidth={0}
            />
            Local workspace
          </span>
        </div>
      </div>
    </header>
  );
}
