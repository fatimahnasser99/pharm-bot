## Project Description

Pharm-bot is an AI-powered tool designed to help users identify interactions between drugs. It provides detailed descriptions and potential interactions to ensure safe and effective medication management. The project leverages Python and machine learning to analyze drug data and predict interactions.

## 📂 Dataset and Model Weights

The dataset fetched from DrugBank in XML format, the processed dataset in JSON format, the YOLO model weights, and a presentation (PPT) are stored on the following Google Drive folder:

> [Google Drive Folder](https://drive.google.com/drive/folders/1AsXPMnnyPdXYRViMd48ZNXTD_oK1KZ2c)

The YOLO model weights were fetched from this Google Drive folder during the **Medicine Detection Service IEP** build process.

## Features

- Identify drug interactions
- Provide detailed descriptions of drugs
- User-friendly interface for easy navigation

## Usage

1. Input the names of the drugs you are taking.
2. The system will analyze the inputs and provide information on potential interactions.
3. Review the detailed descriptions and interaction warnings.

# 💊 PharmaBot Inference Pipeline

PharmaBot is a modular end-to-end pipeline that detects and extracts **medicine names** from images or text. It uses multiple microservices, each containerized with Docker, and connected using Docker Compose.

---

## 🧠 Microservices Overview

| Service                      | Function                                     | Documentation Link                                                          |
| ---------------------------- | -------------------------------------------- | --------------------------------------------------------------------------- |
| `ui`                         | Web interface for image upload or text input | [UI Service README](./ui/README.md)                                         |
| `gateway`                    | Orchestrates the full pipeline               | [Gateway Service README](./gateway/README.md)                               |
| `medicine-detection-service` | Runs object detection (e.g., YOLO)           | [Medicine Detection Service README](./medicine_detection_service/README.md) |
| `ocr-service`                | Performs OCR on cropped image regions        | [OCR Service README](./ocr-service/README.md)                               |
| `drug-extractor-service`     | Extracts medicine names from text            | [Drug Extractor Service README](./drug_extractor_service/README.md)         |
| `drug-interaction-service`   | Analyzes drug interactions using RAG queries | [Drug Interaction Service README](./drug_interaction_service/README.md)     |

---

## ✨ How to Run the App

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pharmabot-inference.git
cd pharmabot-inference
```

### 2. Build and start the containers

## Option 1: Using Docker-compose:

```bash
docker-compose up --build
```

## Option 2: Using Kubernetes:

```bash
kubectl apply -f kubernetes.yaml
```

followed by:

```bash
kubectl port-forward svc/ui 5004:80 -n pharma-bot
```

In case you changed one image no need to build the whole thing again
example:

```bash
docker-compose build gateway
docker-compose up
```

This command builds and launches all services using Docker Compose.

---

## 🌐 Access the Web Interface

After all services are up, open your browser and visit:

> http://localhost:5004/

- 📷 Upload an image containing text
- 💬 Or paste raw text into the form
- ✅ Extracted text and drug names will be displayed below the form

---

## ⚙️ Services and Endpoints

| Service              | Endpoint                 | Description                         |
| -------------------- | ------------------------ | ----------------------------------- |
| **UI**               | `/`                      | Web form for input                  |
| **Gateway API**      | `/analyze` (POST)        | Central orchestrator                |
| **Object Detection** | `/detect` (POST)         | Returns bounding boxes of medicines |
| **OCR**              | `/extracted_text` (POST) | Extracts text from cropped images   |
| **Drug Extractor**   | `/extract` (POST)        | Returns detected drug names         |

---

## ✅ Requirements

- Docker
- Docker Compose

> No Python or other setup is required on your host machine — everything runs in containers.

---

## 🧪 Optional: Test with `curl`

```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@/path/to/your/image.jpg"
```

Or for raw text:

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Panadol 500mg tablets"}'
```
