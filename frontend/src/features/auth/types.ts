/**
 * Authentication types
 */

export interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  roles: string[]
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
}

export interface LoginCredentials {
  email: string
  password: string
}
