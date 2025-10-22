/**
 * Environment configuration
 * Reads from Vite environment variables
 */

interface Env {
  apiBaseUrl: string
  isDevelopment: boolean
  isProduction: boolean
}

export const env: Env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
}
