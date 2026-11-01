# Kernl

**Learn the terminal by actually using it.**

A local-first, Codecademy-style learning app with a real Linux terminal in the
browser. Three pages, real bash, no sign-up, and no external shell service.

![Kernl lesson workspace](docs/screenshots/lesson.png)

## What it is

Kernl pairs short, guided lessons with an ephemeral Linux sandbox. The learner
reads an explanation, runs the command from the lesson, and sees real output
from a real shell—not a simulation or a recorded video.

The challenge scope is intentionally tight:

- **3 pages:** `/` (catalog), `/courses/[slug]` (syllabus), `/learn/[slug]`
  (lesson + terminal).
- **No authentication:** no sign-in, sign-up, accounts, or learner database.
- **No external backend services:** SQLite, in-memory Channels, and a local
  bubblewrap sandbox. No AWS, Google Cloud, hosted Redis, or remote terminal.
- **Tests wired into CI:** Django/Channels tests, Next.js unit tests, and
  Playwright browser tests.

### Screenshots

| Course library | Course syllabus |
| --- | --- |
| ![Course library](docs/screenshots/home.png) | ![Course syllabus](docs/screenshots/course.png) |

## Stack

| Layer | Choice |
| --- | --- |
| Backend | Django 5.2 LTS, Django REST Framework, Channels 4, Daphne |
| Frontend | Next.js 16 App Router, React 19, TypeScript, Tailwind CSS 4 |
| Terminal | xterm.js 6 + WebSockets + a real PTY + bubblewrap |
| Persistence | SQLite by default; any `DATABASE_URL` supported by Django |
| Tests | pytest, pytest-django, pytest-asyncio, Vitest, Testing Library, Playwright |
| CI | GitHub Actions |

## Quickstart

### Prerequisites

