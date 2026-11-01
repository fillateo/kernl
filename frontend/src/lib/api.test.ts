import { describe, expect, it } from "vitest";

import { buildTerminalSocketUrl } from "@/lib/api";

describe("buildTerminalSocketUrl", () => {
  it("uses a ws URL for the local API", () => {
    expect(buildTerminalSocketUrl("/ws/terminal/abc/")).toMatch(
      /^ws:\/\/127\.0\.0\.1:8000\/ws\/terminal\/abc\/$/,
    );
  });
});
