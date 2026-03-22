from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .database import Base, engine, wait_for_db
from .routers.orders import router as orders_router

app = FastAPI(title="Orders Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9000",
        "http://localhost:8500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
wait_for_db()
app.include_router(orders_router)

@app.get("/")
def healthcheck():
    return {"service": "orders-service", "status": "ok"}