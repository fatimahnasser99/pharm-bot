from flask import Flask, request, jsonify
import requests
import io
from PIL import Image

app = Flask(__name__)

DETECTION_URL = "http://medicine-detection-service:5001/detect"
OCR_URL = "http://ocr-service:5001/extracted_text"
EXTRACTOR_URL = "http://drug-extractor-service:5000/extract"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        extracted_text = ""

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
            # print the predictions for debugging
            print(predictions)
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

        elif request.is_json and 'text' in request.json:
            extracted_text = request.json["text"]
        else:
            return jsonify({"error": "No valid input"}), 400

        # Step 2: Send to drug extractor
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
