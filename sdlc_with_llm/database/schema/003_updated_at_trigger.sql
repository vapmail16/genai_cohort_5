-- =====================================================
-- IT Support Portal - Updated At Trigger
-- =====================================================
-- This trigger automatically updates the updated_at timestamp
-- whenever a ticket is modified (UPDATE operation).
-- This ensures we always have an accurate last-modified timestamp.
-- =====================================================

-- Create the function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_ticket_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    -- Set updated_at to current timestamp
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach the trigger to the tickets table
-- BEFORE trigger ensures the timestamp is set before the row is written
CREATE TRIGGER trigger_update_ticket_timestamp
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION update_ticket_timestamp();

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON FUNCTION update_ticket_timestamp() IS 'Automatically updates the updated_at timestamp on ticket modifications';
COMMENT ON TRIGGER trigger_update_ticket_timestamp ON tickets IS 'Ensures updated_at is always current when a ticket is modified';
