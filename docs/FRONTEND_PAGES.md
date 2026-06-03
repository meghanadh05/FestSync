# FestSync Frontend Routes & Components

## Overview

FestSync frontend is built with Next.js 15 App Router. This document outlines planned pages, routes, UI components, and the component hierarchy.

## Page Structure

```
app/
├── (auth)/                    # Auth pages (no sidebar)
│   ├── login/                # Login page
│   ├── signup/               # Signup/Registration page
│   └── forgot-password/      # Password recovery
├── (dashboard)/              # Main app pages (with sidebar/layout)
│   ├── dashboard/            # Dashboard overview
│   ├── events/
│   │   ├── page.tsx          # Events list
│   │   ├── [id]/
│   │   │   ├── page.tsx      # Event detail & overview
│   │   │   ├── ai-plan/      # Event AI plan view
│   │   │   ├── tasks/        # To-do board
│   │   │   ├── budget/       # Budget tracking
│   │   │   ├── vendors/      # Event's saved vendors
│   │   │   └── team/         # Collaborators management
│   │   └── create/           # Create event wizard
│   ├── vendors/
│   │   ├── page.tsx          # Vendor discovery/search
│   │   ├── [id]/             # Vendor detail page
│   │   └── compare/          # Vendor comparison
│   ├── profile/              # User profile & settings
│   └── settings/             # Account settings
├── layout.tsx                # Root layout
├── page.tsx                  # Landing page (/ route)
└── not-found.tsx             # 404 page
```

---

## Route Details

### Authentication Routes (No Layout)

#### `/` - Landing Page
Entry point for non-authenticated users.

**Components**:
- `HeroSection` - Feature highlights and call-to-action
- `FeaturePricingSection` - Key features overview
- `TestimonialsSection` - User testimonials
- `CTAButton` - Sign up / Get Started button
- `Footer` - Footer with links

---

#### `/login` - Login Page
User login with email/password.

**Form Fields**:
- Email input with validation
- Password input
- "Remember me" checkbox
- "Forgot password?" link
- Sign up link

**Components**:
- `AuthCard` - Card wrapper for auth forms
- `EmailInput` - Validated email field
- `PasswordInput` - Password input with show/hide
- `SubmitButton` - Form submission button
- `AuthDivider` - Divider with "or"
- `SocialAuthButtons` - (Future) OAuth buttons

---

#### `/signup` - Registration Page
User account creation and onboarding.

**Form Fields**:
- Full name input
- Email input
- Password input
- Confirm password
- Accept terms checkbox

**Components**:
- `AuthCard`
- `ProgressStepper` - Multi-step signup (future)
- `FormInputs` - Reusable form fields
- `TermsCheckbox` - Terms & conditions checkbox

---

#### `/forgot-password` - Password Recovery
Password reset flow.

**Steps**:
1. Enter email → send reset link
2. Check email confirmation
3. Enter new password
4. Success confirmation

**Components**:
- `AuthCard`
- `StepIndicator` - Show current step
- `EmailInput`
- `PasswordResetForm`

---

### Dashboard Routes (With Sidebar Layout)

#### `/dashboard` - Dashboard Overview
Main dashboard with event overview, upcoming tasks, budget summary.

**Layout**:
- Header: Navigation, user profile, settings
- Sidebar: Navigation menu
- Main Content:
  - Quick stats cards (events, tasks, spent)
  - Upcoming events widget
  - Recent tasks widget
  - Budget overview chart
  - Quick action buttons

**Components**:
- `Header` - Top navigation bar
- `Sidebar` - Left navigation menu
- `StatCard` - KPI card (number + label + trend)
- `UpcomingEventsWidget` - Event preview list
- `RecentTasksWidget` - Task list widget
- `BudgetChart` - Spending overview chart
- `QuickActionButtons` - CTA buttons grid

---

#### `/events` - Events List
Browse all user's events with filtering and sorting.

