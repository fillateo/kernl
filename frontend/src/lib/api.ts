import { cache } from "react";

import type { Lesson, TerminalSession } from "@/lib/types";

const PUBLIC_API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://127.0.0.1:8000";

const SERVER_API_URL = process.env.API_URL?.replace(/\/$/, "") ?? PUBLIC_API_URL;

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function requestJson<T>(url: string): Promise<T | null> {
  let response: Response;
  try {
    response = await fetch(url, {
      cache: "no-store",
      headers: { Accept: "application/json" },
      signal: AbortSignal.timeout(5000),
    });
  } catch {
    throw new ApiError(
      "The course service is not reachable. Is the Django server running?",
      503,
    );
  }

  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new ApiError(
      `The course service returned ${response.status}.`,
      response.status,
    );
  }
  return (await response.json()) as T;
}

export const getLesson = cache(async (slug: string): Promise<Lesson | null> => {
  return requestJson<Lesson>(
    `${SERVER_API_URL}/api/v1/catalog/lessons/${encodeURIComponent(slug)}/`,
  );
});

export async function createTerminalSession(
  lessonSlug?: string,
): Promise<TerminalSession> {
  let response: Response;
  try {
    response = await fetch(`${PUBLIC_API_URL}/api/v1/terminal/sessions/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(lessonSlug ? { lesson_slug: lessonSlug } : {}),
    });
  } catch {
    throw new ApiError(
      "Could not reach the terminal service. Check that Django is running.",
      503,
    );
  }

  if (!response.ok) {
    let detail = "The terminal could not be created.";
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) detail = payload.detail;
    } catch {
      // Keep the friendly fallback.
    }
    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as TerminalSession;
}

export function getWebSocketBaseUrl(): string {
  const configured = process.env.NEXT_PUBLIC_WS_URL?.replace(/\/$/, "");
  if (configured) return configured;

  const url = new URL(PUBLIC_API_URL);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  return url.toString().replace(/\/$/, "");
}

export function buildTerminalSocketUrl(path: string): string {
  return `${getWebSocketBaseUrl()}${path}`;
}
