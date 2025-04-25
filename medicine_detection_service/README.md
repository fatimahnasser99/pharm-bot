## Image Processing Service

This service uses YOLO to detect objects in images and returns their bounding boxes.

### Features
- Accepts an image file as input.
- Returns bounding boxes and object labels.

### Usage
1. Send a POST request to `/detect` with an image file.
2. The response will contain the detected objects and their bounding boxes.

### Installation
1. Navigate to the `image_processing` directory:
    ```
    cd image_processing
    ```
2. Build the Docker image:
    ```
    docker build -t image_processing_service .
    ```
3. Run the container:
    ```
    docker run -p 5001:5001 image_processing_service
    ```
