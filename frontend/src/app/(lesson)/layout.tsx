import type { ReactNode } from "react";

import { AppHeader } from "@/components/site/app-header";

export default function LessonLayout({ children }: { children: ReactNode }) {
  return (
    <div className="bg-cream flex min-h-dvh flex-col">
      <AppHeader />
      <div className="min-h-0 flex-1">{children}</div>
    </div>
  );
}
