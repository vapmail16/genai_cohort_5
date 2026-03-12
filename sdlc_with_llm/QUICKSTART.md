# IT Support Portal - Quick Start Guide

## What's Built

✅ **Complete full-stack IT support portal** with database, backend (FastAPI), middleware (Express), and frontend (React)
✅ **23 passing backend tests** using Gold Standard TDD methodology
✅ **One feature reserved** for live classroom demo: "Add Comment to Ticket"

---

## Setup (Run Once)

### 1. Database Setup

```bash
# Create database
createdb it_support

# Apply schema
psql -U postgres -d it_support -f database/schema/001_initial.sql
psql -U postgres -d it_support -f database/schema/002_audit_trigger.sql
psql -U postgres -d it_support -f database/schema/003_updated_at_trigger.sql

# Load seed data (15 users, 25 tickets, 10 comments)
psql -U postgres -d it_support -f database/seed.sql

# Verify (should show all tables with data)
python database/test_connection.py
```

### 2. Backend Setup (Python/FastAPI)

```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/it_support" > .env
echo "CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:5173" >> .env
```

### 3. Middleware Setup (Node.js/Express)

```bash
cd middleware
npm install

# Create .env file
cat > .env << 'EOF'
PORT=3001
JWT_SECRET=dev-secret-change-in-production
BACKEND_URL=http://localhost:8000
NODE_ENV=development
EOF
```

### 4. Frontend Setup (React/Vite)

```bash
cd frontend
npm install
```

---

## Daily Usage (Start All Services)

Open 3 terminals:

### Terminal 1: Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```
**Runs on**: http://localhost:8000
**Docs**: http://localhost:8000/docs

### Terminal 2: Middleware (Express)
```bash
cd middleware
npm start
```
**Runs on**: http://localhost:3001

### Terminal 3: Frontend (React)
```bash
cd frontend
npm run dev
```
**Runs on**: http://localhost:5173

---

## Test the Application

### Login Credentials

**IT Manager**:
- Email: `sarah.johnson@acmecorp.com`

**IT Agents**:
- Email: `mike.chen@acmecorp.com`
- Email: `alex.rivera@acmecorp.com`

**Employees**:
- Email: `john.smith@acmecorp.com`
- Email: `jane.doe@acmecorp.com`
- Email: `bob.wilson@acmecorp.com`

(Password authentication not fully implemented - any password works)

### Test Workflow

1. **Open**: http://localhost:5173
2. **Login** as `john.smith@acmecorp.com`
3. **Submit a ticket**: Go to "Submit Ticket"
4. **View tickets**: Go to "My Tickets"
5. **View details**: Click on a ticket
6. **See comments**: Scroll down (read-only for now)
7. **Note**: Can't ADD comments yet - that's the live demo feature!

---

## Run Tests

### Backend Tests (23 tests)
```bash
cd backend
pytest tests/ -v
```
**Expected**: ✅ 23/23 passing (100%)

### Middleware Tests
```bash
cd middleware
npm test
```

---

## Live Demo Feature: "Add Comment to Ticket"

### What's Ready:
- ✅ Database table `ticket_comments` exists
- ✅ Backend model `Comment` exists in `backend/models/comment.py`
- ✅ Frontend displays existing comments

### What to Build Live:
1. **Backend endpoint**: `POST /api/tickets/{id}/comments`
   - File: `backend/routers/tickets.py` (line ~388, see TODO comment)
2. **Frontend form**: Comment submission UI
   - File: `frontend/src/pages/TicketDetail.jsx` (see TODO comment)

### Demo Script (30 min):
1. **Show problem** (2 min): Can't add comments currently
2. **Write test** (8 min): TDD RED phase
3. **Implement backend** (10 min): TDD GREEN phase
4. **Add frontend UI** (8 min): Comment form
5. **Test** (2 min): Add comment, verify in database

---

## Troubleshooting

### Database connection errors
```bash
# Check PostgreSQL is running
psql -U postgres -l

# Recreate database if needed
dropdb it_support
createdb it_support
# Then re-run schema and seed files
```

### Backend port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

### Frontend can't connect to middleware
- Check middleware is running on port 3001
- Check `frontend/src/api/client.js` baseURL is `http://localhost:3001`

---

## Project Structure Summary

```
.
├── database/          ← PostgreSQL schema + seed data
├── backend/           ← FastAPI (Python) - 8 endpoints, 23 tests
├── middleware/        ← Express (Node.js) - Auth, validation, proxy
└── frontend/          ← React + Vite + Tailwind - 6 pages
```

---

## Key Files to Show Students

1. **TDD Example**: `backend/tests/test_tickets.py` - shows RED-GREEN-REFACTOR
2. **User Stories**: `USER_STORIES.md` - shows requirements
3. **Business Problem**: `BUSINESS_PROBLEM.md` - shows problem definition
4. **Database Schema**: `database/schema/001_initial.sql` - shows data model

---

## What's Working

✅ Login with JWT authentication
✅ Submit tickets with validation
✅ View all tickets (filtered by user)
✅ Ticket detail page with SLA status
✅ View existing comments (read-only)
✅ Dashboard with metrics
✅ CSV export
✅ Role-based access control
✅ Rate limiting
✅ Audit logging

## What's Reserved for Demo

❌ Add new comments to tickets (this will be built live in class!)

---

**Status**: 🎯 Ready for class!
