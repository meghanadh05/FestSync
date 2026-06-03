# FestSync System Architecture

## Overview

FestSync is a full-stack event planning platform built with a modern, scalable architecture. The system separates concerns between the frontend (Next.js), backend (FastAPI), and infrastructure (Supabase) with clear data flow and API contracts.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                           │
│  Next.js App (Browser) - TypeScript, React, Tailwind       │
│  - Event Dashboard                                          │
│  - Vendor Search & Comparison                               │
│  - Budget Tracking & Analytics                              │
│  - To-Do Board Management                                   │
└──────────────┬──────────────────────────────────────────────┘
               │ HTTPS
               │ JSON
┌──────────────▼──────────────────────────────────────────────┐
│                      API Layer                              │
│  FastAPI Backend (localhost:8000 / Cloud)                   │
│  - Event Management Routes                                  │
│  - Vendor Management Routes                                 │
│  - AI Planning Service                                      │
│  - Budget & Analytics Routes                                │
│  - Authentication Middleware                                │
└──────────────┬──────────────────────────────────────────────┘
               │ PostgreSQL
               │ JWT Auth
┌──────────────▼──────────────────────────────────────────────┐
│                   Data & Auth Layer                         │
│  Supabase (PostgreSQL + Auth + Storage)                     │
│  - Users & Profiles                                         │
│  - Events & Event Details                                   │
│  - Vendors & Ratings                                        │
│  - Budget Transactions                                      │
│  - To-Do Items                                              │
└──────────────┬──────────────────────────────────────────────┘
               │ API Keys
┌──────────────▼──────────────────────────────────────────────┐
│              External AI Services                           │
│  OpenAI API / Google Gemini API                             │
│  - Event Plan Generation                                    │
│  - Vendor Recommendations                                   │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend (Next.js)

**Location**: `frontend/`

**Responsibilities**:
- User interface and user experience
- Client-side state management (Zustand)
- Form handling and validation (React Hook Form, Zod)
- Server state caching (TanStack Query)
- API communication with backend
- Authentication (Supabase JWT)

**Key Technologies**:
- **Next.js 15**: App Router for modern page management
- **TypeScript**: Full type safety
- **Tailwind CSS + ShadCN**: Component styling
- **Framer Motion**: Animations
- **Recharts**: Data visualization
- **TanStack Query**: Server state management

**Architecture Pattern**:
- Page-based routing with App Router
- Component-based UI composition
- Custom hooks for business logic
- API layer abstraction

### 2. Backend (FastAPI)

**Location**: `backend/`

**Responsibilities**:
- REST API endpoints for all operations
- Business logic execution
- Database operations via SQLModel
- Authentication and authorization
- AI service integration
- Email notifications
- Rate limiting and validation

**Key Technologies**:
- **FastAPI**: High-performance Python framework
- **Pydantic**: Request/response validation
- **SQLModel**: ORM with type hints
- **Supabase Python Client**: Database & auth
- **OpenAI/Gemini SDK**: AI integration

**Architecture Pattern**:
- Route-based organization
- Middleware for auth, CORS, error handling
- Service layer for business logic
- Dependency injection for loose coupling

### 3. Database (Supabase PostgreSQL)

**Location**: Cloud-hosted via Supabase

**Responsibilities**:
- Persistent data storage
- Data integrity and constraints
- Transactional consistency
- Full-text search indices
- Real-time capabilities

**Key Features**:
- Automatic migrations via schema files
- Row-level security policies
- Full-text search on vendor/event data
- Real-time subscriptions

### 4. Authentication (Supabase Auth)

**Responsibilities**:
- User registration and login
- JWT token generation
- Password reset and recovery
- OAuth integration (future)
- Session management

**Flow**:
1. User logs in via frontend
2. Supabase generates JWT token
3. Token stored in client localStorage
4. Backend validates token on every request
5. Token refresh handled automatically

### 5. AI Services

**Responsibilities**:
- Event plan generation using OpenAI/Gemini
- Vendor recommendations based on event details
- Smart budget allocation suggestions
- Timeline generation

**Integration Points**:
- Backend calls AI APIs synchronously for plan generation
- AI responses processed and stored in database
- Cache frequently accessed AI results

## Data Flow

### User Registration Flow
```
User Input (Frontend)
    ↓
Supabase Auth API
    ↓
JWT Token Generated
    ↓
Token Stored in Client
    ↓
Create User Profile (Backend)
    ↓
Database Stored
```

