## Project Description

Pharm-bot is an AI-powered tool designed to help users identify interactions between drugs. It provides detailed descriptions and potential interactions to ensure safe and effective medication management. The project leverages Python and machine learning to analyze drug data and predict interactions.

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

| Service                      | Function                                     |
| ---------------------------- | -------------------------------------------- |
| `ui`                         | Web interface for image upload or text input |
| `gateway`                    | Orchestrates the full pipeline               |
| `medicine-detection-service` | Runs object detection (e.g., YOLO)           |
| `ocr-service`                | Performs OCR on cropped image regions        |
| `drug-extractor-service`     | Extracts medicine names from text            |

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
kubectl port-forward svc/ui 5004:5004 -n pharma-bot
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

## 📌 Notes

- All processing is done **in-memory** — no temporary files or shared volumes are used.
- Multiple object detections are supported: each region is cropped, passed to OCR, and combined before drug name extraction.

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

---

## 📬 Contact

For questions or contributions, open an issue or reach out to `@your-username`.
