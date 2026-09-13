"""PostGIS-backed spatial queries shared by API services."""

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import Incident, Sensor


class GeospatialService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_sensors_within_radius(
        self, lat: float, lng: float, radius_m: float
    ) -> list[Sensor]:
        point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        query = select(Sensor).where(
            func.ST_DWithin(func.Geography(Sensor.geom), func.Geography(point), radius_m)
        )
        return list((await self.session.scalars(query)).all())

    async def find_incidents_within_bbox(
        self, bbox: tuple[float, float, float, float]
    ) -> list[Incident]:
        west, south, east, north = bbox
        envelope = func.ST_MakeEnvelope(west, south, east, north, 4326)
        return list(
            (
                await self.session.scalars(
                    select(Incident).where(func.ST_Intersects(Incident.geom, envelope))
                )
            ).all()
        )

    async def calculate_affected_population(self, geojson: str, radius_m: float) -> int:
        query = text("""SELECT COALESCE(SUM(population), 0) FROM population_grid
            WHERE ST_DWithin(geom::geography, ST_SetSRID(ST_GeomFromGeoJSON(:geojson), 4326)::geography, :radius_m)""")
        return int(
            await self.session.scalar(query, {"geojson": geojson, "radius_m": radius_m}) or 0
        )