### Event Creation & AI Planning Flow
```
User Submits Event Form (Frontend)
    ↓
Frontend Validation (Zod)
    ↓
POST /api/events (FastAPI)
    ↓
Backend Validation (Pydantic)
    ↓
Save Event to Database
    ↓
Call OpenAI/Gemini for Plan
    ↓
Parse AI Response
    ↓
Save Plan to Database
    ↓
Return Event with Plan (Frontend)
    ↓
Display in Dashboard
```

### Vendor Search & Comparison Flow
```
User Searches Vendors (Frontend)
    ↓
GET /api/vendors?search=...&filters=... (FastAPI)
    ↓
Backend Query Database
    ↓
Apply Full-Text Search
    ↓
Filter by Budget/Location/Ratings
    ↓
Return Vendor List with Ratings
    ↓
Frontend Displays Results
    ↓
User Compares (Client-Side Calculation)
    ↓
Save to Favorites (POST /api/favorites)
```

## Deployment Architecture

### Frontend Deployment (Vercel)

```
Git Push to Main
    ↓
GitHub Webhook → Vercel
    ↓
Install Dependencies
    ↓
Build Next.js
    ↓
Deploy to CDN
    ↓
Environment Variables Applied
    ↓
Live at https://festsync.vercel.app
```

**Features**:
- Automatic preview deployments
- Edge functions for middleware
- Image optimization
- Incremental Static Regeneration (ISR)

### Backend Deployment (Render/Railway)

```
Git Push to Backend Branch
    ↓
CI/CD Pipeline
    ↓
Install Dependencies
    ↓
Run Tests
    ↓
Build Docker Image
    ↓
Deploy to Production
    ↓
Environment Variables Applied
    ↓
Health Check Verification
```

**Infrastructure**:
- Containerized with Docker
- Auto-scaling based on load
- Health check endpoints
- Automated backups

### Database Deployment (Supabase)

```
Schema Changes
    ↓
Migration Scripts
    ↓
Applied to Production
    ↓
Automatic Backups
    ↓
Version Control in Repository
```

## Security Considerations

### Authentication
- JWT tokens stored in httpOnly cookies (frontend)
- Tokens validated on every backend request
- Token expiration: 24 hours (configurable)
- Refresh tokens for long-term sessions

### Authorization
- Row-level security on database
- User can only access their own events
- Admin-only endpoints for system management
- Vendor data shared publicly (read-only)

### Data Protection
- HTTPS everywhere
- Environment variables for secrets
- No sensitive data in client code
- SQL injection prevention via SQLModel

### API Security
- CORS configured for specific origins
- Rate limiting on auth endpoints
- Input validation on all endpoints
- Request size limits

## Scalability Considerations

### Caching Strategy
- Frontend: TanStack Query for API response caching
- Backend: Redis for expensive queries (future)
- Database: PostgreSQL indices on frequently queried columns

### Database Optimization
- Proper indexing on event_id, user_id, vendor_id
- Pagination for large result sets
- Connection pooling via Supabase

### API Performance
- Asynchronous processing for AI calls
- Background jobs for notifications (future)
- Query optimization with select() to limit fields

### Frontend Performance
- Code splitting with dynamic imports
- Image optimization with Next.js Image component
- Lazy loading for heavy components
- Service Worker for offline support (future)

## Error Handling

### Frontend
- User-friendly error messages
- Retry logic for failed requests
- Error boundary components
- Toast notifications

### Backend
- Structured error responses
- HTTP status codes
- Detailed logging for debugging
- Circuit breaker for external APIs

## Monitoring & Logging

### Frontend Monitoring
- Error tracking (Sentry, future)
- Page performance metrics
- User interaction analytics

### Backend Monitoring
- Application logs (structured JSON)
- Database query logs
- API endpoint metrics
- AI service integration logs

## Development Workflow

1. **Local Development**
   - Frontend: `npm run dev` on localhost:3000
   - Backend: `python -m uvicorn app.main:app --reload` on localhost:8000
   - Database: Supabase cloud for development
   - Swagger API Docs: http://localhost:8000/docs

2. **Testing**
   - Frontend: Jest + React Testing Library
   - Backend: pytest with test fixtures
   - Integration tests with test database

3. **Code Quality**
   - Frontend: ESLint, Prettier, TypeScript strict mode
   - Backend: Black, isort, mypy, pylint
   - Pre-commit hooks

4. **Version Control**
   - Feature branches off main
   - Pull request reviews required
   - Automated tests on PR

## Future Architecture Enhancements

- **Caching Layer**: Redis for session storage and API caching
- **Message Queue**: Celery for async AI processing
- **Real-time Features**: WebSocket for live vendor updates
- **Microservices**: Separate AI service, notification service
- **Analytics Pipeline**: Data warehouse for event insights
- **Mobile App**: React Native sharing backend API
