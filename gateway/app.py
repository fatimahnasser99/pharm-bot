from flask import Flask, request, jsonify
import requests
import io
from PIL import Image
import base64
import json
import os
import time
from metrics import (
    instrument_app,
    start_metrics_server,
    record_detection_metrics,
    record_ocr_metrics,
    record_extractor_metrics,
    record_interaction_metrics
)

app = Flask(__name__)

# Initialize metrics
start_metrics_server(port=8000)
instrument_app(app)

DETECTION_URL = os.environ.get("DETECTION_URL", "http://medicine-detection-service:5001/detect")
OCR_URL = os.environ.get("OCR_URL", "http://ocr-service:5001/extracted_text")
EXTRACTOR_URL = os.environ.get("EXTRACTOR_URL", "http://drug-extractor-service:5000/extract")
INTERACTION_URL = os.environ.get("INTERACTION_URL", "http://drug-interaction-service:8000/rag")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        extracted_text = ""
        predictions = []
        image_data = None
        detection_result = {}
        interaction_result = {}
        start_time = time.time()

        if 'file' in request.files:
            image_file = request.files['file']

            # Read original image in memory
            image_bytes = image_file.read()
            original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            # Step 1: Object detection
            detect_start_time = time.time()
            detect_response = requests.post(DETECTION_URL, files={"file": io.BytesIO(image_bytes)})
            detect_duration = time.time() - detect_start_time
            
            if detect_response.status_code != 200:
                record_detection_metrics(
                    duration=detect_duration,
                    object_count=0,
                    success=False,
                    error_type='5xx'
                )
                return jsonify({"error": "Object detection failed"}), 500

            detection_result = detect_response.json()
            predictions = detection_result.get("predictions", [])
            
            # Record detection metrics
            record_detection_metrics(
                duration=detect_duration,
                object_count=len(predictions),
                success=True
            )

            if not predictions:
                return jsonify({"error": "No objects detected"}), 200

            texts = []
            total_text_length = 0
            for pred in predictions:
                x, y = pred["x"], pred["y"]
                w, h = pred["width"], pred["height"]

                left = int(x - w / 2)
                top = int(y - h / 2)
                right = int(x + w / 2)
                bottom = int(y + h / 2)

                # Crop and prepare image for OCR
                cropped_image = original_image.crop((left, top, right, bottom))
                cropped_bytes = io.BytesIO()
                cropped_image.save(cropped_bytes, format="JPEG")
                cropped_bytes.seek(0)

                # Send to OCR
                ocr_start_time = time.time()
                ocr_response = requests.post(OCR_URL, files={"file": cropped_bytes})
                ocr_duration = time.time() - ocr_start_time
                
                if ocr_response.status_code == 200:
                    text = ocr_response.json().get("extracted_text", "")
                    texts.append(text)
                    total_text_length += len(text)
                    record_ocr_metrics(
                        duration=ocr_duration,
                        text_length=len(text),
                        success=True
                    )
                else:
                    texts.append("[OCR Failed]")
                    record_ocr_metrics(
                        duration=ocr_duration,
                        text_length=0,
                        success=False,
                        error_type='5xx'
                    )

            extracted_text = "\n".join(texts)

            # Convert the original image to base64 for embedding in the response
            image_buffer = io.BytesIO()
            original_image.save(image_buffer, format="JPEG")
            image_buffer.seek(0)
            image_data = base64.b64encode(image_buffer.read()).decode('utf-8')

        elif request.is_json and 'text' in request.json:
            extracted_text = request.json["text"]
        else:
            return jsonify({"error": "No valid input"}), 400

        # Step 2: Send to drug extractor
        extract_start_time = time.time()
        extract_response = requests.post(EXTRACTOR_URL, json={"text": extracted_text})
        extract_duration = time.time() - extract_start_time
        
        if extract_response.status_code not in [200, 201]:
            record_extractor_metrics(
                duration=extract_duration,
                drug_count=0,
                success=False,
                error_type='5xx'
            )
            return jsonify({"error": "Drug extraction failed"}), 500

        drugs = extract_response.json().get("drugs_list", [])
        # add a check to ensure drugs is an array of strings
        if not isinstance(drugs, list) or not all(isinstance(drug, str) for drug in drugs):
            record_extractor_metrics(
                duration=extract_duration,
                drug_count=0,
                success=False,
                error_type='invalid_format'
            )
            return jsonify({"error": "Invalid drug list format"}), 500
            
        # Record extractor metrics
        record_extractor_metrics(
            duration=extract_duration,
            drug_count=len(drugs),
            success=True
        )

        # Step 3: Send drugs to drug interaction service
        interaction_start_time = time.time()
        interaction_response = requests.post(INTERACTION_URL, json={"drugs": drugs})
        interaction_duration = time.time() - interaction_start_time
        
        if interaction_response.status_code == 200:
            interaction_result = interaction_response.json().get("answer", {}).get("content", "")
            # Count interaction pairs (assuming they're separated by newlines)
            interaction_pairs = len(interaction_result.split('\n'))
            record_interaction_metrics(
                duration=interaction_duration,
                interaction_count=interaction_pairs,
                success=True
            )
        else:
            interaction_result = "[Drug interaction analysis failed]"
            record_interaction_metrics(
                duration=interaction_duration,
                interaction_count=0,
                success=False,
                error_type='5xx'
            )

        return jsonify({
            "extracted_text": extracted_text,
            "drugs_list": drugs,
            "image_data": image_data,
            "predictions": predictions,
            "detection_result": json.dumps(detection_result),  # Serialize detection_result
            "interaction_result": interaction_result
        }), 200

    except Exception as e:
        # Record error metrics for any unhandled exceptions
        if 'detect_duration' in locals():
            record_detection_metrics(
                duration=detect_duration,
                object_count=0,
                success=False,
                error_type='exception'
            )
        if 'ocr_duration' in locals():
            record_ocr_metrics(
                duration=ocr_duration,
                text_length=0,
                success=False,
                error_type='exception'
            )
        if 'extract_duration' in locals():
            record_extractor_metrics(
                duration=extract_duration,
                drug_count=0,
                success=False,
                error_type='exception'
            )
        if 'interaction_duration' in locals():
            record_interaction_metrics(
                duration=interaction_duration,
                interaction_count=0,
                success=False,
                error_type='exception'
            )
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5000))
    
    app.run(host=host, port=port)
