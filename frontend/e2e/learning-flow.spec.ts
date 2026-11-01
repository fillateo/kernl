import { expect, test } from "@playwright/test";

test("boots directly into the Git lesson workspace", async ({ page }) => {
  await page.goto("/");

  await expect(page).toHaveURL(/\/learn\/your-first-repository\/?$/);
  await expect(
    page.getByRole("heading", { name: "Your First Repository" }),
  ).toBeVisible();
  await expect(page.locator("header")).toContainText("Git Essentials");

  // The marketing/catalog surfaces are intentionally gone.
  await expect(page.getByRole("link", { name: /All courses/i })).toHaveCount(0);
  await expect(page.getByText("Course overview")).toHaveCount(0);

  await page.getByRole("link", { name: /Staging & Committing/i }).click();
  await expect(page).toHaveURL(/\/learn\/staging-and-committing\/?$/);
  await expect(
    page.getByRole("heading", { name: "Staging & Committing" }),
  ).toBeVisible();
  await expect(page.locator("header")).toContainText("Git Essentials");
});

test("a lesson command runs in a real sandbox", async ({ page, request }) => {
  const healthResponse = await request.get(
    process.env.E2E_HEALTH_URL ?? "http://127.0.0.1:8000/api/health/",
  );
  const health = (await healthResponse.json()) as {
    terminal?: { sandbox?: string };
  };
  test.skip(
    health.terminal?.sandbox !== "available",
    "bubblewrap is not available on this host",
  );

  await page.goto("/learn/your-first-repository");

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
  await expect(page.locator(".xterm-rows")).toContainText(
    "Initialized empty Git repository",
    { timeout: 10_000 },
  );
});
