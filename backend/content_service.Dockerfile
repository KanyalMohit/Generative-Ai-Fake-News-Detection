# Use Python 3.9 slim
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory
COPY . .

# Expose port 8001
EXPOSE 8001

# Run the content service
CMD ["uvicorn", "content_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
