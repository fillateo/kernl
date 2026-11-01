export type CourseLevel = "beginner" | "intermediate" | "advanced";
export type CourseIcon = "terminal" | "branch" | "code";

export interface LessonSummary {
  slug: string;
  title: string;
  summary: string;
  duration_minutes: number;
  is_mandatory: boolean;
  position: number;
}

export interface Module {
  id: number;
  title: string;
  summary: string;
  position: number;
  lessons: LessonSummary[];
}

export interface CourseDetail {
  title: string;
  tagline: string;
  description: string;
  level: CourseLevel;
  icon: CourseIcon;
  lesson_count: number;
  module_count: number;
  modules: Module[];
}

export interface NeighbourLesson {
  slug: string;
  title: string;
  summary: string;
  duration_minutes: number;
  is_mandatory: boolean;
  position: number;
}

export type LessonBlock =
  | {
      type: "heading";
      eyebrow?: string;
      text: string;
    }
  | {
      type: "paragraph";
      text: string;
    }
  | {
      type: "command";
      label?: string;
      command: string;
    }
  | {
      type: "output";
      label?: string;
      text: string;
    }
  | {
      type: "list";
      style?: "bullet" | "number";
      items: string[];
    }
  | {
      type: "callout";
      tone?: "note" | "tip" | "warning";
      title: string;
      text: string;
    }
  | {
      type: "checkpoint";
      title: string;
      text: string;
    }
  | {
      type: "divider";
    };

export interface Lesson extends NeighbourLesson {
  content: LessonBlock[];
  course: CourseDetail;
  module: Omit<Module, "lessons">;
  previous_lesson: NeighbourLesson | null;
  next_lesson: NeighbourLesson | null;
  lesson_number: number;
  total_lessons: number;
}

export interface TerminalSession {
  id: string;
  expires_at: string;
  websocket_path: string;
}
