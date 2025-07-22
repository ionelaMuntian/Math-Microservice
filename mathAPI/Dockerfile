# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install gcc for any C-extensions (optional) and cleanup caches
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port Uvicorn will run on
EXPOSE 8000

# Launch Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
