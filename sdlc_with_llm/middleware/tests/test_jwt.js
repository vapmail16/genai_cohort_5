/**
 * JWT Authentication Tests
 *
 * TDD RED Phase: Tests written first
 */

const request = require('supertest');
const jwt = require('jsonwebtoken');

// Mock dependencies
jest.mock('axios');
const axios = require('axios');

describe('JWT Authentication', () => {
  let app;

  beforeEach(() => {
    jest.clearAllMocks();
    // Set up environment variables for testing
    process.env.JWT_SECRET = 'test-secret-key';
    process.env.JWT_EXPIRES_IN = '8h';
    process.env.BACKEND_URL = 'http://localhost:8000';

    // Import app after setting env vars
    delete require.cache[require.resolve('../index.js')];
    app = require('../index.js');
  });

  describe('POST /auth/login', () => {
    it('should return JWT token for valid credentials', async () => {
      // Mock backend response
      axios.get.mockResolvedValue({
        data: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com',
          full_name: 'Test User',
          role: 'END_USER'
        }
      });

      const response = await request(app)
        .post('/auth/login')
        .send({ username: 'testuser' })
        .expect(200);

      expect(response.body).toHaveProperty('token');
      expect(response.body).toHaveProperty('user');
      expect(response.body.user.username).toBe('testuser');

      // Verify token is valid
      const decoded = jwt.verify(response.body.token, process.env.JWT_SECRET);
      expect(decoded.userId).toBe(1);
      expect(decoded.username).toBe('testuser');
      expect(decoded.role).toBe('END_USER');
    });

    it('should return 404 for invalid username', async () => {
      // Mock backend 404 response
      axios.get.mockRejectedValue({
        response: {
          status: 404,
          data: { detail: "User 'invalid' not found" }
        }
      });

      const response = await request(app)
        .post('/auth/login')
        .send({ username: 'invalid' })
        .expect(404);

      expect(response.body).toHaveProperty('error');
    });

    it('should return 400 if username is missing', async () => {
      const response = await request(app)
        .post('/auth/login')
        .send({})
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });

    it('should return 500 if backend is unreachable', async () => {
      axios.get.mockRejectedValue(new Error('Network error'));

      const response = await request(app)
        .post('/auth/login')
        .send({ username: 'testuser' })
        .expect(500);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('verifyToken middleware', () => {
    it('should allow access with valid token', async () => {
      const token = jwt.sign(
        { userId: 1, username: 'testuser', role: 'END_USER' },
        process.env.JWT_SECRET,
        { expiresIn: '8h' }
      );

      // Mock a protected route for testing
      const response = await request(app)
        .get('/test/protected')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body.message).toBe('Access granted');
      expect(response.body.user.userId).toBe(1);
    });

    it('should reject request without token', async () => {
      const response = await request(app)
        .get('/test/protected')
        .expect(401);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('No token provided');
    });

    it('should reject request with invalid token', async () => {
      const response = await request(app)
        .get('/test/protected')
        .set('Authorization', 'Bearer invalid-token')
        .expect(401);

      expect(response.body).toHaveProperty('error');
    });

    it('should reject expired token', async () => {
      const token = jwt.sign(
        { userId: 1, username: 'testuser', role: 'END_USER' },
        process.env.JWT_SECRET,
        { expiresIn: '0s' }
      );

      // Wait to ensure token is expired
      await new Promise(resolve => setTimeout(resolve, 100));

      const response = await request(app)
        .get('/test/protected')
        .set('Authorization', `Bearer ${token}`)
        .expect(401);

      expect(response.body).toHaveProperty('error');
    });

    it('should attach user info to request object', async () => {
      const token = jwt.sign(
        { userId: 2, username: 'agent', role: 'SUPPORT_AGENT' },
        process.env.JWT_SECRET,
        { expiresIn: '8h' }
      );

      const response = await request(app)
        .get('/test/protected')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body.user.userId).toBe(2);
      expect(response.body.user.username).toBe('agent');
      expect(response.body.user.role).toBe('SUPPORT_AGENT');
    });
  });

  describe('Token expiry', () => {
    it('should create token with 8 hour expiry', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com',
          full_name: 'Test User',
          role: 'END_USER'
        }
      });

      const response = await request(app)
        .post('/auth/login')
        .send({ username: 'testuser' })
        .expect(200);

      const decoded = jwt.verify(response.body.token, process.env.JWT_SECRET);
      const expiryTime = decoded.exp - decoded.iat;

      // Should be 8 hours (28800 seconds)
      expect(expiryTime).toBe(28800);
    });
  });
});
