"""Small physics-informed fallback for a downwind plume cone."""

import math


def plume_geojson(
    latitude: float,
    longitude: float,
    wind_speed: float,
    wind_direction: float,
    distance_m: float = 5000,
) -> dict:
    angle = math.radians(wind_direction)
    scale = distance_m / 111_000
    dx, dy = math.sin(angle) * scale, math.cos(angle) * scale
    width = max(0.003, 0.015 / max(wind_speed, 1))
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"model": "gaussian-plume"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [longitude, latitude],
                            [longitude + dx - width, latitude + dy],
                            [longitude + dx + width, latitude + dy],
                            [longitude, latitude],
                        ]
                    ],
                },
            }
        ],
    }
