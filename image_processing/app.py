import io
import os
from PIL import Image
from flask import Flask, request, jsonify
from ultralytics import YOLO
import uuid
import json

app = Flask(__name__)

model = YOLO("./model/yolo11.pt")

def convert_yolo_to_json(results, class_names=None):
    output = {"predictions": []}
    
    for result in results:
        boxes = result.boxes
        for i in range(len(boxes)):
            box = boxes[i]
            
            # Get box coordinates in xywh format
            xywh = box.xywh[0].cpu().numpy()
            x, y, w, h = xywh
            
            # Get confidence and class
            conf = box.conf[0].cpu().numpy()
            cls_id = int(box.cls[0].cpu().numpy())
            cls_name = class_names[cls_id] if class_names else str(cls_id)
            
            # Generate a random detection ID
            detection_id = str(uuid.uuid4())
            
            # Create prediction dictionary
            prediction = {
                "x": float(x),
                "y": float(y),
                "width": float(w),
                "height": float(h),
                "confidence": float(conf),
                "class": cls_name,
                "class_id": cls_id,
                "detection_id": detection_id
            }
            
            output["predictions"].append(prediction)
    
    return output


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    print(file)
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        class_names = ['Medicine']

        # Get model results
        image = Image.open(io.BytesIO(file.read())).convert("RGB")

        # Run YOLO model on the image
        results = model(image)

        # Convert to desired JSON format
        json_output = convert_yolo_to_json(results, class_names)

        # Save the result image in the static folder
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')
        image.save(result_path)

        # Print or save the JSON
        print(json.dumps(json_output, indent=2))

        return json.dumps(json_output, indent=2), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)