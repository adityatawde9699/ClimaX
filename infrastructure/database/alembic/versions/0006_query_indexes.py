"""add high-frequency query indexes

Revision ID: 0006_query_indexes
Revises: 0005_ai_analysis_audit_fields
"""

from alembic import op

revision = "0006_query_indexes"
down_revision = "0005_ai_analysis_audit_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_incidents_status_severity", "incidents", ["status", "severity"])
    op.create_index("ix_alerts_severity_expires", "alerts", ["severity", "expires_at"])
    op.create_index(
        "ix_predictions_location_horizon", "predictions", ["latitude", "longitude", "horizon_hours"]
    )
    op.create_index("ix_reports_status_created", "citizen_reports", ["status", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_reports_status_created", table_name="citizen_reports")
    op.drop_index("ix_predictions_location_horizon", table_name="predictions")
    op.drop_index("ix_alerts_severity_expires", table_name="alerts")
    op.drop_index("ix_incidents_status_severity", table_name="incidents")
