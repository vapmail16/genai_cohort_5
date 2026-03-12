-- =====================================================
-- IT Support Portal - Audit Trigger
-- =====================================================
-- This trigger automatically logs all INSERT, UPDATE, and DELETE
-- operations on the tickets table to the audit_log table.
-- The old and new row values are stored as JSONB for easy querying.
-- =====================================================

-- Create the audit trigger function
-- This function is called automatically whenever a ticket is modified
CREATE OR REPLACE FUNCTION audit_ticket_changes()
RETURNS TRIGGER AS $$
DECLARE
    v_action VARCHAR(50);
    v_old_value JSONB;
    v_new_value JSONB;
    v_changed_by UUID;
BEGIN
    -- Determine the action type
    v_action := TG_OP;

    -- Extract the user who made the change
    -- For INSERT/UPDATE, use the assigned_to or submitted_by user
    -- For DELETE, use the old assigned_to or submitted_by user
    IF TG_OP = 'DELETE' THEN
        v_changed_by := OLD.assigned_to;
        IF v_changed_by IS NULL THEN
            v_changed_by := OLD.submitted_by;
        END IF;
    ELSE
        v_changed_by := NEW.assigned_to;
        IF v_changed_by IS NULL THEN
            v_changed_by := NEW.submitted_by;
        END IF;
    END IF;

    -- Convert old and new rows to JSONB
    -- Only store old_value for UPDATE and DELETE
    -- Only store new_value for INSERT and UPDATE
    IF TG_OP = 'INSERT' THEN
        v_old_value := NULL;
        v_new_value := to_jsonb(NEW);
    ELSIF TG_OP = 'UPDATE' THEN
        v_old_value := to_jsonb(OLD);
        v_new_value := to_jsonb(NEW);
    ELSIF TG_OP = 'DELETE' THEN
        v_old_value := to_jsonb(OLD);
        v_new_value := NULL;
    END IF;

    -- Insert audit log entry
    INSERT INTO audit_log (
        ticket_id,
        action,
        old_value,
        new_value,
        changed_by,
        changed_at
    ) VALUES (
        COALESCE(NEW.id, OLD.id),
        v_action,
        v_old_value,
        v_new_value,
        v_changed_by,
        CURRENT_TIMESTAMP
    );

    -- Return the appropriate row based on operation
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Attach the trigger to the tickets table
-- AFTER trigger ensures the operation completes before logging
CREATE TRIGGER trigger_audit_ticket_changes
    AFTER INSERT OR UPDATE OR DELETE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION audit_ticket_changes();

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON FUNCTION audit_ticket_changes() IS 'Automatically logs all changes to tickets table in audit_log';
COMMENT ON TRIGGER trigger_audit_ticket_changes ON tickets IS 'Triggers audit logging for all ticket modifications';
