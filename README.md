# MII Order SRE

Reliability and operational documentation for the MII order service.

## Overview

Use this repository to document how the service is monitored, operated, and
supported. Add service-specific details only after confirming them with the
service owners; this README does not define production endpoints or targets.

## Operating guidance

- Check the service's approved dashboards and alerts when investigating an
	issue.
- Review recent deployments and dependency health as part of incident triage.
- Follow the team's approved runbooks and change procedures before taking
	production action.
- Record customer impact, incident timelines, and follow-up work through the
	established incident process.

## Reliability objectives

Document agreed service-level indicators and objectives here once they have
been reviewed by the service owners.

| Indicator | Objective | Measurement window |
| --- | --- | --- |
| Availability | TBD | TBD |
| Request latency | TBD | TBD |
| Order processing delay | TBD | TBD |

## Runbooks and links

Add links to the relevant dashboards, alert definitions, runbooks, deployment
procedures, and incident channel. Useful runbooks may cover elevated errors or
latency, delayed order processing, dependency outages, and deployment rollback.

## Ownership

Add the service owner, on-call rotation, and escalation path here so responders
know where to get help.

## Documentation guidelines

Keep instructions accurate, concise, and actionable. Review operational changes
with the service owners. Do not commit credentials, secrets, or customer data.
