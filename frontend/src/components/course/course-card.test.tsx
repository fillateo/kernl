import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CourseCard } from "@/components/course/course-card";
import type { CourseSummary } from "@/lib/types";

const COURSE: CourseSummary = {
  slug: "linux-foundations",
  title: "Linux Foundations",
  tagline: "Get comfortable in the shell.",
  description: "Learn Linux.",
  level: "beginner",
  duration_minutes: 95,
  accent: "lime",
  icon: "terminal",
  outcomes: ["Use ls"],
  tools: ["bash", "ls", "grep"],
  lesson_count: 4,
  module_count: 2,
};

describe("CourseCard", () => {
  it("links to the course and shows useful metadata", () => {
    render(<CourseCard course={COURSE} index={0} />);

    expect(screen.getByRole("link", { name: /linux foundations/i })).toHaveAttribute(
      "href",
      "/courses/linux-foundations",
    );
    expect(screen.getByText("4 lessons")).toBeInTheDocument();
    expect(screen.getByText("1h 35m")).toBeInTheDocument();
    expect(screen.getByText("Beginner")).toBeInTheDocument();
  });
});
