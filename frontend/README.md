# FestSync Frontend

A premium SaaS event planning dashboard built with Next.js 15, React 19, TypeScript, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + CSS-in-JS
- **UI Components**: ShadCN UI + Radix UI
- **State Management**: Zustand (UI state) + TanStack Query (server state)
- **Forms**: React Hook Form + Zod validation
- **Animation**: Framer Motion
- **Charts**: Recharts
- **Icons**: Lucide React

## Quick Start

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Project Structure

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── (auth)/              # Auth pages (login, signup, etc.)
│   ├── (dashboard)/         # Dashboard pages with sidebar
│   ├── layout.tsx           # Root layout
│   ├── globals.css          # Global styles & design tokens
│   └── page.tsx             # Landing page
├── components/
│   ├── ui/                  # ShadCN primitives (button, card, etc.)
│   ├── layout/              # Layout components (sidebar, topbar)
│   ├── events/              # Event-related components
│   ├── tasks/               # Task/kanban components
│   ├── budget/              # Budget tracking components
│   ├── vendors/             # Vendor marketplace components
│   ├── ai/                  # AI assistant components
│   └── providers.tsx        # TanStack Query + theme providers
├── lib/
│   ├── utils.ts             # Utility functions (cn, formatters, etc.)
│   └── mock-data.ts         # Mock data for development
├── hooks/                   # Custom React hooks
│   ├── use-events.ts        # Event queries (mock TanStack Query)
│   ├── use-vendors.ts       # Vendor queries
│   └── use-tasks.ts         # Task queries
├── store/                   # Zustand stores
│   ├── ui-store.ts          # UI state (sidebar, theme)
│   └── event-store.ts       # Event wizard & selection state
├── types/
│   └── index.ts             # TypeScript interfaces
├── public/                  # Static assets
├── tailwind.config.ts       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
├── next.config.ts           # Next.js configuration
└── package.json             # Dependencies
```

## Design System

### Colors (Dark Mode First)
- **Background**: `#0A0A0B` → `#1A1A1E` (cards)
- **Border**: `rgba(255,255,255,0.08)` (subtle)
- **Primary**: Indigo `#6366F1` → Violet `#7C3AED` (hover)
- **Text**: `#FAFAFA` (primary), `#A1A1AA` (muted)
- **Status**: Green (completed), Amber (in progress), Red (urgent), Blue (planning)

### Typography
- Font: Inter (via next/font)
- Default size: 14px (text-sm)
- Headings use semantic HTML (h1-h6)

### Spacing & Layout
- Base unit: 4px (Tailwind default)
- Cards: 16px padding (p-6)
- Gaps: 16px-24px between sections
- Max width: 7xl container

## Pages Status

### Implemented ✅
- Landing page (`/`)
- Dashboard (`/dashboard`) - with stats, charts, upcoming events
- Events list (`/events`)
- Auth layout (`/(auth)`)

### Placeholder Structure (ready to implement)
- Login (`/(auth)/login`)
- Signup (`/(auth)/signup`)
- Event detail (`/events/[id]`)
- Tasks/Kanban (`/events/[id]/tasks`)
- Budget tracking (`/events/[id]/budget`)
- Vendors marketplace (`/vendors`)
- Vendor detail (`/vendors/[id]`)
- Vendor compare (`/vendors/compare`)
- AI assistant drawer (global component)

## Implemented Components

### UI Primitives (ShadCN)
- Button
- Card (Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter)
- Badge
- Input
- Avatar (Avatar, AvatarImage, AvatarFallback)
- Skeleton
- Label
- Separator
- Dialog
- Sheet (drawers)
- Progress
- Tabs (Tabs, TabsList, TabsTrigger, TabsContent)
- Textarea
- Dropdown Menu

### Layout
- Sidebar (collapsible, animated)
- Topbar (search, notifications, theme toggle, user menu)

### Features
- Dark mode toggle (stored in Zustand + localStorage)
- Responsive design (mobile-first)
- Framer Motion page & component animations
- Recharts integration (pie, area charts)
- Mock data with realistic structure

## State Management

### Zustand Stores

**UI Store** (`store/ui-store.ts`)
```typescript
useUIStore()
  .sidebarOpen    // boolean
  .theme          // 'dark' | 'light'
  .toggleSidebar()
  .setTheme()
```

