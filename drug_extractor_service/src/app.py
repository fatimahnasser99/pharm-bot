import os
from flask import Flask, request, jsonify
from services.drugs_extractor import extract_drugs_from_text

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    try:
        data = request.get_json()
        if "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400
        result = extract_drugs_from_text(data["text"])
        return jsonify({"drugs_list": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5000))
    
    app.run(debug=True, host=host, port=port)