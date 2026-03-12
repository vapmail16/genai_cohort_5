-- =====================================================
-- IT Support Portal - Seed Data
-- =====================================================
-- This script populates the database with realistic test data
-- including users, categories, tickets, and comments.
-- Includes edge cases like SLA breaches and unassigned tickets.
-- =====================================================

-- Clear existing data (for re-running the seed script)
TRUNCATE TABLE audit_log, ticket_comments, tickets, categories, users CASCADE;

-- =====================================================
-- USERS (15 total: 10 employees, 3 IT agents, 1 IT manager, 1 inactive)
-- =====================================================

INSERT INTO users (id, email, full_name, role, department, is_active) VALUES
-- IT Manager
('11111111-1111-1111-1111-111111111111', 'sarah.johnson@acmecorp.com', 'Sarah Johnson', 'it_manager', 'IT Support', TRUE),

-- IT Agents
('22222222-2222-2222-2222-222222222222', 'mike.chen@acmecorp.com', 'Mike Chen', 'it_agent', 'IT Support', TRUE),
('33333333-3333-3333-3333-333333333333', 'alex.rivera@acmecorp.com', 'Alex Rivera', 'it_agent', 'IT Support', TRUE),
('44444444-4444-4444-4444-444444444444', 'emma.williams@acmecorp.com', 'Emma Williams', 'it_agent', 'IT Support', TRUE),

-- Employees (Active)
('55555555-5555-5555-5555-555555555555', 'john.doe@acmecorp.com', 'John Doe', 'employee', 'Sales', TRUE),
('66666666-6666-6666-6666-666666666666', 'jane.smith@acmecorp.com', 'Jane Smith', 'employee', 'Marketing', TRUE),
('77777777-7777-7777-7777-777777777777', 'robert.brown@acmecorp.com', 'Robert Brown', 'employee', 'Finance', TRUE),
('88888888-8888-8888-8888-888888888888', 'lisa.davis@acmecorp.com', 'Lisa Davis', 'employee', 'HR', TRUE),
('99999999-9999-9999-9999-999999999999', 'david.wilson@acmecorp.com', 'David Wilson', 'employee', 'Engineering', TRUE),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'maria.garcia@acmecorp.com', 'Maria Garcia', 'employee', 'Sales', TRUE),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'james.taylor@acmecorp.com', 'James Taylor', 'employee', 'Marketing', TRUE),
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'patricia.anderson@acmecorp.com', 'Patricia Anderson', 'employee', 'Finance', TRUE),
('dddddddd-dddd-dddd-dddd-dddddddddddd', 'michael.thomas@acmecorp.com', 'Michael Thomas', 'employee', 'Operations', TRUE),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'jennifer.martinez@acmecorp.com', 'Jennifer Martinez', 'employee', 'Engineering', TRUE),

-- Inactive Employee
('ffffffff-ffff-ffff-ffff-ffffffffffff', 'inactive.user@acmecorp.com', 'Inactive User', 'employee', 'Sales', FALSE);

-- =====================================================
-- CATEGORIES (6 categories with different SLA requirements)
-- =====================================================

INSERT INTO categories (id, name, description, sla_hours, escalation_hours) VALUES
('c1111111-1111-1111-1111-111111111111', 'VPN', 'VPN connectivity and configuration issues', 4, 2),
('c2222222-2222-2222-2222-222222222222', 'Hardware', 'Computer hardware issues, peripherals, and equipment requests', 24, 12),
('c3333333-3333-3333-3333-333333333333', 'Software', 'Software installation, licensing, and application issues', 8, 4),
('c4444444-4444-4444-4444-444444444444', 'Account Access', 'Password resets, account lockouts, and access permissions', 2, 1),
('c5555555-5555-5555-5555-555555555555', 'Email', 'Email configuration, delivery issues, and mailbox problems', 4, 2),
('c6666666-6666-6666-6666-666666666666', 'Other', 'General IT support requests not fitting other categories', 48, 24);

