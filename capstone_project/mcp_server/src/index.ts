#!/usr/bin/env node

/**
 * MCP Server for IT Support Tools
 *
 * Provides tools for:
 * - VPN status checking
 * - Password reset
 * - Service health monitoring
 * - Network diagnostics
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

// Tool definitions
const TOOLS: Tool[] = [
  {
    name: 'check_vpn_status',
    description: 'Check the status of VPN connection for a user. Returns connection status, latency, and last connected time.',
    inputSchema: {
      type: 'object',
      properties: {
        user_email: {
          type: 'string',
          description: 'Email address of the user to check VPN status for',
        },
      },
      required: ['user_email'],
    },
  },
  {
    name: 'reset_password',
    description: 'Initiate a password reset for a user account. Sends reset email and returns confirmation.',
    inputSchema: {
      type: 'object',
      properties: {
        user_email: {
          type: 'string',
          description: 'Email address of the user requesting password reset',
        },
        send_email: {
          type: 'boolean',
          description: 'Whether to send reset email immediately (default: true)',
          default: true,
        },
      },
      required: ['user_email'],
    },
  },
  {
    name: 'check_service_health',
    description: 'Check the health status of IT services (email, VPN, file server, etc.)',
    inputSchema: {
      type: 'object',
      properties: {
        service_name: {
          type: 'string',
          description: 'Name of the service to check',
          enum: ['email', 'vpn', 'file_server', 'wifi', 'printer', 'all'],
        },
      },
      required: ['service_name'],
    },
  },
  {
    name: 'run_network_diagnostic',
    description: 'Run network diagnostic tests for a user (ping, traceroute, DNS lookup)',
    inputSchema: {
      type: 'object',
      properties: {
        user_email: {
          type: 'string',
          description: 'Email of user experiencing network issues',
        },
        test_type: {
          type: 'string',
          description: 'Type of network test to run',
          enum: ['ping', 'traceroute', 'dns', 'full'],
          default: 'ping',
        },
      },
      required: ['user_email'],
    },
  },
  {
    name: 'check_printer_queue',
    description: 'Check printer queue status and clear stuck jobs if needed',
    inputSchema: {
      type: 'object',
      properties: {
        printer_name: {
          type: 'string',
          description: 'Name of the printer to check',
        },
        clear_queue: {
          type: 'boolean',
          description: 'Whether to clear stuck jobs (default: false)',
          default: false,
        },
      },
      required: ['printer_name'],
    },
  },
];

// Simulated tool implementations
// In production, these would call real APIs

async function checkVPNStatus(userEmail: string): Promise<any> {
  // Simulate VPN status check
  const isConnected = Math.random() > 0.3; // 70% chance connected
  const latency = isConnected ? Math.floor(Math.random() * 100) + 10 : null;

  return {
    status: isConnected ? 'connected' : 'disconnected',
    user_email: userEmail,
    latency_ms: latency,
    last_connected: isConnected
      ? new Date().toISOString()
      : new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
    server: isConnected ? 'vpn-us-east-1' : null,
    ip_address: isConnected ? '10.0.1.42' : null,
  };
}

async function resetPassword(userEmail: string, sendEmail: boolean = true): Promise<any> {
  // Simulate password reset
  const resetToken = Math.random().toString(36).substring(2, 15);

  return {
    success: true,
    user_email: userEmail,
    reset_token: resetToken,
    email_sent: sendEmail,
    reset_link: `https://portal.acme.com/reset?token=${resetToken}`,
    expires_in: '24 hours',
    message: sendEmail
      ? `Password reset email sent to ${userEmail}`
      : `Reset link generated for ${userEmail}`,
  };
}

async function checkServiceHealth(serviceName: string): Promise<any> {
  // Simulate service health check
  const services = {
    email: { status: 'operational', uptime: '99.9%', response_time_ms: 45 },
    vpn: { status: 'operational', uptime: '99.5%', response_time_ms: 120 },
    file_server: { status: 'degraded', uptime: '98.2%', response_time_ms: 350 },
    wifi: { status: 'operational', uptime: '99.8%', response_time_ms: 20 },
    printer: { status: 'operational', uptime: '97.5%', response_time_ms: 80 },
  };

  if (serviceName === 'all') {
    return {
      timestamp: new Date().toISOString(),
      services: services,
      overall_status: 'mostly_operational',
    };
  }

  const service = services[serviceName as keyof typeof services];
  if (!service) {
    throw new Error(`Unknown service: ${serviceName}`);
  }

  return {
    service_name: serviceName,
    timestamp: new Date().toISOString(),
    ...service,
  };
}

async function runNetworkDiagnostic(userEmail: string, testType: string = 'ping'): Promise<any> {
  // Simulate network diagnostic
  const tests: any = {
    ping: {
      target: 'gateway.acme.com',
      packets_sent: 4,
      packets_received: 4,
      packet_loss: '0%',
      avg_latency_ms: 15,
      status: 'success',
    },
  };

  if (testType === 'traceroute' || testType === 'full') {
    tests.traceroute = {
      target: 'gateway.acme.com',
      hops: 8,
      total_time_ms: 45,
      status: 'success',
    };
  }

  if (testType === 'dns' || testType === 'full') {
    tests.dns = {
      query: 'portal.acme.com',
      resolved_ip: '192.168.1.100',
      response_time_ms: 12,
      status: 'success',
    };
  }

  return {
    user_email: userEmail,
    test_type: testType,
    timestamp: new Date().toISOString(),
    tests: tests,
    overall_status: 'healthy',
    recommendation: 'Network connectivity is normal',
  };
}

async function checkPrinterQueue(printerName: string, clearQueue: boolean = false): Promise<any> {
  // Simulate printer queue check
  const queueLength = Math.floor(Math.random() * 5);
  const hasStuckJobs = queueLength > 3;

  return {
    printer_name: printerName,
    status: queueLength === 0 ? 'idle' : hasStuckJobs ? 'warning' : 'printing',
    queue_length: queueLength,
    stuck_jobs: hasStuckJobs ? 2 : 0,
    cleared_jobs: clearQueue && hasStuckJobs ? 2 : 0,
    message: clearQueue && hasStuckJobs
      ? `Cleared 2 stuck jobs from ${printerName}`
      : `${printerName} has ${queueLength} jobs in queue`,
  };
}

// Create MCP server
const server = new Server(
  {
    name: 'it-support-tools',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Handle tool list request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: TOOLS,
  };
});

// Handle tool execution request
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'check_vpn_status': {
        const result = await checkVPNStatus(args.user_email as string);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'reset_password': {
        const result = await resetPassword(
          args.user_email as string,
          args.send_email as boolean ?? true
        );
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'check_service_health': {
        const result = await checkServiceHealth(args.service_name as string);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'run_network_diagnostic': {
        const result = await runNetworkDiagnostic(
          args.user_email as string,
          args.test_type as string ?? 'ping'
        );
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'check_printer_queue': {
        const result = await checkPrinterQueue(
          args.printer_name as string,
          args.clear_queue as boolean ?? false
        );
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error executing tool ${name}: ${error}`,
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('IT Support MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
