import { Circle, Clock3, LockKeyhole } from "lucide-react";
import Link from "next/link";

import { CourseGlyph } from "@/components/course/course-icon";
import type { Lesson, Module } from "@/lib/types";

export function LessonOutline({
  modules,
  currentSlug,
}: {
  modules: Module[];
  currentSlug: string;
}) {
  return (
    <nav aria-label="Course outline">
      {modules.map((module, moduleIndex) => (
        <div key={module.id} className="mb-6 last:mb-0">
          <div className="mb-2 flex items-center gap-2 px-2">
            <span className="text-muted font-mono text-[9px] font-medium tracking-[0.15em] uppercase">
              {String(moduleIndex + 1).padStart(2, "0")}
            </span>
            <span className="text-muted font-mono text-[9px] font-semibold tracking-[0.13em] uppercase">
              {module.title}
            </span>
          </div>
          <ul className="space-y-1">
            {module.lessons.map((lesson) => {
              const active = lesson.slug === currentSlug;
              return (
                <li key={lesson.slug}>
                  <Link
                    href={`/learn/${lesson.slug}`}
                    aria-current={active ? "page" : undefined}
                    className={`group relative flex items-start gap-2.5 rounded-xl px-2.5 py-2.5 transition-colors ${
                      active
                        ? "bg-paper ring-line shadow-sm ring-1"
                        : "hover:bg-paper/60"
                    }`}
                  >
                    {active && (
                      <span className="bg-violet absolute inset-y-2 left-0 w-[3px] rounded-full" />
                    )}
                    <span
                      className={`mt-0.5 grid size-5 shrink-0 place-items-center rounded-full border font-mono text-[8px] font-semibold ${
                        active
                          ? "border-ink bg-ink text-lime"
                          : "border-line-strong text-muted"
                      }`}
                    >
                      {String(lesson.position).padStart(2, "0")}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span
                        className={`block text-[12px] leading-[1.35] font-medium ${
                          active ? "text-ink" : "text-ink/70 group-hover:text-ink"
                        }`}
                      >
                        {lesson.title}
                      </span>
                      <span className="text-muted mt-1 flex items-center gap-2 text-[9px]">
                        <span className="inline-flex items-center gap-1">
                          <Clock3 className="size-2.5" />
                          {lesson.duration_minutes}m
                        </span>
                        {lesson.is_mandatory && (
                          <span className="bg-lime/70 text-ink inline-flex items-center gap-1 rounded px-1.5 py-0.5 font-mono text-[7px] font-semibold tracking-[0.08em] uppercase">
                            <LockKeyhole className="size-2" />
                            Required
                          </span>
                        )}
                      </span>
                    </span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </nav>
  );
}

export function LessonSidebar({ lesson }: { lesson: Lesson }) {
  const { course } = lesson;
  const progress = Math.round((lesson.lesson_number / lesson.total_lessons) * 100);

  return (
    <aside className="border-line bg-cream/70 hidden h-full min-h-0 flex-col border-r lg:flex">
      <div className="border-line/80 border-b p-5">
        <div className="flex items-start gap-3">
          <span className="border-line bg-paper grid size-9 shrink-0 place-items-center rounded-xl border">
            <CourseGlyph icon={course.icon} className="text-ink size-4" />
          </span>
          <div className="min-w-0">
            <h2 className="text-[13px] leading-tight font-semibold">{course.title}</h2>
            <p className="text-muted mt-0.5 font-mono text-[8px] tracking-[0.13em] uppercase">
              {course.level} · {course.lesson_count} lessons
            </p>
          </div>
        </div>
        <div className="text-muted mt-5 flex items-center justify-between font-mono text-[8px] tracking-[0.12em] uppercase">
          <span>Course position</span>
          <span className="text-ink">
            {lesson.lesson_number}/{lesson.total_lessons}
          </span>
        </div>
        <div
          className="bg-line mt-2 h-1.5 overflow-hidden rounded-full"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={progress}
          aria-label="Lesson position"
        >
          <div
            className="bg-violet h-full rounded-full transition-[width] duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="min-h-0 flex-1 scrollbar-thin overflow-y-auto p-3">
        <LessonOutline modules={course.modules} currentSlug={lesson.slug} />
      </div>

      <div className="border-line/80 border-t p-4">
        <div className="border-line bg-paper rounded-xl border p-3">
          <div className="flex items-center gap-2">
            <span className="relative flex size-2">
              <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-50" />
              <span className="relative inline-flex size-2 rounded-full bg-emerald-500" />
            </span>
            <span className="text-muted font-mono text-[8px] font-medium tracking-[0.14em] uppercase">
              Local sandbox
            </span>
          </div>
          <p className="text-muted mt-2 text-[10px] leading-4">
            Changes vanish when you disconnect.
          </p>
        </div>
      </div>
    </aside>
  );
}

export function MobileOutline({ lesson }: { lesson: Lesson }) {
  return (
    <details className="group border-line bg-cream/70 border-b lg:hidden">
      <summary className="flex cursor-pointer list-none items-center justify-between px-5 py-4">
        <span className="flex items-center gap-2 text-[12px] font-semibold">
          <Circle className="fill-violet text-violet size-2" />
          Course outline
        </span>
        <span className="text-muted font-mono text-[9px] tracking-[0.12em] uppercase">
          Lesson {lesson.lesson_number} of {lesson.total_lessons}
          <span className="ml-2 inline-block transition-transform group-open:rotate-180">
            ↓
          </span>
        </span>
      </summary>
      <div className="border-line/70 max-h-80 scrollbar-thin overflow-y-auto border-t px-3 py-4">
        <LessonOutline modules={lesson.course.modules} currentSlug={lesson.slug} />
      </div>
    </details>
  );
}
