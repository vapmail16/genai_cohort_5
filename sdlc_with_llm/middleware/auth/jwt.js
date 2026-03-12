/**
 * JWT Authentication Module
 *
 * Provides JWT-based authentication for the IT Support Portal middleware.
 * Handles user login and token verification.
 */

const jwt = require('jsonwebtoken');
const axios = require('axios');

/**
 * Login endpoint handler
 * Calls backend /api/users/authenticate and returns signed JWT
 *
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function login(req, res) {
  try {
    const { username } = req.body;

    // Validate username presence
    if (!username) {
      return res.status(400).json({
        error: 'Username is required'
      });
    }

    // Call backend authentication endpoint
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await axios.get(
      `${backendUrl}/api/users/authenticate`,
      {
        params: { username }
      }
    );

    const user = response.data;

    // Generate JWT token
    const token = jwt.sign(
      {
        userId: user.id,
        username: user.username,
        role: user.role
      },
      process.env.JWT_SECRET,
      {
        expiresIn: process.env.JWT_EXPIRES_IN || '8h'
      }
    );

    // Return token and user info
    return res.status(200).json({
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        role: user.role
      }
    });
  } catch (error) {
    // Handle backend errors
    if (error.response) {
      // Backend returned an error response
      if (error.response.status === 404) {
        return res.status(404).json({
          error: error.response.data.detail || 'User not found'
        });
      }
      return res.status(error.response.status).json({
        error: error.response.data.detail || 'Authentication failed'
      });
    }

    // Network or other errors
    console.error('Login error:', error.message);
    return res.status(500).json({
      error: 'Internal server error during authentication'
    });
  }
}

/**
 * Verify JWT token middleware
 * Validates the token and attaches user info to request object
 *
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
function verifyToken(req, res, next) {
  try {
    // Get token from Authorization header
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        error: 'No token provided. Authorization header must be in format: Bearer <token>'
      });
    }

    // Extract token
    const token = authHeader.substring(7); // Remove 'Bearer ' prefix

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Attach user info to request
    req.user = {
      userId: decoded.userId,
      username: decoded.username,
      role: decoded.role
    };

    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        error: 'Invalid token'
      });
    }

    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        error: 'Token expired'
      });
    }

    console.error('Token verification error:', error.message);
    return res.status(401).json({
      error: 'Token verification failed'
    });
  }
}

module.exports = {
  login,
  verifyToken
};
