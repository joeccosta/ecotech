import json
import logging
import os
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "service": os.getenv("SERVICE_NAME", "orders-service"),
            "message": record.getMessage(),
        }

        if hasattr(record, "event"):
            log_record["event"] = record.event

        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id

        if hasattr(record, "method"):
            log_record["method"] = record.method

        if hasattr(record, "path"):
            log_record["path"] = record.path

        if hasattr(record, "status_code"):
            log_record["status_code"] = record.status_code

        if hasattr(record, "duration_ms"):
            log_record["duration_ms"] = record.duration_ms

        if hasattr(record, "order_id"):
            log_record["order_id"] = record.order_id

        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id

        if hasattr(record, "customer_name"):
            log_record["customer_name"] = record.customer_name

        if hasattr(record, "status"):
            log_record["status"] = record.status

        if hasattr(record, "old_status"):
            log_record["old_status"] = record.old_status

        if hasattr(record, "new_status"):
            log_record["new_status"] = record.new_status

        if hasattr(record, "status_filter"):
            log_record["status_filter"] = record.status_filter

        if hasattr(record, "result_count"):
            log_record["result_count"] = record.result_count

        return json.dumps(log_record, ensure_ascii=False)


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    root_logger.handlers.clear()
    root_logger.addHandler(handler)