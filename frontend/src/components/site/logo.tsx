import Link from "next/link";

export function Logo({
  compact = false,
  onClick,
}: {
  compact?: boolean;
  onClick?: () => void;
}) {
  return (
    <Link
      href="/"
      className="group inline-flex items-center gap-2.5"
      aria-label="Kernl home"
      onClick={onClick}
    >
      <span className="border-ink/10 bg-ink text-lime grid size-9 place-items-center rounded-[10px] border shadow-[0_3px_0_0_rgb(23_23_44_/_0.14)] transition-transform duration-200 group-hover:-rotate-3">
        <span className="font-mono text-[13px] leading-none font-bold tracking-[-0.12em]">
          &gt;_
        </span>
      </span>
      {!compact && (
        <span className="display text-[21px] leading-none font-bold tracking-[-0.05em]">
          kernl<span className="text-coral">.</span>
        </span>
      )}
    </Link>
  );
}
