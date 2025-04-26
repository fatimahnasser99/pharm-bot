# OCR Service

This is a Flask-based API service that uses Google Cloud Vision API to extract text from images. The service processes uploaded images and returns the extracted text.

## Features

- Accepts image uploads via a POST request.
- Uses Google Cloud Vision API for text extraction.
- Returns extracted text in JSON format.
- Dockerized for easy deployment.

## Requirements

- Docker installed on your system.
- Google Cloud Vision API credentials.

## Setup and Usage

### 1. Set Up Google Cloud Vision API Credentials

Create a `.env` file in the project directory and add your Google Cloud Vision API credentials as environment variables:

```env
TYPE=<your-type>
PROJECT_ID=<your-project-id>
PRIVATE_KEY_ID=<your-private-key-id>
PRIVATE_KEY=<your-private-key>
CLIENT_EMAIL=<your-client-email>
CLIENT_ID=<your-client-id>
AUTH_URI=<your-auth-uri>
TOKEN_URI=<your-token-uri>
AUTH_PROVIDER_X509_CERT_URL=<your-auth-provider-cert-url>
CLIENT_X509_CERT_URL=<your-client-cert-url>
UNIVERSE_DOMAIN=<your-universe-domain>
```

### 2. Build the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t ocr-service .
```

### 3. Run the Docker Container

Start the container using the following command:

```bash
docker run -p 5001:5001 --env-file .env ocr-service
```

### 4. Test the API

Once the container is running, you can test the API using tools like `curl` or Postman.

#### Endpoint: `/extracted_text`

- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Body**: Upload an image file with the key `file`.

Example using `curl`:

```bash
curl -X POST -F "file=@path/to/image.jpg" http://localhost:5001/extracted_text
```

### 5. Response Format

The API returns a JSON response with the extracted text:

```json
{
  "extracted_text": "Detected text from the image"
}
```

### 6. Error Handling

- **400**: No file uploaded or file is empty.
- **500**: Internal server error (e.g., Vision API failure).

### Running Tests

Run the test suite using `pytest`:

```bash
pytest tests/
```
