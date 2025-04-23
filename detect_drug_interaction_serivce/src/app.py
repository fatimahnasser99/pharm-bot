import os
from flask import Flask, request, jsonify
from detect_drug_interaction_serivce.src.services.drugs_interaction_detection import detect_drugs_interaction_from_text

app = Flask(__name__)

@app.route("/interactions/drug", methods=["POST"])
def extract():
    try:
        data = request.get_json()
        if "drugs_couple" not in data:
            return jsonify({"error": "Missing 'drugs_couple' field"}), 400
        if len(data["drugs_couple"])!=2:
            return jsonify({"error": "drugs_couple should be a list of 2 drugs"}), 400
        input_text = data["drugs_couple"].join(" and ")
        result = detect_drugs_interaction_from_text(input_text)
        return jsonify({"drugs_list": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5000))
    
    app.run(debug=True, host=host, port=port)