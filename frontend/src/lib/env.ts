/**
 * Provides a structured way to access environment variables throughout the application.
 *
 * This module reads environment variables from Vite's `import.meta.env` and
 * exports them in a typed object, ensuring consistency and providing default
 * values for essential variables.
 */

interface Env {
  /** The base URL for the API. */
  apiBaseUrl: string
  /** The base path for the application (for Keystone subpath routing). */
  basePath: string
  /** A boolean indicating if the application is in development mode. */
  isDevelopment: boolean
  /** A boolean indicating if the application is in production mode. */
  isProduction: boolean
}

/**
 * Get the base path from environment or Vite's base config.
 * Ensures it starts and ends with '/' for proper routing.
 */
function getBasePath(): string {
  const basePath = import.meta.env.VITE_BASE_PATH || import.meta.env.BASE_URL || '/'
  // Ensure basePath starts and ends with '/'
  let path = basePath
  if (!path.startsWith('/')) path = '/' + path
  if (!path.endsWith('/')) path = path + '/'
  return path === '//' ? '/' : path
}

/**
 * An object containing the environment variables for the application.
 *
 * @property {string} apiBaseUrl The base URL for the API. Defaults to '' (relative URLs).
 * @property {string} basePath The base path for the application (e.g., '/' or '/sims/').
 * @property {boolean} isDevelopment True if the application is in development mode.
 * @property {boolean} isProduction True if the application is in production mode.
 */
export const env: Env = {
  apiBaseUrl: import.meta.env.VITE_API_URL || '',
  basePath: getBasePath(),
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
}
