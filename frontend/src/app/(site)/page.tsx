import {
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  Check,
  CircleDot,
  Clock3,
  Keyboard,
  LockKeyhole,
  Play,
  ShieldCheck,
  Sparkles,
  Terminal,
  WifiOff,
} from "lucide-react";
import Link from "next/link";

import { CourseCard } from "@/components/course/course-card";
import { HeroTerminal } from "@/components/home/hero-terminal";
import { getCourses } from "@/lib/api";

export const dynamic = "force-dynamic";

const MARQUEE_COMMANDS = [
  "pwd",
  "ls -la",
  "mkdir practice",
  "grep ERROR logs/app.log",
  "chmod +x deploy.sh",
  "git commit -m",
  "echo $?",
  "cd ..",
  "cat README.md",
  "find . -type f",
  "git switch -c",
];

const STEPS = [
  {
    number: "01",
    title: "Pick a track",
    body: "Start with Linux, sharpen your Git workflow, or turn commands into reusable bash scripts.",
    icon: BookOpen,
    accent: "bg-lime",
  },
  {
    number: "02",
    title: "Read, then run",
    body: "Every lesson pairs a short explanation with a command you can send straight into the live terminal.",
    icon: Play,
    accent: "bg-violet text-white",
  },
  {
    number: "03",
    title: "Break things",
    body: "Your sandbox is disposable. Experiment freely, make mistakes, and open a fresh shell whenever you want.",
    icon: Terminal,
    accent: "bg-coral",
  },
];

