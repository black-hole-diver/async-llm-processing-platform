import os, json, sqlite3
import pika, requests

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL")
QUERY_DB = os.getenv("QUERY_DB")
QUEUE = "query_queue"

def setup_rabbitmq_consumer():
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

def get_llm_info(shortname):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

def refund_user(user_id, amount):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

def update_query_status(qid, status, response=None, error=None):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

def call_llm(query_id, user_id, fullname, endpoint, prompt, cost):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

def process(ch, method, _, body):
    # TODO
    raise NotImplementedError # REMOVE THIS LINE WHEN IMPLEMENTED

if __name__ == "__main__":
    setup_rabbitmq_consumer()