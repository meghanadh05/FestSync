# FestSync — Frontend Pages

Framework: Next.js 15 App Router.
All dashboard pages require Supabase auth. Public pages: `/`, `/login`, `/signup`, `/vendors/search`.

---

## Route Map

```
/                          Landing page
/login                     Sign in with Supabase Auth
/signup                    Create account

/dashboard                 Overview: stats, upcoming events, quick actions
/events                    Event list with search
/events/create             6-step event creation wizard
/events/[id]               Event dashboard (days left, tasks %, budget %)
/events/[id]/tasks         Kanban board (Pending / In Progress / Done)
/events/[id]/budget        Budget items + health summary + AI advice
/events/[id]/vendors       Saved vendors for this event

/vendors                   Vendor marketplace with filters
```

---

## Page Details

### `/` — Landing
- Hero with gradient, stat counters (9 event types, 5 AI agents, 116 tests)
- Features grid (6 cards)
- How it works (4 steps)
- Tech stack grid
- Testimonials
- CTA section

### `/login` and `/signup`
- React Hook Form + Zod validation
- Supabase `signInWithPassword` / `signUp`
- Redirects to `/dashboard` on success

### `/dashboard`
- Fetches: `GET /events` (all user events)
- KPI strip: total events, active plans, total budget, completed count
- Upcoming events list (sorted by date)
- Quick action links

### `/events`
- Fetches: `GET /events?search=...`
- Event cards with status badge, days remaining, location, budget
- Empty state with create CTA

### `/events/create`
- 6-step wizard using Zustand `event-store`
- Step 1: Event type (icon grid)
- Step 2: Title + description
- Step 3: Date + location
- Step 4: Budget + guests
- Step 5: Theme selection
- Step 6: Review + submit → `POST /events`

### `/events/[id]`
- Fetches: `GET /events/{id}/dashboard`
- KPI cards: days remaining, tasks done, budget spent, vendors saved
- Progress bar
- Navigation tabs → tasks, budget, vendors

### `/events/[id]/tasks`
- Fetches: `GET /events/{id}/tasks?group_by_status=true`
- Drag-and-drop Kanban with optimistic status updates
- "AI Generate" → `POST /ai/events/{id}/generate-tasks` then bulk-creates tasks
- Add task dialog

### `/events/[id]/budget`
- Fetches: `GET /events/{id}/budget` + `GET /events/{id}/budget/summary`
- Health banner (GOOD / WARNING / OVER_BUDGET)
- Line items with planned vs actual progress bars
- "AI Advice" → `POST /ai/events/{id}/budget-advice` → modal with split

### `/events/[id]/vendors`
- Fetches: `GET /events/{id}/vendors/saved`
- Saved vendor cards with unsave button
- Link to marketplace

### `/vendors`
- Fetches: `GET /vendors/search?category=...&location=...`
- Filter bar: category, rating, verified toggle
- Vendor cards with match score bar
- Save → `POST /events/{id}/vendors/save`

---

## Shared Components

| Component | Path | Purpose |
|-----------|------|---------|
| `Topbar` | `components/layout/topbar.tsx` | Live Supabase user, theme toggle |
| `Sidebar` | `components/layout/sidebar.tsx` | Nav links |
| `AIAssistantDrawer` | `components/ai/ai-assistant-drawer.tsx` | Chat + quick actions |
| `EmptyState` | `components/ui/empty-state.tsx` | Reusable empty state |
| `ErrorState` | `components/ui/error-state.tsx` | Error + retry |
| `StatCard` | `components/ui/stat-card.tsx` | KPI card with skeleton |
| `PageHeader` | `components/ui/page-header.tsx` | Title + breadcrumb + action |

---

## State Management

| Store | File | Holds |
|-------|------|-------|
| `useUIStore` | `store/ui-store.ts` | sidebar open/closed, theme |
| `useEventStore` | `store/event-store.ts` | wizard form state, selected event |

TanStack Query hooks in `hooks/` handle all server state.
