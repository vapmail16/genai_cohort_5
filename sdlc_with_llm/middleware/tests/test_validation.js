/**
 * Validation Middleware Tests
 *
 * TDD RED Phase: Tests written first
 */

const request = require('supertest');
const jwt = require('jsonwebtoken');

describe('Ticket Validation Middleware', () => {
  let app;
  let validToken;

  beforeEach(() => {
    jest.clearAllMocks();
    process.env.JWT_SECRET = 'test-secret-key';
    process.env.JWT_EXPIRES_IN = '8h';
    process.env.BACKEND_URL = 'http://localhost:8000';

    delete require.cache[require.resolve('../index.js')];
    app = require('../index.js');

    // Generate valid token for tests
    validToken = jwt.sign(
      { userId: 1, username: 'testuser', role: 'END_USER' },
      process.env.JWT_SECRET,
      { expiresIn: '8h' }
    );
  });

  describe('validateTicketCreate middleware', () => {
    const validTicket = {
      title: 'Valid ticket title',
      description: 'This is a valid description with enough characters to pass validation',
      category_id: '123e4567-e89b-12d3-a456-426614174000',
      priority: 'MEDIUM'
    };

    it('should accept valid ticket data', async () => {
      const response = await request(app)
        .post('/test/validate-ticket')
        .set('Authorization', `Bearer ${validToken}`)
        .send(validTicket)
        .expect(200);

      expect(response.body.message).toBe('Validation passed');
    });

    describe('Title validation', () => {
      it('should reject title less than 5 characters', async () => {
        const invalidTicket = { ...validTicket, title: 'Test' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('title');
      });

      it('should reject title more than 200 characters', async () => {
        const invalidTicket = {
          ...validTicket,
          title: 'a'.repeat(201)
        };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('title');
      });

      it('should accept title with exactly 5 characters', async () => {
        const ticket = { ...validTicket, title: 'Valid' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should accept title with exactly 200 characters', async () => {
        const ticket = { ...validTicket, title: 'a'.repeat(200) };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should reject missing title', async () => {
        const invalidTicket = { ...validTicket };
        delete invalidTicket.title;

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('title');
      });
    });

    describe('Description validation', () => {
      it('should reject description less than 10 characters', async () => {
        const invalidTicket = { ...validTicket, description: 'Too short' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('description');
      });

      it('should reject description more than 2000 characters', async () => {
        const invalidTicket = {
          ...validTicket,
          description: 'a'.repeat(2001)
        };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('description');
      });

      it('should accept description with exactly 10 characters', async () => {
        const ticket = { ...validTicket, description: '1234567890' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should accept description with exactly 2000 characters', async () => {
        const ticket = { ...validTicket, description: 'a'.repeat(2000) };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should reject missing description', async () => {
        const invalidTicket = { ...validTicket };
        delete invalidTicket.description;

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('description');
      });
    });

    describe('Category ID validation', () => {
      it('should reject invalid UUID format', async () => {
        const invalidTicket = { ...validTicket, category_id: 'not-a-uuid' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('category_id');
      });

      it('should accept valid UUID v4', async () => {
        const ticket = {
          ...validTicket,
          category_id: '550e8400-e29b-41d4-a716-446655440000'
        };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should reject missing category_id', async () => {
        const invalidTicket = { ...validTicket };
        delete invalidTicket.category_id;

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('category_id');
      });
    });

    describe('Priority validation', () => {
      it('should accept LOW priority', async () => {
        const ticket = { ...validTicket, priority: 'LOW' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should accept MEDIUM priority', async () => {
        const ticket = { ...validTicket, priority: 'MEDIUM' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should accept HIGH priority', async () => {
        const ticket = { ...validTicket, priority: 'HIGH' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should accept URGENT priority', async () => {
        const ticket = { ...validTicket, priority: 'URGENT' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(ticket)
          .expect(200);

        expect(response.body.message).toBe('Validation passed');
      });

      it('should reject invalid priority', async () => {
        const invalidTicket = { ...validTicket, priority: 'INVALID' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('priority');
      });

      it('should reject lowercase priority', async () => {
        const invalidTicket = { ...validTicket, priority: 'low' };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
      });

      it('should reject missing priority', async () => {
        const invalidTicket = { ...validTicket };
        delete invalidTicket.priority;

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        expect(response.body.error).toContain('priority');
      });
    });

    describe('Multiple validation errors', () => {
      it('should return all validation errors', async () => {
        const invalidTicket = {
          title: 'Bad',
          description: 'Short',
          category_id: 'invalid',
          priority: 'WRONG'
        };

        const response = await request(app)
          .post('/test/validate-ticket')
          .set('Authorization', `Bearer ${validToken}`)
          .send(invalidTicket)
          .expect(400);

        expect(response.body).toHaveProperty('error');
        // Should contain information about validation errors
        expect(response.body.error).toBeTruthy();
      });
    });
  });
});