-- =====================================================
-- TICKETS (25 tickets with variety of statuses and priorities)
-- =====================================================

-- Ticket 1: SLA BREACHED - Created 6 days ago, VPN issue (SLA: 4h)
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t1111111-1111-1111-1111-111111111111',
 'Cannot connect to VPN from home',
 'I have been trying to connect to the company VPN from my home network for the past two days. I keep getting error code 809. I need access urgently as I am working remotely this week.',
 'resolved',
 'high',
 'c1111111-1111-1111-1111-111111111111',
 '55555555-5555-5555-5555-555555555555',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '6 days',
 CURRENT_TIMESTAMP - INTERVAL '5 days 18 hours',
 CURRENT_TIMESTAMP - INTERVAL '5 days 18 hours',
 'Updated VPN client to latest version and reconfigured server settings. Issue resolved.');

-- Ticket 2: SLA BREACHED - Created 8 days ago, Hardware issue (SLA: 24h)
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t2222222-2222-2222-2222-222222222222',
 'Laptop screen flickering constantly',
 'My laptop screen has been flickering for the past week. It is making it very difficult to work. Sometimes the screen goes completely black for a few seconds.',
 'resolved',
 'high',
 'c2222222-2222-2222-2222-222222222222',
 '66666666-6666-6666-6666-666666666666',
 '33333333-3333-3333-3333-333333333333',
 CURRENT_TIMESTAMP - INTERVAL '8 days',
 CURRENT_TIMESTAMP - INTERVAL '5 days',
 CURRENT_TIMESTAMP - INTERVAL '5 days',
 'Replaced display cable and updated graphics drivers. Screen flickering has stopped.');

-- Ticket 3: SLA BREACHED - Created 10 days ago, Email issue (SLA: 4h)
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t3333333-3333-3333-3333-333333333333',
 'Not receiving emails from external clients',
 'I have not been receiving any emails from external clients since last week. Internal emails are working fine. This is affecting my ability to communicate with customers.',
 'resolved',
 'critical',
 'c5555555-5555-5555-5555-555555555555',
 '77777777-7777-7777-7777-777777777777',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '10 days',
 CURRENT_TIMESTAMP - INTERVAL '9 days 12 hours',
 CURRENT_TIMESTAMP - INTERVAL '9 days 12 hours',
 'Email filter was blocking external domains. Removed the filter and restored mailbox. All emails are now being received.');

-- Ticket 4: UNASSIGNED - New ticket
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t4444444-4444-4444-4444-444444444444',
 'Request for Adobe Creative Cloud license',
 'I need an Adobe Creative Cloud license for my role in the Marketing department. I will be creating graphics and videos for our upcoming campaign.',
 'new',
 'medium',
 'c3333333-3333-3333-3333-333333333333',
 '88888888-8888-8888-8888-888888888888',
 NULL,
 CURRENT_TIMESTAMP - INTERVAL '2 hours',
 CURRENT_TIMESTAMP - INTERVAL '2 hours');

-- Ticket 5: UNASSIGNED - New ticket
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t5555555-5555-5555-5555-555555555555',
 'Keyboard not working after coffee spill',
 'I accidentally spilled coffee on my keyboard this morning. Some keys are not responding. I need a replacement keyboard as soon as possible.',
 'new',
 'high',
 'c2222222-2222-2222-2222-222222222222',
 '99999999-9999-9999-9999-999999999999',
 NULL,
 CURRENT_TIMESTAMP - INTERVAL '30 minutes',
 CURRENT_TIMESTAMP - INTERVAL '30 minutes');

-- Ticket 6: In Progress - Account Access
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t6666666-6666-6666-6666-666666666666',
 'Account locked after multiple failed login attempts',
 'My account has been locked after I entered my password incorrectly several times. I need it unlocked urgently to access important files.',
 'in_progress',
 'high',
 'c4444444-4444-4444-4444-444444444444',
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '44444444-4444-4444-4444-444444444444',
 CURRENT_TIMESTAMP - INTERVAL '1 hour',
 CURRENT_TIMESTAMP - INTERVAL '30 minutes');

