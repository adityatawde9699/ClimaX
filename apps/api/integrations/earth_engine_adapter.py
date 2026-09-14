"""Earth Engine acquisition adapter. Credentials are loaded only in deployed jobs."""

from datetime import date

from core.config import settings


class EarthEngineAdapter:
    def _ee(self):
        try:
            import ee

            ee.Initialize(project=settings.GCP_PROJECT_ID)
        except ImportError as exc:
            raise RuntimeError(
                "earthengine-api must be installed to fetch satellite rasters"
            ) from exc
        return ee

    def fetch_sentinel5p_no2(
        self, bbox: tuple[float, float, float, float], start_date: date, end_date: date
    ) -> str:
        ee = self._ee()
        region = ee.Geometry.Rectangle(bbox)
        image = (
            ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
            .filterDate(str(start_date), str(end_date))
            .filterBounds(region)
            .mean()
        )
        return image.select("NO2_column_number_density").getDownloadURL(
            {"region": region, "scale": 1000, "format": "GEO_TIFF"}
        )

    def fetch_modis_aod(self, bbox: tuple[float, float, float, float], for_date: date) -> str:
        ee = self._ee()
        region = ee.Geometry.Rectangle(bbox)
        image = (
            ee.ImageCollection("MODIS/061/MCD19A2_GRANULES")
            .filterDate(str(for_date), str(for_date))
            .filterBounds(region)
            .first()
        )
        return image.select("Optical_Depth_047").getDownloadURL(
            {"region": region, "scale": 1000, "format": "GEO_TIFF"}
        )
