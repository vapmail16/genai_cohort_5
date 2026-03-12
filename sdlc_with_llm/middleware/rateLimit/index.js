/**
 * Rate Limiting Module
 *
 * Provides rate limiting middleware for the IT Support Portal.
 * Prevents abuse by limiting request frequency per user/IP.
 */

const rateLimit = require('express-rate-limit');

/**
 * Rate limiter for login attempts
 * Limit: 5 requests per IP per 15 minutes
 *
 * Protects against brute force attacks on authentication endpoint
 */
const loginRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Max 5 requests per window
  message: {
    error: 'Too many login attempts from this IP, please try again after 15 minutes'
  },
  standardHeaders: true, // Return rate limit info in RateLimit-* headers
  legacyHeaders: false, // Disable X-RateLimit-* headers
  skipSuccessfulRequests: false, // Count all requests, not just failed ones
  keyGenerator: (req) => {
    // Use IP address as key
    return req.ip || req.connection.remoteAddress;
  }
});

/**
 * Rate limiter for ticket creation
 * Limit: 10 requests per user per hour
 *
 * Prevents spam ticket creation while allowing legitimate use
 */
const ticketCreationRateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 10, // Max 10 tickets per hour per user
  message: {
    error: 'Too many tickets created. Limit: 10 tickets per hour. Please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: false,
  keyGenerator: (req) => {
    // Use authenticated user ID if available, otherwise fall back to IP
    if (req.user && req.user.userId) {
      return `user_${req.user.userId}`;
    }
    return req.ip || req.connection.remoteAddress;
  }
});

/**
 * General API rate limiter
 * Limit: 100 requests per IP per 15 minutes
 *
 * General protection against API abuse
 */
const generalRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requests per window
  message: {
    error: 'Too many requests from this IP, please try again after 15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: false,
  keyGenerator: (req) => {
    return req.ip || req.connection.remoteAddress;
  }
});

/**
 * Comment creation rate limiter
 * Limit: 20 comments per user per hour
 *
 * Prevents comment spam
 */
const commentCreationRateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 20, // Max 20 comments per hour per user
  message: {
    error: 'Too many comments created. Limit: 20 comments per hour. Please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: false,
  keyGenerator: (req) => {
    if (req.user && req.user.userId) {
      return `user_comment_${req.user.userId}`;
    }
    return req.ip || req.connection.remoteAddress;
  }
});

module.exports = {
  loginRateLimiter,
  ticketCreationRateLimiter,
  generalRateLimiter,
  commentCreationRateLimiter
};
