import { useAuthStore } from './authStore'
import { login as apiLogin, logout as apiLogout } from '@/api/auth'
import { LoginCredentials } from './types'

/**
 * Custom hook for authentication operations
 */
export function useAuth() {
  const { user, isAuthenticated, isLoading, logout: clearAuth, initialize } = useAuthStore()

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await apiLogin(credentials)
      
      // Initialize auth state after successful login
      initialize()
      
      return response
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    await apiLogout()
    clearAuth()
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    initialize,
  }
}
