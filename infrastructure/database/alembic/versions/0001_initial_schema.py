"""Initial ClimaX relational and spatial schema.

Revision ID: 0001
Revises:
"""

from pathlib import Path

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    schema = Path(__file__).parents[2] / "0001_initial_schema.sql"
    op.execute(schema.read_text())


def downgrade() -> None:
    tables = [
        "audit_logs",
        "intervention_measurements",
        "interventions",
        "verifications",
        "incidents",
        "alerts",
        "risk_assessments",
        "predictions",
        "pollution_events",
        "ai_analyses",
        "citizen_reports",
        "environmental_observations",
        "sensors",
        "data_sources",
        "users",
        "organizations",
    ]
    for table in tables:
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
