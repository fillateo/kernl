export default function LessonLoading() {
  return (
    <div className="lg:grid lg:h-[calc(100dvh-4rem)] lg:grid-cols-[270px_minmax(380px,520px)_minmax(0,1fr)]">
      <aside className="border-line bg-cream/60 hidden border-r p-5 lg:block">
        <div className="bg-line h-3 w-24 animate-pulse rounded" />
        <div className="bg-line mt-6 h-9 w-40 animate-pulse rounded-lg" />
        <div className="mt-8 space-y-3">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="bg-line/70 h-9 animate-pulse rounded-lg" />
          ))}
        </div>
      </aside>
      <div className="border-line bg-paper border-r p-8">
        <div className="bg-line h-3 w-32 animate-pulse rounded" />
        <div className="bg-line mt-6 h-10 w-4/5 animate-pulse rounded-lg" />
        <div className="bg-line/80 mt-4 h-4 w-full animate-pulse rounded" />
        <div className="bg-line/60 mt-10 h-28 animate-pulse rounded-2xl" />
        <div className="bg-line/60 mt-10 h-20 animate-pulse rounded-2xl" />
      </div>
      <div className="bg-terminal h-[68vh] min-h-[480px] animate-pulse lg:h-full lg:min-h-0">
        <div className="border-terminal-line flex h-12 items-center gap-2 border-b px-4">
          <div className="size-6 rounded bg-white/10" />
          <div className="h-3 w-20 rounded bg-white/10" />
        </div>
      </div>
    </div>
  );
}
