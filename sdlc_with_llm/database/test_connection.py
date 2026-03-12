#!/usr/bin/env python3
"""
IT Support Portal - Database Connection Test
==============================================
This script tests the PostgreSQL database connection and verifies
that the schema and seed data have been properly set up.
"""

import sys
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed")
    print("Please install it with: pip install psycopg2-binary")
    sys.exit(1)

# Database connection parameters
DB_CONFIG = {
    'dbname': 'it_support',
    'user': 'postgres',
    'password': '',  # Add password if needed
    'host': 'localhost',
    'port': 5432
}

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message in green"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message in red"""
    print(f"✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"  {text}")

def test_connection():
    """Test database connection"""
    print_header("Testing Database Connection")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print_success("Successfully connected to database 'it_support'")
        return conn
    except psycopg2.OperationalError as e:
        print_error("Failed to connect to database")
        print_info(f"Error: {e}")
        print_info("\nTroubleshooting steps:")
        print_info("1. Verify PostgreSQL is running")
        print_info("2. Check database exists: psql -l")
        print_info("3. Create database if needed: createdb it_support")
        return None

def test_tables(conn):
    """Test that all required tables exist"""
    print_header("Verifying Tables")

    expected_tables = ['users', 'categories', 'tickets', 'ticket_comments', 'audit_log']

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            tables = [row['table_name'] for row in cur.fetchall()]

            all_exist = True
            for table in expected_tables:
                if table in tables:
                    print_success(f"Table '{table}' exists")
                else:
                    print_error(f"Table '{table}' is missing")
                    all_exist = False

            return all_exist
    except Exception as e:
        print_error(f"Error checking tables: {e}")
        return False

def test_record_counts(conn):
    """Test and display record counts"""
    print_header("Checking Record Counts")

    tables = ['users', 'categories', 'tickets', 'ticket_comments', 'audit_log']
    expected_counts = {
        'users': 15,
        'categories': 6,
        'tickets': 25,
        'ticket_comments': 10,
        'audit_log': 25  # One audit entry per ticket from initial INSERT
    }

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            all_correct = True
            for table in tables:
                cur.execute(f"SELECT COUNT(*) as count FROM {table};")
                count = cur.fetchone()['count']
                expected = expected_counts.get(table, 0)

                if count >= expected:
                    print_success(f"{table}: {count} records")
                else:
                    print_error(f"{table}: {count} records (expected at least {expected})")
                    all_correct = False

            return all_correct
    except Exception as e:
        print_error(f"Error counting records: {e}")
        return False

def test_triggers(conn):
    """Test that triggers are installed"""
    print_header("Verifying Triggers")

    expected_triggers = {
        'trigger_audit_ticket_changes': 'tickets',
        'trigger_update_ticket_timestamp': 'tickets'
    }

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT trigger_name, event_object_table
                FROM information_schema.triggers
                WHERE event_object_schema = 'public'
                ORDER BY trigger_name;
            """)
            triggers = {row['trigger_name']: row['event_object_table'] for row in cur.fetchall()}

            all_exist = True
            for trigger_name, table_name in expected_triggers.items():
                if trigger_name in triggers and triggers[trigger_name] == table_name:
                    print_success(f"Trigger '{trigger_name}' on '{table_name}' exists")
                else:
                    print_error(f"Trigger '{trigger_name}' on '{table_name}' is missing")
                    all_exist = False

            return all_exist
    except Exception as e:
        print_error(f"Error checking triggers: {e}")
        return False

def test_sla_breaches(conn):
    """Check for SLA-breached tickets"""
    print_header("Checking SLA-Breached Tickets")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    t.id,
                    t.title,
                    c.name as category,
                    c.sla_hours,
                    EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600 as hours_to_resolve
                FROM tickets t
                JOIN categories c ON t.category_id = c.id
                WHERE t.resolved_at IS NOT NULL
                    AND EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600 > c.sla_hours
                ORDER BY hours_to_resolve DESC;
            """)
            breached_tickets = cur.fetchall()

            if len(breached_tickets) >= 3:
                print_success(f"Found {len(breached_tickets)} SLA-breached tickets")
                for ticket in breached_tickets:
                    print_info(f"  - {ticket['title'][:50]}... ({ticket['category']}, "
                              f"SLA: {ticket['sla_hours']}h, Actual: {ticket['hours_to_resolve']:.1f}h)")
                return True
            else:
                print_error(f"Expected at least 3 SLA-breached tickets, found {len(breached_tickets)}")
                return False
    except Exception as e:
        print_error(f"Error checking SLA breaches: {e}")
        return False

