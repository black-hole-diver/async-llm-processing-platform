# Asynchronous LLM Processing Platform

A cloud computing project using **FastAPI, RabbitMQ, SQLite, and Docker Compose** to process LLM queries asynchronously with a credit-based user system.

## Services

| Service | Purpose | Port |
| --- | --- | --- |
| User Service | Create users, view balances, add/deduct credits | 5001 |
| LLM Service | List available models and their costs | 5002 |
| Query Service | Submit queries and retrieve results | 5003 |
| Model Runner | Local mock LLM inference endpoint | 5004 |
| Worker Service | Consume RabbitMQ messages and execute queries | Internal |
| RabbitMQ | Message broker and management dashboard | 15672 (dashboard) |

## Requirements

- Docker Desktop (with Docker Compose)
- `curl` (for the API examples)

## Build and run

From the project root (where `docker-compose.yaml` and `.env` are located):

```bash
docker compose up -d --build
docker compose ps
```

The `.env` file must contain the service configuration expected by `docker-compose.yaml`. Check that all containers are running before testing.

API documentation: [User](http://localhost:5001/docs) · [LLM](http://localhost:5002/docs) · [Query](http://localhost:5003/docs). RabbitMQ dashboard: http://localhost:15672.

## Test the end-to-end workflow

### 1. List models

```bash
curl -s http://localhost:5002/llms | python3 -m json.tool
```

### 2. Create a user

```bash
curl -s -X POST http://localhost:5001/user \
  -H 'Content-Type: application/json' \
  -d '{"name":"demo_user"}' | python3 -m json.tool
```

Note the returned `id` (the examples below assume it is `1`). New users start with five credits.

### 3. Submit a query

```bash
curl -s -X POST http://localhost:5003/query \
  -H 'Content-Type: application/json' \
  -d '{"user_id":1,"model":"qwen","prompt":"Explain cloud computing in one sentence."}' \
  | python3 -m json.tool
```

The response includes a `query_id` and an initial `queued` status. Copy the returned query ID.

### 4. Retrieve the result

```bash
curl -s http://localhost:5003/query/YOUR_QUERY_ID | python3 -m json.tool
```

Repeat after a short delay if the query is still `queued` or `executing`. On success, the status becomes `executed` and a `response` is stored.

### 5. Verify the credit balance

```bash
curl -s http://localhost:5001/user/1 | python3 -m json.tool
```

A successful Qwen query costs two credits, so a new user's balance should change from **5 to 3**.

### 6. Inspect worker logs

```bash
docker compose logs --tail=50 worker-service
```

## Error handling checks

- Request a nonexistent model to verify model lookup error handling.
- Submit a query for a nonexistent user or a user with insufficient credits to verify validation.
- Check the query's `status` and `error` fields after a failed model execution; the Worker attempts a credit refund.

The application-level tests used simulated broker and HTTP connections. Run the Docker workflow above to verify integration in your environment.

## Stop the project

```bash
docker compose down
```

To inspect all service logs:

```bash
docker compose logs --tail=100
```

**Note:** `docker compose down -v` also deletes persistent SQLite data volumes; avoid it unless you want to reset the project.
