FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-postgres.sh .

RUN chmod +x wait-for-postgres.sh

CMD ["./wait-for-postgres.sh", "db", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]