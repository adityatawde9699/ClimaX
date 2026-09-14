"""Prometheus HTTP and operational metrics."""

import time

from fastapi import Request
from starlette.responses import Response

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
except ImportError:
    CONTENT_TYPE_LATEST = "text/plain"

    class _Metric:
        def __init__(self, *_args, **_kwargs):
            pass

        def labels(self, *_args):
            return self

        def inc(self):
            pass

        def observe(self, _value):
            pass

    Counter = Gauge = Histogram = _Metric

    def generate_latest():
        return b""


api_requests = Counter("api_requests_total", "API requests", ["method", "endpoint", "status"])
api_duration = Histogram("api_request_duration_seconds", "API request latency", ["endpoint"])
active_incidents = Gauge("active_incidents_total", "Active incidents")
critical_alerts = Gauge("critical_alerts_active", "Active critical alerts")


async def metrics_middleware(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    endpoint = request.url.path
    api_requests.labels(request.method, endpoint, response.status_code).inc()
    api_duration.labels(endpoint).observe(time.perf_counter() - started)
    return response


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
