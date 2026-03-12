/**
 * Role-Based Access Control (RBAC) Module
 *
 * Provides role-based authorization middleware for the IT Support Portal.
 * Supports role hierarchy: END_USER < SUPPORT_AGENT < ADMIN
 */

/**
 * Role hierarchy definition
 * Higher index = higher privilege level
 */
const ROLE_HIERARCHY = ['END_USER', 'SUPPORT_AGENT', 'ADMIN'];

/**
 * Get role level in hierarchy
 *
 * @param {string} role - Role name
 * @returns {number} Role level (0-2)
 */
function getRoleLevel(role) {
  return ROLE_HIERARCHY.indexOf(role);
}

/**
 * Check if user role has access to required roles
 *
 * @param {string} userRole - User's role
 * @param {Array<string>} requiredRoles - Required roles
 * @returns {boolean} True if user has access
 */
function hasAccess(userRole, requiredRoles) {
  const userLevel = getRoleLevel(userRole);

  // Check if user's role level is high enough for any of the required roles
  for (const requiredRole of requiredRoles) {
    const requiredLevel = getRoleLevel(requiredRole);
    if (userLevel >= requiredLevel) {
      return true;
    }
  }

  return false;
}

/**
 * Require role middleware factory
 * Creates middleware that restricts access based on user roles
 *
 * @param {...string} roles - Allowed roles (e.g., 'ADMIN', 'SUPPORT_AGENT')
 * @returns {Function} Express middleware function
 *
 * @example
 * // Only admins can access
 * router.get('/admin-only', requireRole('ADMIN'), handler);
 *
 * @example
 * // Agents or admins can access
 * router.get('/agent-area', requireRole('SUPPORT_AGENT', 'ADMIN'), handler);
 *
 * @example
 * // Due to hierarchy, ADMIN can access SUPPORT_AGENT routes automatically
 * router.get('/agent-route', requireRole('SUPPORT_AGENT'), handler);
 */
function requireRole(...roles) {
  // Validate that roles were provided
  if (roles.length === 0) {
    throw new Error('At least one role must be specified for requireRole middleware');
  }

  // Validate all roles are valid
  for (const role of roles) {
    if (!ROLE_HIERARCHY.includes(role)) {
      throw new Error(`Invalid role: ${role}. Valid roles are: ${ROLE_HIERARCHY.join(', ')}`);
    }
  }

  // Return middleware function
  return function (req, res, next) {
    // Ensure user is authenticated (should be set by verifyToken middleware)
    if (!req.user || !req.user.role) {
      return res.status(401).json({
        error: 'Authentication required'
      });
    }

    const userRole = req.user.role;

    // Check if user has access
    if (!hasAccess(userRole, roles)) {
      return res.status(403).json({
        error: `Forbidden: Requires one of the following roles: ${roles.join(', ')}. Your role: ${userRole}`
      });
    }

    // User has access, proceed
    next();
  };
}

module.exports = {
  requireRole,
  ROLE_HIERARCHY,
  hasAccess
};
