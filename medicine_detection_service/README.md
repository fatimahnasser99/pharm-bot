# Medicine Detection Service

This is a Flask-based API service for detecting medicines in images using a YOLO model. The service processes uploaded images and returns predictions with bounding box coordinates, confidence scores, and class names.

## Features

- Accepts image uploads via a POST request.
- Runs a YOLO model to detect medicines in the image.
- Returns predictions in JSON format.
- Dockerized for easy deployment.

## Requirements

- Docker installed on your system.

## Setup and Usage

### 1. Build the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t medicine-detection-service .
```

### 2. Run the Docker Container

Start the container using the following command:

```bash
docker run -p 5001:5001 --env MODEL_FILE_ID="12k1Ni6QKxevlEeWp5Z7360HxEdT_7EQK" medicine-detection-service
```

Replace `12k1Ni6QKxevlEeWp5Z7360HxEdT_7EQK` with the Google Drive file ID of your YOLO model weights if different from the default.

### 4. Test the API

Once the container is running, you can test the API using tools like `curl` or Postman.

#### Endpoint: `/detect`

- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Body**: Upload an image file with the key `file`.

Example using `curl`:

```bash
curl -X POST -F "file=@path/to/image.jpg" http://localhost:5001/detect
```

### 5. Response Format

The API returns a JSON response with predictions:

```json
{
  "predictions": [
    {
      "x": 100.0,
      "y": 150.0,
      "width": 50.0,
      "height": 50.0,
      "confidence": 0.85,
      "class_name": "Medicine"
    }
  ]
}
```

### 6. Error Handling

- **400**: No file uploaded or file is empty.
- **500**: Internal server error (e.g., model failure).

### Running Tests

Run the test suite using `pytest`:

```bash
pytest tests/
```
