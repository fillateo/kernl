"use client";

import { RefreshCw, ServerCrash } from "lucide-react";
import Link from "next/link";
import { useEffect } from "react";

import { Logo } from "@/components/site/logo";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="bg-cream flex min-h-dvh flex-col">
      <header className="border-line border-b">
        <div className="container-page flex h-16 items-center">
          <Logo />
        </div>
      </header>
      <main className="grid flex-1 place-items-center px-5 py-20">
        <div className="w-full max-w-xl text-center">
          <span className="border-line bg-paper text-coral shadow-float mx-auto grid size-14 place-items-center rounded-2xl border">
            <ServerCrash className="size-6" />
          </span>
          <p className="eyebrow text-coral mt-6 justify-center">
            Connection interrupted
          </p>
          <h1 className="display mt-4 text-[clamp(2.6rem,6vw,4.5rem)] leading-[0.95] font-bold tracking-[-0.06em] text-balance">
            The lesson couldn&apos;t reach the server.
          </h1>
          <p className="text-muted mx-auto mt-5 max-w-md text-sm leading-6">
            Check that the Django API is running on port 8000, then try the request
            again. Your sandbox is safe.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <button type="button" onClick={reset} className="btn btn-dark">
              <RefreshCw className="size-4" />
              Try again
            </button>
            <Link href="/" className="btn btn-outline">
              Back home
            </Link>
          </div>
          <code className="text-muted mt-10 block font-mono text-[11px]">
            learner@kernl:~$ curl -s localhost:8000/api/health/
            <br />
            <span className="text-coral">connection refused</span>
          </code>
        </div>
      </main>
    </div>
  );
}
