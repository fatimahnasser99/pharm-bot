import io
import os
from PIL import Image
from flask import Flask, request, jsonify
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO("src/model/yolo11.pt")

@app.route('/detect', methods=['POST'])
def detect_medicine():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Get model results
        image = Image.open(io.BytesIO(file.read())).convert("RGB")

        # Run YOLO model on the image
        results = model(image)

        # Extract relevant data from results
        predictions = []
        for result in results:
            for box in result.boxes:
                xywh = box.xywh[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                predictions.append({
                    "x": float(xywh[0]),
                    "y": float(xywh[1]),
                    "width": float(xywh[2]),
                    "height": float(xywh[3]),
                    "confidence": float(conf),
                    "class_name": "Medicine"
                })

        # Return the predictions as JSON
        return jsonify({"predictions": predictions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5001))
    
    app.run(debug=True, host=host, port=port)