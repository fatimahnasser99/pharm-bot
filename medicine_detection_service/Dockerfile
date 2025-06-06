FROM python:3.11-slim

ENV APP_HOST="0.0.0.0"
ENV APP_PORT=5001

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install gdown for downloading files from Google Drive
RUN pip install gdown

# Set the default Google Drive file ID as an environment variable
ENV MODEL_FILE_ID="12k1Ni6QKxevlEeWp5Z7360HxEdT_7EQK"

# Create the directory for the model weights
RUN mkdir -p src/model

# Use gdown to download the model weights using the environment variable
RUN gdown --id $MODEL_FILE_ID -O src/model/yolo11.pt

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5001

# Run the application
CMD ["python", "src/app.py"]