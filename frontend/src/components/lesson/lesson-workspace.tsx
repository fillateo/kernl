"use client";

import { ArrowLeft, ArrowRight, ArrowUp, Clock3, LockKeyhole } from "lucide-react";
import Link from "next/link";
import { useCallback, useRef } from "react";

import { LessonContent } from "@/components/lesson/lesson-content";
import { LessonSidebar, MobileOutline } from "@/components/lesson/lesson-sidebar";
import { TerminalPanel, type TerminalHandle } from "@/components/lesson/terminal-panel";
import type { Lesson } from "@/lib/types";

export function LessonWorkspace({ lesson }: { lesson: Lesson }) {
  const terminalRef = useRef<TerminalHandle>(null);
  const terminalWrapRef = useRef<HTMLDivElement>(null);
  const firstLessonSlug = lesson.course.modules[0]?.lessons[0]?.slug ?? lesson.slug;

  const runCommand = useCallback((command: string) => {
    terminalRef.current?.runCommand(command);
    if (window.matchMedia("(max-width: 1023px)").matches) {
      terminalWrapRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }
  }, []);

  return (
    <div className="lg:grid lg:h-[calc(100dvh-4rem)] lg:grid-cols-[270px_minmax(380px,520px)_minmax(0,1fr)]">
      <LessonSidebar lesson={lesson} />

      <main className="border-line bg-paper min-w-0 scrollbar-thin lg:h-full lg:overflow-y-auto lg:border-r">
        <MobileOutline lesson={lesson} />

        <div className="mx-auto max-w-[640px] px-5 py-7 sm:px-8 lg:px-9 lg:py-8">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <span className="eyebrow text-violet text-[9px]">
              {lesson.module.title}
            </span>
            <span className="text-muted font-mono text-[9px] tracking-[0.13em] uppercase">
              {lesson.lesson_number} / {lesson.total_lessons} steps
            </span>
          </div>

          <h1 className="display mt-4 text-[clamp(2rem,4vw,2.8rem)] leading-[0.98] font-bold tracking-[-0.055em] text-balance">
            {lesson.title}
          </h1>
          <p className="text-muted mt-4 max-w-[560px] text-[14px] leading-7 text-pretty">
            {lesson.summary}
          </p>

          <div className="border-line text-muted mt-5 flex flex-wrap items-center gap-3 border-b pb-6 text-[10px] font-medium">
            <span className="inline-flex items-center gap-1.5">
              <Clock3 className="size-3" />
              {lesson.duration_minutes} min
            </span>
            {lesson.is_mandatory && (
              <span className="bg-lime/70 text-ink inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 font-mono text-[8px] tracking-[0.1em] uppercase">
                <LockKeyhole className="size-2.5" />
                Required
              </span>
            )}
            <span className="text-muted ml-auto hidden items-center gap-1.5 font-mono text-[8px] tracking-[0.1em] uppercase sm:inline-flex">
              <span className="size-1.5 rounded-full bg-emerald-500" />
              Live sandbox
            </span>
          </div>

          <div className="mt-8">
            <LessonContent blocks={lesson.content} onRun={runCommand} />
          </div>

          <div className="border-line-strong bg-cream/60 mt-10 flex items-start gap-3 rounded-2xl border border-dashed p-4 lg:hidden">
            <ArrowUp className="text-violet mt-0.5 size-4 shrink-0" />
            <p className="text-muted text-[11px] leading-5">
              The terminal is just below this lesson. Hit{" "}
              <span className="text-ink font-mono">Run</span> on any command and it will
              be sent to your sandbox.
            </p>
          </div>

          <nav
            className="border-line mt-12 flex items-center justify-between gap-3 border-t pt-6"
            aria-label="Lesson navigation"
          >
            {lesson.previous_lesson ? (
              <Link
                href={`/learn/${lesson.previous_lesson.slug}`}
                className="btn btn-outline px-4! py-2.5! text-[11px]"
              >
                <ArrowLeft className="size-3.5" />
                <span className="max-w-[150px] truncate">
                  {lesson.previous_lesson.title}
                </span>
              </Link>
            ) : (
              <span className="text-muted font-mono text-[9px] tracking-[0.12em] uppercase">
                Start of track
              </span>
            )}

            {lesson.next_lesson ? (
              <Link
                href={`/learn/${lesson.next_lesson.slug}`}
                className="btn btn-dark px-4! py-2.5! text-[11px]"
              >
                Next lesson
                <ArrowRight className="size-3.5" />
              </Link>
            ) : (
              <Link
                href={`/learn/${firstLessonSlug}`}
                className="btn btn-dark px-4! py-2.5! text-[11px]"
              >
                Back to first lesson
                <ArrowRight className="size-3.5" />
              </Link>
            )}
          </nav>
        </div>
      </main>

      <div
        ref={terminalWrapRef}
        className="h-[68vh] min-h-[480px] lg:h-full lg:min-h-0"
      >
        <TerminalPanel ref={terminalRef} lessonSlug={lesson.slug} className="h-full" />
      </div>
    </div>
  );
}
