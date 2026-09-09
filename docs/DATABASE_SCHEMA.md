# FestSync — Database Schema

Database: PostgreSQL hosted on Supabase.
ORM: SQLAlchemy 2 (models in `backend/app/models/`).

---

## Tables

### events
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | auto-generated |
| user_id | String | Supabase auth UID, indexed |
| title | String(255) | required |
| event_type | Enum | WEDDING, BIRTHDAY, COLLEGE_FEST, CORPORATE_EVENT, CONFERENCE, RECEPTION, ENGAGEMENT, CONCERT, OTHER |
| status | Enum | PLANNING, ACTIVE, COMPLETED, CANCELLED |
| start_date | Date | required |
| end_date | Date | required |
| location | String(255) | |
| estimated_guests | Integer | |
| budget | Numeric(12,2) | |
| currency | String(10) | default INR |
| description | Text | |
| thumbnail_url | String(500) | |
| created_at | DateTime | auto |
| updated_at | DateTime | auto |
| deleted_at | DateTime | soft delete |

### tasks
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| event_id | UUID FK → events | |
| title | String(255) | required |
| description | Text | |
| status | Enum | PENDING, IN_PROGRESS, COMPLETED |
| priority | Enum | LOW, MEDIUM, HIGH, URGENT |
| category | String(100) | |
| due_date | Date | |
| assigned_to | String | user ID |
| ai_generated | Boolean | default false |
| created_at | DateTime | |
| updated_at | DateTime | |
| deleted_at | DateTime | soft delete |

### subtasks
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| task_id | UUID FK → tasks | |
| title | String(255) | required |
| description | Text | |
| status | Enum | PENDING, IN_PROGRESS, COMPLETED |
| order | Integer | display order |
| created_at | DateTime | |
| updated_at | DateTime | |

### budget_items
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| event_id | UUID FK → events | |
| category | String(100) | required |
| planned_amount | Numeric(12,2) | |
| actual_amount | Numeric(12,2) | default 0 |
| notes | Text | |
| created_at | DateTime | |
| updated_at | DateTime | |
| deleted_at | DateTime | soft delete |

### vendors
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| owner_user_id | String | nullable (seeded vendors have no owner) |
| business_name | String(255) | required |
| category | Enum | CATERING, VENUE, PHOTOGRAPHY, VIDEOGRAPHY, DECORATION, MUSIC, DJ, FLORIST, BAKERY, TRANSPORT, MAKEUP, ATTIRE, EVENT_PLANNER, SECURITY, LIGHTING, OTHER |
| location | String(255) | |
| city | String(100) | |
| starting_price | Numeric(12,2) | |
| currency | String(10) | |
| rating | Float | 0–5 |
| review_count | Integer | |
| verified | Boolean | |
| active | Boolean | |
| supported_event_types | String(500) | comma-separated |
| primary_image_url | String(500) | |
| created_at | DateTime | |
| updated_at | DateTime | |
| deleted_at | DateTime | soft delete |

### vendor_services
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| vendor_id | UUID FK → vendors | |
| name | String(255) | required |
| description | Text | |
| price | Numeric(12,2) | |
| unit | String(50) | e.g. "per person" |
| created_at | DateTime | |
| updated_at | DateTime | |

### saved_vendors
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| event_id | UUID FK → events | |
| vendor_id | UUID FK → vendors | |
| user_id | String | |
| notes | Text | |
| created_at | DateTime | |
| **unique** | (event_id, vendor_id) | prevents duplicates |

### ai_generations
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| user_id | String | |
| event_id | String | nullable (chat has no event) |
| agent_type | Enum | EVENT_PLANNER, TASK_GENERATOR, BUDGET_ADVISOR, VENDOR_RECOMMENDATION, CHAT_ASSISTANT |
| prompt | Text | full user prompt sent to AI |
| response_json | Text | null if FAILED or INVALID_JSON |
| status | Enum | SUCCESS, FAILED, INVALID_JSON |
| error_message | Text | |
| model_used | String(100) | e.g. "openai/gpt-4o-mini" |
| created_at | DateTime | |

---

## Migrations

SQL migration files are in `backend/migrations/`:
- `001_initial_schema.sql` — all table definitions
- `002_rls_policies.sql` — Row-Level Security
- `003_seed_vendors.sql` — sample vendor data

Run against Supabase via the SQL editor or `psql`.