-- Ticket 7: Resolved - Software
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t7777777-7777-7777-7777-777777777777',
 'Microsoft Teams crashing on startup',
 'Microsoft Teams keeps crashing whenever I try to open it. I have tried restarting my computer but the issue persists.',
 'resolved',
 'medium',
 'c3333333-3333-3333-3333-333333333333',
 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '3 days',
 CURRENT_TIMESTAMP - INTERVAL '2 days 20 hours',
 CURRENT_TIMESTAMP - INTERVAL '2 days 20 hours',
 'Cleared Teams cache and reinstalled application. Teams is now working normally.');

-- Ticket 8: In Progress - VPN
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t8888888-8888-8888-8888-888888888888',
 'VPN connection very slow',
 'When I connect to the VPN, my internet speed becomes extremely slow. Downloads that normally take seconds are taking several minutes.',
 'in_progress',
 'medium',
 'c1111111-1111-1111-1111-111111111111',
 'cccccccc-cccc-cccc-cccc-cccccccccccc',
 '33333333-3333-3333-3333-333333333333',
 CURRENT_TIMESTAMP - INTERVAL '5 hours',
 CURRENT_TIMESTAMP - INTERVAL '2 hours');

-- Ticket 9: Closed - Hardware
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t9999999-9999-9999-9999-999999999999',
 'Need second monitor for workstation',
 'I would like to request a second monitor to improve my productivity. My current setup has only one monitor.',
 'closed',
 'low',
 'c2222222-2222-2222-2222-222222222222',
 'dddddddd-dddd-dddd-dddd-dddddddddddd',
 '44444444-4444-4444-4444-444444444444',
 CURRENT_TIMESTAMP - INTERVAL '7 days',
 CURRENT_TIMESTAMP - INTERVAL '4 days',
 CURRENT_TIMESTAMP - INTERVAL '4 days',
 'Second monitor delivered and set up at workstation. Ticket closed.');

-- Ticket 10: New - Email
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t1010101-1010-1010-1010-101010101010',
 'Cannot send emails with large attachments',
 'I am unable to send emails with attachments larger than 10MB. I frequently need to send design files to clients.',
 'new',
 'medium',
 'c5555555-5555-5555-5555-555555555555',
 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '4 hours',
 CURRENT_TIMESTAMP - INTERVAL '4 hours');

-- Ticket 11: In Progress - Software
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t1111112-1111-1111-1111-111111111111',
 'Excel macros not working after update',
 'After the recent Excel update, my macros are not working. I use these macros daily for financial reporting.',
 'in_progress',
 'high',
 'c3333333-3333-3333-3333-333333333333',
 '77777777-7777-7777-7777-777777777777',
 '44444444-4444-4444-4444-444444444444',
 CURRENT_TIMESTAMP - INTERVAL '6 hours',
 CURRENT_TIMESTAMP - INTERVAL '3 hours');

-- Ticket 12: Resolved - Account Access
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t1212121-1212-1212-1212-121212121212',
 'Need access to shared drive for new project',
 'I have been assigned to a new project and need access to the shared drive folder. My manager has already approved this request.',
 'resolved',
 'medium',
 'c4444444-4444-4444-4444-444444444444',
 '55555555-5555-5555-5555-555555555555',
 '33333333-3333-3333-3333-333333333333',
 CURRENT_TIMESTAMP - INTERVAL '1 day',
 CURRENT_TIMESTAMP - INTERVAL '23 hours',
 CURRENT_TIMESTAMP - INTERVAL '23 hours',
 'Access granted to shared drive folder. User confirmed they can now access the files.');

-- Ticket 13: New - Other
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t1313131-1313-1313-1313-131313131313',
 'Printer not connecting to network',
 'The printer on the 3rd floor is not connecting to the network. Multiple people are unable to print their documents.',
 'new',
 'medium',
 'c6666666-6666-6666-6666-666666666666',
 '66666666-6666-6666-6666-666666666666',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '1 hour',
 CURRENT_TIMESTAMP - INTERVAL '1 hour');

