import { describe, expect, it } from "vitest";

import { buildTerminalSocketUrl, formatDuration, formatLessonLabel } from "@/lib/api";

describe("formatDuration", () => {
  it("formats minutes and whole hours", () => {
    expect(formatDuration(45)).toBe("45 min");
    expect(formatDuration(60)).toBe("1h");
    expect(formatDuration(95)).toBe("1h 35m");
  });
});

describe("formatLessonLabel", () => {
  it("shows the current position and total", () => {
    expect(formatLessonLabel(1, 4)).toBe("1 / 4 lessons");
  });
});

describe("buildTerminalSocketUrl", () => {
  it("uses a ws URL for the local API", () => {
    expect(buildTerminalSocketUrl("/ws/terminal/abc/")).toMatch(
      /^ws:\/\/127\.0\.0\.1:8000\/ws\/terminal\/abc\/$/,
    );
  });
});
