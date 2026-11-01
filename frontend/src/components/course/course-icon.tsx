import { Code2, GitBranch, Terminal } from "lucide-react";

import type { CourseIcon } from "@/lib/types";

const ICONS = {
  terminal: Terminal,
  branch: GitBranch,
  code: Code2,
};

export function CourseGlyph({
  icon,
  className,
}: {
  icon: CourseIcon;
  className?: string;
}) {
  const Icon = ICONS[icon] ?? Terminal;
  return <Icon className={className} strokeWidth={1.6} aria-hidden />;
}
