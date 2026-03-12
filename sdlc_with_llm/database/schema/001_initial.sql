-- =====================================================
-- IT Support Portal - Initial Database Schema
-- =====================================================
-- This schema creates the core tables for the IT Support Portal
-- including users, categories, tickets, comments, and audit logging.
-- All tables use UUID primary keys for better scalability and security.
-- =====================================================

-- Enable UUID extension for generating random UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- ENUMS
-- =====================================================

-- User roles define access levels in the system
CREATE TYPE user_role AS ENUM ('employee', 'it_agent', 'it_manager');

-- Ticket status workflow: new -> in_progress -> resolved/closed
-- 'cancelled' for tickets that are abandoned
CREATE TYPE ticket_status AS ENUM ('new', 'in_progress', 'resolved', 'closed', 'cancelled');

-- Priority levels for ticket triage
CREATE TYPE ticket_priority AS ENUM ('low', 'medium', 'high', 'critical');

-- =====================================================
-- TABLES
-- =====================================================

-- Users table: stores all system users (employees and IT staff)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'employee',
    department VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Categories table: defines ticket categories with SLA requirements
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    sla_hours INTEGER NOT NULL CHECK (sla_hours > 0),
    escalation_hours INTEGER,
    CONSTRAINT valid_escalation CHECK (escalation_hours IS NULL OR escalation_hours <= sla_hours)
);

-- Tickets table: core entity for support requests
CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status ticket_status NOT NULL DEFAULT 'new',
    priority ticket_priority NOT NULL DEFAULT 'medium',
    category_id UUID NOT NULL,
    submitted_by UUID NOT NULL,
    assigned_to UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    resolution_note TEXT,
    CONSTRAINT fk_tickets_category FOREIGN KEY (category_id) REFERENCES categories(id),
    CONSTRAINT fk_tickets_submitted_by FOREIGN KEY (submitted_by) REFERENCES users(id),
    CONSTRAINT fk_tickets_assigned_to FOREIGN KEY (assigned_to) REFERENCES users(id),
    CONSTRAINT resolved_at_with_note CHECK (
        (resolved_at IS NULL AND resolution_note IS NULL) OR
        (resolved_at IS NOT NULL)
    )
);

-- Ticket comments table: conversation thread for each ticket
CREATE TABLE ticket_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID NOT NULL,
    author_id UUID NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comments_ticket FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
    CONSTRAINT fk_comments_author FOREIGN KEY (author_id) REFERENCES users(id)
);

-- Audit log table: tracks all changes to tickets for compliance and debugging
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    changed_by UUID,
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_ticket FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    CONSTRAINT fk_audit_changed_by FOREIGN KEY (changed_by) REFERENCES users(id)
);

-- =====================================================
-- INDEXES
-- =====================================================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Categories indexes
CREATE INDEX idx_categories_name ON categories(name);

-- Tickets indexes - critical for query performance
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_category_id ON tickets(category_id);
CREATE INDEX idx_tickets_submitted_by ON tickets(submitted_by);
CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
CREATE INDEX idx_tickets_updated_at ON tickets(updated_at);
CREATE INDEX idx_tickets_resolved_at ON tickets(resolved_at);

-- Composite index for common query: active tickets by agent
CREATE INDEX idx_tickets_assigned_status ON tickets(assigned_to, status) WHERE assigned_to IS NOT NULL;

-- Composite index for SLA monitoring
CREATE INDEX idx_tickets_category_created ON tickets(category_id, created_at) WHERE status NOT IN ('resolved', 'closed', 'cancelled');

-- Ticket comments indexes
CREATE INDEX idx_comments_ticket_id ON ticket_comments(ticket_id);
CREATE INDEX idx_comments_author_id ON ticket_comments(author_id);
CREATE INDEX idx_comments_created_at ON ticket_comments(created_at);

-- Audit log indexes
CREATE INDEX idx_audit_ticket_id ON audit_log(ticket_id);
CREATE INDEX idx_audit_changed_by ON audit_log(changed_by);
CREATE INDEX idx_audit_changed_at ON audit_log(changed_at);
CREATE INDEX idx_audit_action ON audit_log(action);

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON TABLE users IS 'Stores all system users including employees and IT staff';
COMMENT ON TABLE categories IS 'Ticket categories with SLA requirements';
COMMENT ON TABLE tickets IS 'Core support ticket entity';
COMMENT ON TABLE ticket_comments IS 'Comments and conversation history for tickets';
COMMENT ON TABLE audit_log IS 'Audit trail of all ticket changes';

COMMENT ON COLUMN categories.sla_hours IS 'Service Level Agreement - hours to resolve';
COMMENT ON COLUMN categories.escalation_hours IS 'Hours before automatic escalation';
COMMENT ON COLUMN tickets.resolved_at IS 'Timestamp when ticket was marked resolved';
COMMENT ON COLUMN tickets.resolution_note IS 'Final resolution description';
