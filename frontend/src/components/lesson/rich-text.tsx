import type { ReactNode } from "react";

/**
 * A deliberately tiny inline renderer. Backticks become <code>; everything
 * else is rendered as plain text, so lesson content can never inject HTML.
 */
export function RichText({
  text,
  className,
}: {
  text: string;
  className?: string;
}): ReactNode {
  const parts = text.split(/(`[^`]+`)/g);

  return (
    <span className={className}>
      {parts.map((part, index) => {
        if (part.startsWith("`") && part.endsWith("`") && part.length > 2) {
          return <code key={index}>{part.slice(1, -1)}</code>;
        }
        return <span key={index}>{part}</span>;
      })}
    </span>
  );
}
