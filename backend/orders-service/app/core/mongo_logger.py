import logging
import os
from datetime import datetime, timezone
from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError

class MongoLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        mongo_url = os.getenv("MONGODB_URL")
        self.collection = None

        if not mongo_url:
            return

        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=2000)
            client.admin.command("ping")
            db = client["ecotech_logs"]
            self.collection = db["logs"]

            self.collection.create_index([("service", ASCENDING)])
            self.collection.create_index([("event", ASCENDING)])
            self.collection.create_index([("request_id", ASCENDING)])
            self.collection.create_index([("user_id", ASCENDING)])
            self.collection.create_index([("order_id", ASCENDING)])
            self.collection.create_index(
                [("timestamp", ASCENDING)],
                expireAfterSeconds=60 * 60 * 24 * 30,
            )
        except Exception as exc:
            self.collection = None
            logging.getLogger("orders-service").exception(
                "mongo_logger_init_failed",
                extra={"error": str(exc)},
            )

    def emit(self, record: logging.LogRecord) -> None:
        if self.collection is None:
            return

        try:
            log_doc = {
                "timestamp": datetime.now(timezone.utc),
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
                    log_doc[field] = value
            
            # le variavel de ambiente e imprime se true, em producao é silenciosa
            if os.getenv("DEBUG_MONGO_LOGGER") == "true":
                print(f"[mongo_logger] inserting log: {log_doc}")

            self.collection.insert_one(log_doc)
        except PyMongoError as exc:
            logging.getLogger("orders-service").exception(
                "mongo_log_insert_failed",
                extra={"error": str(exc)},
            )