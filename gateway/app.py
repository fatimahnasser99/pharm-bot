from flask import Flask, request, jsonify
import requests
import io
from PIL import Image
import base64
import json
import os


app = Flask(__name__)

DETECTION_URL = "http://medicine-detection-service:5001/detect"
OCR_URL = "http://ocr-service:5001/extracted_text"
EXTRACTOR_URL = "http://drug-extractor-service:5000/extract"
INTERACTION_URL = "http://drug-interaction-service:8000/rag"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        extracted_text = ""
        predictions = []
        image_data = None
        detection_result = {}
        interaction_result = {}

        if 'file' in request.files:
            image_file = request.files['file']

            # Read original image in memory
            image_bytes = image_file.read()
            original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            # Step 1: Object detection
            detect_response = requests.post(DETECTION_URL, files={"file": io.BytesIO(image_bytes)})
            if detect_response.status_code != 200:
                return jsonify({"error": "Object detection failed"}), 500

            detection_result = detect_response.json()
            predictions = detection_result.get("predictions", [])

            if not predictions:
                return jsonify({"error": "No objects detected"}), 200

            texts = []
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
                ocr_response = requests.post(OCR_URL, files={"file": cropped_bytes})
                if ocr_response.status_code == 200:
                    text = ocr_response.json().get("extracted_text", "")
                    texts.append(text)
                else:
                    texts.append("[OCR Failed]")

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
        extract_response = requests.post(EXTRACTOR_URL, json={"text": extracted_text})
        if extract_response.status_code not in [200, 201]:
            return jsonify({"error": "Drug extraction failed"}), 500

        drugs = extract_response.json().get("drugs_list", [])
        # add a check to ensure drugs is an array of strings
        if not isinstance(drugs, list) or not all(isinstance(drug, str) for drug in drugs):
            return jsonify({"error": "Invalid drug list format"}), 500
        # Step 3: Send drugs to drug interaction service
        interaction_response = requests.post(INTERACTION_URL, json={"drugs": drugs})
        if interaction_response.status_code == 200:
            interaction_result = interaction_response.json().get("answer", {}).get("content", "")
        else:
            interaction_result = "[Drug interaction analysis failed]"

        return jsonify({
            "extracted_text": extracted_text,
            "drugs_list": drugs,
            "image_data": image_data,
            "predictions": predictions,
            "detection_result": json.dumps(detection_result),  # Serialize detection_result
            "interaction_result": interaction_result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5000))
    
    app.run(host=host, port=port)