-- Ticket 14: Cancelled - Hardware
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t1414141-1414-1414-1414-141414141414',
 'Request for standing desk',
 'I would like to request a standing desk for ergonomic reasons.',
 'cancelled',
 'low',
 'c2222222-2222-2222-2222-222222222222',
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '44444444-4444-4444-4444-444444444444',
 CURRENT_TIMESTAMP - INTERVAL '5 days',
 CURRENT_TIMESTAMP - INTERVAL '4 days',
 CURRENT_TIMESTAMP - INTERVAL '4 days',
 'Cancelled by user - decided to purchase own standing desk converter instead.');

-- Ticket 15: Resolved - VPN
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t1515151-1515-1515-1515-151515151515',
 'VPN disconnects frequently',
 'My VPN connection drops every 15-20 minutes. I have to reconnect multiple times throughout the day.',
 'resolved',
 'medium',
 'c1111111-1111-1111-1111-111111111111',
 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
 '33333333-3333-3333-3333-333333333333',
 CURRENT_TIMESTAMP - INTERVAL '2 days',
 CURRENT_TIMESTAMP - INTERVAL '1 day 18 hours',
 CURRENT_TIMESTAMP - INTERVAL '1 day 18 hours',
 'Updated VPN timeout settings and switched to more stable server. Connection is now stable.');

-- Ticket 16: In Progress - Email
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t1616161-1616-1616-1616-161616161616',
 'Emails going to spam folder',
 'My emails to clients are going to their spam folders. This is affecting my business communications.',
 'in_progress',
 'high',
 'c5555555-5555-5555-5555-555555555555',
 '88888888-8888-8888-8888-888888888888',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '8 hours',
 CURRENT_TIMESTAMP - INTERVAL '5 hours');

-- Ticket 17: New - Software
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t1717171-1717-1717-1717-171717171717',
 'Need Zoom Pro license for client meetings',
 'I need a Zoom Pro license to host client meetings longer than 40 minutes. This is essential for my role in Sales.',
 'new',
 'medium',
 'c3333333-3333-3333-3333-333333333333',
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '44444444-4444-4444-4444-444444444444',
 CURRENT_TIMESTAMP - INTERVAL '3 hours',
 CURRENT_TIMESTAMP - INTERVAL '3 hours');

-- Ticket 18: Resolved - Account Access
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t1818181-1818-1818-1818-181818181818',
 'Forgot password - need reset',
 'I forgot my password and need it reset. I cannot access my email to receive the reset link.',
 'resolved',
 'critical',
 'c4444444-4444-4444-4444-444444444444',
 '99999999-9999-9999-9999-999999999999',
 '33333333-3333-3333-3333-333333333333',
 CURRENT_TIMESTAMP - INTERVAL '2 days',
 CURRENT_TIMESTAMP - INTERVAL '2 days',
 CURRENT_TIMESTAMP - INTERVAL '2 days',
 'Password reset completed. User verified identity and created new password.');

-- Ticket 19: Closed - Hardware
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t1919191-1919-1919-1919-191919191919',
 'Mouse not working - need replacement',
 'My mouse stopped working. I have tried different USB ports but it is still not responding.',
 'closed',
 'low',
 'c2222222-2222-2222-2222-222222222222',
 'dddddddd-dddd-dddd-dddd-dddddddddddd',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '3 days',
 CURRENT_TIMESTAMP - INTERVAL '2 days 20 hours',
 CURRENT_TIMESTAMP - INTERVAL '2 days 20 hours',
 'Replacement mouse delivered. Old mouse disposed of. Ticket closed.');

