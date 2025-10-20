import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the dashboard header', () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok', service: 'SIMS Backend' }),
    })

    render(<App />)
    expect(screen.getByText('SIMS Operations Console')).toBeTruthy()
  })

  it('displays loading state initially', () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok', service: 'SIMS Backend' }),
    })

    render(<App />)
    expect(screen.getByText(/Checking service health/i)).toBeTruthy()
  })

  it('displays health data when API call succeeds', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok', service: 'SIMS Backend' }),
    })

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByText('SIMS Backend')).toBeTruthy()
      expect(screen.getByText('ok')).toBeTruthy()
    })
  })

  it('displays error when API call fails', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 500,
    })

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByText(/Health check failed/i)).toBeTruthy()
    })
  })

  it('displays error when fetch throws', async () => {
    global.fetch.mockRejectedValue(new Error('Network error'))

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByText(/Network error/i)).toBeTruthy()
    })
  })

  it('renders navigation sidebar', () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok', service: 'SIMS Backend' }),
    })

    render(<App />)
    expect(screen.getByText('Quick Navigation')).toBeTruthy()
    expect(screen.getByText('Admissions overview')).toBeTruthy()
    expect(screen.getByText('Enrollment pipeline')).toBeTruthy()
  })

  it('renders dashboard cards', () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok', service: 'SIMS Backend' }),
    })

    render(<App />)
    expect(screen.getByText("What's next?")).toBeTruthy()
    expect(screen.getByText('Team checklist')).toBeTruthy()
    expect(screen.getByText('Documentation')).toBeTruthy()
  })
})
