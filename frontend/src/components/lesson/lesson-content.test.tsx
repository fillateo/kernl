import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { LessonContent } from "@/components/lesson/lesson-content";
import type { LessonBlock } from "@/lib/types";

const BLOCKS: LessonBlock[] = [
  { type: "heading", eyebrow: "Step 01", text: "Directory listing" },
  { type: "paragraph", text: "Run `ls` to list the current directory." },
  { type: "command", label: "List files", command: "ls" },
  { type: "output", label: "Command output", text: "README.md  projects" },
  {
    type: "callout",
    tone: "tip",
    title: "Tab completion",
    text: "Press Tab to complete a path.",
  },
  {
    type: "checkpoint",
    title: "Your turn",
    text: "Run `pwd` and read the path.",
  },
];

describe("LessonContent", () => {
  it("renders all supported lesson block types", () => {
    render(<LessonContent blocks={BLOCKS} onRun={vi.fn()} />);

    expect(
      screen.getByRole("heading", { name: "Directory listing" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Step 01")).toBeInTheDocument();
    expect(screen.getByText(/README\.md/)).toBeInTheDocument();
    expect(screen.getByText("Tab completion")).toBeInTheDocument();
    expect(screen.getByText("Your turn")).toBeInTheDocument();
  });

  it("wires command blocks to the terminal callback", async () => {
    const user = userEvent.setup();
    const onRun = vi.fn();
    render(<LessonContent blocks={BLOCKS} onRun={onRun} />);

    await user.click(screen.getByRole("button", { name: /run/i }));

    expect(onRun).toHaveBeenCalledWith("ls");
  });
});
