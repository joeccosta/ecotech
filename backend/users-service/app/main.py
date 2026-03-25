import logging
import time
import uuid

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

from app.core.logging_config import setup_logging

from .database import Base, engine, wait_for_db
from .routers.auth import router as auth_router
from .routers.users import router as users_router

setup_logging()
logger = logging.getLogger("users-service")

app = FastAPI(title="Users Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9000",
        "http://localhost:8500",
        "http://localhost:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    started_data = {
        "event": "request_started",
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
    }

    logger.info(
        "request_started",
        extra={
            **started_data,
            "structured_data": started_data,
        },
    )

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        failed_data = {
            "event": "request_failed",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "duration_ms": duration_ms,
        }
        logger.exception(
            "request_failed",
            extra={
                **failed_data,
                "structured_data": failed_data,
            },
        )
        raise

    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    finished_data = {
        "event": "request_finished",
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
    }

    logger.info(
        "request_finished",
        extra={
            **finished_data,
            "structured_data": finished_data,
        },
    )

    response.headers["X-Request-ID"] = request_id
    return response


app.include_router(auth_router)

Base.metadata.create_all(bind=engine)
wait_for_db()
app.include_router(users_router)


@app.get("/")
def healthcheck():
    return {"service": "users-service", "status": "ok"}