**Layout**:
- Header with title and create button
- Filter sidebar (status, event type, date range)
- Events grid/list view toggle
- Event cards with key info

**Components**:
- `EventFilters` - Filter panel
- `EventCard` - Event preview card
  - Event title, type, date
  - Guest count, budget status
  - Quick action menu (edit, delete, view)
- `ViewToggle` - Grid/List view switcher
- `EventEmptyState` - CTA when no events
- `Pagination` - For large lists

---

#### `/events/[id]` - Event Detail & Overview
Main event page with tabs for different sections.

**Layout**:
- Header: Event title, dates, location
- Event progress bar (tasks completed, budget used)
- Tabs: Overview, AI Plan, Tasks, Budget, Vendors, Team
- Event actions menu (edit, duplicate, share)

**Components**:
- `EventHeader` - Title, dates, location, actions
- `EventProgressBar` - Tasks and budget progress
- `EventTabs` - Tabbed navigation
- `EventOverviewSection` - Key event details
- `CollaboratorsPreview` - Team members
- `EventActions` - Edit, share, delete buttons

---

#### `/events/[id]/ai-plan` - Event AI Plan
Display AI-generated event planning.

**Sections**:
- Plan overview/summary
- Timeline with phases and milestones
- Detailed tasks by phase
- Budget breakdown by category
- Vendor suggestions
- Regenerate plan button

**Components**:
- `PlanHeader` - Generated date, regenerate button
- `PlanSummary` - Overview text
- `TimelineView` - Visual timeline with phases
  - Phase cards with task list
  - Expandable phase details
  - Task count indicators
- `BudgetBreakdown` - Pie/bar chart by category
- `VendorSuggestions` - Suggested vendor types with search links

---

#### `/events/[id]/tasks` - To-Do Board (Kanban)
Task management with drag-and-drop Kanban board.

**Layout**:
- Header with filters and view options
- Kanban board with columns:
  - Pending
  - In Progress
  - Completed
- Add task button and modal

**Features**:
- Drag-and-drop task cards between columns
- Filter by priority, category, assignee
- Sort by due date, priority
- Quick task creation modal
- Bulk operations (mark complete, delete)

**Components**:
- `TaskFilters` - Filter and search panel
- `KanbanBoard` - Main board component
- `KanbanColumn` - Single status column
- `TaskCard` - Individual task card
  - Title, priority badge, due date
  - Assigned person
  - Quick actions (edit, delete, detail)
- `TaskModal` - Create/edit task form
- `TaskDetail` - Detailed view modal

---

#### `/events/[id]/budget` - Budget Tracking & Analytics
Budget overview, spending tracking, analytics.

**Sections**:
- Budget summary cards (total, spent, remaining)
- Budget vs. actual chart
- Category breakdown (pie chart)
- Transaction list
- Add transaction button
- Budget forecast

**Components**:
- `BudgetHeader` - Total, spent, remaining
- `BudgetCharts` - Line/pie/bar charts (Recharts)
  - Budget vs. actual over time
  - Category breakdown
  - Spending trends
- `TransactionTable` - List of transactions
  - Category, description, amount, status
  - Search and filter
  - Sortable columns
  - Inline actions (edit, delete)
- `AddTransactionForm` - Create transaction modal
- `CategoryStats` - Category-wise breakdown cards
- `UpcomingPayments` - Upcoming dues widget

---

#### `/events/[id]/vendors` - Event Vendors
Saved vendors, contacts, booking status.

**Layout**:
- Vendor list/grid view toggle
- Saved vendors with status
- Vendor contact info and quick links
- Add vendor button (search modal)
- Comparison tool

**Components**:
- `SavedVendorCard` - Vendor preview
  - Name, type, rating
  - Saved status, quoted price
  - Contact buttons
