# FestSync — Architecture

## Overview

FestSync is a full-stack AI-powered event planning platform. The frontend (Next.js 15) communicates with a FastAPI backend via REST, authenticated with Supabase JWT tokens. PostgreSQL (Supabase hosted) is the primary data store.

---

## System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Next.js 15)                      │
│                                                                 │
│  /              Landing page                                    │
│  /login         Supabase Auth                                   │
│  /signup        Supabase Auth                                   │
│  /dashboard     Stats overview                                  │
│  /events        Event list                                      │
│  /events/[id]   Event dashboard                                 │
│  /vendors       Vendor marketplace                              │
│                                                                 │
│  lib/api.ts ─── Bearer JWT ──────────────────────────────────►  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/JSON
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│                                                                 │
│  /api/v1/events        CRUD + dashboard aggregate              │
│  /api/v1/tasks         CRUD + Kanban status                    │
│  /api/v1/budget        CRUD + health summary                   │
│  /api/v1/vendors       Search + save + compare                 │
│  /api/v1/ai            5 AI agents                             │
│                                                                 │
│  JWT verification → user_id ownership enforcement              │
└──────────────────────────────┬──────────────────────────────────┘
                               │ SQLAlchemy ORM
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATABASE (PostgreSQL / Supabase)               │
│                                                                 │
│  events  tasks  subtasks  budget_items                         │
│  vendors  vendor_services  saved_vendors                       │
│  ai_generations                                                │
│                                                                 │
│  Row-Level Security: users access only their own data          │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI LAYER                                   │
│                                                                 │
│  MockProvider   — instant responses, no API key required       │
│  OpenAIProvider — gpt-4o-mini, JSON mode                       │
│  GeminiProvider — gemini-1.5-flash, JSON mime type             │
│                                                                 │
│  All outputs validated with Pydantic before DB write           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 App Router, React 19, Tailwind CSS, Framer Motion |
| State | TanStack Query (server), Zustand (UI) |
| Forms | React Hook Form + Zod |
| Auth | Supabase JS (browser client) |
| Backend | FastAPI, Pydantic v2, SQLAlchemy 2 |
| Database | PostgreSQL via Supabase |
| AI | OpenAI GPT-4o-mini / Google Gemini 1.5 Flash |
| Cache | Redis |
| CI | GitHub Actions |
| Container | Docker + Docker Compose |

---

## Data Flow — Event Creation

```
User fills wizard → POST /api/v1/events
  → JWT verified → user_id extracted
  → Pydantic validates body
  → SQLAlchemy inserts row
  → 201 response → TanStack Query cache updated
```

## Data Flow — AI Plan Generation

```
User clicks "Generate Plan" → POST /api/v1/ai/events/{id}/generate-plan
  → Event fetched from DB → context built
  → Provider.complete(system_prompt, user_prompt)
  → JSON parsed → Pydantic validated
  → Saved to ai_generations table
  → 201 response with structured plan
```
