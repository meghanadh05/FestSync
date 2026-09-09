# FestSync Backend API

Production-ready FastAPI backend for FestSync, an AI-powered event planning and vendor discovery platform.

## Features

- ✅ FastAPI with async/await support
- ✅ SQLAlchemy ORM with PostgreSQL
- ✅ Supabase authentication and authorization
- ✅ JWT token verification
- ✅ CORS configured for frontend
- ✅ Health check endpoints
- ✅ Structured error handling
- ✅ Modular architecture
- ✅ Comprehensive testing setup
- ✅ Swagger/OpenAPI documentation
- ✅ Environment-based configuration

## Tech Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL (via Supabase)
- **Auth**: Supabase JWT
- **Server**: Uvicorn
- **Testing**: Pytest + AsyncIO
- **Migrations**: Alembic

## Quick Start

### 1. Setup Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Optional: edit .env with your Supabase credentials
```

If `DATABASE_URL` is left blank, the backend uses a local SQLite file at `backend/festsync.db`.
That fallback keeps `pytest` and local API startup working without a provisioned Supabase database.

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Start Development Server

```bash
python -m uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

### 6. View API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py          # Configuration & settings
│   │   ├── database.py        # Database connection
│   │   ├── security.py        # JWT & auth
│   │   └── exceptions.py      # Custom exceptions
│   ├── modules/
│   │   ├── auth/              # Authentication
│   │   ├── users/             # User management
│   │   ├── events/            # Event management
│   │   ├── tasks/             # To-do tasks
│   │   ├── vendors/           # Vendor management
│   │   ├── budget/            # Budget tracking
│   │   ├── plans/             # AI event plans
│   │   ├── guests/            # Guest management
│   │   ├── bookings/          # Vendor bookings
│   │   ├── ai/                # AI services
│   │   └── notifications/     # Notifications
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   ├── utils/                 # Utility functions
│   └── api/
│       └── v1/
│           └── routes.py      # API v1 routes
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── conftest.py           # Pytest configuration
├── migrations/                # Alembic migrations
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── pytest.ini                # Pytest config
├── Dockerfile                # Docker container definition
└── README.md                 # This file
```

## Environment Variables

See `.env.example` for all available options:

```bash
# Core
ENVIRONMENT=development
DEBUG=True

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/festsync
# Leave blank to use backend/festsync.db locally

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# JWT
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
SECRET_KEY=your-secret-key

# Cache / background services
REDIS_URL=redis://localhost:6379/0

# CORS
ALLOWED_ORIGINS=http://localhost:3000
```

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /health/db` - Database health check
- `GET /` - API root with info

### API v1
- `GET /api/v1/status` - API status
- More endpoints to be implemented...

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/unit/test_health.py
```

### Run with Coverage

```bash
pytest --cov=app tests/
```

### Run Integration Tests Only

```bash
pytest -m integration
```

## Database Migrations

### Create New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Last Migration

```bash
alembic downgrade -1
```

### View Migration Status

```bash
alembic current
```

## Docker

### Build Image

```bash
docker build -t festsync-api .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env festsync-api
```

## Module Structure Pattern

Each module follows this pattern:

```
modules/{module_name}/
├── __init__.py      # Module definition
├── routes.py        # API endpoints
├── service.py       # Business logic (to be created)
├── model.py         # Database models (to be created)
└── schema.py        # Request/response schemas (to be created)
```

### Route Example

```python
from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
async def list_items(user = Depends(get_current_user)):
    """List user's items."""
    return {"items": []}

@router.post("/")
async def create_item(data: dict, user = Depends(get_current_user)):
    """Create new item."""
    return {"created": True}
```

## Authentication

All protected endpoints require JWT token in Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/...
```

Tokens are verified via `get_current_user` dependency:

```python
@router.get("/protected")
async def protected_route(user: Dict = Depends(get_current_user)):
    # user contains decoded JWT payload
    user_id = user.get("sub")  # User ID from Supabase
    return {"user_id": user_id}
```

## Error Handling

Custom exceptions provide consistent error responses:

```python
from app.core.exceptions import NotFoundError, ValidationError

# Raise custom exception
raise NotFoundError("Event", event_id)

# Returns:
{
  "detail": "Event with ID {event_id} not found",
  "status_code": 404
}
```

Available exceptions:
- `NotFoundError` - 404 Not Found
- `ValidationError` - 422 Unprocessable Entity
- `AuthenticationError` - 401 Unauthorized
- `AuthorizationError` - 403 Forbidden
- `ConflictError` - 409 Conflict
- `BadRequestError` - 400 Bad Request
- `DatabaseError` - 500 Server Error
- `ExternalServiceError` - 503 Service Unavailable

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints throughout
- 4-space indentation
- Max line length: 100 characters

### Naming Conventions

- **Models**: PascalCase (e.g., `User`, `Event`)
- **Tables**: plural snake_case (e.g., `users`, `events`)
- **Functions/methods**: snake_case (e.g., `create_event`)
- **Constants**: UPPER_CASE (e.g., `API_VERSION`)

### Docstring Format

```python
def function_name(param1: str, param2: int) -> dict:
    """
    Brief description of what this does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        SomeError: When this error occurs
    """
```

## Common Tasks

### Add New Endpoint

1. Create function in `modules/{module_name}/routes.py`
2. Add route with appropriate HTTP method
3. Add authentication if needed
4. Create request/response schemas if needed
5. Add tests in `tests/`

### Add New Database Model

1. Create model in `models/` or `modules/{module_name}/model.py`
2. Inherit from `Base`
3. Define columns with appropriate types
4. Add relationships
5. Create migration: `alembic revision --autogenerate`
6. Run migration: `alembic upgrade head`

### Add New Service

1. Create `modules/{module_name}/service.py`
2. Define service class with business logic
3. Use in routes via dependency injection

## Troubleshooting

### Database Connection Error

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Solution**: Check DATABASE_URL in .env and ensure PostgreSQL is running

### JWT Validation Error

```
HTTPException: Invalid authentication token
```

**Solution**: Ensure token is valid and not expired. Check SUPABASE_KEY matches your Supabase project.

### Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solution**: Run on different port: `uvicorn app.main:app --port 8001`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Pydantic Documentation](https://docs.pydantic.dev)

## Performance Checklist

- [ ] Add database indices for frequently queried columns
- [ ] Implement pagination for list endpoints
- [ ] Add caching for read-heavy operations
- [ ] Optimize N+1 queries with SQLAlchemy joins
- [ ] Add rate limiting for expensive operations
- [ ] Profile and optimize slow endpoints

## Security Checklist

- [ ] All passwords hashed (handled by Supabase)
- [ ] HTTPS enforced in production
- [ ] CORS properly configured
- [ ] SQL injection prevention (SQLAlchemy)
- [ ] XSS prevention in responses
- [ ] Rate limiting configured
- [ ] Secrets in environment variables only
- [ ] Regular security audits

## Next Steps

1. Implement database models for core entities
2. Create service classes for business logic
3. Implement API endpoints for each module
4. Add comprehensive test coverage
5. Set up CI/CD pipeline
6. Deploy to production environment

---

**Built with FastAPI + SQLAlchemy + PostgreSQL**

For questions or issues, refer to the [FestSync Documentation](../docs/API_SPEC.md)
