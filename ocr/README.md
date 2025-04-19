
# Flask Google OCR App

This is a simple web app that uses **Google Cloud Vision OCR** to extract text from uploaded images using a Flask interface.

## Features

- Upload an image through the browser
- View the uploaded image and the extracted text
- Uses Google Cloud's Vision API for high-accuracy OCR

## Prerequisites

- Docker
- A Google Cloud Platform account
- A service account with access to the **Vision API**
- A downloaded `key.json` (your service account key)

## Setup Instructions

1. **Add your Google Cloud credentials**

   Place your `key.json` file inside the project root, and add this to your Docker run command:

   ```bash
   docker run -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json -v $(pwd)/key.json:/app/key.json -p 5001:5001 ocr-app-flask
   ```

2. **Build the Docker image**

   ```bash
   docker build -t ocr-app-flask .
   ```

3. **Run the app**

   ```bash
   docker run -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json -v $(pwd)/key.json:/app/key.json -p 5001:5001 ocr-app-flask
   ```

4. **Go to your browser**

   Visit `http://localhost:5001` to use the app.

## Notes

- The `static/uploads/` directory is used to store uploaded images.
- The app uses `full_text_annotation` to return layout-aware OCR results.
