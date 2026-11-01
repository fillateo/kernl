import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RichText } from "@/components/lesson/rich-text";

describe("RichText", () => {
  it("turns backticked segments into inline code", () => {
    render(<RichText text="Run `ls -la` to list everything." />);

    const code = screen.getByText("ls -la");
    expect(code.tagName).toBe("CODE");
    expect(screen.getByText(/to list everything/)).toBeInTheDocument();
  });

  it("renders raw HTML as text instead of injecting it", () => {
    render(<RichText text={"<script>alert('xss')</script>"} />);

    expect(screen.queryByRole("script")).not.toBeInTheDocument();
    expect(screen.getByText("<script>alert('xss')</script>")).toBeInTheDocument();
  });
});
