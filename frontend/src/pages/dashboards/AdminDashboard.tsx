import { DashboardLayout } from '@/components/layouts/DashboardLayout'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { useAuth } from '@/features/auth/useAuth'

export const AdminDashboard = () => {
  const { user } = useAuth()

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Admin Dashboard
          </h1>
          <p className="text-gray-600">
            Welcome back, {user?.firstName || 'Administrator'}. Here's your system overview.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Students</p>
                <p className="text-2xl font-bold text-gray-900">1,234</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center text-2xl">
                👥
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <Badge variant="success">+12%</Badge>
              <span className="text-xs text-gray-500">from last month</span>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Active Courses</p>
                <p className="text-2xl font-bold text-gray-900">45</p>
              </div>
              <div className="w-12 h-12 bg-emerald-100 rounded-2xl flex items-center justify-center text-2xl">
                📚
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <Badge variant="primary">5 New</Badge>
              <span className="text-xs text-gray-500">this semester</span>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Faculty Members</p>
                <p className="text-2xl font-bold text-gray-900">78</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-2xl flex items-center justify-center text-2xl">
                👨‍🏫
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <Badge variant="warning">3 Pending</Badge>
              <span className="text-xs text-gray-500">approvals</span>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">System Health</p>
                <p className="text-2xl font-bold text-gray-900">98%</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center text-2xl">
                ✅
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <Badge variant="success">Operational</Badge>
              <span className="text-xs text-gray-500">all services</span>
            </div>
          </Card>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Recent Enrollments
            </h2>
            <div className="space-y-3">
              {[
                { name: 'John Doe', course: 'Computer Science 101', time: '2 hours ago' },
                { name: 'Jane Smith', course: 'Mathematics 201', time: '4 hours ago' },
                { name: 'Mike Johnson', course: 'Physics 301', time: '6 hours ago' },
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{item.name}</p>
                    <p className="text-xs text-gray-500">{item.course}</p>
                  </div>
                  <span className="text-xs text-gray-400">{item.time}</span>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Pending Actions
            </h2>
            <div className="space-y-3">
              {[
                { action: 'Review Faculty Applications', count: 3, priority: 'high' },
                { action: 'Approve Course Updates', count: 5, priority: 'medium' },
                { action: 'Process Student Appeals', count: 2, priority: 'low' },
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${
                      item.priority === 'high' ? 'bg-red-500' :
                      item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                    }`} />
                    <p className="text-sm font-medium text-gray-900">{item.action}</p>
                  </div>
                  <Badge variant="primary">{item.count}</Badge>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Add Student', icon: '➕' },
              { label: 'Create Course', icon: '📝' },
              { label: 'Manage Users', icon: '👤' },
              { label: 'View Reports', icon: '📊' },
            ].map((action, index) => (
              <button
                key={index}
                className="p-4 border border-gray-200 rounded-2xl hover:border-[#3B82F6] hover:bg-blue-50 transition-all duration-150 text-center"
              >
                <div className="text-3xl mb-2">{action.icon}</div>
                <p className="text-sm font-medium text-gray-900">{action.label}</p>
              </button>
            ))}
          </div>
        </Card>
      </div>
    </DashboardLayout>
  )
}
