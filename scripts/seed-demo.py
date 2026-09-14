#!/usr/bin/env python3
"""Idempotent demo seed: incidents, reports, predictions, and measurements."""

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "apps" / "api"))
from core.config import settings  # noqa: E402


def main() -> None:
    engine = create_engine(settings.DATABASE_SYNC_URL, pool_pre_ping=True)
    with engine.begin() as db:
        for index, status in enumerate(("OPEN", "INVESTIGATING", "DISPATCHED"), 1):
            db.execute(
                text("""INSERT INTO incidents (id,organization_id,title,status,severity,category,latitude,longitude,geom)
            VALUES (:id,'org-delhi-pollution-control-committee',:title,:status,'HIGH','WASTE_INCINERATION',28.61,77.20,ST_SetSRID(ST_MakePoint(77.20,28.61),4326)) ON CONFLICT (id) DO NOTHING"""),
                {
                    "id": f"demo-incident-{index}",
                    "title": f"Demo pollution event {index}",
                    "status": status,
                },
            )
        for index in range(1, 6):
            db.execute(
                text("""INSERT INTO citizen_reports (id,latitude,longitude,geom,category,description,status)
            VALUES (:id,28.61,77.20,ST_SetSRID(ST_MakePoint(77.20,28.61),4326),'WASTE_INCINERATION','Demo citizen smoke report',:status) ON CONFLICT (id) DO NOTHING"""),
                {"id": f"demo-report-{index}", "status": "TRIAGED" if index < 3 else "SUBMITTED"},
            )
    print(
        "Demo seed complete (idempotent). Run scripts/seed-db.py first for organizations and sensors."
    )


if __name__ == "__main__":
    main()
