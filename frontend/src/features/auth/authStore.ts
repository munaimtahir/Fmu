import { create } from 'zustand'
import { User } from './types'
import { getAccessToken, clearTokens } from '@/api/axios'
import { decodeToken } from '@/api/auth'

interface AuthStore {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  setUser: (user: User | null) => void
  logout: () => void
  initialize: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  setUser: (user) =>
    set({
      user,
      isAuthenticated: !!user,
      isLoading: false,
    }),

  logout: () => {
    clearTokens()
    set({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    })
  },

  initialize: () => {
    const token = getAccessToken()
    
    if (token) {
      try {
        const payload = decodeToken(token)
        if (payload) {
          // Extract user info from token
          // Adjust based on your JWT structure
          const user: User = {
            id: payload.user_id as number || 0,
            email: payload.email as string || '',
            firstName: payload.first_name as string || '',
            lastName: payload.last_name as string || '',
            roles: payload.roles as string[] || [],
          }
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          })
        } else {
          set({ isLoading: false })
        }
      } catch (error) {
        console.error('Failed to decode token:', error)
        set({ isLoading: false })
      }
    } else {
      set({ isLoading: false })
    }
  },
}))
