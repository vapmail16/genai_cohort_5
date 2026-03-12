/**
 * Proxy Module
 *
 * Forwards API requests to the FastAPI backend with JWT user context.
 * Injects X-User-Id and X-User-Role headers from authenticated JWT tokens.
 */

const { createProxyMiddleware } = require('http-proxy-middleware');
const logger = require('../logger');

/**
 * Create proxy middleware for backend API
 * Forwards all /api/* requests to the FastAPI backend
 *
 * @returns {Function} Express middleware function
 */
function createBackendProxy() {
  const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';

  return createProxyMiddleware({
    target: backendUrl,
    changeOrigin: true,
    // Don't rewrite the path - keep /api prefix
    pathRewrite: {},

    // Add user context headers from JWT
    onProxyReq: (proxyReq, req, res) => {
      // Inject user information from JWT token
      if (req.user) {
        proxyReq.setHeader('X-User-Id', req.user.userId.toString());
        proxyReq.setHeader('X-User-Role', req.user.role);
        proxyReq.setHeader('X-Username', req.user.username);
      }

      // Log proxied request
      logger.info('Proxying request', {
        method: req.method,
        path: req.path,
        userId: req.user ? req.user.userId : null,
        role: req.user ? req.user.role : null,
        target: backendUrl + req.path
      });
    },

    // Log proxy response
    onProxyRes: (proxyRes, req, res) => {
      logger.info('Proxy response', {
        method: req.method,
        path: req.path,
        statusCode: proxyRes.statusCode,
        userId: req.user ? req.user.userId : null
      });
    },

    // Handle proxy errors
    onError: (err, req, res) => {
      logger.error('Proxy error', {
        error: err.message,
        method: req.method,
        path: req.path,
        userId: req.user ? req.user.userId : null
      });

      res.status(502).json({
        error: 'Bad Gateway: Unable to reach backend service',
        details: process.env.NODE_ENV === 'development' ? err.message : undefined
      });
    },

    // Logging configuration
    logLevel: process.env.NODE_ENV === 'development' ? 'debug' : 'error'
  });
}

/**
 * Middleware to ensure user is authenticated before proxying
 * This should be used in combination with verifyToken middleware
 *
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
function requireAuthForProxy(req, res, next) {
  if (!req.user) {
    logger.warn('Unauthenticated proxy request blocked', {
      method: req.method,
      path: req.path,
      ip: req.ip
    });

    return res.status(401).json({
      error: 'Authentication required to access this resource'
    });
  }

  next();
}

module.exports = {
  createBackendProxy,
  requireAuthForProxy
};
