"use client";

import { ArrowUpRight, Menu, ShieldCheck, X } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { Logo } from "@/components/site/logo";

const NAV_ITEMS = [
  { label: "Courses", href: "/#courses" },
  { label: "How it works", href: "/#how-it-works" },
  { label: "Why local", href: "/#local-first" },
];

export function SiteHeader() {
  const [open, setOpen] = useState(false);

  return (
    <header className="border-line/80 bg-cream/85 sticky top-0 z-50 border-b backdrop-blur-xl">
      <div className="container-page flex h-16 items-center justify-between gap-6">
        <div className="flex items-center gap-9">
          <Logo onClick={() => setOpen(false)} />
          <nav className="hidden items-center gap-7 md:flex" aria-label="Primary">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-muted hover:text-ink text-[13px] font-medium transition-colors"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-muted hidden items-center gap-1.5 text-[11px] font-medium lg:inline-flex">
            <ShieldCheck className="size-3.5 text-emerald-600" strokeWidth={2} />
            Local sandbox
          </span>
          <Link
            href="/courses/linux-foundations"
            className="btn btn-dark hidden px-4! py-2.5! text-[13px] sm:inline-flex"
          >
            Start learning
            <ArrowUpRight className="size-3.5" />
          </Link>
          <button
            type="button"
            onClick={() => setOpen((value) => !value)}
            className="border-line-strong text-ink grid size-10 place-items-center rounded-full border md:hidden"
            aria-label={open ? "Close navigation" : "Open navigation"}
            aria-expanded={open}
          >
            {open ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>
        </div>
      </div>

      {open && (
        <div className="border-line bg-paper border-t md:hidden">
          <nav
            className="container-page flex flex-col py-3"
            aria-label="Mobile navigation"
          >
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="border-line/60 border-b py-3 text-sm font-medium last:border-0"
              >
                {item.label}
              </Link>
            ))}
            <Link
              href="/courses/linux-foundations"
              onClick={() => setOpen(false)}
              className="btn btn-dark mt-3"
            >
              Start learning
              <ArrowUpRight className="size-4" />
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
