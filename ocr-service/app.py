from flask import Flask, request, jsonify
from google.cloud import vision
import os
import json

app = Flask(__name__)

# Set Google Cloud Vision API credentials dynamically from environment variables
credentials = {
    "type": os.environ.get("TYPE"),
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY", "").replace("\\n", "\n"),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": os.environ.get("AUTH_URI"),
    "token_uri": os.environ.get("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
    "universe_domain": os.environ.get("UNIVERSE_DOMAIN"),
}

try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp_credentials.json"
    with open("/tmp/gcp_credentials.json", "w") as cred_file:
        json.dump(credentials, cred_file)
except Exception as e:
    raise RuntimeError(f"Failed to set up Google Cloud credentials: {e}")

# Initialize Google Cloud Vision client
try:
    client = vision.ImageAnnotatorClient()
except Exception as e:
    raise RuntimeError(f"Failed to initialize Google Cloud Vision client: {e}")

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
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5001))
    app.run(debug=True, host=host, port=port)
