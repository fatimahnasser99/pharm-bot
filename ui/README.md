# PharmaBot UI

This is the user interface for PharmaBot, a tool designed to detect medicines, extract text, and analyze potential drug interactions. The UI communicates with backend services via a gateway API.

## Features

- Upload images or enter text to analyze drug interactions.
- Displays detected objects, extracted text, and interaction analysis.
- Responsive design for both desktop and mobile devices.
- Camera integration for capturing images directly.

## Requirements

- Docker installed on your system.
- A running instance of the PharmaBot backend services.

## Setup and Usage

### 1. Build the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t pharmabot-ui .
```

### 2. Run the Docker Container

Start the container using the following command:

```bash
docker run -p 5004:5004 --env GATEWAY_URL=http://<gateway-service-url>/analyze pharmabot-ui
```

Replace `<gateway-service-url>` with the actual URL of your gateway service.

### 3. Access the UI

Once the container is running, open your browser and navigate to:

```
http://localhost:5004
```

### 4. Usage

- **Upload an Image**: Click the "Upload Image" button to upload an image for analysis.
- **Take a Picture**: Use the "Take Picture" button to capture an image using your device's camera.
- **Enter Text**: Type drug names in the text field to analyze interactions.
- **Submit**: Click the submit button to send the data for processing.

### 5. Response

The UI displays the following results:

- **Detected Objects**: Shows bounding boxes for detected objects in the uploaded image.
- **Detected Drugs**: Lists the drugs detected in the image or text.
- **Drug Interaction Analysis**: Displays the interaction analysis or a message if fewer than two drugs are provided.

### 6. Error Handling

- If no file or text is provided, an error message is displayed.
- If the gateway service is unreachable or returns an error, the error message is shown.

### File Structure

- `templates/index.html`: Main HTML template for the UI.
- `static/js/bounding-box.js`: JavaScript for drawing bounding boxes on detected objects.
- `app.py`: Flask application for handling requests and rendering the UI.
