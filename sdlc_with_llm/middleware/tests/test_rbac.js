/**
 * Role-Based Access Control (RBAC) Tests
 *
 * TDD RED Phase: Tests written first
 */

const request = require('supertest');
const jwt = require('jsonwebtoken');

describe('RBAC Middleware', () => {
  let app;

  beforeEach(() => {
    jest.clearAllMocks();
    process.env.JWT_SECRET = 'test-secret-key';
    process.env.JWT_EXPIRES_IN = '8h';
    process.env.BACKEND_URL = 'http://localhost:8000';

    delete require.cache[require.resolve('../index.js')];
    app = require('../index.js');
  });

  const generateToken = (role) => {
    return jwt.sign(
      { userId: 1, username: 'testuser', role },
      process.env.JWT_SECRET,
      { expiresIn: '8h' }
    );
  };

  describe('requireRole middleware', () => {
    it('should allow END_USER to access end-user routes', async () => {
      const token = generateToken('END_USER');

      const response = await request(app)
        .get('/test/end-user-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body.message).toBe('End user access granted');
    });

    it('should allow SUPPORT_AGENT to access agent routes', async () => {
      const token = generateToken('SUPPORT_AGENT');

      const response = await request(app)
        .get('/test/agent-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body.message).toBe('Agent access granted');
    });

    it('should allow ADMIN to access admin routes', async () => {
      const token = generateToken('ADMIN');

      const response = await request(app)
        .get('/test/admin-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body.message).toBe('Admin access granted');
    });

    it('should deny END_USER access to agent routes', async () => {
      const token = generateToken('END_USER');

      const response = await request(app)
        .get('/test/agent-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(403);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('Forbidden');
    });

    it('should deny END_USER access to admin routes', async () => {
      const token = generateToken('END_USER');

      const response = await request(app)
        .get('/test/admin-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(403);

      expect(response.body).toHaveProperty('error');
    });

    it('should deny SUPPORT_AGENT access to admin routes', async () => {
      const token = generateToken('SUPPORT_AGENT');

      const response = await request(app)
        .get('/test/admin-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(403);

      expect(response.body).toHaveProperty('error');
    });

    it('should allow multiple roles in requireRole', async () => {
      const agentToken = generateToken('SUPPORT_AGENT');
      const adminToken = generateToken('ADMIN');

      const agentResponse = await request(app)
        .get('/test/agent-or-admin-route')
        .set('Authorization', `Bearer ${agentToken}`)
        .expect(200);

      const adminResponse = await request(app)
        .get('/test/agent-or-admin-route')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(agentResponse.body.message).toBe('Agent or admin access granted');
      expect(adminResponse.body.message).toBe('Agent or admin access granted');
    });

    it('should deny access if role not in allowed list', async () => {
      const token = generateToken('END_USER');

      const response = await request(app)
        .get('/test/agent-or-admin-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(403);

      expect(response.body).toHaveProperty('error');
    });

    it('should require authentication before checking roles', async () => {
      const response = await request(app)
        .get('/test/admin-route')
        .expect(401);

      expect(response.body).toHaveProperty('error');
    });

    it('should include required roles in error message', async () => {
      const token = generateToken('END_USER');

      const response = await request(app)
        .get('/test/agent-route')
        .set('Authorization', `Bearer ${token}`)
        .expect(403);

      expect(response.body.error).toContain('SUPPORT_AGENT');
    });
  });

  describe('Role hierarchy', () => {
    it('should allow ADMIN to access all routes', async () => {
      const adminToken = generateToken('ADMIN');

      const endUserResponse = await request(app)
        .get('/test/end-user-route')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      const agentResponse = await request(app)
        .get('/test/agent-route')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      const adminResponse = await request(app)
        .get('/test/admin-route')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(endUserResponse.body.message).toBeDefined();
      expect(agentResponse.body.message).toBeDefined();
      expect(adminResponse.body.message).toBeDefined();
    });

    it('should allow SUPPORT_AGENT to access end-user routes', async () => {
      const agentToken = generateToken('SUPPORT_AGENT');

      const response = await request(app)
        .get('/test/end-user-route')
        .set('Authorization', `Bearer ${agentToken}`)
        .expect(200);

      expect(response.body.message).toBe('End user access granted');
    });
  });
});
