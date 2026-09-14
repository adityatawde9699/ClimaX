"""add AI audit and incident root-cause fields

Revision ID: 0005_ai_analysis_audit_fields
Revises: 0004_observation_quality_flag
"""

import sqlalchemy as sa
from alembic import op

revision = "0005_ai_analysis_audit_fields"
down_revision = "0004_observation_quality_flag"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "ai_analyses", sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0")
    )
    op.alter_column("ai_analyses", "confidence_score", server_default=None)
    op.add_column("ai_analyses", sa.Column("raw_model_response", sa.Text(), nullable=True))
    op.add_column("incidents", sa.Column("root_cause_summary", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("incidents", "root_cause_summary")
    op.drop_column("ai_analyses", "raw_model_response")
    op.drop_column("ai_analyses", "confidence_score")
