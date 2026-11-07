import os
import sqlite3
import json
import uuid
import pika
import requests
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    setup_rabbitmq_producer()
    yield
    try:
        if conn and conn.is_open:
            conn.close()
    except Exception:
        pass          # the broker may already have closed it

app = FastAPI(lifespan=lifespan)

QUERY_DB = os.getenv("QUERY_DB")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL")
QUEUE = "query_queue"
conn = None
ch = None

class QueryRequest(BaseModel):
    user_id: int
    model: str
    prompt: str

def init_db():
    os.makedirs(os.path.dirname(QUERY_DB), exist_ok=True)
    with sqlite3.connect(QUERY_DB) as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            llm_shortname TEXT,
            prompt TEXT,
            response TEXT,
            status TEXT,
            error TEXT
        )
        """)
        c.commit()

def setup_rabbitmq_producer():
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

def publish_message(msg):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

def get_llm_info(shortname):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED


def deduct_user_credits(user_id, amount):
    try:
        r = requests.post(f"{USER_SERVICE_URL}/user/{user_id}/deduct_credits",
            json={"amount": amount}, timeout=5)
        if r.status_code == 400 or r.status_code == 404:
            raise HTTPException(status_code=r.status_code, detail=r.json().get("detail"))
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"User service unreachable: {e}")

def insert_query(q: QueryRequest):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

@app.post("/query")
def submit_query(q: QueryRequest):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

@app.get("/query/{qid}")
def get_query(qid: str):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED