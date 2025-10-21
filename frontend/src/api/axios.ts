import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import { env } from '@/lib/env'

export interface TokenResponse {
  access: string
  refresh: string
}

const api = axios.create({
  baseURL: env.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Token management
let accessToken: string | null = null
let refreshToken: string | null = null

// Single-flight refresh queue
let isRefreshing = false
let refreshSubscribers: Array<(token: string) => void> = []

function subscribeTokenRefresh(callback: (token: string) => void) {
  refreshSubscribers.push(callback)
}

function onTokenRefreshed(token: string) {
  refreshSubscribers.forEach((callback) => callback(token))
  refreshSubscribers = []
}

export function setTokens(access: string, refresh: string) {
  accessToken = access
  refreshToken = refresh
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}

export function getAccessToken(): string | null {
  if (!accessToken) {
    accessToken = localStorage.getItem('access_token')
  }
  return accessToken
}

export function getRefreshToken(): string | null {
  if (!refreshToken) {
    refreshToken = localStorage.getItem('refresh_token')
  }
  return refreshToken
}

export function clearTokens() {
  accessToken = null
  refreshToken = null
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

// Request interceptor - attach access token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getAccessToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle 401 and refresh token
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean
    }

    // If error is not 401 or request already retried, reject
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    // If already refreshing, queue this request
    if (isRefreshing) {
      return new Promise((resolve) => {
        subscribeTokenRefresh((token: string) => {
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${token}`
          }
          resolve(api(originalRequest))
        })
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    const refresh = getRefreshToken()

    if (!refresh) {
      isRefreshing = false
      clearTokens()
      // Redirect to login will be handled by auth store
      return Promise.reject(error)
    }

    try {
      const response = await axios.post<{ access: string }>(
        `${env.apiBaseUrl}/api/auth/token/refresh/`,
        { refresh }
      )

      const newAccessToken = response.data.access
      setTokens(newAccessToken, refresh)

      // Notify all queued requests
      onTokenRefreshed(newAccessToken)

      // Retry original request
      if (originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
      }

      return api(originalRequest)
    } catch (refreshError) {
      // Refresh failed - clear tokens and redirect to login
      clearTokens()
      isRefreshing = false
      refreshSubscribers = []
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  }
)

export default api
