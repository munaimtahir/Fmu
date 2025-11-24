import api, { TokenResponse, setTokens, clearTokens } from './axios'

export interface LoginCredentials {
  /** The user's username. */
  username: string
  /** The user's password. */
  password: string
}

export interface User {
  /** The unique identifier for the user. */
  id: number
  /** The user's email address. */
  email: string
  /** The user's first name. */
  first_name: string
  /** The user's last name. */
  last_name: string
  /** An array of roles assigned to the user. */
  roles: string[]
}

export interface LoginResponse extends TokenResponse {
  /** Optional user information returned upon login. */
  user?: User
}

/**
 * Authenticates a user with the given credentials.
 *
 * This function sends a POST request to the login endpoint and, upon a
 * successful response, stores the received access and refresh tokens.
 *
 * @param {LoginCredentials} credentials The user's username and password.
 * @returns {Promise<LoginResponse>} A promise that resolves with the access and refresh tokens.
 * @throws {Error} If the login request fails.
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
 * Logs out the current user.
 *
 * This function clears the authentication tokens from storage. It can be
 * extended to also call a backend logout endpoint if one exists.
 *
 * @returns {Promise<void>} A promise that resolves when the logout is complete.
 */
export async function logout(): Promise<void> {
  clearTokens()
  // Optionally call backend logout endpoint if it exists
  // await api.post('/api/auth/logout/')
}

/**
 * Retrieves the profile of the currently authenticated user.
 *
 * This function would typically make a request to an endpoint like `/api/me/`.
 * (This is a placeholder implementation).
 *
 * @returns {Promise<User | null>} A promise that resolves with the user's profile, or null if not found.
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
 * Decodes a JWT token to extract its payload.
 *
 * Note: This is a basic implementation for demonstration purposes. In a
 * production environment, a robust JWT decoding library should be used.
 *
 * @param {string} token The JWT token to decode.
 * @returns {Record<string, unknown> | null} The decoded payload as an object, or null if decoding fails.
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
