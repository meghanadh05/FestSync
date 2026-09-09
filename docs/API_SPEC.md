# FestSync — API Specification

Base URL: `http://localhost:8000/api/v1`
Auth: `Authorization: Bearer <supabase_jwt>` on all endpoints except search/get vendor.
Interactive docs: `http://localhost:8000/docs`

---

## Health

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | API health check |
| GET | `/` | No | Root info |

---

## Events

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/events` | Yes | List user's events |
| POST | `/events` | Yes | Create event |
| GET | `/events/{id}` | Yes | Get event |
| PATCH | `/events/{id}` | Yes | Update event |
| DELETE | `/events/{id}` | Yes | Soft-delete event |
| GET | `/events/{id}/dashboard` | Yes | Aggregate stats |

### Create event body
```json
{
  "title": "string",
  "event_type": "WEDDING|BIRTHDAY|COLLEGE_FEST|CORPORATE_EVENT|CONFERENCE|RECEPTION|ENGAGEMENT|CONCERT|OTHER",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "location": "string",
  "estimated_guests": 0,
  "budget": 0,
  "currency": "INR"
}
```

---

## Tasks

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/events/{id}/tasks` | Yes | List tasks (`?group_by_status=true` for Kanban) |
| POST | `/events/{id}/tasks` | Yes | Create task |
| GET | `/tasks/{id}` | Yes | Get task |
| PATCH | `/tasks/{id}` | Yes | Update task |
| DELETE | `/tasks/{id}` | Yes | Delete task |
| PATCH | `/tasks/{id}/status` | Yes | Update status only |
| POST | `/tasks/{id}/subtasks` | Yes | Add subtask |
| PATCH | `/subtasks/{id}` | Yes | Update subtask |

---

## Budget

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/events/{id}/budget` | Yes | List budget items |
| POST | `/events/{id}/budget` | Yes | Create item |
| PATCH | `/budget/{id}` | Yes | Update item |
| DELETE | `/budget/{id}` | Yes | Delete item |
| GET | `/events/{id}/budget/summary` | Yes | Health + totals |

### Budget health status values
- `GOOD` — actual ≤ 80% of total budget
- `WARNING` — actual 80–100%
- `OVER_BUDGET` — actual > total budget

---

## Vendors

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vendors/search` | No | Search vendors |
| GET | `/vendors/{id}` | No | Get vendor |
| POST | `/vendors` | Yes | Create vendor profile |
| PATCH | `/vendors/{id}` | Yes (owner) | Update vendor |
| POST | `/vendors/{id}/services` | Yes (owner) | Add service |
| GET | `/vendors/{id}/services` | No | List services |
| POST | `/events/{id}/vendors/save` | Yes | Save vendor to event |
| GET | `/events/{id}/vendors/saved` | Yes | List saved vendors |
| DELETE | `/events/{id}/vendors/{vid}/unsave` | Yes | Remove saved vendor |
| POST | `/events/{id}/vendors/compare` | Yes | Compare 2–4 vendors |

### Search query params
`category`, `location`, `event_type`, `min_price`, `max_price`, `min_rating`, `verified_only`, `skip`, `limit`

---

## AI

All AI endpoints require auth. AI runs in `mock` mode by default.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/ai/events/{id}/generate-plan` | Generate full event plan |
| POST | `/ai/events/{id}/generate-tasks` | Generate task list |
| POST | `/ai/events/{id}/budget-advice` | Budget allocation advice |
| POST | `/ai/events/{id}/recommend-vendors` | Rank vendors by fit |
| POST | `/ai/chat` | Chat assistant |

### Response shape (all AI endpoints)
```json
{
  "meta": {
    "generation_id": "uuid",
    "agent_type": "EVENT_PLANNER",
    "model_used": "mock",
    "created_at": "ISO8601"
  },
  "result": { }
}
```