-- Ticket 20: In Progress - Other
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t2020202-2020-2020-2020-202020202020',
 'WiFi signal weak in conference room B',
 'The WiFi signal in conference room B is very weak. This is affecting our video calls with clients.',
 'in_progress',
 'medium',
 'c6666666-6666-6666-6666-666666666666',
 'cccccccc-cccc-cccc-cccc-cccccccccccc',
 '44444444-4444-4444-4444-444444444444',
 CURRENT_TIMESTAMP - INTERVAL '1 day',
 CURRENT_TIMESTAMP - INTERVAL '18 hours');

-- Ticket 21: New - Software
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t2121212-2121-2121-2121-212121212121',
 'PowerPoint slides not saving automatically',
 'My PowerPoint presentations are not auto-saving. I lost 2 hours of work yesterday when the application crashed.',
 'new',
 'high',
 'c3333333-3333-3333-3333-333333333333',
 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
 '33333333-3333-3333-3333-333333333333',
 CURRENT_TIMESTAMP - INTERVAL '90 minutes',
 CURRENT_TIMESTAMP - INTERVAL '90 minutes');

-- Ticket 22: Resolved - VPN
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t2222223-2222-2222-2222-222222222222',
 'Cannot access internal resources via VPN',
 'I can connect to the VPN but cannot access internal file shares or intranet.',
 'resolved',
 'high',
 'c1111111-1111-1111-1111-111111111111',
 '55555555-5555-5555-5555-555555555555',
 '22222222-2222-2222-2222-222222222222',
 CURRENT_TIMESTAMP - INTERVAL '12 hours',
 CURRENT_TIMESTAMP - INTERVAL '10 hours',
 CURRENT_TIMESTAMP - INTERVAL '10 hours',
 'Updated routing table and DNS settings. User can now access all internal resources via VPN.');

-- Ticket 23: New - Email
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t2323232-2323-2323-2323-232323232323',
 'Outlook freezes when opening calendar',
 'Outlook freezes and becomes unresponsive whenever I try to open my calendar. I need access to my schedule for upcoming meetings.',
 'new',
 'high',
 'c5555555-5555-5555-5555-555555555555',
 '66666666-6666-6666-6666-666666666666',
 '44444444-4444-4444-4444-444444444444',
 CURRENT_TIMESTAMP - INTERVAL '45 minutes',
 CURRENT_TIMESTAMP - INTERVAL '45 minutes');

-- Ticket 24: Closed - Account Access
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at, resolved_at, resolution_note) VALUES
('t2424242-2424-2424-2424-242424242424',
 'Remove access for departing employee',
 'Employee John Smith is leaving the company next week. Please remove all system access.',
 'closed',
 'high',
 'c4444444-4444-4444-4444-444444444444',
 '88888888-8888-8888-8888-888888888888',
 '11111111-1111-1111-1111-111111111111',
 CURRENT_TIMESTAMP - INTERVAL '2 days',
 CURRENT_TIMESTAMP - INTERVAL '1 day 12 hours',
 CURRENT_TIMESTAMP - INTERVAL '1 day 12 hours',
 'All access removed for departing employee. Account deactivated. Ticket closed.');

-- Ticket 25: In Progress - Hardware
INSERT INTO tickets (id, title, description, status, priority, category_id, submitted_by, assigned_to, created_at, updated_at) VALUES
('t2525252-2525-2525-2525-252525252525',
 'Laptop overheating and shutting down',
 'My laptop gets very hot and shuts down unexpectedly. This happens especially when running multiple applications.',
 'in_progress',
 'critical',
 'c2222222-2222-2222-2222-222222222222',
 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
 '33333333-3333-3333-3333-333333333333',
 CURRENT_TIMESTAMP - INTERVAL '4 hours',
 CURRENT_TIMESTAMP - INTERVAL '2 hours');

-- =====================================================
-- TICKET COMMENTS (10 comments on various tickets)
-- =====================================================

-- Comments on Ticket 1 (VPN issue - resolved)
INSERT INTO ticket_comments (ticket_id, author_id, comment_text, created_at) VALUES
('t1111111-1111-1111-1111-111111111111',
 '22222222-2222-2222-2222-222222222222',
 'I have assigned this ticket to myself. Can you please provide the exact error message you are seeing?',
 CURRENT_TIMESTAMP - INTERVAL '6 days'),

