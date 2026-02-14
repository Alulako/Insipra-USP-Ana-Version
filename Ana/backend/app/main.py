import time
from fastapi import FastAPI
from sqlalchemy import text
from .db import engine, Base
from . import models  # noqa: F401
from .routers import auth, users, courses

app = FastAPI(title="InspiraUSP MVP")

@app.on_event("startup")
def startup():
    for _ in range(30):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError("DB não ficou pronto a tempo")

    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)

@app.get("/")
def root():
    return {"status": "success", "message": "Hello, InspiraUSP!"}

@app.get("/db-health")
def db_health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}
