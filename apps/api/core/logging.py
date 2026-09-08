"""
ClimaX Observability & Structured Logging
Provides JSON structured logging for Google Cloud Logging and OpenTelemetry integration.
"""

import logging
import sys


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("climax")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '{"time":"%(asctime)s", "level":"%(levelname)s", "name":"%(name)s", "message":"%(message)s"}'
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = setup_logging()
