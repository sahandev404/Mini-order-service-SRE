# Incident 001 – Database Unavailable

## Summary
The order service could not create new orders.

## Impact
Users could not submit orders during the incident.

## Detection
The readiness endpoint reported failure.
Application logs showed database connection errors.

## Root Cause
The PostgreSQL container was stopped.

## Resolution
Restarted the PostgreSQL container.

## Prevention
- Add database health checks.
- Configure appropriate retry handling.
- Add monitoring and alerting.
