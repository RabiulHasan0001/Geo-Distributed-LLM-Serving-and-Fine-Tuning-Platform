# Use a smaller Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Update pip and set retry options to avoid network failures
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --timeout=100 --retries=10 torch torchvision torchaudio transformers fastapi uvicorn

# Expose the port
EXPOSE 8001

# Run the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8001"]
