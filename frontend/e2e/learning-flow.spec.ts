import { expect, test } from "@playwright/test";

test("the three-page learning flow is navigable", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: /Learn the terminal/i }),
  ).toBeVisible();
  await expect(page.getByRole("heading", { name: /Pick a path/i })).toBeVisible();

  await page.getByRole("link", { name: /Start with Linux/i }).click();
  await expect(page).toHaveURL(/\/courses\/linux-foundations\/?$/);
  await expect(page.getByRole("heading", { name: "Linux Foundations" })).toBeVisible();

  await page.getByRole("link", { name: /Start the first lesson/i }).click();
  await expect(page).toHaveURL(/\/learn\/working-with-linux-commands\/?$/);
  await expect(
    page.getByRole("heading", { name: "Working With Linux Commands" }),
  ).toBeVisible();
  await expect(page.getByRole("heading", { name: "Directory listing" })).toBeVisible();
  await expect(page.locator(".xterm-screen")).toBeVisible();

  // The workspace header must follow the selected course, not a hard-coded one.
  await page.goto("/learn/your-first-repository");
  await expect(
    page.getByRole("heading", { name: "Your First Repository" }),
  ).toBeVisible();
  await expect(page.locator("header")).toContainText("Git Essentials");
});

test("a lesson command runs in a real sandbox", async ({ page, request }) => {
  const healthResponse = await request.get("http://127.0.0.1:8000/api/health/");
  const health = (await healthResponse.json()) as {
    terminal?: { sandbox?: string };
  };
  test.skip(
    health.terminal?.sandbox !== "available",
    "bubblewrap is not available on this host",
  );

  await page.goto("/learn/working-with-linux-commands");

  await expect(page.locator(".xterm-screen")).toBeVisible();
  await expect(page.getByText("Connected", { exact: true })).toBeVisible({
    timeout: 20_000,
  });

  await page.locator(".xterm-screen").click();
  await page.keyboard.type("pwd");
  await page.keyboard.press("Enter");

  await expect(page.locator(".xterm-rows")).toContainText("/home/learner", {
    timeout: 10_000,
  });

  await page.keyboard.type(
    "printf '#!/bin/sh\\necho SCRIPT_OK\\n' > run.sh && chmod +x run.sh && ./run.sh",
  );
  await page.keyboard.press("Enter");
  await expect(page.locator(".xterm-rows")).toContainText("SCRIPT_OK", {
    timeout: 10_000,
  });

  await page.getByRole("button", { name: /^run$/i }).first().click();
  await expect(page.locator(".xterm-rows")).toContainText("README.md", {
    timeout: 10_000,
  });
});
