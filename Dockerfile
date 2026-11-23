# Use an official Python slim runtime as the base image
FROM python:3.11-slim

# Set environment variables to prevent python from buffering stdout/stderr and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency requirements first to leverage Docker layer cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose FastAPI's default port
EXPOSE 8000

# Health check to verify that the API is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "myapp:app", "--host", "0.0.0.0", "--port", "8000"]
