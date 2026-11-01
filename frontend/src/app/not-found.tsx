import { ArrowRight, TerminalSquare } from "lucide-react";
import Link from "next/link";

import { Logo } from "@/components/site/logo";

export default function NotFound() {
  return (
    <div className="bg-cream flex min-h-dvh flex-col">
      <header className="border-line border-b">
        <div className="container-page flex h-16 items-center">
          <Logo />
        </div>
      </header>
      <main className="grid flex-1 place-items-center px-5 py-20">
        <div className="w-full max-w-xl text-center">
          <span className="border-line bg-paper text-violet shadow-float mx-auto grid size-14 place-items-center rounded-2xl border">
            <TerminalSquare className="size-6" />
          </span>
          <p className="eyebrow text-violet mt-6 justify-center">404 — not found</p>
          <h1 className="display mt-4 text-[clamp(2.6rem,6vw,4.5rem)] leading-[0.95] font-bold tracking-[-0.06em] text-balance">
            That command isn&apos;t in this sandbox.
          </h1>
          <p className="text-muted mx-auto mt-5 max-w-md text-sm leading-6">
            The lesson you followed does not exist. Open the workspace and start from
            the first prompt.
          </p>
          <div className="mt-8 flex justify-center">
            <Link href="/learn/your-first-repository" className="btn btn-dark">
              Open the lesson
              <ArrowRight className="size-4" />
            </Link>
          </div>
          <code className="text-muted mt-10 block font-mono text-[11px]">
            learner@kernl:~$ find /lesson -name &quot;this-one&quot;
            <br />
            <span className="text-coral">find: no such file or directory</span>
          </code>
        </div>
      </main>
    </div>
  );
}
