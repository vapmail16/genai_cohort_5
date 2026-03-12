/**
 * Ticket Validation Module
 *
 * Provides Joi-based validation schemas and middleware for ticket operations.
 * Validates ticket creation requests before forwarding to backend.
 */

const Joi = require('joi');

/**
 * Ticket creation schema
 * Validates all required fields for creating a new ticket
 */
const ticketCreateSchema = Joi.object({
  title: Joi.string()
    .min(5)
    .max(200)
    .required()
    .messages({
      'string.min': 'Title must be at least 5 characters long',
      'string.max': 'Title must not exceed 200 characters',
      'any.required': 'Title is required'
    }),

  description: Joi.string()
    .min(10)
    .max(2000)
    .required()
    .messages({
      'string.min': 'Description must be at least 10 characters long',
      'string.max': 'Description must not exceed 2000 characters',
      'any.required': 'Description is required'
    }),

  category_id: Joi.string()
    .uuid()
    .required()
    .messages({
      'string.guid': 'Category ID must be a valid UUID',
      'any.required': 'Category ID is required'
    }),

  priority: Joi.string()
    .valid('LOW', 'MEDIUM', 'HIGH', 'URGENT')
    .required()
    .messages({
      'any.only': 'Priority must be one of: LOW, MEDIUM, HIGH, URGENT',
      'any.required': 'Priority is required'
    })
});

/**
 * Validate ticket creation middleware
 * Validates request body against ticketCreateSchema
 *
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
function validateTicketCreate(req, res, next) {
  const { error, value } = ticketCreateSchema.validate(req.body, {
    abortEarly: false, // Return all errors, not just the first one
    stripUnknown: true // Remove unknown properties
  });

  if (error) {
    // Format validation errors
    const errors = error.details.map(detail => detail.message);
    return res.status(400).json({
      error: `Validation failed: ${errors.join('; ')}`
    });
  }

  // Replace request body with validated and sanitized value
  req.body = value;
  next();
}

/**
 * Ticket update schema
 * Validates partial updates to existing tickets
 */
const ticketUpdateSchema = Joi.object({
  title: Joi.string()
    .min(5)
    .max(200)
    .optional()
    .messages({
      'string.min': 'Title must be at least 5 characters long',
      'string.max': 'Title must not exceed 200 characters'
    }),

  description: Joi.string()
    .min(10)
    .max(2000)
    .optional()
    .messages({
      'string.min': 'Description must be at least 10 characters long',
      'string.max': 'Description must not exceed 2000 characters'
    }),

  status: Joi.string()
    .valid('OPEN', 'IN_PROGRESS', 'RESOLVED')
    .optional()
    .messages({
      'any.only': 'Status must be one of: OPEN, IN_PROGRESS, RESOLVED'
    }),

  priority: Joi.string()
    .valid('LOW', 'MEDIUM', 'HIGH', 'URGENT')
    .optional()
    .messages({
      'any.only': 'Priority must be one of: LOW, MEDIUM, HIGH, URGENT'
    }),

  resolution_note: Joi.string()
    .min(10)
    .max(2000)
    .optional()
    .messages({
      'string.min': 'Resolution note must be at least 10 characters long',
      'string.max': 'Resolution note must not exceed 2000 characters'
    })
}).min(1); // At least one field must be provided

/**
 * Validate ticket update middleware
 *
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
function validateTicketUpdate(req, res, next) {
  const { error, value } = ticketUpdateSchema.validate(req.body, {
    abortEarly: false,
    stripUnknown: true
  });

  if (error) {
    const errors = error.details.map(detail => detail.message);
    return res.status(400).json({
      error: `Validation failed: ${errors.join('; ')}`
    });
  }

  req.body = value;
  next();
}

/**
 * Comment creation schema
 * Validates comment creation requests
 */
const commentCreateSchema = Joi.object({
  comment_text: Joi.string()
    .min(1)
    .max(2000)
    .required()
    .messages({
      'string.min': 'Comment cannot be empty',
      'string.max': 'Comment must not exceed 2000 characters',
      'any.required': 'Comment text is required'
    })
});

/**
 * Validate comment creation middleware
 *
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
function validateCommentCreate(req, res, next) {
  const { error, value } = commentCreateSchema.validate(req.body, {
    abortEarly: false,
    stripUnknown: true
  });

  if (error) {
    const errors = error.details.map(detail => detail.message);
    return res.status(400).json({
      error: `Validation failed: ${errors.join('; ')}`
    });
  }

  req.body = value;
  next();
}

module.exports = {
  ticketCreateSchema,
  ticketUpdateSchema,
  commentCreateSchema,
  validateTicketCreate,
  validateTicketUpdate,
  validateCommentCreate
};
