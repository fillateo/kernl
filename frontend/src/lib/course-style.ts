import type { CourseAccent } from "@/lib/types";

interface AccentStyle {
  panel: string;
  panelText: string;
  panelMuted: string;
  badge: string;
  accentText: string;
  soft: string;
  border: string;
  icon: string;
  ring: string;
}

export const ACCENT_STYLES: Record<CourseAccent, AccentStyle> = {
  lime: {
    panel: "bg-lime",
    panelText: "text-ink",
    panelMuted: "text-ink/65",
    badge: "bg-ink text-lime",
    accentText: "text-[#547a0a]",
    soft: "bg-[#eef8d8]",
    border: "border-[#c5dc91]",
    icon: "bg-ink text-lime",
    ring: "ring-ink/10",
  },
  violet: {
    panel: "bg-violet",
    panelText: "text-white",
    panelMuted: "text-white/70",
    badge: "bg-white text-violet",
    accentText: "text-violet",
    soft: "bg-violet-soft",
    border: "border-[#c9c2ff]",
    icon: "bg-white text-violet",
    ring: "ring-white/20",
  },
  coral: {
    panel: "bg-coral",
    panelText: "text-ink",
    panelMuted: "text-ink/65",
    badge: "bg-ink text-coral",
    accentText: "text-[#b53d26]",
    soft: "bg-coral-soft",
    border: "border-[#f3b9aa]",
    icon: "bg-ink text-coral",
    ring: "ring-ink/10",
  },
  sky: {
    panel: "bg-sky",
    panelText: "text-ink",
    panelMuted: "text-ink/65",
    badge: "bg-ink text-sky",
    accentText: "text-[#1c729b]",
    soft: "bg-sky-soft",
    border: "border-[#b8def2]",
    icon: "bg-ink text-sky",
    ring: "ring-ink/10",
  },
};

export const LEVEL_LABEL: Record<string, string> = {
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced",
};
