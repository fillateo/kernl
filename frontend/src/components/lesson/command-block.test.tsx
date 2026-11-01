import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { CommandBlock } from "@/components/lesson/command-block";

describe("CommandBlock", () => {
  it("sends the exact command to the terminal", async () => {
    const user = userEvent.setup();
    const onRun = vi.fn();

    render(
      <CommandBlock
        command="grep ERROR logs/app.log"
        label="Find errors"
        onRun={onRun}
      />,
    );

    await user.click(screen.getByRole("button", { name: /run/i }));

    expect(onRun).toHaveBeenCalledWith("grep ERROR logs/app.log");
  });

  it("copies the command to the clipboard", async () => {
    const user = userEvent.setup();
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });

    render(<CommandBlock command="pwd" onRun={vi.fn()} />);
    await user.click(screen.getByRole("button", { name: /copy command/i }));

    expect(writeText).toHaveBeenCalledWith("pwd");
    expect(screen.getByRole("button", { name: /command copied/i })).toBeInTheDocument();
  });
});
