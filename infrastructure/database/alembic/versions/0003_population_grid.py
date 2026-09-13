"""Add population grid required by spatial exposure calculations."""

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "CREATE TABLE population_grid (id BIGSERIAL PRIMARY KEY, population INTEGER NOT NULL CHECK (population >= 0), geom GEOMETRY(Polygon, 4326) NOT NULL)"
    )
    op.execute("CREATE INDEX idx_population_grid_geom ON population_grid USING GIST (geom)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS population_grid")
