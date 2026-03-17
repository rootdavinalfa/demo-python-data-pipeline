FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/services/mock-server/src

COPY packages/shared /app/packages/shared

COPY services/mock-server /app/services/mock-server

WORKDIR /app/services/mock-server

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]