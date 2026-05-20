FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/

RUN mkdir -p /app/data /app/backup /app/logs

WORKDIR /app/src

ENTRYPOINT ["python", "main.py"]
CMD ["/app/data", "/app/backup"]
