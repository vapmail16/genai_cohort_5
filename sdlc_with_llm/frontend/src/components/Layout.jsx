import { useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, Ticket, PlusCircle, LogOut, User } from 'lucide-react';

function Layout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const user = JSON.parse(localStorage.getItem('user'));

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const canAccessDashboard = () => {
    return user && (user.role === 'SUPPORT_AGENT' || user.role === 'ADMIN');
  };

  const navigationItems = [
    {
      name: 'My Tickets',
      path: '/tickets',
      icon: Ticket,
      show: true,
    },
    {
      name: 'Submit Ticket',
      path: '/tickets/new',
      icon: PlusCircle,
      show: true,
    },
    {
      name: 'Dashboard',
      path: '/dashboard',
      icon: LayoutDashboard,
      show: canAccessDashboard(),
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-64 bg-gray-900 text-white">
        {/* Logo/Header */}
        <div className="flex items-center justify-center h-16 border-b border-gray-800">
          <h1 className="text-xl font-bold">IT Support Portal</h1>
        </div>

        {/* Navigation */}
        <nav className="mt-6">
          {navigationItems.map(
            (item) =>
              item.show && (
                <button
                  key={item.path}
                  onClick={() => navigate(item.path)}
                  className={`w-full flex items-center px-6 py-3 text-left transition-colors ${
                    isActive(item.path)
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  }`}
                >
                  <item.icon className="w-5 h-5 mr-3" />
                  {item.name}
                </button>
              )
          )}
        </nav>

        {/* User Info & Logout */}
        <div className="absolute bottom-0 left-0 right-0 border-t border-gray-800">
          <div className="px-6 py-4">
            <div className="flex items-center mb-3">
              <div className="bg-gray-700 rounded-full p-2 mr-3">
                <User className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-white truncate">
                  {user?.full_name || 'User'}
                </div>
                <div className="text-xs text-gray-400 truncate">
                  {user?.role?.replace('_', ' ') || 'Role'}
                </div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="ml-64">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <div className="px-8 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-gray-800">
                  Welcome, {user?.full_name || 'User'}
                </h2>
                <p className="text-sm text-gray-600">{user?.email || ''}</p>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="p-8">
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
