import { ArrowUpRight, Clock3, GitBranch, Layers3, Terminal } from "lucide-react";
import Link from "next/link";

import { formatDuration } from "@/lib/api";
import { ACCENT_STYLES, LEVEL_LABEL } from "@/lib/course-style";
import type { CourseAccent, CourseIcon, CourseSummary } from "@/lib/types";

const ICONS = {
  terminal: Terminal,
  branch: GitBranch,
  code: Layers3,
} satisfies Record<CourseIcon, typeof Terminal>;

export function CourseCard({
  course,
  index,
}: {
  course: CourseSummary;
  index: number;
}) {
  const Icon = ICONS[course.icon] ?? Terminal;
  const accent = ACCENT_STYLES[course.accent as CourseAccent] ?? ACCENT_STYLES.lime;
  const courseNumber = String(index + 1).padStart(2, "0");

  return (
    <Link
      href={`/courses/${course.slug}`}
      className="group border-line bg-paper hover:border-ink/25 hover:shadow-card relative flex flex-col overflow-hidden rounded-[26px] border transition-all duration-300 hover:-translate-y-1.5"
    >
      <div
        className={`relative h-[172px] overflow-hidden p-5 ${accent.panel} ${accent.panelText}`}
      >
        <div className="bg-dots absolute inset-0 opacity-20" aria-hidden />
        <div className="relative flex items-start justify-between">
          <span className="rounded-full border border-current/20 bg-white/15 px-2.5 py-1 font-mono text-[10px] font-semibold tracking-[0.15em] uppercase backdrop-blur-sm">
            {LEVEL_LABEL[course.level] ?? course.level}
          </span>
          <span className={`font-mono text-[11px] font-medium ${accent.panelMuted}`}>
            /{courseNumber}
          </span>
        </div>
        <div className="relative mt-9 flex items-end justify-between">
          <Icon
            className="size-10 opacity-90 transition-transform duration-300 group-hover:scale-110 group-hover:-rotate-6"
            strokeWidth={1.5}
          />
          <span
            className={`font-display text-[64px] leading-none font-bold tracking-[-0.08em] ${accent.panelMuted}`}
          >
            {courseNumber}
          </span>
        </div>
      </div>

      <div className="flex flex-1 flex-col p-6">
        <div className="text-muted flex flex-wrap items-center gap-x-4 gap-y-2 text-[11px] font-medium">
          <span className="inline-flex items-center gap-1.5">
            <Clock3 className="size-3.5" />
            {formatDuration(course.duration_minutes)}
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Layers3 className="size-3.5" />
            {course.lesson_count} lessons
          </span>
          <span className="text-muted/80 font-mono text-[10px] tracking-[0.1em] uppercase">
            {course.tools.slice(0, 2).join(" · ")}
          </span>
        </div>

        <h3 className="display mt-4 text-[26px] leading-[1.05] font-bold tracking-[-0.045em]">
          {course.title}
        </h3>
        <p className="text-muted mt-3 text-[13px] leading-6">{course.tagline}</p>

        <div className="border-line/80 mt-auto flex items-center justify-between border-t pt-5">
          <span
            className={`font-mono text-[10px] font-semibold tracking-[0.13em] uppercase ${accent.accentText}`}
          >
            {course.module_count} modules
          </span>
          <span className="text-ink inline-flex items-center gap-1.5 text-[12px] font-semibold">
            Open track
            <span className="bg-ink text-paper grid size-7 place-items-center rounded-full transition-transform duration-200 group-hover:rotate-45">
              <ArrowUpRight className="size-3.5" />
            </span>
          </span>
        </div>
      </div>
    </Link>
  );
}
