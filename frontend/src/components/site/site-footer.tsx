import { ArrowUpRight, CodeXml } from "lucide-react";
import Link from "next/link";

import { Logo } from "@/components/site/logo";

export function SiteFooter() {
  return (
    <footer className="border-line bg-cream border-t">
      <div className="container-page grid gap-10 py-12 md:grid-cols-[1.2fr_1fr_1fr]">
        <div className="max-w-sm">
          <Logo />
          <p className="text-muted mt-4 text-sm leading-6">
            Real Linux practice, without the setup. Built locally with Django, Channels,
            Next.js, and an honest-to-goodness terminal.
          </p>
          <span className="border-line-strong bg-paper text-muted mt-5 inline-flex items-center gap-2 rounded-full border px-3 py-1.5 font-mono text-[10px] tracking-[0.13em] uppercase">
            <span className="size-1.5 rounded-full bg-emerald-500" />
            No account required
          </span>
        </div>

        <div>
          <p className="eyebrow text-muted">Explore</p>
          <div className="mt-4 flex flex-col gap-3 text-sm">
            <Link href="/#courses" className="hover:text-violet w-fit">
              Course library
            </Link>
            <Link href="/courses/linux-foundations" className="hover:text-violet w-fit">
              Linux Foundations
            </Link>
            <Link href="/#how-it-works" className="hover:text-violet w-fit">
              How it works
            </Link>
          </div>
        </div>

        <div>
          <p className="eyebrow text-muted">Under the hood</p>
          <div className="text-muted mt-4 flex flex-col gap-3 text-sm">
            <span>Django + Channels</span>
            <span>Next.js + xterm.js</span>
            <span>bubblewrap sandbox</span>
            <a
              href="https://github.com"
              className="hover:text-violet inline-flex w-fit items-center gap-1.5"
              aria-label="Project source"
            >
              Source
              <CodeXml className="size-3.5" />
              <ArrowUpRight className="size-3" />
            </a>
          </div>
        </div>
      </div>
      <div className="border-line/70 border-t">
        <div className="container-page text-muted flex flex-col gap-2 py-5 text-[11px] sm:flex-row sm:items-center sm:justify-between">
          <span>© {new Date().getFullYear()} Kernl. A local-first learning lab.</span>
          <span className="font-mono tracking-[0.12em] uppercase">
            Learn by doing · reset by disconnecting
          </span>
        </div>
      </div>
    </footer>
  );
}