def test_unassigned_tickets(conn):
    """Check for unassigned tickets"""
    print_header("Checking Unassigned Tickets")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, title, status, priority
                FROM tickets
                WHERE assigned_to IS NULL
                ORDER BY created_at DESC;
            """)
            unassigned_tickets = cur.fetchall()

            if len(unassigned_tickets) >= 2:
                print_success(f"Found {len(unassigned_tickets)} unassigned tickets")
                for ticket in unassigned_tickets:
                    print_info(f"  - {ticket['title'][:50]}... (Status: {ticket['status']}, Priority: {ticket['priority']})")
                return True
            else:
                print_error(f"Expected at least 2 unassigned tickets, found {len(unassigned_tickets)}")
                return False
    except Exception as e:
        print_error(f"Error checking unassigned tickets: {e}")
        return False

def test_audit_trigger_functionality(conn):
    """Test that the audit trigger is actually working"""
    print_header("Testing Audit Trigger Functionality")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get initial audit log count
            cur.execute("SELECT COUNT(*) as count FROM audit_log;")
            initial_count = cur.fetchone()['count']

            # Update a ticket to trigger the audit log
            cur.execute("""
                UPDATE tickets
                SET status = 'in_progress'
                WHERE id = (SELECT id FROM tickets WHERE status = 'new' LIMIT 1)
                RETURNING id;
            """)
            updated_ticket_id = cur.fetchone()

            if updated_ticket_id:
                # Check if audit log was created
                cur.execute("SELECT COUNT(*) as count FROM audit_log;")
                new_count = cur.fetchone()['count']

                # Rollback the test change
                conn.rollback()

                if new_count > initial_count:
                    print_success("Audit trigger is working correctly")
                    print_info(f"  Audit log entries increased from {initial_count} to {new_count}")
                    return True
                else:
                    print_error("Audit trigger did not create log entry")
                    return False
            else:
                print_info("No 'new' tickets available to test trigger")
                return True  # Not a failure, just no data to test

    except Exception as e:
        conn.rollback()
        print_error(f"Error testing audit trigger: {e}")
        return False

def test_enums(conn):
    """Test that all enums are created correctly"""
    print_header("Verifying Enums")

    expected_enums = {
        'user_role': ['employee', 'it_agent', 'it_manager'],
        'ticket_status': ['new', 'in_progress', 'resolved', 'closed', 'cancelled'],
        'ticket_priority': ['low', 'medium', 'high', 'critical']
    }

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            all_correct = True
            for enum_name, expected_values in expected_enums.items():
                cur.execute("""
                    SELECT e.enumlabel
                    FROM pg_type t
                    JOIN pg_enum e ON t.oid = e.enumtypid
                    WHERE t.typname = %s
                    ORDER BY e.enumsortorder;
                """, (enum_name,))
                actual_values = [row['enumlabel'] for row in cur.fetchall()]

                if set(actual_values) == set(expected_values):
                    print_success(f"Enum '{enum_name}' has correct values")
                else:
                    print_error(f"Enum '{enum_name}' has incorrect values")
                    print_info(f"  Expected: {expected_values}")
                    print_info(f"  Found: {actual_values}")
                    all_correct = False

            return all_correct
    except Exception as e:
        print_error(f"Error checking enums: {e}")
        return False

def main():
    """Main test execution"""
    print_header("IT Support Portal - Database Test Suite")
    print_info("Database: it_support")
    print_info(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")

    # Test connection
    conn = test_connection()
    if not conn:
        sys.exit(1)

    # Run all tests
    tests = [
        ("Tables", test_tables),
        ("Record Counts", test_record_counts),
        ("Triggers", test_triggers),
        ("Enums", test_enums),
        ("SLA Breaches", test_sla_breaches),
        ("Unassigned Tickets", test_unassigned_tickets),
        ("Audit Trigger", test_audit_trigger_functionality)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func(conn)
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Unexpected error in {test_name}: {e}")
            results.append((test_name, False))

    # Close connection
    conn.close()

    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")

    print("\n" + "=" * 60)
    print(f"  Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n✓ All tests passed! Database is ready to use.")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
