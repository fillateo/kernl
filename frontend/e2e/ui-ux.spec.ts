import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

const PAGES = [
  { name: "course overview", path: "/", terminal: false },
  {
    name: "lesson workspace",
    path: "/learn/your-first-repository",
    terminal: true,
  },
  { name: "terminal playground", path: "/playground", terminal: true },
] as const;

for (const target of PAGES) {
  test(`${target.name} has no accessibility violations`, async ({ page }) => {
    await page.goto(target.path, { waitUntil: "networkidle" });
    if (target.terminal) {
      await expect(page.locator(".xterm-screen")).toBeVisible();
    }

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa"])
      .analyze();

    expect(results.violations).toEqual([]);
  });
}

test("all three pages fit a mobile viewport without horizontal overflow", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });

  for (const target of PAGES) {
    await page.goto(target.path, { waitUntil: "networkidle" });
    const header = page.locator("header");
    await expect(header).toBeVisible();
    await expect(
      header.getByRole("link", { name: "Course", exact: true }),
    ).toBeVisible();
    await expect(
      header.getByRole("link", { name: "Playground", exact: true }),
    ).toBeVisible();

    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow, `${target.path} overflows horizontally`).toBeLessThanOrEqual(1);
  }
});

test("unknown routes show the lesson-focused 404 page", async ({ page }) => {
  const response = await page.goto("/this-lesson-does-not-exist");

  expect(response?.status()).toBe(404);
  await expect(
    page.getByRole("heading", { name: /That command isn't in this sandbox/i }),
  ).toBeVisible();
  await expect(page.getByRole("link", { name: /Open the lesson/i })).toHaveAttribute(
    "href",
    "/learn/your-first-repository",
  );
});

test("course outline links are keyboard reachable", async ({ page }) => {
  await page.goto("/");

  const lessonLink = page.getByRole("link", {
    name: /Your First Repository/i,
  });
  await lessonLink.focus();

  await expect(lessonLink).toBeFocused();
  await expect(lessonLink).toHaveAttribute("href", "/learn/your-first-repository");
});

test("all pages load without browser console errors", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });

  for (const target of PAGES) {
    await page.goto(target.path, { waitUntil: "networkidle" });
    if (target.terminal) {
      await expect(page.locator(".xterm-screen")).toBeVisible();
    }
  }

  expect(errors).toEqual([]);
});
