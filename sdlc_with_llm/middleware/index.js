/**
 * IT Support Portal - Middleware Layer
 *
 * Express.js middleware that sits between React frontend and FastAPI backend.
 * Provides authentication, authorization, validation, rate limiting, and request proxying.
 *
 * Architecture:
 * Frontend (3000) -> Middleware (3001) -> Backend (8000)
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

// Import middleware modules
const { login, verifyToken } = require('./auth/jwt');
const { requireRole } = require('./auth/rbac');
const { validateTicketCreate, validateTicketUpdate, validateCommentCreate } = require('./validators/ticket');
const { loginRateLimiter, ticketCreationRateLimiter, generalRateLimiter, commentCreationRateLimiter } = require('./rateLimit');
const { createBackendProxy } = require('./proxy');
const logger = require('./logger');
const { requestLogger, logStartup } = require('./logger');

// Initialize Express app
const app = express();

// Trust proxy for correct IP addresses (needed for rate limiting)
app.set('trust proxy', 1);

// Security middleware
app.use(helmet());

// CORS configuration
const corsOptions = {
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true,
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));

// Request parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// HTTP request logging (Morgan)
if (process.env.NODE_ENV !== 'test') {
  app.use(morgan('combined'));
}

// Custom request logger
app.use(requestLogger);

// General rate limiting for all requests
app.use(generalRateLimiter);

// Health check endpoint (no auth required)
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    service: 'middleware'
  });
});

// Authentication routes
app.post('/auth/login', loginRateLimiter, login);

// Test routes for TDD (only in test environment)
if (process.env.NODE_ENV === 'test') {
  // Protected route test
  app.get('/test/protected', verifyToken, (req, res) => {
    res.json({
      message: 'Access granted',
      user: req.user
    });
  });

  // RBAC test routes
  app.get('/test/end-user-route', verifyToken, requireRole('END_USER'), (req, res) => {
    res.json({ message: 'End user access granted' });
  });

  app.get('/test/agent-route', verifyToken, requireRole('SUPPORT_AGENT'), (req, res) => {
    res.json({ message: 'Agent access granted' });
  });

  app.get('/test/admin-route', verifyToken, requireRole('ADMIN'), (req, res) => {
    res.json({ message: 'Admin access granted' });
  });

  app.get('/test/agent-or-admin-route', verifyToken, requireRole('SUPPORT_AGENT', 'ADMIN'), (req, res) => {
    res.json({ message: 'Agent or admin access granted' });
  });

  // Validation test route
  app.post('/test/validate-ticket', verifyToken, validateTicketCreate, (req, res) => {
    res.json({ message: 'Validation passed', data: req.body });
  });
}

// API routes - all require authentication and are proxied to backend

// Ticket routes
app.post(
  '/api/tickets',
  verifyToken,
  requireRole('END_USER'), // All authenticated users can create tickets
  ticketCreationRateLimiter,
  validateTicketCreate,
  createBackendProxy()
);

app.patch(
  '/api/tickets/:id',
  verifyToken,
  requireRole('SUPPORT_AGENT'), // Only agents and admins can update tickets
  validateTicketUpdate,
  createBackendProxy()
);

app.patch(
  '/api/tickets/:id/assign',
  verifyToken,
  requireRole('SUPPORT_AGENT'), // Only agents and admins can assign tickets
  createBackendProxy()
);

app.post(
  '/api/tickets/:id/comments',
  verifyToken,
  requireRole('END_USER'), // All authenticated users can comment
  commentCreationRateLimiter,
  validateCommentCreate,
  createBackendProxy()
);

// All other /api/* routes - proxy with authentication
app.use(
  '/api',
  verifyToken,
  createBackendProxy()
);

// 404 handler
app.use((req, res) => {
  logger.warn('Route not found', {
    method: req.method,
    path: req.path,
    ip: req.ip
  });

  res.status(404).json({
    error: 'Not Found',
    message: `Cannot ${req.method} ${req.path}`
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  logger.error('Unhandled error', {
    error: err.message,
    stack: err.stack,
    method: req.method,
    path: req.path,
    user_id: req.user ? req.user.userId : null
  });

  // Don't leak error details in production
  const errorResponse = {
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'An unexpected error occurred'
  };

  if (process.env.NODE_ENV === 'development') {
    errorResponse.stack = err.stack;
  }

  res.status(err.status || 500).json(errorResponse);
});

// Start server (only if not in test mode)
if (process.env.NODE_ENV !== 'test') {
  const PORT = process.env.PORT || 3001;
  app.listen(PORT, () => {
    logStartup(PORT);
    console.log(`\n========================================`);
    console.log(`IT Support Portal Middleware`);
    console.log(`========================================`);
    console.log(`Server running on: http://localhost:${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`Backend URL: ${process.env.BACKEND_URL || 'http://localhost:8000'}`);
    console.log(`Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
    console.log(`========================================\n`);
  });
}

// Export app for testing
module.exports = app;
