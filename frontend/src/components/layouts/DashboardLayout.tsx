import React from 'react'
import { useAuth } from '@/features/auth/useAuth'
import { Button } from '../ui/Button'

export interface DashboardLayoutProps {
  children: React.ReactNode
}

/**
 * DashboardLayout - Main application layout with sidebar and topbar
 * Features: Responsive design, user profile, navigation placeholder
 */
export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const { user, logout } = useAuth()

  const handleLogout = async () => {
    try {
      await logout()
      // Redirect will be handled by router
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-offwhite">
      {/* Topbar */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-navy">
                SIMS
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              {user && (
                <div className="flex items-center gap-3">
                  <div className="text-right hidden sm:block">
                    <p className="text-sm font-medium text-navy">
                      {user.firstName && user.lastName 
                        ? `${user.firstName} ${user.lastName}` 
                        : user.email}
                    </p>
                    {user.roles.length > 0 && (
                      <p className="text-xs text-gray-500">
                        {user.roles.join(', ')}
                      </p>
                    )}
                  </div>
                  <div className="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-medium">
                    {user.email.charAt(0).toUpperCase()}
                  </div>
                </div>
              )}
              
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                aria-label="Logout"
              >
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex">
        {/* Sidebar - Placeholder for navigation */}
        <aside className="hidden lg:block w-64 bg-white border-r border-gray-200 min-h-[calc(100vh-4rem)] p-4">
          <nav className="space-y-2">
            <div className="px-4 py-2 text-sm font-medium text-gray-900">
              Navigation
            </div>
            <div className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg cursor-pointer transition-colors duration-150">
              Dashboard
            </div>
            <div className="px-4 py-2 text-sm text-gray-400 cursor-not-allowed">
              Students (Coming Soon)
            </div>
            <div className="px-4 py-2 text-sm text-gray-400 cursor-not-allowed">
              Courses (Coming Soon)
            </div>
            <div className="px-4 py-2 text-sm text-gray-400 cursor-not-allowed">
              Enrollment (Coming Soon)
            </div>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
