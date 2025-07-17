# Use official Python image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy requirements (or poetry/pyproject if you use those)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code
COPY . .

# Expose the port (FastAPI default is 8000)
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
