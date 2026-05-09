FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Expose the gateway port (Railway maps this)
EXPOSE 8000

# Start both services using a shell script
CMD ["sh", "-c", "uvicorn content_service.main:app --host 0.0.0.0 --port 8001 & uvicorn gateway.main:app --host 0.0.0.0 --port 8000"]
