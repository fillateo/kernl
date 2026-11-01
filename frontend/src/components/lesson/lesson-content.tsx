"use client";

import { CircleCheck, Info, Lightbulb, TriangleAlert } from "lucide-react";
import type { ReactNode } from "react";

import { CommandBlock } from "@/components/lesson/command-block";
import { OutputBlock } from "@/components/lesson/output-block";
import { RichText } from "@/components/lesson/rich-text";
import type { LessonBlock } from "@/lib/types";

const CALLOUT_STYLES = {
  note: {
    wrapper: "border-sky/80 bg-sky-soft/70",
    icon: "text-[#247a9e]",
    Icon: Info,
  },
  tip: {
    wrapper: "border-[#b4d477] bg-lime/30",
    icon: "text-[#547a0a]",
    Icon: Lightbulb,
  },
  warning: {
    wrapper: "border-[#f0b3a2] bg-coral-soft/80",
    icon: "text-[#b53d26]",
    Icon: TriangleAlert,
  },
} as const;

export function LessonContent({
  blocks,
  onRun,
}: {
  blocks: LessonBlock[];
  onRun: (command: string) => void;
}) {
  return (
    <div className="lesson-prose space-y-6">
      {blocks.map((block, index) => {
        const key = `${block.type}-${index}`;
        return <Block key={key} block={block} onRun={onRun} />;
      })}
    </div>
  );
}

function Block({
  block,
  onRun,
}: {
  block: LessonBlock;
  onRun: (command: string) => void;
}): ReactNode {
  switch (block.type) {
    case "heading":
      return (
        <div className="pt-4">
          {block.eyebrow && (
            <span className="eyebrow text-violet mb-2.5 block text-[9px]">
              {block.eyebrow}
            </span>
          )}
          <h2 className="display text-ink text-[26px] leading-[1.1] font-bold tracking-[-0.045em]">
            {block.text}
          </h2>
        </div>
      );

    case "paragraph":
      return (
        <p className="text-ink/70 text-[14px] leading-7">
          <RichText text={block.text} />
        </p>
      );

    case "command":
      return <CommandBlock command={block.command} label={block.label} onRun={onRun} />;

    case "output":
      return <OutputBlock text={block.text} label={block.label} />;

    case "list":
      return block.style === "number" ? (
        <ol className="text-ink/70 space-y-2.5 text-[14px] leading-6">
          {block.items.map((item, index) => (
            <li key={index} className="flex gap-3">
              <span className="bg-ink/5 text-ink/50 mt-0.5 grid size-5 shrink-0 place-items-center rounded-full font-mono text-[9px] font-semibold">
                {index + 1}
              </span>
              <RichText text={item} />
            </li>
          ))}
        </ol>
      ) : (
        <ul className="text-ink/70 space-y-2.5 text-[14px] leading-6">
          {block.items.map((item, index) => (
            <li key={index} className="flex gap-3">
              <span className="bg-violet mt-[11px] size-1.5 shrink-0 rounded-full" />
              <RichText text={item} />
            </li>
          ))}
        </ul>
      );

    case "callout": {
      const style = CALLOUT_STYLES[block.tone ?? "note"];
      return (
        <div className={`rounded-2xl border p-4 sm:p-5 ${style.wrapper}`}>
          <div className="flex items-start gap-3">
            <style.Icon className={`mt-0.5 size-4 shrink-0 ${style.icon}`} />
            <div>
              <p className="text-ink text-[12px] font-semibold">{block.title}</p>
              <p className="text-ink/65 mt-1.5 text-[12px] leading-6">
                <RichText text={block.text} />
              </p>
            </div>
          </div>
        </div>
      );
    }

    case "checkpoint":
      return (
        <div className="border-ink bg-ink text-paper relative overflow-hidden rounded-2xl border p-5">
          <div
            className="border-lime/10 absolute -top-8 -right-8 size-28 rounded-full border-[16px]"
            aria-hidden
          />
          <div className="relative flex items-start gap-3">
            <span className="bg-lime text-ink grid size-8 shrink-0 place-items-center rounded-full">
              <CircleCheck className="size-4" strokeWidth={2.5} />
            </span>
            <div>
              <p className="text-lime font-mono text-[9px] tracking-[0.14em] uppercase">
                {block.title}
              </p>
              <p className="text-paper/80 mt-2 text-[13px] leading-6">
                <RichText text={block.text} />
              </p>
            </div>
          </div>
        </div>
      );

    case "divider":
      return <hr className="border-line" />;

    default:
      return null;
  }
}
