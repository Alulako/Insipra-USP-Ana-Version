import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .db import engine, Base
from . import models  # noqa: F401
from .routers import auth, users, courses

app = FastAPI(title="InspiraUSP MVP")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:53477",  
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8010",
        "http://127.0.0.1:53477",
        "http://127.0.0.1:8010",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
