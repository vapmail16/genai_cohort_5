# IT Support Portal - Backend API

FastAPI backend built following TDD (Test-Driven Development) Gold Standard methodology.

## Project Structure

```
backend/
├── database/
│   ├── __init__.py
│   └── connection.py          # Async SQLAlchemy setup
├── models/                    # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── audit_log.py
│   ├── category.py
│   ├── comment.py
│   ├── ticket.py
│   └── user.py
├── routers/                   # FastAPI route handlers
│   ├── __init__.py
│   ├── analytics.py           # Dashboard analytics
│   ├── tickets.py             # Ticket CRUD operations
│   └── users.py               # User authentication
├── schemas/                   # Pydantic v2 schemas
│   ├── __init__.py
│   ├── analytics.py
│   └── ticket.py
├── services/                  # Business logic
│   ├── __init__.py
│   └── sla.py                 # SLA checking logic
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── test_analytics.py      # Analytics endpoint tests
│   └── test_tickets.py        # Ticket endpoint tests
├── .env.example               # Environment configuration template
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
```

3. Update `.env` with your configuration:
```
DATABASE_URL=postgresql://postgres:password@localhost/it_support
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Running the Application

Start the development server:
```bash
uvicorn backend.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

Run all tests:
```bash
pytest backend/tests/ -v
```

Run specific test file:
```bash
pytest backend/tests/test_tickets.py -v
pytest backend/tests/test_analytics.py -v
```

Run specific test:
```bash
pytest backend/tests/test_tickets.py::test_create_ticket_success -v
```

## Test Results

**23/23 tests passing** (100% success rate)

### Test Coverage:
- **Analytics Tests (4)**: Summary counts, SLA breach tracking
- **Ticket Tests (19)**: CRUD operations, filtering, pagination, validation, CSV export

### TDD Methodology Confirmed:
1. Tests written FIRST (RED phase)
2. Implementation created to pass tests (GREEN phase)
3. All tests verified passing (REFACTOR phase)

## API Endpoints

### Tickets
- `POST /api/tickets` - Create new ticket
- `GET /api/tickets` - List tickets (with filters & pagination)
- `GET /api/tickets/{id}` - Get single ticket
- `PATCH /api/tickets/{id}` - Update ticket status/resolution
- `PATCH /api/tickets/{id}/assign` - Assign ticket to agent
- `GET /api/tickets/export/csv` - Export tickets to CSV
- `POST /api/tickets/{id}/comments` - **TODO: Reserved for live demo**

### Analytics
- `GET /api/analytics/summary` - Dashboard metrics (open, in-progress, resolved, SLA breaches)

### Users
- `GET /api/users/authenticate` - Authenticate user by username

## Key Features

### SLA Management
- Automatic SLA tracking based on category
- SLA breach detection (check_sla_breach)
- SLA status monitoring (ON_TRACK, AT_RISK, BREACHED)

### Ticket Workflow
- Status transitions: OPEN → IN_PROGRESS → RESOLVED
- Invalid transition prevention (e.g., RESOLVED → OPEN blocked)
- Resolution note required when resolving tickets
- Auto-transition to IN_PROGRESS when assigned

### Filtering & Search
- Filter by: status, category, priority, assigned_to, submitted_by
- Pagination support (page, page_size)
- CSV export with same filter options

### Validation
- Pydantic v2 schemas for request/response validation
- Type hints on all functions
- Comprehensive error handling (404, 400, 422)

## Database Models

- **User**: System users with roles (END_USER, SUPPORT_AGENT, ADMIN)
- **Category**: Ticket categories with SLA hours
- **Ticket**: Support tickets with status, priority, assignments
- **Comment**: Ticket comments (model ready, endpoint reserved for demo)
- **AuditLog**: System change tracking

## Development Notes

- Async/await used throughout for database operations
- SQLAlchemy 2.0 style with async engine
- In-memory SQLite for testing
- PostgreSQL for production
- CORS configured for frontend integration
- Comprehensive docstrings on all functions
- FastAPI best practices followed

## Reserved for Live Demo

The `POST /api/tickets/{id}/comments` endpoint has been intentionally left as a TODO comment in the code. This endpoint will be implemented during the live demonstration to showcase TDD methodology in real-time.

Expected functionality:
- Accept comment_text and user_id
- Create Comment associated with ticket
- Return created comment with user details
- Validate ticket exists
- Update ticket's updated_at timestamp
