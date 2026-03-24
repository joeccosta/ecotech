import json
import logging
import os
from datetime import datetime, timezone

from app.core.mongo_logger import MongoLogHandler


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "service": os.getenv("SERVICE_NAME", "orders-service"),
            "message": record.getMessage(),
        }

        for field in (
            "event",
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
            "order_id",
            "user_id",
            "customer_name",
            "status",
            "old_status",
            "new_status",
            "status_filter",
            "result_count",
            "email",
            "error",
        ):
            value = getattr(record, field, None)
            if value is not None:
                log_record[field] = value

        return json.dumps(log_record, ensure_ascii=False)


def setup_logging() -> None:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    mongo_handler = MongoLogHandler()
    if mongo_handler.collection is not None:
        root_logger.addHandler(mongo_handler)