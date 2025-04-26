# PharmaBot Gateway

The Gateway service acts as the external endpoint for PharmaBot, orchestrating communication between various backend services such as medicine detection, OCR, drug extraction, and drug interaction analysis. It also provides Prometheus metrics for monitoring.

## Features

- Accepts image or text input for analysis.
- Routes requests to backend services for detection, OCR, extraction, and interaction analysis.
- Aggregates and returns results in a unified response.
- Exposes Prometheus metrics for monitoring.

## Requirements

- Docker installed on your system.
- Running instances of the backend services:
  - Medicine Detection Service
  - OCR Service
  - Drug Extractor Service
  - Drug Interaction Service

## Setup and Usage

### 1. Environment Variables

Create a `.env` file or add them to the docker-compose file in the project directory and configure the URLs for the backend services:

```env
DETECTION_URL=http://<medicine-detection-service-url>/detect
OCR_URL=http://<ocr-service-url>/extracted_text
EXTRACTOR_URL=http://<drug-extractor-service-url>/extract
INTERACTION_URL=http://<drug-interaction-service-url>/rag
APP_HOST=0.0.0.0
APP_PORT=5000
```

Replace `<service-url>` with the actual URLs of the respective services.

### 2. Build and Run with Docker

#### Build the Docker Image

```bash
docker build -t pharmabot-gateway .
```

#### Run the Docker Container

```bash
docker run -p 5000:5000 --env-file .env pharmabot-gateway
```

### 3. API Endpoints

#### `/analyze` (POST)

- **Description**: Accepts an image or text input and returns the analysis results.
- **Request**:
  - **Image Input**: `multipart/form-data` with a file field named `file`.
  - **Text Input**: JSON payload with a `text` field.
- **Response**:
  ```json
  {
    "extracted_text": "Extracted text from OCR",
    "drugs_list": ["Drug1", "Drug2"],
    "image_data": "Base64-encoded image data",
    "predictions": [
      {
        "x": 100,
        "y": 100,
        "width": 50,
        "height": 50,
        "confidence": 0.9
      }
    ],
    "detection_result": "Serialized detection result",
    "interaction_result": "Drug interaction analysis result"
  }
  ```
- **Error Handling**:
  - **400**: Invalid input.
  - **500**: Internal server error or backend service failure.

#### `/metrics` (GET)

- **Description**: Exposes Prometheus metrics for monitoring.
- **Response**: Plain text metrics data.

### 4. Development

#### Running Tests

Run the test suite using `pytest`:

```bash
pytest tests/
```

### 5. Prometheus Metrics

The Gateway service provides the following Prometheus metrics:

- **HTTP Metrics**:

  - `http_requests_total`: Total HTTP requests by method, endpoint, and status.
  - `http_request_duration_seconds`: Latency of HTTP requests.

- **Service-Specific Metrics**:
  - Detection, OCR, extraction, and interaction metrics (e.g., latency, success rate, error count).

### 6. File Structure

- `app.py`: Main Flask application.
- `metrics/`: Prometheus metrics instrumentation.
- `tests/`: Unit tests for the Gateway service.
