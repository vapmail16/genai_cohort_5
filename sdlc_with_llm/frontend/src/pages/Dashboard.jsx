import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import {
  AlertCircle,
  Inbox,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';

function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [recentTickets, setRecentTickets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    // Check if user has appropriate role
    if (user.role !== 'SUPPORT_AGENT' && user.role !== 'ADMIN') {
      navigate('/tickets');
      return;
    }
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch analytics summary
      const analyticsResponse = await apiClient.get('/api/analytics/summary');
      setAnalytics(analyticsResponse.data);

      // Fetch recent tickets (last 10)
      const ticketsResponse = await apiClient.get('/api/tickets?page=1&page_size=10');
      setRecentTickets(ticketsResponse.data.tickets);
    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusBadgeClass = (status) => {
    const baseClasses = 'px-2 py-1 rounded-full text-xs font-semibold';
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

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading dashboard...</div>
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

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Open Tickets */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="bg-red-100 p-3 rounded-lg">
                <Inbox className="w-6 h-6 text-red-600" />
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-gray-900">
                {analytics?.open_count || 0}
              </div>
              <div className="text-sm text-gray-500">Open Tickets</div>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Tickets awaiting assignment
          </div>
        </div>

        {/* In Progress */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="bg-amber-100 p-3 rounded-lg">
                <Clock className="w-6 h-6 text-amber-600" />
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-gray-900">
                {analytics?.in_progress_count || 0}
              </div>
              <div className="text-sm text-gray-500">In Progress</div>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Currently being worked on
          </div>
        </div>

        {/* Resolved Today */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-gray-900">
                {analytics?.resolved_today_count || 0}
              </div>
              <div className="text-sm text-gray-500">Resolved Today</div>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Tickets resolved in the last 24h
          </div>
        </div>

        {/* SLA Breaches */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="bg-red-100 p-3 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-red-600" />
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-gray-900">
                {analytics?.sla_breach_count || 0}
              </div>
              <div className="text-sm text-gray-500">SLA Breaches</div>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Tickets exceeding SLA
          </div>
        </div>
      </div>

      {/* Recent Tickets Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Tickets</h2>
        </div>

        {recentTickets.length === 0 ? (
          <div className="p-8 text-center text-gray-600">
            No tickets found.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Submitter
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Priority
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recentTickets.map((ticket) => (
                  <tr
                    key={ticket.id}
                    onClick={() => navigate(`/tickets/${ticket.id}`)}
                    className="hover:bg-gray-50 cursor-pointer transition-colors"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      #{ticket.id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      <div className="max-w-xs truncate">{ticket.title}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {ticket.submitter.full_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={getStatusBadgeClass(ticket.status)}>
                        {ticket.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {ticket.priority}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {formatDate(ticket.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
