FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/services/pipeline-service/src

COPY packages/shared /app/packages/shared

COPY services/pipeline-service /app/services/pipeline-service

WORKDIR /app/services/pipeline-service

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]