- `VendorStatusBadge` - Status indicator (saved, quoted, booked)
- `VendorSearchModal` - Vendor discovery modal
- `ComparisonButton` - Open comparison view
- `VendorContactForm` - Send inquiry modal

---

#### `/events/[id]/team` - Event Collaborators
Manage event team members and permissions.

**Sections**:
- Collaborators list with roles
- Add collaborator form (by email)
- Permission management
- Remove collaborator button

**Components**:
- `CollaboratorTable` - Collaborators list
  - Name, email, role
  - Permission checkboxes
  - Remove button
- `AddCollaboratorForm` - Email input + role selector
- `RoleSelector` - Role dropdown (owner, admin, collaborator, viewer)
- `PermissionsPanel` - Individual permission checkboxes

---

#### `/events/create` - Create Event Wizard
Multi-step form to create new event.

**Steps**:
1. Event basics (title, type, dates, location)
2. Guest & budget info
3. Event description & preferences
4. Review & create

**Components**:
- `FormWizard` - Multi-step form wrapper
- `StepIndicator` - Show progress (1/4, 2/4, etc.)
- `EventBasicsForm` - Step 1 form
- `GuestBudgetForm` - Step 2 form
- `DescriptionForm` - Step 3 form
- `ReviewStep` - Step 4 summary
- `NavigationButtons` - Next, Previous, Create

---

### Vendor Routes

#### `/vendors` - Vendor Discovery & Search
Browse and search vendors with filters.

**Layout**:
- Search bar at top
- Filters sidebar (type, location, price, rating)
- Vendor grid/list view
- Pagination
- Sorting options

**Components**:
- `SearchBar` - Main search input with filters button
- `FilterSidebar` - Multi-select filters
  - Vendor type (checkboxes)
  - Location/city (search)
  - Price range (slider)
  - Minimum rating (stars)
  - Availability
- `VendorCard` - Vendor preview card (grid view)
  - Name, type, location
  - Rating and review count
  - Portfolio image
  - Price range
  - "View Details" / "Save" buttons
- `VendorListItem` - Vendor row (list view)
  - Similar to card but horizontal
  - More space for description
- `SortDropdown` - Sort by rating, reviews, price
- `ViewToggle` - Grid/List switcher
- `EmptyState` - No results message
- `Pagination` - Navigate results

---

#### `/vendors/[id]` - Vendor Detail Page
Comprehensive vendor information and reviews.

**Sections**:
- Hero section with portfolio images
- Vendor info card (name, type, location, contact)
- Rating and reviews summary
- Detailed review list
- Service details and pricing
- Availability and booking info
- Inquiry/Contact button
- Related vendors

**Components**:
- `VendorGallery` - Portfolio image carousel
  - Lightbox/modal for full images
- `VendorInfoCard` - Key vendor details
  - Name, type, location
  - Phone, email, website buttons
  - Social media links
- `RatingsSummary` - Star rating and stats
  - Average rating (large)
  - Review breakdown (5★ count, 4★ count, etc.)
  - "Read reviews" button
- `ReviewsList` - Paginated reviews
  - Review card with rating, title, text
  - Author name, verified badge
  - Helpful vote button
  - Sort options (recent, helpful, rating)
- `ReviewFilters` - Filter by rating
- `ServiceDetails` - Detailed info section
  - Services offered
  - Certifications
  - Response time
  - Cancellation policy
- `PricingTable` - Service pricing
- `AvailabilitySection` - Booking calendar
- `ContactVendorButton` - CTA to contact
- `ContactModal` - Message/inquiry form
- `RelatedVendors` - Carousel of similar vendors

---

#### `/vendors/compare` - Vendor Comparison Tool
Compare multiple vendors side-by-side.

**Layout**:
- Add vendor button/search
- Comparison table with vendors as columns
- Remove vendor button on each column
- Key comparison fields (price, rating, services)
- Visual indicators (best value, best rating, etc.)

