from fastapi import FastAPI

from .database import Base, engine, wait_for_db
from .routers.orders import router as orders_router

app = FastAPI(title="Orders Service", version="1.0.0")

Base.metadata.create_all(bind=engine)
wait_for_db()
app.include_router(orders_router)

@app.get("/")
def healthcheck():
    return {"service": "orders-service", "status": "ok"}