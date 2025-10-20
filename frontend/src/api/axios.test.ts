import { describe, it, expect, beforeEach, vi } from 'vitest'
import api, { setTokens, clearTokens, getAccessToken, getRefreshToken } from './axios'

describe('axios setup and token management', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    clearTokens()
  })

  describe('Token management', () => {
    it('should set and get tokens', () => {
      const accessToken = 'test-access-token'
      const refreshToken = 'test-refresh-token'

      setTokens(accessToken, refreshToken)

      expect(getAccessToken()).toBe(accessToken)
      expect(getRefreshToken()).toBe(refreshToken)
      expect(localStorage.getItem('access_token')).toBe(accessToken)
      expect(localStorage.getItem('refresh_token')).toBe(refreshToken)
    })

    it('should clear tokens', () => {
      setTokens('access', 'refresh')
      clearTokens()

      expect(getAccessToken()).toBeNull()
      expect(getRefreshToken()).toBeNull()
      expect(localStorage.getItem('access_token')).toBeNull()
      expect(localStorage.getItem('refresh_token')).toBeNull()
    })

    it('should retrieve tokens from localStorage', () => {
      localStorage.setItem('access_token', 'stored-access')
      localStorage.setItem('refresh_token', 'stored-refresh')

      expect(getAccessToken()).toBe('stored-access')
      expect(getRefreshToken()).toBe('stored-refresh')
    })
  })

  describe('API instance', () => {
    it('should have correct base URL', () => {
      expect(api.defaults.baseURL).toBeDefined()
    })

    it('should have JSON content type header', () => {
      expect(api.defaults.headers['Content-Type']).toBe('application/json')
    })
  })
})
