import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ecotech445a:zigryw-hurgo0-kaxwAv@localhost:5432/users_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def wait_for_db():
    max_retries = 10
    retry_interval = 3

    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                print("Database is ready.")
                return
        except Exception as e:
            print(f"Database not ready yet (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_interval)

    raise Exception("Could not connect to the database after several attempts.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()