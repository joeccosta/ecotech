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
            self.collection.create_index(
                [("timestamp", ASCENDING)],
                expireAfterSeconds=60 * 60 * 24 * 30,
            )
        except Exception:
            self.collection = None

    def emit(self, record: logging.LogRecord) -> None:
        if self.collection is None:
            return

        try:
            log_doc = {
                "timestamp": datetime.now(timezone.utc),
                "level": record.levelname,
                "logger": record.name,
                "service": os.getenv("SERVICE_NAME", record.name),
                "message": record.getMessage(),
            }

            if hasattr(record, "exc_info") and record.exc_info:
                log_doc["has_exception"] = True

            if hasattr(record, "structured_data") and isinstance(record.structured_data, dict):
                log_doc.update(record.structured_data)

            self.collection.insert_one(log_doc)
        except PyMongoError:
            pass