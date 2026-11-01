import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  Check,
  Clock3,
  Layers3,
  LockKeyhole,
  Play,
  Terminal,
} from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { CourseGlyph } from "@/components/course/course-icon";
import { formatDuration, getCourse } from "@/lib/api";
import { ACCENT_STYLES, LEVEL_LABEL } from "@/lib/course-style";

export const dynamic = "force-dynamic";

interface CoursePageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: CoursePageProps): Promise<Metadata> {
  const { slug } = await params;
  const course = await getCourse(slug);
  if (!course) return { title: "Course not found" };
  return {
    title: course.title,
    description: course.tagline,
  };
}

export default async function CoursePage({ params }: CoursePageProps) {
  const { slug } = await params;
  const course = await getCourse(slug);
  if (!course) notFound();

  const accent = ACCENT_STYLES[course.accent] ?? ACCENT_STYLES.lime;
  const firstLesson = course.first_lesson;
  const allLessons = course.modules.flatMap((module) => module.lessons);

  return (
    <>
      <section
        className={`border-line relative overflow-hidden border-b ${accent.soft}`}
      >
        <div className="bg-dots absolute inset-0 opacity-25" aria-hidden />
        <div className="container-page relative py-8 md:py-10">
          <Link
            href="/#courses"
            className="text-ink/60 hover:text-ink inline-flex items-center gap-2 text-[12px] font-medium transition-colors"
          >
            <ArrowLeft className="size-3.5" />
            All courses
          </Link>

          <div className="mt-8 grid gap-10 pb-12 lg:grid-cols-[1fr_360px] lg:items-end lg:pb-16">
            <div>
              <div className="flex flex-wrap items-center gap-3">
                <span
                  className={`rounded-full px-3 py-1.5 font-mono text-[10px] font-semibold tracking-[0.13em] uppercase ${accent.badge}`}
                >
                  {LEVEL_LABEL[course.level] ?? course.level}
                </span>
                <span className="text-ink/50 font-mono text-[10px] tracking-[0.14em] uppercase">
                  {course.module_count} modules · {course.lesson_count} lessons
                </span>
              </div>

              <div className="mt-6 flex items-start gap-5">
                <span
                  className={`border-ink/10 hidden size-16 shrink-0 place-items-center rounded-2xl border sm:grid ${accent.icon}`}
                >
                  <CourseGlyph icon={course.icon} className="size-8" />
                </span>
                <div>
                  <h1 className="display max-w-[700px] text-[clamp(2.85rem,5vw,4.6rem)] leading-[0.94] font-bold tracking-[-0.06em] text-balance">
                    {course.title}
                  </h1>
                  <p className="text-ink/60 mt-4 max-w-[560px] text-[15px] leading-7 text-pretty">
                    {course.description}
                  </p>
                </div>
              </div>

              <div className="text-ink/65 mt-8 flex flex-wrap items-center gap-x-6 gap-y-3 text-[12px] font-medium">
                <span className="inline-flex items-center gap-1.5">
                  <Clock3 className="size-3.5" />
                  {formatDuration(course.duration_minutes)} total
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <Layers3 className="size-3.5" />
                  {course.lesson_count} guided lessons
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <Terminal className="size-3.5" />
                  Real Linux sandbox
                </span>
              </div>
            </div>

            <div className="border-ink/10 bg-paper/85 shadow-float rounded-[24px] border p-5 backdrop-blur">
              <p className="eyebrow text-muted">Your first command</p>
              <div className="border-terminal-line bg-terminal mt-4 overflow-hidden rounded-xl border">
                <div className="border-terminal-line flex items-center gap-1.5 border-b px-3 py-2">
                  <span className="bg-coral size-1.5 rounded-full" />
                  <span className="size-1.5 rounded-full bg-[#ffc857]" />
                  <span className="bg-lime size-1.5 rounded-full" />
                  <span className="text-terminal-muted ml-auto font-mono text-[8px] tracking-[0.15em] uppercase">
                    bash
                  </span>
                </div>
                <div className="px-4 py-5 font-mono text-[11px] leading-6 text-[#dfe0ee]">
                  <span className="text-lime">learner</span>
                  <span className="text-terminal-muted">@</span>
                  <span className="text-sky">kernl</span>
                  <span className="text-terminal-muted">:</span>
                  <span className="text-[#ffd479]">~</span>
                  <span className="text-terminal-muted">$ </span>
                  ls
                  <br />
                  <span className="text-terminal-muted">
                    README.md projects welcome.txt
                  </span>
                </div>
              </div>
              <p className="text-muted mt-4 text-[12px] leading-5">
                No setup. The sandbox boots with your lesson files already in place.
              </p>
              {firstLesson && (
                <Link
                  href={`/learn/${firstLesson}`}
                  className="btn btn-dark mt-4 w-full"
                >
                  <Play className="size-3.5 fill-current" />
                  Start the first lesson
                </Link>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 md:py-20">
        <div className="container-page grid gap-12 lg:grid-cols-[1fr_340px]">
          <div>
            <div className="mb-8 flex flex-wrap items-end justify-between gap-3">
              <div>
                <span className="eyebrow text-violet">
                  <span className="bg-violet size-1.5 rounded-full" />
                  The syllabus
                </span>
                <h2 className="display mt-3 text-[34px] leading-none font-bold tracking-[-0.05em]">
                  What you&apos;ll practice
                </h2>
              </div>
              <span className="text-muted font-mono text-[10px] tracking-[0.14em] uppercase">
                {allLessons.length} lessons · self-paced
              </span>
            </div>

            <div className="space-y-5">
              {course.modules.map((module, moduleIndex) => (
                <div
                  key={module.id}
                  className="border-line bg-paper overflow-hidden rounded-[22px] border"
                >
                  <div className="border-line/80 flex items-start gap-4 border-b px-5 py-4 sm:px-6">
                    <span className="text-muted mt-0.5 font-mono text-[10px] font-semibold tracking-[0.12em] uppercase">
                      {String(moduleIndex + 1).padStart(2, "0")}
                    </span>
                    <div>
                      <h3 className="display text-[19px] font-bold tracking-[-0.035em]">
                        {module.title}
                      </h3>
                      {module.summary && (
                        <p className="text-muted mt-1 text-[12px] leading-5">
                          {module.summary}
                        </p>
                      )}
                    </div>
                  </div>
                  <ul>
                    {module.lessons.map((lesson, lessonIndex) => (
                      <li key={lesson.slug}>
                        <Link
                          href={`/learn/${lesson.slug}`}
                          className="group border-line/60 hover:bg-cream/70 flex items-center gap-4 border-b px-5 py-4 transition-colors last:border-0 sm:px-6"
                        >
                          <span className="border-line-strong bg-cream text-muted group-hover:border-ink group-hover:bg-ink group-hover:text-lime grid size-9 shrink-0 place-items-center rounded-full border font-mono text-[10px] font-semibold transition-colors">
                            {String(lessonIndex + 1).padStart(2, "0")}
                          </span>
                          <div className="min-w-0 flex-1">
                            <div className="flex flex-wrap items-center gap-2">
                              <h4 className="text-[14px] font-semibold tracking-[-0.01em]">
                                {lesson.title}
                              </h4>
                              {lesson.is_mandatory && (
                                <span className="bg-lime/60 text-ink/60 rounded-full px-2 py-0.5 font-mono text-[8px] font-semibold tracking-[0.1em] uppercase">
                                  Mandatory
                                </span>
                              )}
                            </div>
                            <p className="text-muted mt-0.5 line-clamp-1 text-[11px]">
                              {lesson.summary}
                            </p>
                          </div>
                          <span className="text-muted hidden shrink-0 font-mono text-[10px] sm:block">
                            {lesson.duration_minutes} min
                          </span>
                          <ArrowUpRight className="text-muted group-hover:text-ink size-4 shrink-0 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          <aside className="space-y-5 lg:sticky lg:top-24 lg:self-start">
            <div className="border-line bg-paper rounded-[22px] border p-5">
              <p className="eyebrow text-muted">You&apos;ll walk away with</p>
              <ul className="mt-4 space-y-3">
                {course.outcomes.map((outcome) => (
                  <li key={outcome} className="flex gap-2.5 text-[12px] leading-5">
                    <span className="bg-lime mt-0.5 grid size-4 shrink-0 place-items-center rounded-full">
                      <Check className="text-ink size-2.5" strokeWidth={3} />
                    </span>
                    {outcome}
                  </li>
                ))}
              </ul>
            </div>

            <div className="border-line bg-paper rounded-[22px] border p-5">
              <p className="eyebrow text-muted">Tools in this track</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {course.tools.map((tool) => (
                  <span
                    key={tool}
                    className="border-line bg-cream text-ink/70 rounded-lg border px-2.5 py-1.5 font-mono text-[10px]"
                  >
                    {tool}
                  </span>
                ))}
              </div>
            </div>

            <div className="border-terminal-line bg-terminal text-paper rounded-[22px] border p-5">
              <LockKeyhole className="text-lime size-4" />
              <p className="mt-3 text-[13px] font-semibold">
                A shell you can&apos;t hurt
              </p>
              <p className="text-terminal-muted mt-1.5 text-[11px] leading-5">
                Every session is isolated, networkless, and deleted when you disconnect.
                Your real computer never sees a command.
              </p>
              <Link
                href="/#local-first"
                className="text-lime mt-4 inline-flex items-center gap-1.5 text-[11px] font-medium hover:underline"
              >
                How the sandbox works
                <ArrowRight className="size-3" />
              </Link>
            </div>
          </aside>
        </div>
      </section>

      {firstLesson && (
        <section className="pb-20 md:pb-24">
          <div className="container-page">
            <div className="border-line bg-paper flex flex-col items-start justify-between gap-6 rounded-[24px] border p-7 sm:flex-row sm:items-center">
              <div>
                <p className="eyebrow text-muted">Ready when you are</p>
                <h2 className="display mt-2 text-[28px] font-bold tracking-[-0.045em]">
                  Open a terminal. Type the first command.
                </h2>
              </div>
              <Link href={`/learn/${firstLesson}`} className="btn btn-dark shrink-0">
                Start {course.title}
                <ArrowRight className="size-4" />
              </Link>
            </div>
          </div>
        </section>
      )}
    </>
  );
}
