import type { ReactNode } from "react";

export default function LessonLayout({ children }: { children: ReactNode }) {
  return <div className="bg-cream min-h-dvh">{children}</div>;
}
