#!/usr/bin/env python3
"""Idempotently seed local ClimaX organizations, sources, and sensors."""

import argparse
import json
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "apps" / "api"))

from core.config import settings  # noqa: E402

SOURCES = [
    ("ds-gov-cpcb-feed", "CPCB reference monitors", "GOVERNMENT_API", "CPCB", 300),
    ("ds-iot-community-mesh", "Delhi community sensor mesh", "IOT", "ClimaX", 60),
]


def load_json(name: str) -> list[dict]:
    return json.loads((ROOT / "data" / "fixtures" / name).read_text())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default="development", choices=["development"])
    parser.parse_args()
    engine = create_engine(settings.DATABASE_SYNC_URL, pool_pre_ping=True)
    with engine.begin() as connection:
        for source in SOURCES:
            connection.execute(
                text("""
                INSERT INTO data_sources (id, name, source_type, provider, refresh_interval_seconds)
                VALUES (:id, :name, :source_type, :provider, :refresh)
                ON CONFLICT (id) DO NOTHING
            """),
                dict(
                    zip(["id", "name", "source_type", "provider", "refresh"], source, strict=True)
                ),
            )
        for organization in load_json("organizations_seed.json"):
            connection.execute(
                text("""
                INSERT INTO organizations (id, name, jurisdiction_code, department, contact_email)
                VALUES (:id, :name, :jurisdiction_code, :department, :contact_email)
                ON CONFLICT (id) DO NOTHING
            """),
                organization,
            )
        for sensor in load_json("sensors_seed.json"):
            location = sensor.pop("location")
            connection.execute(
                text("""
                INSERT INTO sensors (id, data_source_id, external_sensor_id, sensor_type, model_name,
                    latitude, longitude, geom, is_calibrated, is_active)
                VALUES (:id, :data_source_id, :external_sensor_id, :sensor_type, :model_name,
                    :latitude, :longitude, ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326),
                    :is_calibrated, :is_active)
                ON CONFLICT (id) DO NOTHING
            """),
                {**sensor, **location},
            )
    print("Seeded development database: organizations, 2 data sources, and sensors.")


if __name__ == "__main__":
    main()