- Python **3.13+**
- Node.js **22+**
- [`bubblewrap`](https://github.com/containers/bubblewrap) (`bwrap`)

On Debian/Ubuntu:

```bash
sudo apt-get install bubblewrap
```

`bubblewrap` is not optional for the interactive terminal. The catalog still
loads without it, but the terminal fails closed rather than running an
unconfined shell. This is intentional.

### One command

```bash
make setup   # venv + Python deps + npm ci + migrations + seed data
make dev     # Django on :8000 and Next.js on :3000
```

Open **http://localhost:3000**.

### Manual setup

```bash
# Backend
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements-dev.txt
cd backend
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_catalog --prune
.venv/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Frontend (another terminal)
cd frontend
npm ci
npm run dev
```

No `.env` file is required for the default local setup. Copy
`backend/.env.example` or `frontend/.env.example` if you need overrides.

## How the terminal works

```
Browser
  Next.js App Router
    ├── GET catalog / lesson content ────────┐
    │                                        v
    │                                  Django REST API
    │                                        │
    │  POST /api/v1/terminal/sessions/       │
    │  → single-use ticket, 30 min TTL       │
    │                                        │
    └── WebSocket /ws/terminal/<uuid>/       │
              │                              │
              v                              │
        Django Channels consumer ────────────┘
              │
              ├── validates origin
              ├── claims ticket exactly once
              ├── spawns PTY + bubblewrap bash
              ├── streams bytes ↔ xterm.js
              └── kills the process group + deletes the workspace
```

1. The lesson page mounts xterm.js and requests a terminal ticket over HTTP.
2. The ticket is a UUID with a short TTL and is stored in SQLite.
3. The browser opens a WebSocket with that UUID.
4. `TerminalConsumer` validates the origin, atomically claims the ticket, and
   starts a PTY-backed bash process inside a bubblewrap sandbox.
5. Output and input are JSON-framed. Resize events keep the PTY in sync with
   xterm.js.
6. On disconnect, idle timeout, or maximum lifetime, the process group is
   killed and the session directory is deleted.

### WebSocket protocol

Client → server:

```json
{"type": "input", "data": "ls -la\r"}
{"type": "resize", "cols": 120, "rows": 32}
{"type": "ping"}
```

Server → client:

```json
{"type": "ready", "cwd": "/home/learner"}
{"type": "output", "data": "README.md  projects\r\n"}
{"type": "error", "code": "idle_timeout", "message": "..."}
{"type": "exit", "code": 0}
{"type": "pong"}
```

## Sandbox security model

This is a **single-user, local-first** application. There is deliberately no
authentication, so the development server binds to `127.0.0.1` by default.

The shell is isolated with bubblewrap:

- `--unshare-all`: private user, PID, network, IPC, UTS, and cgroup namespaces.
- Network access is unshared; outbound connections fail.
- `/usr`, `/bin`, `/lib`, and a minimal `/etc` are mounted **read-only**.
- Only `/home/learner` is writable. Every lesson starts with its own seeded
  files and the directory is deleted when the session ends.
- The host home directory, `/etc` secrets, Docker socket, and project source are
  not mounted inside the sandbox.
- `--die-with-parent` plus process-group cleanup prevents orphaned shells.
- Resource limits: 8 MB max file, 128 file descriptors, 2 MB output per session,
  10 min idle timeout, 20 min maximum lifetime.
- Server-side guardrails: single-use tickets, origin validation, a global
  session cap, and per-IP ticket throttling.

**Do not expose this app directly to the public internet.** Running arbitrary
commands for anonymous users requires authentication, per-user quotas, a
separate sandbox host, auditing, and a defensive reverse proxy. The local
sandbox is appropriate for the challenge and for local learning; it is not a
multi-tenant hosting design.

The only data persisted about a terminal is a UUID, timestamps, and a close
reason. Input and output are never written to the database.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health/` | Database and sandbox health |
| `GET` | `/api/v1/catalog/courses/` | Published courses |
| `GET` | `/api/v1/catalog/courses/<slug>/` | Course + modules + lessons |
| `GET` | `/api/v1/catalog/lessons/<slug>/` | Lesson content + prev/next |
| `POST` | `/api/v1/terminal/sessions/` | Create a one-time terminal ticket |

Example:

```bash
curl -s http://127.0.0.1:8000/api/health/
curl -s http://127.0.0.1:8000/api/v1/catalog/courses/ | jq
curl -s -X POST http://127.0.0.1:8000/api/v1/terminal/sessions/ \
  -H 'Content-Type: application/json' \
  -d '{"lesson_slug":"working-with-linux-commands"}' | jq
```

## Tests

```bash
make test          # backend + frontend
make lint          # Ruff, ESLint, TypeScript, Prettier
make e2e-install  # once per machine
make e2e           # Playwright (starts both servers)
```

Current suites:

- **19 backend tests** covering the catalog API, session issuing, ticket
  lifecycle, origin rejection, WebSocket I/O, input validation, and real
  bubblewrap isolation (network + filesystem).
- **10 frontend tests** covering content rendering, XSS-safe rich text, command
  execution wiring, course cards, and URL/format helpers.
- **2 Playwright tests** covering the full three-page navigation flow and a real
  command round-trip through xterm.js and the sandbox.

The E2E terminal test automatically skips when the host cannot run bubblewrap.
Backend sandbox tests do the same, so the suite remains portable.

### CI

`.github/workflows/ci.yml` runs three jobs on every push and pull request:

1. **Backend** — Ruff, Django checks, migration drift check, pytest with
   coverage, artifact upload.
2. **Frontend** — npm install from lockfile, ESLint, TypeScript, Vitest, Prettier
   check, and a production Next.js build.
3. **E2E** — installs Chromium, starts Django + Next.js, and runs Playwright.

No hosted services or secrets are required. Tests use SQLite and the in-memory
Channels layer.

## Configuration

### Backend

| Variable | Default | Notes |
| --- | --- | --- |
| `DJANGO_DEBUG` | `true` | Use `false` in production |
| `DJANGO_SECRET_KEY` | dev-only value | Change outside local development |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Also used for WebSocket origins |
| `DATABASE_URL` | `sqlite:///backend/db.sqlite3` | Any Django-supported database |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000,...` | Browser origin for ticket POSTs |
| `TERMINAL_SESSION_TTL_SECONDS` | `1800` | Time allowed to claim a ticket |
| `TERMINAL_IDLE_TIMEOUT_SECONDS` | `600` | No-input timeout |
| `TERMINAL_MAX_LIFETIME_SECONDS` | `1200` | Hard session cap |
| `TERMINAL_MAX_SESSIONS` | `25` | Global concurrent ticket cap |
| `TERMINAL_SESSION_THROTTLE` | `20/min` | DRF throttle for ticket creation |

### Frontend

| Variable | Default | Notes |
| --- | --- | --- |
| `API_URL` | `http://127.0.0.1:8000` | Server-side catalog fetches |
| `NEXT_PUBLIC_API_URL` | `http://127.0.0.1:8000` | Browser ticket POST |
| `NEXT_PUBLIC_WS_URL` | derived from API URL | WebSocket origin override |

## Course content

The catalog lives in `backend/apps/catalog/seed_data.py` so it can be reviewed
and versioned with the code. The seed command is idempotent:

```bash
cd backend
.venv/bin/python manage.py seed_catalog --prune
```

To edit content through Django admin:

```bash
cd backend
.venv/bin/python manage.py createsuperuser
# visit http://127.0.0.1:8000/admin/
```

Three tracks are included: **Linux Foundations**, **Git Essentials**, and
**Bash Scripting**—10 guided lessons with per-lesson starter files.

## Project layout

```text
backend/
  config/                    Django settings, ASGI, URLs
  apps/catalog/              Courses, modules, lessons, API, seed data
  apps/terminal/             Session tickets, Channels consumer, bwrap PTY
  tests/                     API + WebSocket + real-shell integration tests
frontend/
  src/app/(site)/            Home + course pages
  src/app/(lesson)/          Lesson workspace
  src/components/lesson/     xterm panel, command blocks, lesson renderer
  src/lib/                   Typed API client, content types, design tokens
  e2e/                       Playwright flows
```

## Design decisions & tradeoffs

- **bubblewrap, not Docker.** No daemon or image pull is needed, and the
  namespace boundary is created per session. The tradeoff is a Linux-only host
  requirement.
- **Real PTY, not a fake shell.** Commands, colors, job control, history, and
  signals behave like a terminal because it is a terminal.
- **Direct WebSocket rather than proxying through Next.js.** This keeps the
  Channels consumer simple and avoids buffering issues in the Node layer. CORS
  and origin validation are configured explicitly.
- **SQLite + in-memory Channels.** Perfect for a local single-process app. For
  multiple ASGI workers, replace the channel layer with a local Redis instance.
- **No auth.** Deliberate challenge constraint. The app is not intended to be
  exposed publicly.
- **Progress is not persisted.** The progress bar reflects lesson position, not
  a learner account. No account or progress data is stored.

## License

MIT