('t1111111-1111-1111-1111-111111111111',
 '55555555-5555-5555-5555-555555555555',
 'The error message is: "The network connection between your computer and the VPN server could not be established because the remote server is not responding. Error 809."',
 CURRENT_TIMESTAMP - INTERVAL '5 days 22 hours');

-- Comments on Ticket 6 (Account locked - in progress)
INSERT INTO ticket_comments (ticket_id, author_id, comment_text, created_at) VALUES
('t6666666-6666-6666-6666-666666666666',
 '44444444-4444-4444-4444-444444444444',
 'I am working on unlocking your account now. For security purposes, I will need to verify your identity. Can you please confirm your employee ID?',
 CURRENT_TIMESTAMP - INTERVAL '45 minutes'),

('t6666666-6666-6666-6666-666666666666',
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'My employee ID is EMP-10567. Thank you for the quick response!',
 CURRENT_TIMESTAMP - INTERVAL '40 minutes');

-- Comments on Ticket 8 (VPN slow - in progress)
INSERT INTO ticket_comments (ticket_id, author_id, comment_text, created_at) VALUES
('t8888888-8888-8888-8888-888888888888',
 '33333333-3333-3333-3333-333333333333',
 'I see you are connecting to the East Coast server. Can you try switching to the West Coast server and let me know if the speed improves?',
 CURRENT_TIMESTAMP - INTERVAL '3 hours'),

('t8888888-8888-8888-8888-888888888888',
 'cccccccc-cccc-cccc-cccc-cccccccccccc',
 'I tried the West Coast server and it is much faster! Should I continue using this server?',
 CURRENT_TIMESTAMP - INTERVAL '2 hours 30 minutes'),

('t8888888-8888-8888-8888-888888888888',
 '33333333-3333-3333-3333-333333333333',
 'Yes, please continue using the West Coast server. I will update your VPN configuration to default to this server. I will resolve this ticket once the configuration is complete.',
 CURRENT_TIMESTAMP - INTERVAL '2 hours 15 minutes');

-- Comments on Ticket 11 (Excel macros - in progress)
INSERT INTO ticket_comments (ticket_id, author_id, comment_text, created_at) VALUES
('t1111112-1111-1111-1111-111111111111',
 '44444444-4444-4444-4444-444444444444',
 'This is likely due to the new Excel security update. I will need to update the macro security settings. Can you send me the error message you are seeing?',
 CURRENT_TIMESTAMP - INTERVAL '4 hours'),

('t1111112-1111-1111-1111-111111111111',
 '77777777-7777-7777-7777-777777777777',
 'The error says "Macros have been disabled due to security settings." I really need these macros for my daily reports.',
 CURRENT_TIMESTAMP - INTERVAL '3 hours 30 minutes');

-- Comment on Ticket 16 (Emails to spam - in progress)
INSERT INTO ticket_comments (ticket_id, author_id, comment_text, created_at) VALUES
('t1616161-1616-1616-1616-161616161616',
 '22222222-2222-2222-2222-222222222222',
 'I am checking the email server logs and SPF records. This may be related to our recent server migration. I will update you shortly.',
 CURRENT_TIMESTAMP - INTERVAL '6 hours');

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Database seeded successfully!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Users created: 15 (10 employees, 3 IT agents, 1 IT manager, 1 inactive)';
    RAISE NOTICE 'Categories created: 6';
    RAISE NOTICE 'Tickets created: 25';
    RAISE NOTICE '  - New: 6 (including 2 unassigned)';
    RAISE NOTICE '  - In Progress: 7';
    RAISE NOTICE '  - Resolved: 8 (including 3 SLA breached)';
    RAISE NOTICE '  - Closed: 3';
    RAISE NOTICE '  - Cancelled: 1';
    RAISE NOTICE 'Comments created: 10';
    RAISE NOTICE '========================================';
END $$;
