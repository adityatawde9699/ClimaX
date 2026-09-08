# Alerts & Notification Service (`services/alerts`)

Responsible for multi-channel emergency advisory dispatch and automated environmental threshold monitors.

## Responsibilities:
- **Threshold Rule Engine**: Continuously evaluates sensor streams against statutory thresholds (e.g. PM2.5 > 250 µg/m³ for 2 consecutive hours).
- **Spatial Geofenced Broadcasts**: Dispatches notifications strictly to citizens situated within affected polygon radii.
- **Multi-Channel Dispatcher**: Integrates Firebase Cloud Messaging (Web/Mobile Push), SMS gateways, email alerts, and municipal broadcast webhooks.

## Planned Implementation Phase:
- Phase 9 (Alerts and Incident Management).
