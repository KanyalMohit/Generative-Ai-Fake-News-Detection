# Use Python 3.9 slim
FROM python:3.9-slim

# Install system dependencies for OpenCV if needed (though numpy/pillow might be enough depending on implementation)
# RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory
COPY . .

# Run the video service worker
CMD ["python", "video_service/main.py"]
