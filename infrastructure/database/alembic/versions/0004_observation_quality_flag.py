"""add observation quality flag

Revision ID: 0004_observation_quality_flag
Revises: 0003
"""

import sqlalchemy as sa
from alembic import op

revision = "0004_observation_quality_flag"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "environmental_observations",
        sa.Column("quality_flag", sa.String(length=20), nullable=False, server_default="VALID"),
    )
    op.alter_column("environmental_observations", "quality_flag", server_default=None)


def downgrade() -> None:
    op.drop_column("environmental_observations", "quality_flag")
