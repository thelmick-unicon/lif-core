import logging
import os

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
numeric_log_level = getattr(logging, log_level, logging.INFO)


# -------------------------------------------------------------------------
# Logging Setup
# -------------------------------------------------------------------------
# Example output: 2025-10-09 14:33:21.123 INFO | my.logger | message
logging.basicConfig(
    level=numeric_log_level,
    format="%(asctime)s.%(msecs)03d %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    return logger
