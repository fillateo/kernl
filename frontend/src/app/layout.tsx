import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";

import "@fontsource-variable/inter";
import "@fontsource-variable/jetbrains-mono";
import "@fontsource-variable/space-grotesk";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Kernl — Learn the terminal by doing",
    template: "%s · Kernl",
  },
  description:
    "A local-first, browser-based Linux lab. Learn the command line with real sandboxed terminals, guided lessons, and no setup.",
  applicationName: "Kernl",
  keywords: [
    "Linux",
    "terminal",
    "command line",
    "learn bash",
    "Git",
    "interactive course",
  ],
};

export const viewport: Viewport = {
  colorScheme: "light",
  themeColor: "#f5f1e7",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body>{children}</body>
    </html>
  );
}
