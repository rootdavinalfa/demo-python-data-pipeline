#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Error: venv not found. Run ./setup.sh first"
    exit 1
fi

source venv/bin/activate
export PYTHONPATH=$(pwd)/services/mock-server/src:$(pwd)/services/pipeline-service/src
export FLASK_APP=app
export FLASK_ENV=development
source .env

echo "Starting PostgreSQL via Podman..."
podman rm -f local-postgres 2>/dev/null || true
podman run -d --name local-postgres -p 5432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=customer_db \
    postgres:15

echo "Waiting for PostgreSQL..."
sleep 3

echo "Starting mock-server (dev mode) on port 5000..."
cd services/mock-server/src
flask run --host 0.0.0.0 --port 5000 &
MOCK_PID=$!
cd ../../..

echo "Starting pipeline-service (dev mode) on port 8000..."
cd services/pipeline-service/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
PIPELINE_PID=$!
cd ../../..

echo ""
echo "Services running (development mode):"
echo "  - Mock Server:    http://localhost:5000"
echo "  - Pipeline API:   http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop..."

trap "echo 'Stopping services...'; kill $MOCK_PID $PIPELINE_PID 2>/dev/null; podman stop local-postgres 2>/dev/null; exit 0" SIGINT SIGTERM

wait