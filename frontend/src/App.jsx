import { useEffect, useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const controller = new AbortController()

    async function loadHealth() {
      try {
        setLoading(true)
        const response = await fetch(`${API_BASE_URL}/health/`, {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error(`Health check failed with status ${response.status}`)
        }

        const payload = await response.json()
        setHealth({ ...payload, fetchedAt: new Date().toISOString() })
        setError(null)
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message || 'Unable to reach the API')
          setHealth(null)
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      }
    }

    loadHealth()

    return () => controller.abort()
  }, [])

  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <div>
          <h1>SIMS Operations Console</h1>
          <p className="dashboard__subtitle">
            Unified entry point for admissions, enrollment, and records management.
          </p>
        </div>
        <div className="dashboard__environment">
          <span className="dashboard__badge">API</span>
          <code className="dashboard__code">{API_BASE_URL}</code>
        </div>
      </header>

      <div className="dashboard__body">
        <aside className="dashboard__sidebar">
          <h2>Quick Navigation</h2>
          <ul>
            <li>Admissions overview</li>
            <li>Enrollment pipeline</li>
            <li>Attendance tracking</li>
            <li>Assessment workflows</li>
            <li>Transcripts and requests</li>
          </ul>
        </aside>

        <main className="dashboard__main">
          <section className="dashboard__status-card">
            <header>
              <h2>Backend health</h2>
              <p>Live status from the Django API health endpoint.</p>
            </header>
            <div className="dashboard__status-content">
              {loading && <p className="dashboard__muted">Checking service health…</p>}
              {error && <p className="dashboard__error">{error}</p>}
              {!loading && !error && health && (
                <dl className="dashboard__metrics">
                  <div>
                    <dt>Service</dt>
                    <dd>{health.service}</dd>
                  </div>
                  <div>
                    <dt>Status</dt>
                    <dd className="dashboard__status-indicator">{health.status}</dd>
                  </div>
                  <div>
                    <dt>Checked</dt>
                    <dd>{new Date(health.fetchedAt).toLocaleTimeString()}</dd>
                  </div>
                </dl>
              )}
            </div>
          </section>

          <section className="dashboard__grid">
            <article className="dashboard__card">
              <h3>What&apos;s next?</h3>
              <p>
                Replace these placeholders with widgets that matter for your rollout—recent admissions,
                pending approvals, or student support tickets.
              </p>
            </article>
            <article className="dashboard__card">
              <h3>Team checklist</h3>
              <ul>
                <li>Finalize authentication flow with SimpleJWT tokens.</li>
                <li>Connect frontend state to protected API endpoints.</li>
                <li>Visualize enrollment KPIs and alerts.</li>
              </ul>
            </article>
            <article className="dashboard__card">
              <h3>Documentation</h3>
              <p>
                Explore the API reference at <strong>/api/docs</strong> or the schema at <strong>/api/schema</strong> to
                plan integrations with external systems.
              </p>
            </article>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
