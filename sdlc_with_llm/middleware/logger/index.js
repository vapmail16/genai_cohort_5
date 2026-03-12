/**
 * Logger Module
 *
 * Provides Winston-based logging for the IT Support Portal middleware.
 * Logs to console and file with structured format.
 */

const winston = require('winston');
const path = require('path');
const fs = require('fs');

// Create logs directory if it doesn't exist
const logsDir = path.join(__dirname, '..', 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

/**
 * Custom format for log messages
 * Format: timestamp | level | message | metadata
 */
const customFormat = winston.format.combine(
  winston.format.timestamp({
    format: 'YYYY-MM-DD HH:mm:ss'
  }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json(),
  winston.format.printf(({ timestamp, level, message, ...metadata }) => {
    let msg = `${timestamp} | ${level.toUpperCase().padEnd(5)} | ${message}`;

    // Add metadata if present
    if (Object.keys(metadata).length > 0) {
      // Remove empty or undefined values
      const cleanMetadata = Object.entries(metadata)
        .filter(([_, v]) => v !== undefined && v !== null && v !== '')
        .reduce((acc, [k, v]) => ({ ...acc, [k]: v }), {});

      if (Object.keys(cleanMetadata).length > 0) {
        msg += ` | ${JSON.stringify(cleanMetadata)}`;
      }
    }

    return msg;
  })
);

/**
 * Winston logger instance
 */
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: customFormat,
  transports: [
    // Console transport for development
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        customFormat
      )
    }),

    // File transport for all logs
    new winston.transports.File({
      filename: path.join(logsDir, 'app.log'),
      maxsize: 5242880, // 5MB
      maxFiles: 5
    }),

    // Separate file for errors
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      maxsize: 5242880,
      maxFiles: 5
    })
  ]
});

/**
 * Express middleware for request logging
 * Logs: timestamp | method | path | user_id | status | response_time
 *
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
function requestLogger(req, res, next) {
  const startTime = Date.now();

  // Capture original end function
  const originalEnd = res.end;

  // Override end function to log after response
  res.end = function (...args) {
    // Calculate response time
    const responseTime = Date.now() - startTime;

    // Log request details
    logger.info('Request completed', {
      method: req.method,
      path: req.path,
      user_id: req.user ? req.user.userId : null,
      username: req.user ? req.user.username : null,
      role: req.user ? req.user.role : null,
      status: res.statusCode,
      response_time: `${responseTime}ms`,
      ip: req.ip || req.connection.remoteAddress,
      user_agent: req.get('user-agent')
    });

    // Call original end function
    originalEnd.apply(res, args);
  };

  next();
}

/**
 * Log startup message
 */
function logStartup(port) {
  logger.info('IT Support Portal Middleware started', {
    port,
    environment: process.env.NODE_ENV || 'development',
    backend_url: process.env.BACKEND_URL || 'http://localhost:8000',
    log_level: process.env.LOG_LEVEL || 'info'
  });
}

/**
 * Log error with stack trace
 *
 * @param {Error} error - Error object
 * @param {Object} context - Additional context
 */
function logError(error, context = {}) {
  logger.error(error.message, {
    ...context,
    stack: error.stack,
    error_name: error.name
  });
}

module.exports = logger;
module.exports.requestLogger = requestLogger;
module.exports.logStartup = logStartup;
module.exports.logError = logError;
