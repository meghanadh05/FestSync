<div align="center">

# ✨ FestSync

### AI-Powered Event Planning & Vendor Discovery Platform

[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-Auth%20%2B%20DB-3ECF8E?logo=supabase)](https://supabase.com)
[![Tests](https://img.shields.io/badge/tests-116%20passing-brightgreen)](./backend)

A full-stack AI project — Next.js 15 frontend, FastAPI backend, Supabase auth + PostgreSQL, and 5 AI agents powered by GPT-4 or Gemini.

</div>

---

## Quick Start

```bash
git clone https://github.com/meghanadh05b/festsync.git
cd festsync

chmod +x setup.sh stop.sh
./setup.sh
```

`setup.sh` copies `.env.example` files, builds Docker images, and starts all services.

For full Supabase auth + PostgreSQL integration, fill in your Supabase credentials in `backend/.env` and `frontend/.env` before running.
The backend now falls back to a local SQLite database plus mock AI settings when those values are blank, which keeps local startup and tests working out of the box.

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

```bash
./stop.sh              # stop containers
docker compose logs -f # live logs
```

---

## Features

| Feature | API |
|---|---|
| AI Event Planner | `POST /ai/events/{id}/generate-plan` |
| AI Task Generator | `POST /ai/events/{id}/generate-tasks` |
| AI Budget Advisor | `POST /ai/events/{id}/budget-advice` |
| AI Vendor Recommender | `POST /ai/events/{id}/recommend-vendors` |
| AI Chat Assistant | `POST /ai/chat` |
| Kanban Task Board (drag + optimistic) | `PATCH /tasks/{id}/status` |
| Budget Tracker (GOOD / WARNING / OVER_BUDGET) | `GET /events/{id}/budget/summary` |
| Vendor Marketplace | `GET /vendors/search` |
| Vendor Comparison | `POST /events/{id}/vendors/compare` |
| Event Dashboard | `GET /events/{id}/dashboard` |

---

## Project Structure

```
festsync/
├── frontend/          Next.js 15 app
├── backend/           FastAPI app
│   ├── app/
│   │   ├── modules/   events, tasks, budget, vendors, ai
│   │   ├── models/    SQLAlchemy ORM
│   │   └── core/      config, security, database
│   ├── migrations/    SQL files for Supabase
│   ├── scripts/       seed_demo.py
│   └── tests/unit/    116 pytest tests
├── docs/              Architecture, API spec, schema, pages
├── docker-compose.yml frontend + backend + redis
├── setup.sh           One-command startup
└── stop.sh            One-command shutdown
```

---

## Environment Variables

Copy `.env.example` files (done automatically by `setup.sh`):

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### backend/.env (key values)
| Variable | Description |
|---|---|
| `DATABASE_URL` | Supabase PostgreSQL connection string |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase anon key |
| `SUPABASE_SERVICE_KEY` | Supabase service role key (backend only) |
| `SECRET_KEY` | JWT signing secret |
| `AI_PROVIDER` | `mock` / `openai` / `gemini` (default: `mock`) |
| `OPENAI_API_KEY` | Required if `AI_PROVIDER=openai` |
| `GEMINI_API_KEY` | Required if `AI_PROVIDER=gemini` |

### frontend/.env (key values)
| Variable | Description |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key (public safe) |
| `NEXT_PUBLIC_API_URL` | Backend base URL |

---

## Local Dev (without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Seed demo data (optional)
cd backend
python scripts/seed_demo.py
```

`backend/.env` may be left mostly blank for local API development and unit tests.
When `DATABASE_URL` is empty, the backend uses `backend/festsync.db`.

---

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [API Spec](docs/API_SPEC.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [Frontend Pages](docs/FRONTEND_PAGES.md)

---

## License

MIT