**Components**:
- `ComparisonTable` - Main comparison grid
  - Rows: features, price, rating, availability
  - Columns: vendors
  - Color-coded best values
- `AddVendorButton` - Open search modal to add
- `VendorColumn` - Single vendor column
  - Header with vendor name and remove button
  - Feature rows with values
  - Save/Book action buttons
- `FeatureRow` - Single comparison row
  - Feature name on left
  - Values for each vendor
  - Icon/indicators for comparison
- `VendorSearchModal` - Add vendors modal

---

### Profile & Settings Routes

#### `/profile` - User Profile
User profile with personal information and preferences.

**Sections**:
- Profile picture and basic info (name, email)
- Contact information
- Bio/about section
- Edit profile button

**Components**:
- `ProfileHeader` - Avatar, name, edit button
- `ProfileForm` - Editable profile fields
  - Full name, phone, email
  - Bio, location
  - Profile picture upload
- `UploadZone` - Drag-and-drop image uploader
- `FormButtons` - Save/Cancel buttons

---

#### `/settings` - Account Settings
App preferences, notifications, privacy, danger zone.

**Sections**:
1. **Preferences**
   - Theme (light/dark)
   - Language
   - Timezone
   - Notification preferences

2. **Privacy & Security**
   - Email visibility
   - Profile visibility
   - Password change
   - Two-factor auth (future)

3. **Notifications**
   - Email notifications toggle
   - Notification frequency
   - Event notifications
   - Task reminders
   - Vendor inquiries

4. **Data & Storage**
   - Download data (future)
   - Clear cache

5. **Danger Zone**
   - Delete account button
   - Confirmation modal

**Components**:
- `SettingSection` - Section wrapper with title
- `ToggleSetting` - Boolean setting toggle
- `SelectSetting` - Dropdown setting
- `PasswordChangeForm` - Current/new password
- `ConfirmationModal` - Danger action confirmation
- `SettingButtons` - Save/Cancel for each section

---

## Shared Components Library

### Layout Components
- `Layout` - Main app layout with header and sidebar
- `Header` - Top navigation bar
- `Sidebar` - Left navigation menu
- `Container` - Content wrapper with max-width
- `Section` - Semantic section wrapper

### Common Components
- `Button` - Reusable button (variants: primary, secondary, danger, ghost)
- `Card` - Content card wrapper
- `Input` - Text input field
- `Select` - Dropdown select
- `Checkbox` - Checkbox input
- `Radio` - Radio button
- `Textarea` - Multi-line text input
- `Label` - Form label

### Form Components
- `Form` - Form wrapper with validation
- `FormField` - Field wrapper with label and error
- `FormError` - Error message display
- `SubmitButton` - Styled submit button
- `FormGroup` - Group of fields

### Data Display
- `Table` - Data table with sorting/pagination
- `DataGrid` - Advanced data grid (future)
- `List` - Ordered/unordered list
- `Pagination` - Pagination controls
- `Badge` - Status badges and labels
- `Avatar` - User avatar component
- `AvatarGroup` - Group of avatars

### Modals & Overlays
- `Modal` - Modal dialog wrapper
- `Dialog` - Confirmation dialog
- `Drawer` - Side drawer/panel
- `Toast` - Notification toast (via Sonner)
- `AlertDialog` - Alert/confirmation modal

### Navigation & Menu
- `Tabs` - Tabbed interface
- `Tab` - Individual tab
- `Menu` - Dropdown menu
- `MenuItem` - Menu item
- `Breadcrumb` - Breadcrumb navigation
- `Pagination` - Pagination controls

### Chart Components (Recharts)
- `LineChart` - Line chart
- `BarChart` - Bar chart
- `PieChart` - Pie chart
- `AreaChart` - Area chart
- `Tooltip` - Chart tooltip

