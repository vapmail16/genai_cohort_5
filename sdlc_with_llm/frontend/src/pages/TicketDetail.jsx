import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { AlertCircle, ArrowLeft, User, Calendar, Tag, AlertTriangle } from 'lucide-react';

function TicketDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTicket();
  }, [id]);

  const fetchTicket = async () => {
    try {
      const response = await apiClient.get(`/api/tickets/${id}`);
      setTicket(response.data);
    } catch (err) {
      setError('Failed to load ticket details. Please try again.');
      console.error('Error fetching ticket:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusBadgeClass = (status) => {
    const baseClasses = 'px-3 py-1 rounded-full text-sm font-semibold';
    switch (status) {
      case 'OPEN':
        return `${baseClasses} bg-red-100 text-red-800`;
      case 'IN_PROGRESS':
        return `${baseClasses} bg-amber-100 text-amber-800`;
      case 'RESOLVED':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'CLOSED':
        return `${baseClasses} bg-gray-100 text-gray-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  const getPriorityBadgeClass = (priority) => {
    const baseClasses = 'px-3 py-1 rounded text-sm font-semibold';
    switch (priority) {
      case 'CRITICAL':
        return `${baseClasses} bg-red-600 text-white`;
      case 'HIGH':
        return `${baseClasses} bg-orange-500 text-white`;
      case 'MEDIUM':
        return `${baseClasses} bg-blue-500 text-white`;
      case 'LOW':
        return `${baseClasses} bg-gray-400 text-white`;
      default:
        return `${baseClasses} bg-gray-400 text-white`;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading ticket details...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded flex items-center">
        <AlertCircle className="w-5 h-5 mr-2" />
        {error}
      </div>
    );
  }

  if (!ticket) {
    return (
      <div className="bg-yellow-50 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
        Ticket not found.
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={() => navigate('/tickets')}
        className="flex items-center text-blue-600 hover:text-blue-800 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to My Tickets
      </button>

      <div className="bg-white rounded-lg shadow-md">
        {/* Header */}
        <div className="border-b border-gray-200 px-6 py-4">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center mb-2">
                <h1 className="text-2xl font-bold text-gray-900 mr-4">
                  Ticket #{ticket.id}
                </h1>
                <span className={getStatusBadgeClass(ticket.status)}>
                  {ticket.status.replace('_', ' ')}
                </span>
                {ticket.sla_breach === 1 && (
                  <span className="ml-2 px-3 py-1 rounded-full text-sm font-semibold bg-red-600 text-white flex items-center">
                    <AlertTriangle className="w-4 h-4 mr-1" />
                    SLA BREACHED
                  </span>
                )}
              </div>
              <h2 className="text-xl text-gray-800">{ticket.title}</h2>
            </div>
            <span className={getPriorityBadgeClass(ticket.priority)}>
              {ticket.priority}
            </span>
          </div>
        </div>

        {/* Ticket Details */}
        <div className="px-6 py-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="flex items-start">
              <Tag className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
              <div>
                <div className="text-sm font-medium text-gray-500">Category</div>
                <div className="text-gray-900">{ticket.category.name}</div>
                <div className="text-sm text-gray-500">SLA: {ticket.category.sla_hours} hours</div>
              </div>
            </div>

            <div className="flex items-start">
              <User className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
              <div>
                <div className="text-sm font-medium text-gray-500">Submitted By</div>
                <div className="text-gray-900">{ticket.submitter.full_name}</div>
                <div className="text-sm text-gray-500">{ticket.submitter.email}</div>
              </div>
            </div>

            <div className="flex items-start">
              <User className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
              <div>
                <div className="text-sm font-medium text-gray-500">Assigned To</div>
                <div className="text-gray-900">
                  {ticket.agent ? ticket.agent.full_name : 'Unassigned'}
                </div>
                {ticket.agent && (
                  <div className="text-sm text-gray-500">{ticket.agent.email}</div>
                )}
              </div>
            </div>

            <div className="flex items-start">
              <Calendar className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
              <div>
                <div className="text-sm font-medium text-gray-500">Created</div>
                <div className="text-gray-900">{formatDate(ticket.created_at)}</div>
              </div>
            </div>

            <div className="flex items-start">
              <Calendar className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
              <div>
                <div className="text-sm font-medium text-gray-500">Last Updated</div>
                <div className="text-gray-900">{formatDate(ticket.updated_at)}</div>
              </div>
            </div>

            {ticket.resolved_at && (
              <div className="flex items-start">
                <Calendar className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-gray-500">Resolved</div>
                  <div className="text-gray-900">{formatDate(ticket.resolved_at)}</div>
                </div>
              </div>
            )}
          </div>

          {/* Description */}
          <div className="border-t border-gray-200 pt-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Description</h3>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-800 whitespace-pre-wrap">{ticket.description}</p>
            </div>
          </div>

          {/* Resolution Note */}
          {ticket.resolution_note && (
            <div className="border-t border-gray-200 pt-6 mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Resolution</h3>
              <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                <p className="text-gray-800 whitespace-pre-wrap">{ticket.resolution_note}</p>
              </div>
            </div>
          )}

          {/* Comments Section */}
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Comments</h3>

            {/* TODO: Add comment form - Reserved for live demo */}
            {/*
              The comment form UI has been intentionally excluded and will be
              implemented during the live demonstration to showcase TDD methodology.

              Expected functionality:
              - Text area for comment input
              - Submit button
              - Display existing comments with user info and timestamps
              - POST to /api/tickets/{id}/comments endpoint
            */}

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
              <p className="text-blue-800">
                Comment functionality will be added during the live demo.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TicketDetail;
