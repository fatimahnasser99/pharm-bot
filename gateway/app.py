from flask import Flask, request, jsonify
import requests
import os
import io

app = Flask(__name__)

# Config for service URLs (assume internal Docker hostnames via docker-compose)
DETECTION_URL = "http://medicine-detection-service:5001/detect"
OCR_URL = "http://ocr-service:5001/extracted_text"
EXTRACTOR_URL = "http://drug-extractor-service:5000/extract"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if 'file' in request.files:
            # 📦 Step 1: Send to Object Detection
            image_file = request.files['file']
            files = {'file': image_file.stream}

            detect_response = requests.post(DETECTION_URL, files=files)
            if detect_response.status_code != 200:
                return jsonify({"error": "Object detection failed"}), 500

            # 📸 Step 2: Read result image (saved by detection service)
            result_image_path = "/app/static/uploads/result.jpg"  # Must match detection service output
            with open(result_image_path, "rb") as img:
                ocr_response = requests.post(OCR_URL, files={"file": img})

            if ocr_response.status_code != 200:
                return jsonify({"error": "OCR failed"}), 500

            extracted_text = ocr_response.json().get("extracted_text", "")

        elif 'text' in request.json:
            # Direct text input from UI
            extracted_text = request.json["text"]

        else:
            return jsonify({"error": "No valid input"}), 400

        # 💊 Step 3: Send to Drug Extractor
        extract_response = requests.post(EXTRACTOR_URL, json={"text": extracted_text})

        if extract_response.status_code not in [200, 201]:
            return jsonify({"error": "Drug extraction failed"}), 500

        drugs = extract_response.json().get("drugs_list", [])

        return jsonify({
            "extracted_text": extracted_text,
            "drugs_list": drugs
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
