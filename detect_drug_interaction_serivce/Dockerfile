# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV $(cat .env | xargs)
ENV APP_HOST="0.0.0.0"
ENV APP_PORT=5000

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "src/app.py"]
