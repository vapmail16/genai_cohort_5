# IT Support Portal - Frontend

React 18 frontend application for the IT Support Portal, built with Vite, Tailwind CSS, and React Router v6.

## Tech Stack

- React 18.2
- Vite 5.0 (build tool & dev server)
- Tailwind CSS 3.3 (styling)
- React Router v6 (routing)
- Axios (HTTP client)
- Lucide React (icons)

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.js           # Axios instance with interceptors
│   ├── components/
│   │   └── Layout.jsx          # Main layout with sidebar & header
│   ├── pages/
│   │   ├── Login.jsx           # Login page
│   │   ├── MyTickets.jsx       # List of user's tickets
│   │   ├── SubmitTicket.jsx    # Ticket submission form
│   │   ├── TicketDetail.jsx    # Ticket details view
│   │   └── Dashboard.jsx       # Analytics dashboard (Agents/Admins only)
│   ├── App.jsx                 # Router configuration
│   ├── main.jsx                # React entry point
│   └── index.css               # Tailwind imports & global styles
├── index.html                  # HTML template
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
└── package.json                # Dependencies & scripts
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API Endpoint

The frontend is configured to connect to the middleware at `http://localhost:3001`.

If you need to change this, edit `/Users/user/Desktop/AI/projects/genai_cohort_5/sdlc_with_llm/frontend/src/api/client.js`:

```javascript
const apiClient = axios.create({
  baseURL: 'http://localhost:3001', // Change this URL if needed
  // ...
});
```

### 3. Start Development Server

```bash
npm run dev
```

The application will open automatically at `http://localhost:3000`.

## Available Routes

### Public Routes
- `/login` - Login page

### Protected Routes (require authentication)
- `/tickets` - My Tickets page (all users)
- `/tickets/new` - Submit new ticket form (all users)
- `/tickets/:id` - Ticket detail view (all users)
- `/dashboard` - Analytics dashboard (Support Agents & Admins only)

### Route Protection
- All routes except `/login` require authentication
- Users without a valid token are automatically redirected to `/login`
- 401 responses clear the token and redirect to `/login`

## Test User Credentials

Use these credentials for testing (assuming they're configured in your backend):

**End User:**
- Email: `user@test.com`
- Password: `password`
- Access: Submit tickets, view own tickets

**Support Agent:**
- Email: `agent@test.com`
- Password: `password`
- Access: All end user features + Dashboard

**Admin:**
- Email: `admin@test.com`
- Password: `password`
- Access: Full system access + Dashboard

## Features Overview

### 1. Login Page (`/login`)
- Email + password authentication
- Calls `POST /auth/login` endpoint
- Stores JWT token in localStorage
- Displays inline error messages for invalid credentials
- Redirects to `/tickets` on success

### 2. Submit Ticket Page (`/tickets/new`)
- Form fields:
  - Title (1-200 characters, required)
  - Description (required)
  - Category (dropdown from `GET /api/categories`)
  - Priority (radio buttons: LOW, MEDIUM, HIGH, CRITICAL)
- Client-side validation matching backend rules
- Calls `POST /api/tickets`
- Shows success confirmation with ticket ID
- Prevents double submission (button disabled after click)

### 3. My Tickets Page (`/tickets`)
- Table view of user's submitted tickets
- Fetches `GET /api/tickets?submitted_by=current_user`
- Columns: ID, Title, Category, Priority, Status, Created, Updated
- Color-coded status badges:
  - RED: OPEN
  - AMBER: IN_PROGRESS
  - GREEN: RESOLVED
  - GREY: CLOSED
- Click row to navigate to ticket detail

### 4. Ticket Detail Page (`/tickets/:id`)
- Full ticket information display
- Fetches `GET /api/tickets/{id}`
- Shows:
  - Title, description, status, priority
  - Category with SLA hours
  - Submitter info
  - Assigned agent info
  - Created/updated/resolved timestamps
  - Resolution note (if resolved)
  - SLA breach indicator
- **Comment form EXCLUDED** - Reserved for live demo
  - Placeholder message indicates feature will be added
  - TODO comment in code marks where form will go

### 5. Dashboard Page (`/dashboard`) - Agents/Admins Only
- 4 metric cards from `GET /api/analytics/summary`:
  1. Open Tickets count
  2. In Progress Tickets count
  3. Resolved Today count
  4. SLA Breaches count
- Recent tickets table (last 10 tickets)
- Auto-redirects non-agents to `/tickets`

### 6. Layout Component
- Persistent sidebar navigation
- Navigation items:
  - My Tickets (all users)
  - Submit Ticket (all users)
  - Dashboard (agents/admins only)
- Header with user info
- Logout button (clears token & redirects to login)

## Styling

- Built with Tailwind CSS utility classes
- Responsive design (mobile-friendly)
- Professional color scheme:
  - Primary: Blue (#2563eb)
  - Success: Green (#16a34a)
  - Warning: Amber (#d97706)
  - Error: Red (#dc2626)
  - Gray scale for backgrounds & text
- Consistent spacing and typography
- Hover states and transitions for better UX

## API Client Configuration

The API client (`/Users/user/Desktop/AI/projects/genai_cohort_5/sdlc_with_llm/frontend/src/api/client.js`) includes:

**Request Interceptor:**
- Automatically adds `Authorization: Bearer <token>` header from localStorage

**Response Interceptor:**
- Detects 401 Unauthorized responses
- Clears localStorage (token & user data)
- Redirects to `/login` page

## Build for Production

```bash
npm run build
```

Builds optimized production files to `dist/` directory.

Preview production build:
```bash
npm run preview
```

## Reserved for Live Demo

The **comment form UI** has been intentionally excluded from the Ticket Detail page. This feature will be implemented during the live demonstration to showcase Test-Driven Development (TDD) methodology.

**Expected functionality (to be added):**
- Text area for comment input
- Submit button
- Display existing comments with user info and timestamps
- POST to `/api/tickets/{id}/comments` endpoint

A TODO comment and placeholder message are included in `/Users/user/Desktop/AI/projects/genai_cohort_5/sdlc_with_llm/frontend/src/pages/TicketDetail.jsx` to mark where this feature will be added.

## Notes

- The app uses localStorage for authentication state
- No password hashing on frontend (handled by backend/middleware)
- Form validation mirrors backend validation rules
- All timestamps displayed in user's local timezone
- Responsive tables with horizontal scroll on mobile

## Troubleshooting

**Issue:** API requests fail with CORS errors
- **Solution:** Ensure backend CORS is configured to allow `http://localhost:3000`

**Issue:** 401 errors after login
- **Solution:** Check that middleware is correctly forwarding the auth token

**Issue:** Blank page or console errors
- **Solution:** Check browser console for errors and verify all dependencies are installed

**Issue:** Styles not loading
- **Solution:** Ensure Tailwind CSS is properly configured and `index.css` is imported in `main.jsx`
