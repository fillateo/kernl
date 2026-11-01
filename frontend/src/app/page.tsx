import { ArrowRight, Clock3, Layers3, Play, Terminal } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { CourseGlyph } from "@/components/course/course-icon";
import { AppHeader } from "@/components/site/app-header";
import { getLesson } from "@/lib/api";

export const dynamic = "force-dynamic";

const FIRST_LESSON = "your-first-repository";

export async function generateMetadata(): Promise<Metadata> {
  const lesson = await getLesson(FIRST_LESSON);
  if (!lesson) return { title: "Course not found" };
  return {
    title: lesson.course.title,
    description: lesson.course.tagline,
  };
}

export default async function CoursePage() {
  const lesson = await getLesson(FIRST_LESSON);
  if (!lesson) notFound();

  const { course } = lesson;
  const firstLesson = course.modules[0]?.lessons[0]?.slug ?? FIRST_LESSON;

  return (
    <div className="bg-cream flex min-h-dvh flex-col">
      <AppHeader title={course.title} />
      <main className="container-page flex-1 py-12 md:py-16">
        <div className="grid gap-10 lg:grid-cols-[1fr_390px] lg:gap-16">
          <div className="max-w-[680px]">
            <div className="flex flex-wrap items-center gap-3">
              <span className="bg-ink text-lime rounded-full px-3 py-1.5 font-mono text-[10px] font-semibold tracking-[0.13em] uppercase">
                {course.level}
              </span>
              <span className="text-muted font-mono text-[10px] tracking-[0.14em] uppercase">
                {course.module_count} modules · {course.lesson_count} lessons
              </span>
            </div>

            <div className="mt-7 flex items-start gap-5">
              <span className="border-line bg-paper hidden size-16 shrink-0 place-items-center rounded-2xl border sm:grid">
                <CourseGlyph icon={course.icon} className="text-ink size-8" />
              </span>
              <div>
                <h1 className="display text-[clamp(2.8rem,5vw,4.5rem)] leading-[0.94] font-bold tracking-[-0.06em] text-balance">
                  {course.title}
                </h1>
                <p className="text-muted mt-4 text-[15px] leading-7 text-pretty">
                  {course.tagline}
                </p>
              </div>
            </div>

            <p className="text-muted mt-7 max-w-[560px] text-[13px] leading-6 text-pretty">
              {course.description}
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <Link href={`/learn/${firstLesson}`} className="btn btn-dark">
                <Play className="size-3.5 fill-current" />
                Open first lesson
              </Link>
              <Link href="/playground" className="btn btn-outline">
                <Terminal className="size-4" />
                Terminal playground
              </Link>
            </div>

            <div className="border-line text-muted mt-10 flex flex-wrap items-center gap-6 border-t pt-6 text-[11px]">
              <span className="inline-flex items-center gap-1.5">
                <Clock3 className="size-3.5" />
                Self-paced
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

          <aside className="lg:pt-1">
            <div className="border-line bg-paper shadow-float rounded-[22px] border p-5">
              <div className="border-line flex items-center justify-between border-b pb-4">
                <p className="eyebrow text-muted">Course outline</p>
                <span className="text-muted font-mono text-[9px] tracking-[0.1em] uppercase">
                  Git Essentials
                </span>
              </div>

              <div className="mt-5 space-y-6">
                {course.modules.map((module, moduleIndex) => (
                  <div key={module.id}>
                    <div className="mb-2 flex items-center gap-2">
                      <span className="text-muted font-mono text-[9px]">
                        {String(moduleIndex + 1).padStart(2, "0")}
                      </span>
                      <span className="text-muted font-mono text-[9px] font-semibold tracking-[0.13em] uppercase">
                        {module.title}
                      </span>
                    </div>
                    <ul className="space-y-1.5">
                      {module.lessons.map((item) => (
                        <li key={item.slug}>
                          <Link
                            href={`/learn/${item.slug}`}
                            className="group hover:border-line hover:bg-cream/70 flex items-center gap-3 rounded-xl border border-transparent px-2.5 py-2 transition-colors"
                          >
                            <span className="border-line-strong text-muted grid size-6 shrink-0 place-items-center rounded-full border font-mono text-[8px]">
                              {String(item.position).padStart(2, "0")}
                            </span>
                            <span className="min-w-0 flex-1">
                              <span className="text-ink block truncate text-[12px] font-medium">
                                {item.title}
                              </span>
                              <span className="text-muted mt-0.5 block font-mono text-[8px] tracking-[0.08em] uppercase">
                                {item.duration_minutes} min
                              </span>
                            </span>
                            <ArrowRight className="text-muted group-hover:text-ink size-3.5 shrink-0 transition-transform group-hover:translate-x-0.5" />
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>

              <Link href={`/learn/${firstLesson}`} className="btn btn-dark mt-6 w-full">
                Start learning
                <ArrowRight className="size-4" />
              </Link>
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
}
