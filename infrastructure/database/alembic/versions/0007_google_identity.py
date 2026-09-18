"""Add stable Google identity linkage for OAuth login.

Revision ID: 0007_google_identity
Revises: 0006_query_indexes
"""

import sqlalchemy as sa
from alembic import op

revision = "0007_google_identity"
down_revision = "0006_query_indexes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("google_sub", sa.String(255), nullable=True))
    op.create_index("ix_users_google_sub", "users", ["google_sub"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_google_sub", table_name="users")
    op.drop_column("users", "google_sub")