**Event Store** (`store/event-store.ts`)
```typescript
useEventStore()
  .selectedEventId     // string | null
  .wizardState         // form state for event creation
  .setSelectedEvent()
  .updateWizardState()
  .resetWizard()
```

### TanStack Query (Ready to hook up to backend)

All hook placeholders created in `hooks/` directory. Currently return mock data.

Example pattern:
```typescript
// hooks/use-events.ts
export function useEvents() {
  // When backend ready, replace with:
  // return useQuery({
  //   queryKey: ['events'],
  //   queryFn: () => api.getEvents(),
  // })
  return { data: mockEvents, isLoading: false }
}
```

## Mock Data

Comprehensive mock data in `lib/mock-data.ts`:
- Current user
- 3 sample events
- 7 sample tasks
- 6 sample vendors
- 4 budget items
- 3 saved vendors
- 3 guests
- 2 bookings

All data is typed with interfaces from `types/index.ts`.

## Customization

### Change Theme
Edit `lib/utils.ts` or `app/globals.css` color variables:
```css
:root {
  --primary: 226 100% 55.6%; /* Indigo */
}
```

### Add New Page
1. Create folder in `app/(dashboard)/new-page/`
2. Add `page.tsx`
3. Add to sidebar in `components/layout/sidebar.tsx`

### Add New Component
1. Create in `components/[feature]/component-name.tsx`
2. Export from index (optional)
3. Use in pages with `import { Component } from '@/components/[feature]'`

## Connecting to Backend

When FastAPI backend is ready:

1. **Create API client** in `lib/api-client.ts`:
```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
})

export const eventsAPI = {
  getEvents: () => api.get('/events'),
  // ...
}
```

2. **Update hooks** in `hooks/use-events.ts`:
```typescript
export function useEvents() {
  return useQuery({
    queryKey: ['events'],
    queryFn: () => eventsAPI.getEvents(),
  })
}
```

3. **Add auth header** in API client using Supabase token

4. **Update environment** in `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

## Performance Tips

- Images use Next.js Image component for optimization
- Page transitions use Framer Motion with `initial` and `animate`
- Lazy loading via React.lazy (commented placeholders)
- CSS-in-JS via Tailwind (no runtime overhead)
- Type-safe with TypeScript strict mode

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Development Guidelines

### Code Style
- Use functional components + hooks
- Prefer composition over complex nesting
- Keep components under 300 lines
- Extract business logic to hooks

### Naming
- Components: PascalCase (e.g., EventCard.tsx)
- Utilities: camelCase (e.g., formatDate.ts)
- Stores: kebab-case + store suffix (e.g., ui-store.ts)

### Git Workflow
1. Create feature branch: `git checkout -b feature/add-kanban-board`
2. Commit often: `git commit -m "feat: add drag-and-drop to kanban"`
3. Push and create PR

## Troubleshooting

### Styles not applying
- Ensure `dark` class is on `<html>` element
- Check Tailwind content paths in `tailwind.config.ts`
- Run `npm run build` to check for build errors

### Components not showing
- Verify exports in `components/ui/`
- Check TypeScript errors with `npm run type-check`
- Restart dev server

### Dark mode not persisting
- Check Zustand persist middleware is working
- Verify localStorage has `ui-store` key
- Check theme is set on `<html>` element in Providers

## Resources

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [ShadCN UI](https://ui.shadcn.com)
- [Framer Motion](https://www.framer.com/motion)
- [TanStack Query](https://tanstack.com/query/latest)
- [Zustand](https://github.com/pmndrs/zustand)

## Next Steps

1. **Implement remaining pages** following the pattern in existing pages
2. **Create custom components** for tasks (kanban), budget (charts), vendors (filters)
3. **Connect to backend** using API client pattern
4. **Add Supabase auth** integration
5. **Set up CI/CD** for Vercel deployment
6. **Add tests** with Jest + React Testing Library
7. **Optimize images** and implement lazy loading
8. **Add error boundary** and error pages
9. **Implement analytics** (Posthog, Vercel Analytics)
10. **Deploy to Vercel**

---

**Build status**: Foundation complete, ready for feature implementation ✨
