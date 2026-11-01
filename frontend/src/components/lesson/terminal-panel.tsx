"use client";

import "@xterm/xterm/css/xterm.css";

import type { FitAddon } from "@xterm/addon-fit";
import type { Terminal } from "@xterm/xterm";
import { Eraser, Loader2, RefreshCw, TerminalSquare, WifiOff } from "lucide-react";
import {
  forwardRef,
  useCallback,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";

import { buildTerminalSocketUrl, createTerminalSession } from "@/lib/api";

export interface TerminalHandle {
  runCommand: (command: string) => void;
  clear: () => void;
  focus: () => void;
}

type TerminalStatus = "connecting" | "ready" | "closed" | "error";

interface TerminalMessage {
  type: "ready" | "output" | "pong" | "error" | "exit";
  data?: string;
  code?: string | number;
  message?: string;
}

const STATUS_LABELS: Record<TerminalStatus, string> = {
  connecting: "Connecting",
  ready: "Connected",
  closed: "Disconnected",
  error: "Unavailable",
};

const STATUS_DOT: Record<TerminalStatus, string> = {
  connecting: "bg-amber-400",
  ready: "bg-emerald-400",
  closed: "bg-slate-500",
  error: "bg-coral",
};

const TERMINAL_THEME = {
  background: "#14152b",
  foreground: "#e5e6f3",
  cursor: "#cbff67",
  cursorAccent: "#14152b",
  selectionBackground: "#3b3c66",
  black: "#262742",
  red: "#ff7a66",
  green: "#bdf27a",
  yellow: "#ffd479",
  blue: "#8ecbff",
  magenta: "#c2a5ff",
  cyan: "#7ce7d8",
  white: "#e5e6f3",
  brightBlack: "#737492",
  brightRed: "#ff9a8b",
  brightGreen: "#d4ff9c",
  brightYellow: "#ffe3a3",
  brightBlue: "#b6e0ff",
  brightMagenta: "#d8c4ff",
  brightCyan: "#a5f4e8",
  brightWhite: "#ffffff",
};

export const TerminalPanel = forwardRef<
  TerminalHandle,
  { lessonSlug: string; className?: string }
>(function TerminalPanel({ lessonSlug, className = "" }, ref) {
  const containerRef = useRef<HTMLDivElement>(null);
  const terminalRef = useRef<Terminal | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const statusRef = useRef<TerminalStatus>("connecting");
  const pendingCommandRef = useRef<string | null>(null);
  const [status, setStatus] = useState<TerminalStatus>("connecting");
  const [error, setError] = useState<string | null>(null);
  const [sessionKey, setSessionKey] = useState(0);

  const updateStatus = useCallback((next: TerminalStatus) => {
    statusRef.current = next;
    setStatus(next);
  }, []);

  const sendInput = useCallback((data: string) => {
    const socket = socketRef.current;
    if (socket?.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ type: "input", data }));
      return true;
    }
    return false;
  }, []);

  useImperativeHandle(
    ref,
    () => ({
      runCommand(command: string) {
        if (statusRef.current === "ready" && sendInput(`${command}\r`)) {
          terminalRef.current?.focus();
          return;
        }
        pendingCommandRef.current = command;
        terminalRef.current?.focus();
      },
      clear() {
        terminalRef.current?.clear();
        terminalRef.current?.focus();
      },
      focus() {
        terminalRef.current?.focus();
      },
    }),
    [sendInput],
  );

  useEffect(() => {
    let disposed = false;
    let socket: WebSocket | null = null;
    let observer: ResizeObserver | null = null;
    let resizeFrame = 0;
    let term: Terminal | null = null;
    let fit: FitAddon | null = null;
    let activeSocket: WebSocket | null = null;

    updateStatus("connecting");
    setError(null);

    const sendResize = () => {
      if (!term || !activeSocket || activeSocket.readyState !== WebSocket.OPEN) {
        return;
      }
      activeSocket.send(
        JSON.stringify({
          type: "resize",
          cols: term.cols,
          rows: term.rows,
        }),
      );
    };

    const scheduleFit = () => {
      window.cancelAnimationFrame(resizeFrame);
      resizeFrame = window.requestAnimationFrame(() => {
        if (!fit || !term || disposed) return;
        try {
          fit.fit();
        } catch {
          return;
        }
        sendResize();
      });
    };

    const boot = async () => {
      const [{ Terminal: Xterm }, { FitAddon: XtermFitAddon }, { WebLinksAddon }] =
        await Promise.all([
          import("@xterm/xterm"),
          import("@xterm/addon-fit"),
          import("@xterm/addon-web-links"),
        ]);

      if (disposed || !containerRef.current) return;

      term = new Xterm({
        allowProposedApi: false,
        convertEol: true,
        cursorBlink: true,
        cursorStyle: "block",
        fontFamily:
          '"JetBrains Mono Variable", ui-monospace, SFMono-Regular, monospace',
        fontSize: 13,
        fontWeight: "400",
        fontWeightBold: "600",
        letterSpacing: 0,
        lineHeight: 1.4,
        scrollback: 4000,
        theme: TERMINAL_THEME,
      });
      fit = new XtermFitAddon();
      term.loadAddon(fit);
      term.loadAddon(new WebLinksAddon());
      term.open(containerRef.current);
      try {
        fit.fit();
      } catch {
        // The panel may not have dimensions during the first paint.
      }
      term.textarea?.setAttribute(
        "aria-label",
        "Interactive sandbox terminal. Type a command and press Enter.",
      );
      terminalRef.current = term;
      term.onData((data) => {
        sendInput(data);
      });

      observer = new ResizeObserver(scheduleFit);
      observer.observe(containerRef.current);
      window.addEventListener("resize", scheduleFit);
      if (document.fonts) {
        void document.fonts.ready.then(() => {
          if (!disposed) scheduleFit();
        });
      }

      let session;
      try {
        session = await createTerminalSession(lessonSlug);
      } catch (sessionError) {
        if (disposed) return;
        const message =
          sessionError instanceof Error
            ? sessionError.message
            : "The terminal service could not be reached.";
        setError(message);
        updateStatus("error");
        term.writeln(`\x1b[31m${message}\x1b[0m`);
        return;
      }

      if (disposed) return;

      socket = new WebSocket(buildTerminalSocketUrl(session.websocket_path));
      activeSocket = socket;
      socketRef.current = socket;

      socket.onopen = () => {
        sendResize();
      };

      socket.onmessage = (event) => {
        let message: TerminalMessage;
        try {
          message = JSON.parse(event.data as string) as TerminalMessage;
        } catch {
          return;
        }

        switch (message.type) {
          case "ready": {
            updateStatus("ready");
            sendResize();
            const pending = pendingCommandRef.current;
            pendingCommandRef.current = null;
            if (pending) sendInput(`${pending}\r`);
            term?.focus();
            break;
          }
          case "output":
            if (message.data) term?.write(message.data);
            break;
          case "error": {
            const text = message.message ?? "The terminal encountered an error.";
            setError(text);
            updateStatus("error");
            term?.write(`\r\n\x1b[31m${text}\x1b[0m\r\n`);
            break;
          }
          case "exit":
            updateStatus("closed");
            term?.writeln("\r\n\x1b[2mSession ended.\x1b[0m");
            break;
          case "pong":
            break;
        }
      };

      socket.onerror = () => {
        if (disposed) return;
        setError("The terminal connection was interrupted.");
        updateStatus("error");
      };

      socket.onclose = (event) => {
        if (disposed) return;
        if (statusRef.current === "ready") {
          updateStatus("closed");
          if (event.code !== 1000 && event.code !== 1005) {
            term?.writeln(
              `\r\n\x1b[2mConnection closed (${event.code}). Start a new session to continue.\x1b[0m`,
            );
          }
          return;
        }
        if (statusRef.current === "connecting") {
          setError(
            "The connection closed before the sandbox was ready. Is the Django server running?",
          );
          updateStatus("error");
        }
      };
    };

    boot().catch((bootError) => {
      if (disposed) return;
      const message =
        bootError instanceof Error
          ? bootError.message
          : "The terminal could not be started.";
      setError(message);
      updateStatus("error");
    });

    return () => {
      disposed = true;
      window.cancelAnimationFrame(resizeFrame);
      window.removeEventListener("resize", scheduleFit);
      observer?.disconnect();
      if (socket && socket.readyState < WebSocket.CLOSING) {
        socket.close(1000, "Leaving lesson");
      }
      socketRef.current = null;
      try {
        term?.dispose();
      } catch {
        // Already disposed.
      }
      term = null;
      fit = null;
      terminalRef.current = null;
    };
  }, [lessonSlug, sessionKey, sendInput, updateStatus]);

  const restart = () => {
    setError(null);
    updateStatus("connecting");
    setSessionKey((value) => value + 1);
  };

  return (
    <section
      className={`bg-terminal text-paper flex min-h-0 flex-col overflow-hidden ${className}`}
      aria-label="Interactive terminal panel"
    >
      <div className="border-terminal-line flex h-12 shrink-0 items-center gap-3 border-b bg-[#111226] px-4">
        <div className="flex items-center gap-2">
          <span className="grid size-6 place-items-center rounded-md bg-white/[0.06]">
            <TerminalSquare className="text-lime size-3.5" />
          </span>
          <span className="text-paper text-[11px] font-semibold">Terminal</span>
          <span className="border-terminal-line text-terminal-muted rounded border px-1.5 py-0.5 font-mono text-[8px] tracking-[0.1em] uppercase">
            bash
          </span>
        </div>
        <div className="ml-auto flex items-center gap-1">
          <span
            className="text-terminal-muted mr-2 hidden items-center gap-1.5 font-mono text-[8px] tracking-[0.12em] uppercase sm:inline-flex"
            aria-live="polite"
          >
            <span
              className={`size-1.5 rounded-full ${STATUS_DOT[status]}`}
              aria-hidden
            />
            {STATUS_LABELS[status]}
          </span>
          <button
            type="button"
            onClick={() => {
              terminalRef.current?.clear();
              terminalRef.current?.focus();
            }}
            className="text-terminal-muted hover:text-paper grid size-7 place-items-center rounded-md transition-colors hover:bg-white/[0.06]"
            aria-label="Clear terminal"
            title="Clear terminal"
          >
            <Eraser className="size-3.5" />
          </button>
          <button
            type="button"
            onClick={restart}
            className="text-terminal-muted hover:text-paper grid size-7 place-items-center rounded-md transition-colors hover:bg-white/[0.06]"
            aria-label="Start a new terminal session"
            title="New session"
          >
            <RefreshCw className="size-3.5" />
          </button>
        </div>
      </div>

      <div className="relative min-h-0 flex-1">
        <div
          ref={containerRef}
          className="terminal-shell absolute inset-0 overflow-hidden"
          onClick={() => terminalRef.current?.focus()}
        />

        {status === "connecting" && (
          <div className="pointer-events-none absolute inset-x-0 top-4 flex justify-center">
            <span className="border-terminal-line text-terminal-muted inline-flex items-center gap-2 rounded-full border bg-[#111226]/90 px-3 py-1.5 font-mono text-[9px] tracking-[0.12em] uppercase shadow-lg backdrop-blur">
              <Loader2 className="text-lime size-3 animate-spin" />
              Starting sandbox
            </span>
          </div>
        )}

        {status === "error" && error && (
          <div className="bg-terminal/75 absolute inset-0 grid place-items-center p-6 backdrop-blur-[2px]">
            <div className="border-terminal-line bg-terminal-soft max-w-sm rounded-2xl border p-5 text-center shadow-2xl">
              <span className="bg-coral/15 text-coral mx-auto grid size-10 place-items-center rounded-full">
                <WifiOff className="size-5" />
              </span>
              <p className="mt-3 text-[13px] font-semibold">Terminal unavailable</p>
              <p className="text-terminal-muted mt-1.5 text-[11px] leading-5">
                {error}
              </p>
              <button
                type="button"
                onClick={restart}
                className="bg-lime text-ink hover:bg-lime-bright mt-4 inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-[11px] font-semibold transition-colors"
              >
                <RefreshCw className="size-3" />
                Try a new session
              </button>
            </div>
          </div>
        )}

        {status === "closed" && !error && (
          <div className="absolute inset-x-0 bottom-4 flex justify-center">
            <button
              type="button"
              onClick={restart}
              className="border-terminal-line text-terminal-muted hover:text-paper inline-flex items-center gap-2 rounded-full border bg-[#111226]/90 px-3.5 py-2 font-mono text-[9px] tracking-[0.1em] uppercase shadow-lg backdrop-blur transition-colors"
            >
              <RefreshCw className="size-3" />
              Start a new session
            </button>
          </div>
        )}
      </div>

      <div className="border-terminal-line text-terminal-muted flex h-9 shrink-0 items-center gap-4 border-t bg-[#111226] px-4 font-mono text-[8px] tracking-[0.12em] uppercase">
        <span className="inline-flex items-center gap-1.5">
          <span className="size-1.5 rounded-full bg-emerald-400" />
          Local
        </span>
        <span className="hidden sm:inline">/home/learner</span>
        <span className="ml-auto inline-flex items-center gap-1.5">
          <WifiOff className="size-2.5" />
          No network
        </span>
        <span>UTF-8</span>
      </div>
    </section>
  );
});
