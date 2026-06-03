# FestSync - AI-Powered Event Planning & Vendor Discovery Platform

## Overview

FestSync is a comprehensive event planning platform that leverages AI to help users create and manage events seamlessly. From weddings and birthdays to corporate conferences and college fests, FestSync provides intelligent planning, vendor discovery, budget tracking, and a collaborative dashboard to bring events to life.

## Key Features

### Event Management
- **Multi-event support**: Create and manage weddings, birthdays, college fests, corporate events, conferences, and custom events
- **AI-powered planning**: Generate comprehensive event plans using OpenAI/Gemini APIs
- **Smart to-do board**: Organize and track event tasks with priority and due dates
- **Budget tracking**: Monitor event spending with real-time analytics and category-based breakdowns

### Vendor Discovery
- **Smart vendor search**: Find vendors based on event type, location, budget, and ratings
- **Vendor comparison**: Compare multiple vendors side-by-side on pricing, services, and reviews
- **Vendor management**: Save, organize, and track vendor communications
- **Reviews & ratings**: Community-driven vendor ratings and detailed reviews

### Dashboard & Analytics
- **Premium dashboard**: Get a bird's eye view of all event details, timeline, and progress
- **Real-time analytics**: Track budget burn, task completion, and vendor pipeline
- **Event timeline**: Visual timeline of events and key milestones
- **Team collaboration**: Share event details and coordinate with family/team members

## Tech Stack

### Frontend
- **Next.js 15** - App Router with TypeScript for type-safe development
- **TypeScript** - Full type safety across the application
- **Tailwind CSS** - Utility-first CSS for rapid UI development
- **ShadCN UI** - High-quality accessible component library
- **Framer Motion** - Smooth animations and transitions
- **TanStack Query** - Server state management and caching
- **Zustand** - Lightweight client state management
- **React Hook Form** - Efficient form handling
- **Zod** - Runtime schema validation
- **Recharts** - Beautiful, composable charting library

### Backend
- **FastAPI** - Modern, fast Python web framework
- **Pydantic** - Data validation using Python type hints
- **SQLModel** - SQL databases in Python with ORM/Pydantic integration
- **PostgreSQL** - Robust relational database
- **Supabase** - Authentication, real-time database, and storage
- **OpenAI/Gemini API** - AI-powered event planning and recommendations

### Infrastructure & Deployment
- **Supabase** - Backend-as-a-Service for auth, database, and storage
- **Vercel** - Frontend deployment with edge functions
- **Render/Railway** - Backend deployment options
- **JWT Authentication** - Secure token-based auth via Supabase

## Project Structure

```
festsync/
├── frontend/              # Next.js application
│   ├── app/              # App router pages and layouts
│   ├── components/       # Reusable React components
│   ├── lib/              # Utilities, hooks, API clients
│   ├── styles/           # Global styles and CSS
│   ├── types/            # TypeScript type definitions
│   └── package.json
├── backend/              # FastAPI application
│   ├── app/              # FastAPI routes and endpoints
│   ├── models/           # SQLModel database models
│   ├── schemas/          # Pydantic schemas for validation
│   ├── services/         # Business logic and AI services
│   ├── middleware/       # Custom middleware
│   ├── config.py         # Configuration
│   └── requirements.txt
├── docs/                 # Project documentation
│   ├── ARCHITECTURE.md    # System architecture overview
│   ├── DATABASE_SCHEMA.md # Database tables and relationships
│   ├── API_SPEC.md        # API endpoints and contracts
│   └── FRONTEND_PAGES.md  # Frontend routes and components
├── README.md             # This file
└── LICENSE              # MIT License
```

## Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.10+
- PostgreSQL 14+
- Supabase account
- OpenAI API key (for AI features)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

### Environment Variables

Create `.env.local` in frontend and `.env` in backend:

**Frontend** (.env.local):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

**Backend** (.env):
```
DATABASE_URL=postgresql://user:password@localhost/festsync
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_key
OPENAI_API_KEY=your_openai_key
JWT_SECRET=your_jwt_secret
```

## Development Workflow

1. Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
2. Review [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) for data models
3. Check [API_SPEC.md](docs/API_SPEC.md) for backend endpoints
4. Review [FRONTEND_PAGES.md](docs/FRONTEND_PAGES.md) for UI structure

## API Documentation

Full API documentation available at `/docs` when running the backend (OpenAPI/Swagger).

## Deployment

### Frontend (Vercel)
```bash
vercel deploy
```

### Backend (Render/Railway)
Deploy via GitHub integration or CLI tools provided by the platform.

## Contributing

This is a private project. For contributions, please follow the development workflow and ensure all tests pass.

## License

MIT License - See LICENSE file for details

## Contact

Project Lead: Meghanadh Borra (meghanadh05b@gmail.com)

---

**Last Updated**: June 2026
