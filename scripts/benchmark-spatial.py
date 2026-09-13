#!/usr/bin/env python3
"""Benchmark a representative 10k-row PostGIS radius query."""

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "apps" / "api"))

from core.config import settings  # noqa: E402


def main() -> None:
    engine = create_engine(settings.DATABASE_SYNC_URL)
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TEMP TABLE benchmark_sensors (id integer, geom geometry(Point, 4326))")
        )
        connection.execute(
            text("""INSERT INTO benchmark_sensors
            SELECT value, ST_SetSRID(ST_MakePoint(77.2 + (random() - .5), 28.6 + (random() - .5)), 4326)
            FROM generate_series(1, 10000) AS value""")
        )
        connection.execute(
            text("CREATE INDEX benchmark_sensors_geom ON benchmark_sensors USING GIST (geom)")
        )
        connection.execute(text("ANALYZE benchmark_sensors"))
        plan = connection.execute(
            text("""EXPLAIN (ANALYZE, FORMAT JSON)
            SELECT id FROM benchmark_sensors WHERE ST_DWithin(
              geom::geography, ST_SetSRID(ST_MakePoint(77.2, 28.6), 4326)::geography, 5000)""")
        ).scalar_one()
        execution_ms = plan[0]["Execution Time"]
    print(f"10k sensor radius query: {execution_ms:.2f}ms")
    if execution_ms >= 100:
        raise SystemExit("Spatial query exceeded the 100ms Phase 2 target")


if __name__ == "__main__":
    main()
