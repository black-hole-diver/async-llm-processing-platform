import sqlite3, os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from urllib.parse import urljoin

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

MODEL_ENDPOINT = os.getenv("MODEL_ENDPOINT")
SMOL_MODEL_FULLNAME = os.getenv("SMOL_MODEL_FULLNAME")
SMOL_MODEL_SHORTNAME = "smol"
SMOL_MODEL_COST = 1
QWEN_MODEL_FULLNAME = os.getenv("QWEN_MODEL_FULLNAME")
QWEN_MODEL_SHORTNAME = "qwen"
QWEN_MODEL_COST = 2
CHAT_ENDPOINT = urljoin(MODEL_ENDPOINT, "chat/completions")
LLM_DB = os.getenv("LLM_DB")

def init_db():
    with sqlite3.connect(LLM_DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS llms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT UNIQUE,
            shortname TEXT UNIQUE,
            endpoint TEXT,
            cost INTEGER
        )""")
        # preload two sample models (internal runner hostname)
        c.execute("INSERT OR IGNORE INTO llms (fullname, shortname, endpoint, cost) VALUES (?, ?, ?, ?)",
                (SMOL_MODEL_FULLNAME, SMOL_MODEL_SHORTNAME, CHAT_ENDPOINT, SMOL_MODEL_COST))
        c.execute("INSERT OR IGNORE INTO llms (fullname, shortname, endpoint, cost) VALUES (?, ?, ?, ?)",
                (QWEN_MODEL_FULLNAME, QWEN_MODEL_SHORTNAME, CHAT_ENDPOINT, QWEN_MODEL_COST))
        c.commit()

@app.get("/llm/{shortname}")
def get_llm(shortname: str):
    with sqlite3.connect(LLM_DB) as c:
        row = c.execute("SELECT fullname, shortname, endpoint, cost FROM llms WHERE shortname = ?", (shortname,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="LLM not found")
        return {"fullname": row[0], "shortname": row[1], "endpoint": row[2], "cost": row[3]}

@app.get("/llms")
def list_llms():
    with sqlite3.connect(LLM_DB) as c:
        rows = c.execute("SELECT fullname, shortname, endpoint, cost FROM llms").fetchall()
        return [{"fullname": r[0], "shortname": r[1], "endpoint": r[2], "cost": r[3]} for r in rows]
