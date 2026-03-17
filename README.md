# Data Pipeline Demo

A data pipeline with 3 services: Flask mock server → FastAPI ingestion → PostgreSQL

## Services

| Service | Framework | Port | Description |
|---------|-----------|------|-------------|
| mock-server | Flask | 5000 | REST API serving customer data from JSON |
| pipeline-service | FastAPI | 8000 | Data ingestion using dlt + SQLAlchemy |
| postgres | PostgreSQL 15 | 5432 | Database storage |

## Prerequisites

- Python 3.11+
- Podman (for containers or local PostgreSQL)

---

## Running Locally (Development Mode)

Development servers with auto-reload enabled.

### Setup (first time)

```bash
chmod +x setup.sh run.sh
./setup.sh
```

### Run Services

```bash
source venv/bin/activate
./run.sh
```

### Stop Services

Press `Ctrl+C` or:

```bash
podman stop local-postgres
```

---

## Running with Containers (Production Mode)

Production servers using Gunicorn with multiple workers.

```bash
# Start all services with Podman
podman-compose up -d --build

# Or with Docker
docker-compose up -d --build
```

### Stop Containers

```bash
podman-compose down
# Or
docker-compose down
```

---

## Server Modes

| Mode | mock-server | pipeline-service | Use Case |
|------|-------------|------------------|----------|
| Local | Flask dev server | Uvicorn --reload | Development |
| Container | Gunicorn (4 workers) | Gunicorn + Uvicorn workers (4) | Production |

---

## Test Endpoints

```bash
# Test Flask mock server
curl "http://localhost:5000/api/health"
curl "http://localhost:5000/api/customers?page=1&limit=5"
curl "http://localhost:5000/api/customers/CUST001"

# Trigger data ingestion (FastAPI → Flask → PostgreSQL)
curl -X POST http://localhost:8000/api/ingest

# Query PostgreSQL via FastAPI
curl "http://localhost:8000/api/customers?page=1&limit=5"
curl "http://localhost:8000/api/customers/CUST001"
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/customer_db` |
| `FLASK_API_URL` | Mock server URL | `http://localhost:5000` |

---

## Project Structure

```
demo-python-pipeline/
├── docker-compose.yml       # Container orchestration
├── requirements.txt         # Combined dependencies
├── setup.sh                 # Local setup script
├── run.sh                   # Local run script (dev mode)
├── .env.example             # Environment variables template
├── packages/
│   └── shared/              # Shared Pydantic schemas
│       └── src/schemas.py
└── services/
    ├── mock-server/         # Flask REST API
    │   ├── src/app.py
    │   ├── data/customers.json
    │   ├── Dockerfile
    │   └── requirements.txt
    └── pipeline-service/    # FastAPI + dlt + SQLAlchemy
        ├── src/
        │   ├── main.py
        │   ├── database.py
        │   ├── models/customer.py
        │   └── services/ingestion.py
        ├── Dockerfile
        └── requirements.txt
```

---

## API Endpoints

### Mock Server (Flask)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/customers` | Paginated customer list (params: `page`, `limit`) |
| GET | `/api/customers/{id}` | Single customer by ID |

### Pipeline Service (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/ingest` | Fetch from Flask, upsert to PostgreSQL |
| GET | `/api/customers` | Paginated customers from database |
| GET | `/api/customers/{id}` | Single customer from database |