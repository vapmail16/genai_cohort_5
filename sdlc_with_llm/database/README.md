# IT Support Portal - Database Setup

This directory contains the PostgreSQL database schema, migrations, seed data, and testing utilities for the IT Support Portal.

## Prerequisites

- **PostgreSQL 14 or higher** installed locally
- **Python 3.8+** (for running the test connection script)
- **psycopg2** Python package (install with `pip install psycopg2-binary`)

### Verify PostgreSQL Installation

```bash
psql --version
```

You should see output like: `psql (PostgreSQL) 14.x` or higher.

## Database Setup

### 1. Create the Database

```bash
createdb it_support
```

If you need to specify a username:
```bash
createdb -U postgres it_support
```

### 2. Apply Schema Migrations

Run the schema files in order:

```bash
# Apply initial schema (tables, indexes, constraints)
psql -U postgres -d it_support -f schema/001_initial.sql

# Apply audit trigger
psql -U postgres -d it_support -f schema/002_audit_trigger.sql

# Apply updated_at trigger
psql -U postgres -d it_support -f schema/003_updated_at_trigger.sql
```

### 3. Load Seed Data

```bash
psql -U postgres -d it_support -f seed.sql
```

## Verification

### Using SQL

Connect to the database and verify the setup:

```bash
psql -U postgres -d it_support
```

Run these verification queries:

```sql
-- Check tables were created
\dt

-- Count records in each table
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'tickets', COUNT(*) FROM tickets
UNION ALL
SELECT 'ticket_comments', COUNT(*) FROM ticket_comments
UNION ALL
SELECT 'audit_log', COUNT(*) FROM audit_log;

-- Verify triggers exist
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE event_object_schema = 'public';

-- Check for SLA-breached tickets
SELECT
    t.id,
    t.title,
    t.status,
    c.name as category,
    c.sla_hours,
    EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600 as hours_to_resolve
FROM tickets t
JOIN categories c ON t.category_id = c.id
WHERE t.resolved_at IS NOT NULL
    AND EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600 > c.sla_hours;

-- Check for unassigned tickets
SELECT id, title, status, priority FROM tickets WHERE assigned_to IS NULL;

-- Exit psql
\q
```

### Using Python Test Script

```bash
python test_connection.py
```

This script will:
- Test database connectivity
- Count records in all tables
- Verify triggers are installed
- Check for SLA-breached tickets
- Identify unassigned tickets

## Database Schema Overview

### Tables

1. **users** - System users (employees, IT agents, IT managers)
2. **categories** - Ticket categories with SLA requirements
3. **tickets** - Core support tickets
4. **ticket_comments** - Comments/conversation on tickets
5. **audit_log** - Automatic audit trail of all ticket changes

### Key Features

- **UUID Primary Keys**: All tables use UUIDs for better security and scalability
- **Automatic Timestamps**: `created_at` and `updated_at` are managed automatically
- **Audit Logging**: All ticket changes are automatically logged via triggers
- **SLA Tracking**: Categories have SLA hours for compliance monitoring
- **Referential Integrity**: All foreign keys enforce data consistency
- **Comprehensive Indexes**: Optimized for common query patterns

### Enums

- **user_role**: `employee`, `it_agent`, `it_manager`
- **ticket_status**: `new`, `in_progress`, `resolved`, `closed`, `cancelled`
- **ticket_priority**: `low`, `medium`, `high`, `critical`

## Seed Data Summary

The seed data includes:

- **15 Users**:
  - 1 IT Manager
  - 3 IT Agents
  - 10 Active Employees
  - 1 Inactive Employee

- **6 Categories**:
  - VPN (4h SLA)
  - Hardware (24h SLA)
  - Software (8h SLA)
  - Account Access (2h SLA)
  - Email (4h SLA)
  - Other (48h SLA)

- **25 Tickets**:
  - 6 New (including 2 unassigned)
  - 7 In Progress
  - 8 Resolved (including 3 SLA-breached)
  - 3 Closed
  - 1 Cancelled
  - Mix of all priority levels

- **10 Comments**: Realistic conversation threads on various tickets

### Notable Test Cases

- **SLA Breaches**: 3 resolved tickets that exceeded their category's SLA hours
- **Unassigned Tickets**: 2 new tickets without an assigned agent
- **Inactive User**: 1 user marked as inactive for testing user filtering
- **Various Statuses**: Complete coverage of all ticket statuses

## Reset Database

To start fresh, drop and recreate the database:

```bash
dropdb it_support
createdb it_support
psql -U postgres -d it_support -f schema/001_initial.sql
psql -U postgres -d it_support -f schema/002_audit_trigger.sql
psql -U postgres -d it_support -f schema/003_updated_at_trigger.sql
psql -U postgres -d it_support -f seed.sql
```

## Troubleshooting

### Connection Issues

If you get connection errors, verify PostgreSQL is running:

```bash
# macOS (if installed via Homebrew)
brew services list

# Start PostgreSQL if not running
brew services start postgresql@14
```

### Permission Issues

If you get permission denied errors:

```bash
# Create a postgres superuser if needed
createuser -s postgres
```

### Port Already in Use

PostgreSQL default port is 5432. If it's in use:

```bash
# Check what's using port 5432
lsof -i :5432

# Or specify a different port
psql -U postgres -d it_support -p 5433
```

## Database Schema Diagram

```
┌─────────────────────┐
│      users          │
├─────────────────────┤
│ id (PK, UUID)       │
│ email (UNIQUE)      │
│ full_name           │
│ role (ENUM)         │
│ department          │
│ created_at          │
│ is_active           │
└─────────────────────┘
         ▲
         │
         │ submitted_by, assigned_to, changed_by
         │
         ├────────────┐
         │            │
┌────────┴────────┐   │
│   categories    │   │
├─────────────────┤   │
│ id (PK, UUID)   │   │
│ name (UNIQUE)   │   │
│ description     │   │
│ sla_hours       │   │
│ escalation_hrs  │   │
└────────┬────────┘   │
         │            │
         │ category_id│
         │            │
┌────────▼────────────▼───────┐
│       tickets              │
├────────────────────────────┤
│ id (PK, UUID)              │
│ title                      │
│ description                │
│ status (ENUM)              │
│ priority (ENUM)            │
│ category_id (FK)           │
│ submitted_by (FK)          │
│ assigned_to (FK)           │
│ created_at                 │
│ updated_at (auto-trigger)  │
│ resolved_at                │
│ resolution_note            │
└────────┬───────────────────┘
         │
         │ ticket_id
         │
         ├─────────────────┐
         │                 │
┌────────▼──────────┐  ┌───▼──────────────┐
│ ticket_comments   │  │   audit_log      │
├───────────────────┤  ├──────────────────┤
│ id (PK, UUID)     │  │ id (PK, UUID)    │
│ ticket_id (FK)    │  │ ticket_id (FK)   │
│ author_id (FK)    │  │ action           │
│ comment_text      │  │ old_value (JSON) │
│ created_at        │  │ new_value (JSON) │
└───────────────────┘  │ changed_by (FK)  │
                       │ changed_at       │
                       └──────────────────┘
                       (auto-populated
                        via trigger)
```

## Next Steps

After setting up the database:

1. Configure your application's database connection string
2. Run the test connection script to verify connectivity
3. Review the seed data to understand the test scenarios
4. Begin developing your application logic
5. Write integration tests using the seeded data

## Support

For issues or questions about the database setup, please refer to:
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Project User Stories: ../USER_STORIES.md
