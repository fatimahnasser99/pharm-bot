from flask import Flask, request, jsonify
from google.cloud import vision
import io
import os

app = Flask(__name__)

# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

@app.route("/extracted_text", methods=["POST"])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Read file content directly into memory
        content = file.read()
        image = vision.Image(content=content)

        # Call Google Cloud Vision API
        response = client.text_detection(image=image)

        # Handle potential API errors
        if response.error.message:
            return jsonify({"error": response.error.message}), 500

        # Extract text or fallback message
        text = response.full_text_annotation.text if response.full_text_annotation else "No text found"
        return jsonify({"extracted_text": text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5001))
    app.run(debug=True, host=host, port=port)
