import time
from fastapi import FastAPI
from sqlalchemy import text
from .db import engine, Base
from . import models  # noqa: F401 (só pra registrar as tabelas)

app = FastAPI(title="InspiraUSP MVP")

@app.on_event("startup")
def startup():
    # espera o MariaDB ficar pronto
    for i in range(30):  # ~30s
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError("DB não ficou pronto a tempo")

    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "success", "message": "Hello, InspiraUSP!"}

@app.get("/db-health")
def db_health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}
