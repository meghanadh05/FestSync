# FestSync API Specification

## Overview

FestSync API is a RESTful API built with FastAPI. All endpoints require JWT authentication (except login/signup). The API follows standard REST conventions with JSON request/response bodies.

**Base URL**: `http://localhost:8000` (development) | `https://api.festsync.com` (production)

**API Documentation**: `GET /docs` - Interactive Swagger documentation

## Authentication

All requests (except `/auth/login` and `/auth/signup`) require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

Tokens are obtained from Supabase Auth and are valid for 24 hours. Include token in all subsequent requests.

---

## Core Endpoints

### Authentication

#### POST `/auth/signup`
Register a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "access_token": "jwt_token",
  "expires_in": 86400
}
```

---

#### POST `/auth/login`
Authenticate user and get JWT token.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200):
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe"
  }
}
```

---

#### POST `/auth/logout`
Invalidate current session.

**Response** (200):
```json
{
  "message": "Successfully logged out"
}
```

---

### Users

#### GET `/users/me`
Get current user profile.

**Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "profile_image_url": "https://...",
  "bio": "Event enthusiast",
  "location": "San Francisco, CA",
  "preferences": {
    "theme": "dark",
    "notifications_enabled": true,
    "newsletter": false
  },
  "created_at": "2026-06-03T00:00:00Z",
  "updated_at": "2026-06-03T00:00:00Z"
}
```

---

#### PATCH `/users/me`
Update user profile.

**Request**:
```json
{
  "full_name": "Jane Doe",
  "phone_number": "+1234567890",
  "bio": "Event planner",
  "preferences": {
    "theme": "light"
  }
}
```

**Response** (200): Updated user object

---

#### GET `/users/{user_id}`
Get public user profile (limited info).

**Response** (200):
```json
{
  "id": "uuid",
  "full_name": "John Doe",
  "bio": "Event enthusiast",
  "profile_image_url": "https://..."
}
```

---

### Events

#### POST `/events`
Create a new event.

**Request**:
```json
{
  "title": "My Wedding",
  "description": "Destination wedding in Bali",
  "event_type": "wedding",
  "start_date": "2026-12-15",
  "end_date": "2026-12-17",
  "location": "Bali, Indonesia",
  "estimated_guests": 150,
  "budget": 50000,
  "currency": "USD"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "My Wedding",
  "description": "Destination wedding in Bali",
  "event_type": "wedding",
  "status": "planning",
  "start_date": "2026-12-15",
  "end_date": "2026-12-17",
  "location": "Bali, Indonesia",
  "estimated_guests": 150,
  "budget": 50000,
  "currency": "USD",
  "created_at": "2026-06-03T00:00:00Z",
  "updated_at": "2026-06-03T00:00:00Z"
}
```

---

#### GET `/events`
List all user's events with pagination and filtering.

**Query Parameters**:
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)
- `status`: Filter by status (planning, ongoing, completed, cancelled)
- `event_type`: Filter by event type
- `sort_by`: Sort field (start_date, created_at, title)
- `order`: Sort order (asc, desc)

**Response** (200):
```json
{
  "total": 25,
  "items": [
    {
      "id": "uuid",
      "title": "My Wedding",
      "event_type": "wedding",
      "start_date": "2026-12-15",
      "status": "planning",
      "budget": 50000,
      "guests_count": 150
    }
  ],
  "skip": 0,
  "limit": 10
}
```

---

#### GET `/events/{event_id}`
Get detailed event information.

**Response** (200):
```json
{
  "id": "uuid",
  "title": "My Wedding",
  "description": "Destination wedding in Bali",
  "event_type": "wedding",
  "status": "planning",
  "start_date": "2026-12-15",
  "end_date": "2026-12-17",
  "location": "Bali, Indonesia",
  "estimated_guests": 150,
  "budget": 50000,
  "currency": "USD",
  "thumbnail_url": "https://...",
  "creator": {
    "id": "uuid",
    "full_name": "John Doe"
  },
  "collaborators_count": 2,
  "tasks_count": 15,
  "tasks_completed": 5,
  "spent_amount": 12500,
  "created_at": "2026-06-03T00:00:00Z",
  "updated_at": "2026-06-03T00:00:00Z"
}
```

---

#### PATCH `/events/{event_id}`
Update event details (only owner and admins).

**Request**:
```json
{
  "title": "My Dream Wedding",
  "budget": 75000,
  "estimated_guests": 200,
  "status": "ongoing"
}
```

**Response** (200): Updated event object

---

#### DELETE `/events/{event_id}`
Delete an event (soft delete).

**Response** (204): No content

---

### Event AI Plans

#### POST `/events/{event_id}/ai-plan`
Generate or regenerate AI event plan.

**Request**:
```json
{
  "regenerate": false,
  "focus_areas": ["timeline", "budget", "vendors"]
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "event_id": "uuid",
  "plan_content": {
    "overview": "Comprehensive wedding planning guide...",
    "phases": [
      {
        "name": "Pre-Wedding (6 months before)",
        "tasks": ["Book venue", "Hire photographer"]
      }
    ]
  },
  "timeline": {
    "phases": [...]
  },
  "budget_breakdown": {
    "venue": 20000,
    "catering": 15000,
    "decoration": 8000
  },
  "vendor_suggestions": [
    "venue",
    "catering",
    "photography"
  ],
  "generated_at": "2026-06-03T00:00:00Z"
}
```

---

#### GET `/events/{event_id}/ai-plan`
Get the current AI event plan.

**Response** (200): AI plan object

---

### Tasks (To-Do Board)

#### POST `/events/{event_id}/tasks`
Create a task for an event.

**Request**:
```json
{
  "title": "Book venue",
  "description": "Contact and finalize venue booking",
  "priority": "high",
  "category": "venue",
  "due_date": "2026-09-15",
  "assigned_to": "uuid"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "event_id": "uuid",
  "title": "Book venue",
  "description": "Contact and finalize venue booking",
  "status": "pending",
  "priority": "high",
  "category": "venue",
  "due_date": "2026-09-15",
  "assigned_to": "uuid",
  "created_at": "2026-06-03T00:00:00Z"
}
```

---

#### GET `/events/{event_id}/tasks`
Get all tasks for an event.

**Query Parameters**:
- `status`: Filter by status (pending, in_progress, completed)
- `priority`: Filter by priority (low, medium, high, urgent)
- `category`: Filter by category
- `assigned_to`: Filter by assigned user

**Response** (200):
```json
{
  "total": 45,
  "items": [
    {
      "id": "uuid",
      "title": "Book venue",
      "status": "pending",
      "priority": "high",
      "due_date": "2026-09-15",
      "assigned_to": "uuid"
    }
  ]
}
```

---

#### PATCH `/events/{event_id}/tasks/{task_id}`
Update task details.

**Request**:
```json
{
  "status": "in_progress",
  "priority": "medium",
  "assigned_to": "new_user_id"
}
```

**Response** (200): Updated task object

---

#### DELETE `/events/{event_id}/tasks/{task_id}`
Delete a task.

**Response** (204): No content

---

### Vendors

#### GET `/vendors`
Search and list vendors.

**Query Parameters**:
- `search`: Text search (name, description)
- `vendor_type`: Filter by vendor type (catering, venue, photography, etc.)
- `city`: Filter by city
- `state`: Filter by state
- `min_rating`: Minimum rating (0-5)
- `price_range`: Filter by price range (budget, mid-range, premium)
- `availability`: Filter by availability status
- `skip`: Pagination skip
- `limit`: Pagination limit (max: 100)
- `sort_by`: Sort field (rating, review_count, price)

**Response** (200):
```json
{
  "total": 156,
  "items": [
    {
      "id": "uuid",
      "name": "The Grand Venue",
      "vendor_type": "venue",
      "location": "San Francisco, CA",
      "price_range": "premium",
      "min_price": 5000,
      "max_price": 25000,
      "rating": 4.8,
      "review_count": 127,
      "portfolio_images": ["https://...", "https://..."],
      "availability_status": "available"
    }
  ],
  "skip": 0,
  "limit": 20
}
```

---

#### GET `/vendors/{vendor_id}`
Get detailed vendor information.

**Response** (200):
```json
{
  "id": "uuid",
  "name": "The Grand Venue",
  "description": "Elegant venue for weddings and events",
  "vendor_type": "venue",
  "location": "123 Main St, San Francisco, CA 94102",
  "city": "San Francisco",
  "state": "CA",
  "country": "USA",
  "phone_number": "+1-555-1234",
  "email": "contact@thegrandvenue.com",
  "website_url": "https://thegrandvenue.com",
  "social_media": {
    "instagram": "https://instagram.com/thegrandvenue",
    "facebook": "https://facebook.com/thegrandvenue"
  },
  "price_range": "premium",
  "min_price": 5000,
  "max_price": 25000,
  "rating": 4.8,
  "review_count": 127,
  "total_bookings": 512,
  "response_time_hours": 4,
  "portfolio_images": ["https://...", "https://..."],
  "certifications": ["Professional Venues Association"],
  "reviews": [
    {
      "id": "uuid",
      "author": "Jane Doe",
      "rating": 5,
      "title": "Perfect venue!",
      "review_text": "Amazing venue with great service",
      "verified_booking": true,
      "created_at": "2026-03-15T00:00:00Z"
    }
  ]
}
```

---

### Vendor Reviews

#### POST `/vendors/{vendor_id}/reviews`
Create a review for a vendor.

**Request**:
```json
{
  "rating": 5,
  "title": "Excellent service",
  "review_text": "The venue was perfect for our event!",
  "event_id": "uuid"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "vendor_id": "uuid",
  "user_id": "uuid",
  "rating": 5,
  "title": "Excellent service",
  "review_text": "The venue was perfect for our event!",
  "verified_booking": true,
  "created_at": "2026-06-03T00:00:00Z"
}
```

---

#### GET `/vendors/{vendor_id}/reviews`
Get all reviews for a vendor.

**Query Parameters**:
- `sort_by`: Sort field (rating, date, helpfulness)
- `rating`: Filter by rating
- `skip`: Pagination skip
- `limit`: Pagination limit

**Response** (200):
```json
{
  "total": 127,
  "average_rating": 4.8,
  "items": [
    {
      "id": "uuid",
      "author": "Jane Doe",
      "rating": 5,
      "title": "Excellent service",
      "review_text": "The venue was perfect for our event!",
      "helpfulness_score": 34,
      "verified_booking": true,
      "created_at": "2026-03-15T00:00:00Z"
    }
  ]
}
```

---

### Saved Vendors

#### POST `/saved-vendors`
Save a vendor for an event.

**Request**:
```json
{
  "vendor_id": "uuid",
  "event_id": "uuid",
  "notes": "Great reviews, within budget",
  "price_quote": 8500
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "vendor_id": "uuid",
  "event_id": "uuid",
  "notes": "Great reviews, within budget",
  "price_quote": 8500,
  "status": "saved",
  "created_at": "2026-06-03T00:00:00Z"
}
```

---

#### GET `/events/{event_id}/saved-vendors`
Get all saved vendors for an event.

**Query Parameters**:
- `status`: Filter by status (saved, contacted, quoted, booked)
- `skip`: Pagination skip
- `limit`: Pagination limit

**Response** (200):
```json
{
  "total": 8,
  "items": [
    {
      "id": "uuid",
      "vendor": {
        "id": "uuid",
        "name": "The Grand Venue",
        "rating": 4.8,
        "price_range": "premium"
      },
      "notes": "Great reviews, within budget",
      "price_quote": 8500,
      "status": "quoted",
      "saved_at": "2026-06-01T00:00:00Z"
    }
  ]
}
```

---

#### PATCH `/saved-vendors/{saved_vendor_id}`
Update saved vendor status or notes.

**Request**:
```json
{
  "status": "booked",
  "notes": "Confirmed for Dec 15-17"
}
```

**Response** (200): Updated saved vendor object

---

#### DELETE `/saved-vendors/{saved_vendor_id}`
Remove a saved vendor.

**Response** (204): No content

---

### Budget Tracking

#### POST `/events/{event_id}/budget/transactions`
Create a budget transaction.

**Request**:
```json
{
  "category": "catering",
  "description": "Catering deposit",
  "amount": 2500,
  "transaction_type": "expense",
  "status": "paid",
  "payment_method": "card",
  "paid_date": "2026-06-03",
  "vendor_id": "uuid"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "event_id": "uuid",
  "category": "catering",
  "description": "Catering deposit",
  "amount": 2500,
  "transaction_type": "expense",
  "status": "paid",
  "payment_method": "card",
  "paid_date": "2026-06-03",
  "created_at": "2026-06-03T00:00:00Z"
}
```

---

#### GET `/events/{event_id}/budget/transactions`
Get all budget transactions for an event.

**Query Parameters**:
- `category`: Filter by category
- `status`: Filter by status (pending, paid, refunded)
- `transaction_type`: Filter by type (expense, income)
- `skip`: Pagination skip
- `limit`: Pagination limit

**Response** (200):
```json
{
  "total": 32,
  "items": [
    {
      "id": "uuid",
      "category": "catering",
      "description": "Catering deposit",
      "amount": 2500,
      "status": "paid",
      "paid_date": "2026-06-03"
    }
  ]
}
```

---

#### GET `/events/{event_id}/budget/summary`
Get budget summary and analytics.

**Response** (200):
```json
{
  "event_id": "uuid",
  "total_budget": 50000,
  "total_spent": 12500,
  "remaining_budget": 37500,
  "budget_percentage": 25,
  "by_category": {
    "venue": {
      "budgeted": 20000,
      "spent": 8500,
      "percentage": 42.5
    },
    "catering": {
      "budgeted": 15000,
      "spent": 4000,
      "percentage": 26.7
    }
  },
  "upcoming_payments": [
    {
      "category": "decoration",
      "amount": 3000,
      "due_date": "2026-08-15"
    }
  ]
}
```

---

#### PATCH `/events/{event_id}/budget/transactions/{transaction_id}`
Update a transaction.

**Request**:
```json
{
  "status": "refunded",
  "amount": 2500
}
```

**Response** (200): Updated transaction object

---

#### DELETE `/events/{event_id}/budget/transactions/{transaction_id}`
Delete a transaction.

**Response** (204): No content

---

### Collaborators

#### POST `/events/{event_id}/collaborators`
Add a collaborator to an event (owner only).

**Request**:
```json
{
  "email": "collaborator@example.com",
  "role": "collaborator",
  "can_edit": true,
  "can_manage_budget": true
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "event_id": "uuid",
  "user": {
    "id": "uuid",
    "full_name": "Jane Smith",
    "email": "collaborator@example.com"
  },
  "role": "collaborator",
  "can_edit": true,
  "can_manage_budget": true,
  "invited_at": "2026-06-03T00:00:00Z"
}
```

---

#### GET `/events/{event_id}/collaborators`
Get all collaborators for an event.

**Response** (200):
```json
{
  "total": 3,
  "items": [
    {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "full_name": "John Doe",
        "email": "john@example.com"
      },
      "role": "owner",
      "joined_at": "2026-06-03T00:00:00Z"
    }
  ]
}
```

---

#### PATCH `/events/{event_id}/collaborators/{collaborator_id}`
Update collaborator permissions.

**Request**:
```json
{
  "role": "admin",
  "can_manage_budget": false
}
```

**Response** (200): Updated collaborator object

---

#### DELETE `/events/{event_id}/collaborators/{collaborator_id}`
Remove a collaborator.

**Response** (204): No content

---

## Error Handling

All error responses follow this format:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "status_code": 400
}
```

**Common Status Codes**:
- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing/invalid auth)
- `403`: Forbidden (permission denied)
- `404`: Not Found
- `409`: Conflict (duplicate)
- `500`: Internal Server Error

---

## Rate Limiting

- **Auth endpoints**: 5 requests/minute per IP
- **Search endpoints**: 100 requests/minute per user
- **Write endpoints**: 30 requests/minute per user
- **General endpoints**: 60 requests/minute per user

---

## Pagination

List endpoints support standard pagination:

```json
{
  "total": 156,
  "items": [...],
  "skip": 0,
  "limit": 20
}
```

---

## Versioning

API endpoints currently at `v1` (implicit). Future versions will use `/api/v2/` prefix.

---

## OpenAPI/Swagger Documentation

When backend is running, detailed API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`
