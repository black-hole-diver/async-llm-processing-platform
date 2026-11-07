import os
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

INITIAL_CREDITS = 5
USER_DB = os.getenv("USER_DB")

class CreateUser(BaseModel):
    name: str

class AmountBody(BaseModel):
    amount: int

def init_db():
    os.makedirs(os.path.dirname(USER_DB), exist_ok=True)
    with sqlite3.connect(USER_DB) as c:
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                credits INTEGER NOT NULL DEFAULT {INITIAL_CREDITS}
            )
        """)
        c.commit()

@app.post("/user", status_code=201)
def create_user(body: CreateUser):
    with sqlite3.connect(USER_DB) as c:
        try:
            cur = c.execute("INSERT INTO users (name) VALUES (?)", (body.name, ))
            c.commit()
            uid = cur.lastrowid
            return {"id": uid, "name": body.name, "credits": INITIAL_CREDITS}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="User exists")


@app.get("/user/{user_id}")
def get_user(user_id: int):
    with sqlite3.connect(USER_DB) as c:
        row = c.execute("SELECT id, name, credits FROM users WHERE id = ?", (user_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "name": row[1], "credits": row[2]}


@app.post("/user/{user_id}/add_credits")
def add_credits(user_id: int, body: AmountBody):
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    with sqlite3.connect(USER_DB) as c:
        c.execute("UPDATE users SET credits = credits + ? WHERE id = ?", (body.amount, user_id))
        c.commit()
        row = c.execute("SELECT credits FROM users WHERE id = ?", (user_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
    return {"status": "ok", "credits": row[0]}


@app.post("/user/{user_id}/deduct_credits")
def deduct_credits(user_id: int, body: AmountBody):
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    with sqlite3.connect(USER_DB) as c:
        user = c.execute(
            "SELECT credits FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        current_credits = user[0]
        if current_credits < body.amount:
            raise HTTPException(status_code=400, detail="Insufficient credits")
        new_credits = current_credits - body.amount
        c.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))
        c.commit()
    return {"status": "ok", "credits": new_credits}