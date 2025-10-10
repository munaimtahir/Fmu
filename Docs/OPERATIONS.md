# Operations Runbook

    ## Backups
    - Postgres: nightly dump + weekly full image snapshot.
    - Verify restores monthly in staging.

    ## Monitoring
    - Health endpoints: `/healthz` for API; FE static check.
    - Error tracking: Sentry (optional).
    - Logs: rotate daily; keep 14 days hot.

    ## Incidents
    - Triage channel: #ops-fmu
    - Severity levels, on-call rota, postmortem template.

    ## Restore
    - Stop writers, restore DB from latest verified dump.
    - Re-index, verify health, re-enable writers.
