import api, { TokenResponse, setTokens, clearTokens } from './axios'

export interface LoginCredentials {
  email: string
  password: string
}

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  roles: string[]
}

export interface LoginResponse extends TokenResponse {
  user?: User
}

/**
 * Login with email and password
 * Returns access and refresh tokens
 */
export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  try {
    const response = await api.post<TokenResponse>('/api/auth/token/', credentials)
    const { access, refresh } = response.data
    
    setTokens(access, refresh)
    
    // Optionally fetch user profile after login
    // For now, we'll extract basic info from token or return tokens only
    return { access, refresh }
  } catch (error) {
    throw error
  }
}

/**
 * Logout - clear tokens and invalidate session
 */
export async function logout(): Promise<void> {
  clearTokens()
  // Optionally call backend logout endpoint if it exists
  // await api.post('/api/auth/logout/')
}

/**
 * Get current user profile
 * This would typically call /api/me/ or similar endpoint
 */
export async function getCurrentUser(): Promise<User | null> {
  try {
    // This endpoint may not exist yet in backend
    // For now, return null or decode from JWT
    // const response = await api.get<User>('/api/auth/me/')
    // return response.data
    return null
  } catch (error) {
    return null
  }
}

/**
 * Decode JWT token to extract user info
 * Basic implementation - in production, use a proper JWT library
 */
export function decodeToken(token: string): Record<string, unknown> | null {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (error) {
    return null
  }
}
