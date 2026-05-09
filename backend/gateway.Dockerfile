# Use Python 3.9 slim
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements from backend root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory to /app
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the gateway using uvicorn
# We run as module 'gateway.main'
CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
