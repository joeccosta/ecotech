from fastapi import FastAPI

from .database import Base, engine, wait_for_db
from .routers.users import router as users_router

app = FastAPI(title="Users Service", version="1.0.0")

Base.metadata.create_all(bind=engine)

wait_for_db()

app.include_router(users_router)


@app.get("/")
def healthcheck():
    return {"service": "users-service", "status": "ok"}