export default async function HomePage() {
  const courses = await getCourses();
  const totalLessons = courses.reduce(
    (total, course) => total + course.lesson_count,
    0,
  );

  return (
    <>
      <section className="border-line relative overflow-hidden border-b">
        <div
          className="bg-grid pointer-events-none absolute inset-0 [mask-image:linear-gradient(to_bottom,black,transparent_82%)] opacity-70"
          aria-hidden
        />
        <div
          className="bg-lime/35 pointer-events-none absolute top-0 -right-40 size-[600px] rounded-full blur-3xl"
          aria-hidden
        />
        <div className="container-page relative grid items-center gap-16 pt-16 pb-24 lg:grid-cols-[1.04fr_0.96fr] lg:gap-12 lg:pt-24 lg:pb-28">
          <div className="animate-rise">
            <div className="border-line-strong bg-paper inline-flex items-center gap-2 rounded-full border px-3 py-1.5 shadow-sm">
              <Sparkles className="text-violet size-3.5" />
              <span className="eyebrow text-ink text-[10px]!">
                Browser-based Linux labs
              </span>
              <span className="bg-lime rounded-full px-2 py-0.5 font-mono text-[9px] font-semibold tracking-[0.1em] uppercase">
                local
              </span>
            </div>

            <h1 className="display mt-7 max-w-[650px] text-[clamp(3.15rem,6vw,5.35rem)] leading-[0.94] font-bold tracking-[-0.065em] text-balance">
              Learn the terminal
              <br />
              by{" "}
              <span className="relative inline-block">
                actually
                <svg
                  className="text-lime absolute -bottom-2 left-0 h-3 w-full"
                  viewBox="0 0 260 12"
                  fill="none"
                  preserveAspectRatio="none"
                  aria-hidden
                >
                  <path
                    d="M2 8.5C63 2.5 191 2.5 258 7"
                    stroke="currentColor"
                    strokeWidth="7"
                    strokeLinecap="round"
                  />
                </svg>
              </span>{" "}
              using it.
            </h1>

            <p className="text-muted mt-8 max-w-[500px] text-[16px] leading-7 text-pretty sm:text-[17px]">
              Real Linux. Real commands. A private sandbox that starts in your browser
              and disappears when you leave. No installs, no accounts, no cloud shell.
            </p>

            <div className="mt-9 flex flex-wrap items-center gap-3">
              <Link
                href="/courses/linux-foundations"
                className="btn btn-dark px-6! py-3.5!"
              >
                Start with Linux
                <ArrowRight className="size-4" />
              </Link>
              <Link href="#courses" className="btn btn-outline px-5! py-3.5!">
                Browse all tracks
                <ArrowUpRight className="size-4" />
              </Link>
            </div>

            <div className="text-muted mt-10 flex flex-wrap items-center gap-x-7 gap-y-3 text-[11px] font-medium">
              <span className="inline-flex items-center gap-1.5">
                <Check className="size-3.5 text-emerald-600" strokeWidth={3} />
                No sign-up
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Check className="size-3.5 text-emerald-600" strokeWidth={3} />
                No local setup
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Check className="size-3.5 text-emerald-600" strokeWidth={3} />
                Resets on disconnect
              </span>
            </div>
          </div>

          <div className="animate-rise [animation-delay:120ms]">
            <HeroTerminal />
          </div>
        </div>

        <div className="container-page relative pb-12">
          <dl className="divide-line border-line grid divide-y border-y sm:grid-cols-3 sm:divide-x sm:divide-y-0">
            {[
              { value: String(totalLessons), label: "guided lessons" },
              { value: String(courses.length), label: "focused tracks" },
              { value: "0", label: "accounts required" },
            ].map((stat) => (
              <div key={stat.label} className="px-1 py-5 sm:px-7 sm:py-6">
                <dt className="font-display text-[32px] leading-none font-bold tracking-[-0.05em]">
                  {stat.value}
                  <span className="text-coral">.</span>
                </dt>
                <dd className="text-muted mt-1.5 font-mono text-[10px] tracking-[0.15em] uppercase">
                  {stat.label}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      <div className="border-ink bg-ink text-lime overflow-hidden border-b py-3.5">
        <div className="animate-marquee flex w-max items-center">
          {[0, 1].map((copy) => (
            <div
              key={copy}
              className="flex shrink-0 items-center"
              aria-hidden={copy === 1}
            >
              {MARQUEE_COMMANDS.map((command) => (
                <span
                  key={`${copy}-${command}`}
                  className="flex items-center font-mono text-[11px] tracking-tight sm:text-xs"
                >
                  <span className="text-lime/70 px-5">$</span>
                  {command}
                  <span className="text-coral px-5">✦</span>
                </span>
              ))}
            </div>
          ))}
        </div>
      </div>

      <section id="courses" className="relative scroll-mt-20 py-20 md:py-28">
        <div className="container-page">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">
            <div>
              <span className="eyebrow text-violet">
                <span className="bg-violet size-1.5 rounded-full" />
                01 — The tracks
              </span>
              <h2 className="display mt-4 max-w-[620px] text-[clamp(2.4rem,4vw,3.65rem)] leading-[0.98] font-bold tracking-[-0.055em] text-balance">
                Pick a path. Start typing.
              </h2>
            </div>
            <p className="text-muted max-w-[330px] text-sm leading-6 text-pretty">
              Short, deliberate lessons. Each one ends with a command in your hands and
              a filesystem you cannot permanently break.
            </p>
          </div>

          <div className="mt-12 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {courses.map((course, index) => (
              <CourseCard key={course.slug} course={course} index={index} />
            ))}
          </div>

          {courses.length === 0 && (
            <div className="border-line-strong bg-paper mt-12 rounded-2xl border border-dashed p-10 text-center">
              <p className="font-medium">The catalog is empty.</p>
              <p className="text-muted mt-2 text-sm">
                Run{" "}
                <code className="bg-ink/5 rounded px-1.5 py-0.5 font-mono text-xs">
                  python manage.py seed_catalog
                </code>{" "}
                to load the local course content.
              </p>
            </div>
          )}
        </div>
      </section>

      <section
        id="how-it-works"
        className="border-line bg-paper scroll-mt-20 border-y py-20 md:py-28"
      >
        <div className="container-page">
          <div className="max-w-[650px]">
            <span className="eyebrow text-coral">
              <span className="bg-coral size-1.5 rounded-full" />
              02 — How it works
            </span>
            <h2 className="display mt-4 text-[clamp(2.4rem,4vw,3.65rem)] leading-[0.98] font-bold tracking-[-0.055em] text-balance">
              A lesson, a shell, and nowhere to hide.
            </h2>
            <p className="text-muted mt-5 max-w-[520px] text-sm leading-6 text-pretty">
              There is no video to watch passively. You read a little, run the exact
              command from the lesson, and see real output immediately.
            </p>
          </div>

          <div className="relative mt-14 grid gap-5 md:grid-cols-3">
            <div
              className="border-line-strong absolute top-12 right-[16%] left-[16%] hidden border-t border-dashed md:block"
              aria-hidden
            />
            {STEPS.map((step) => (
              <div
                key={step.number}
                className="border-line bg-cream hover:border-ink/20 hover:shadow-float relative rounded-[24px] border p-6 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex items-center justify-between">
                  <span
                    className={`grid size-11 place-items-center rounded-2xl ${step.accent}`}
                  >
                    <step.icon className="size-5" strokeWidth={1.8} />
                  </span>
                  <span className="text-muted font-mono text-[10px] font-medium tracking-[0.14em]">
                    {step.number}
                  </span>
                </div>
                <h3 className="display mt-9 text-[23px] font-bold tracking-[-0.04em]">
                  {step.title}
                </h3>
                <p className="text-muted mt-2.5 text-[13px] leading-6">{step.body}</p>
              </div>
            ))}
          </div>

          <div className="border-line bg-cream mt-10 flex flex-wrap items-center gap-3 rounded-2xl border px-5 py-4">
            <Keyboard className="text-violet size-4" />
            <p className="text-muted text-[12px]">
              Built for keyboards. Tab completion, arrow-key history, and every prompt
              is a real bash process.
            </p>
            <span className="ml-auto hidden items-center gap-1.5 font-mono text-[10px] tracking-[0.12em] text-emerald-700 uppercase sm:inline-flex">
              <CircleDot className="size-3" />
              xterm.js
            </span>
          </div>
        </div>
      </section>

      <section
        id="local-first"
        className="bg-terminal text-paper relative scroll-mt-20 overflow-hidden py-20 md:py-28"
      >
        <div className="bg-grid absolute inset-0 opacity-[0.07]" aria-hidden />
        <div
          className="bg-violet/20 absolute top-20 -left-40 size-[480px] rounded-full blur-3xl"
          aria-hidden
        />
        <div className="container-page relative grid gap-14 lg:grid-cols-[1fr_0.9fr] lg:items-center">
          <div>
            <span className="eyebrow text-lime">
              <span className="bg-lime size-1.5 rounded-full" />
              03 — Local by design
            </span>
            <h2 className="display text-paper mt-4 max-w-[620px] text-[clamp(2.4rem,4vw,3.65rem)] leading-[0.98] font-bold tracking-[-0.055em] text-balance">
              Your own private Linux box.
              <span className="text-terminal-muted"> Actually local.</span>
            </h2>
            <p className="text-terminal-muted mt-6 max-w-[500px] text-sm leading-6 text-pretty">
              The terminal is a real bash process inside a bubblewrap sandbox, not a
              shell emulator and not somebody else&apos;s cloud. No AWS, no remote shell
              service, no secret infrastructure.
            </p>

            <div className="mt-9 grid gap-3 sm:grid-cols-2">
              {[
                {
                  icon: ShieldCheck,
                  title: "Kernel-level isolation",
                  body: "Private PID, network, and mount namespaces.",
                },
                {
                  icon: WifiOff,
                  title: "No network inside",
                  body: "Network access is unshared, full stop.",
                },
                {
                  icon: LockKeyhole,
                  title: "Read-only system",
                  body: "Only /home/learner can be written.",
                },
                {
                  icon: Clock3,
                  title: "Disposable by default",
                  body: "Every session gets a fresh filesystem.",
                },
              ].map((item) => (
                <div
                  key={item.title}
                  className="border-terminal-line rounded-2xl border bg-white/[0.035] p-4"
                >
                  <item.icon className="text-lime size-4" />
                  <p className="text-paper mt-3 text-[12px] font-semibold">
                    {item.title}
                  </p>
                  <p className="text-terminal-muted mt-1 text-[11px] leading-5">
                    {item.body}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div
              className="bg-lime/10 absolute -inset-4 rounded-[32px] blur-2xl"
              aria-hidden
            />
            <div className="border-terminal-line relative overflow-hidden rounded-[22px] border bg-[#101124]">
              <div className="border-terminal-line flex items-center gap-2 border-b px-4 py-3">
                <span className="bg-coral size-2 rounded-full" />
                <span className="size-2 rounded-full bg-[#ffc857]" />
                <span className="bg-lime size-2 rounded-full" />
                <span className="text-terminal-muted ml-2 font-mono text-[9px] tracking-[0.15em] uppercase">
                  kernl-shell.service
                </span>
              </div>
              <pre className="overflow-x-auto p-5 font-mono text-[11px] leading-[1.9] text-[#c6c7dd]">
                <code>
                  <span className="text-terminal-muted"># one ticket, one shell</span>
                  {"\n"}
                  <span className="text-lime">POST</span> /api/v1/terminal/sessions/
                  {"\n"}
                  <span className="text-terminal-muted">→ 201 Created</span>
                  {"\n\n"}
                  <span className="text-lime">WS</span> /ws/terminal/&lt;uuid&gt;/
                  {"\n"}
                  <span className="text-terminal-muted">→ 101 Switching Protocols</span>
                  {"\n\n"}
                  <span className="text-terminal-muted"># inside the sandbox</span>
                  {"\n"}
                  <span className="text-[#ffd479]">bwrap</span> --unshare-all ...
                  {"\n"}
                  <span className="text-[#ffd479]">bash</span> --noprofile --rcfile ...
                  {"\n\n"}
                  <span className="text-terminal-muted"># no network route</span>
                  {"\n"}
                  <span className="text-lime">$</span> curl example.com
                  {"\n"}
                  <span className="text-coral">Could not resolve host</span>
                </code>
              </pre>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 md:py-28">
        <div className="container-page">
          <div className="border-ink/15 bg-lime relative overflow-hidden rounded-[30px] border p-8 md:p-12 lg:p-16">
            <div className="bg-dots absolute inset-0 opacity-25" aria-hidden />
            <div
              className="border-ink/5 absolute -top-20 -right-20 size-72 rounded-full border-[40px]"
              aria-hidden
            />
            <div className="relative grid gap-10 lg:grid-cols-[1fr_auto] lg:items-end">
              <div>
                <span className="eyebrow text-ink/60">
                  <span className="bg-ink size-1.5 rounded-full" />
                  No better time
                </span>
                <h2 className="display mt-4 max-w-[680px] text-[clamp(2.5rem,5vw,4.6rem)] leading-[0.94] font-bold tracking-[-0.06em] text-balance">
                  The fastest way to learn{" "}
                  <span className="bg-ink text-lime rounded-lg px-2 py-0.5 font-mono text-[0.7em] tracking-[-0.05em]">
                    ls
                  </span>{" "}
                  is to type it.
                </h2>
                <p className="text-ink/65 mt-5 max-w-[500px] text-sm leading-6">
                  Open a track, get a prompt, and make your first mistake. The sandbox
                  can take it.
                </p>
              </div>
              <Link
                href="/courses/linux-foundations"
                className="btn btn-dark px-6! py-4!"
              >
                Open Linux Foundations
                <ArrowRight className="size-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