### Specialized Components
- `Calendar` - Date picker (React Datepicker or similar)
- `DateInput` - Date input field
- `StarRating` - Star rating display/input
- `LoadingSpinner` - Loading indicator
- `EmptyState` - Empty content placeholder
- `ErrorBoundary` - Error boundary wrapper
- `SkeletonLoader` - Content skeleton loaders

---

## State Management

### Zustand Stores
```typescript
// stores/userStore.ts
- currentUser
- setUser
- logout
- updateProfile

// stores/eventStore.ts
- currentEvent
- events
- setCurrentEvent
- addEvent
- updateEvent
- deleteEvent

// stores/filterStore.ts
- activeFilters
- setFilter
- clearFilters

// stores/uiStore.ts
- sidebarOpen
- theme
- toggleSidebar
- setTheme
```

### TanStack Query (Server State)
```typescript
// hooks/queries
- useEvents() - Get user's events
- useEvent(id) - Get single event
- useAIPlan(eventId) - Get AI plan
- useTasks(eventId) - Get event tasks
- useBudget(eventId) - Get budget data
- useVendors(filters) - Search vendors
- useVendor(id) - Get vendor details
- useVendorReviews(vendorId) - Get reviews
- useSavedVendors(eventId) - Get saved vendors

// hooks/mutations
- useCreateEvent()
- useUpdateEvent()
- useDeleteEvent()
- useCreateTask()
- useUpdateTask()
- useDeleteTask()
- useSaveVendor()
- useAddTransaction()
- useGenerateAIPlan()
```

### API Client
```typescript
// lib/api-client.ts
- EventService
  - createEvent()
  - getEvents()
  - getEvent()
  - updateEvent()
  - deleteEvent()
  - generateAIPlan()

- VendorService
  - searchVendors()
  - getVendor()
  - getReviews()
  - addReview()

- TaskService
  - getTasks()
  - createTask()
  - updateTask()
  - deleteTask()

- BudgetService
  - getTransactions()
  - addTransaction()
  - updateTransaction()
  - deleteTransaction()
  - getBudgetSummary()
```

---

## Styling & Theme

### Tailwind CSS
- Custom color palette
- Component-scoped utilities
- Dark mode support via Zustand theme store

### ShadCN UI
- Pre-built, customizable components
- Accessible components out of the box
- Consistent design system

### Animations (Framer Motion)
- Page transitions
- Modal/drawer animations
- Card hover effects
- Loading states
- Task completion animations

---

## Key Features & Interactions

### Event Creation Flow
1. User clicks "Create Event" → Opens wizard modal
2. Fill event details across steps
3. AI plan automatically generated on creation
4. Redirect to event dashboard

### Vendor Search Flow
1. User searches vendors on `/vendors`
2. Select vendors and compare
3. Save favorites to event
4. Track vendor communication status

### Budget Tracking Flow
1. User adds transactions from budget tab
2. Real-time calculation of spent vs. budget
3. Visual indicators for overages
4. Export report (future)

### Task Management Flow
1. User creates tasks from AI plan or manually
2. Drag tasks between status columns
3. Assign to team members
4. Track completion progress

---

## Accessibility

- ARIA labels on all interactive elements
- Keyboard navigation support
- Color contrast compliance (WCAG AA)
- Focus indicators on buttons and inputs
- Semantic HTML structure

---

## Performance Optimizations

- Code splitting with dynamic imports
- Image optimization (Next.js Image)
- Lazy loading for modals and heavy components
- TanStack Query caching
- Debounced search inputs
- Pagination for large lists

---

## Error Handling & Loading States

- Error boundaries for component errors
- Toast notifications for API errors
- Loading skeletons instead of spinners
- Optimistic updates in mutations
- Retry logic for failed requests
- Fallback UI for network errors

---

## Future Enhancements

- Real-time collaboration (WebSocket)
- Mobile app (React Native)
- Email notifications with templates
- PDF export for plans and budgets
- Calendar integration
- Payment processing integration
- Video tours and onboarding
- Advanced search with full-text search
