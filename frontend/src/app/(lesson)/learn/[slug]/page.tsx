import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { LessonWorkspace } from "@/components/lesson/lesson-workspace";
import { AppHeader } from "@/components/site/app-header";
import { getLesson } from "@/lib/api";

export const dynamic = "force-dynamic";

interface LessonPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: LessonPageProps): Promise<Metadata> {
  const { slug } = await params;
  const lesson = await getLesson(slug);
  if (!lesson) return { title: "Lesson not found" };
  return {
    title: lesson.title,
    description: lesson.summary,
  };
}

export default async function LessonPage({ params }: LessonPageProps) {
  const { slug } = await params;
  const lesson = await getLesson(slug);
  if (!lesson) notFound();

  return (
    <div className="bg-cream flex min-h-dvh flex-col">
      <AppHeader courseTitle={lesson.course.title} />
      <div className="min-h-0 flex-1">
        <LessonWorkspace lesson={lesson} />
      </div>
    </div>
  );
}
