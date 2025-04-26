# Pharm-Bot: Drug Interaction Service

Drug Interaction Service is a FastAPI-based service designed to process drug-related data, embed it into a vector database, and perform Retrieval-Augmented Generation (RAG) queries to identify potential drug interactions. It leverages OpenAI's language models and Pinecone for vector storage.

## Features

- **Process ZIP Files**: Extract and process JSON files containing drug-related data from uploaded ZIP files.
- **Vector Embedding**: Embed processed data into a Pinecone vector database for efficient retrieval.
- **RAG Queries**: Perform RAG queries to identify clinically significant drug interactions.
- **REST API**: Expose endpoints for embedding data and querying interactions.

## Requirements

- Docker
- Docker Compose (optional)

## Installation and Running with Docker

1. Build the Docker image:

   ```bash
   docker build -t pharm-bot .
   ```

2. Run the container:

   ```bash
   docker run -p 8000:8000 --env OPENAI_API_KEY=your_api_key pharm-bot
   ```

3. Access the application at `http://localhost:8000`.

## API Endpoints

### 1. `/chunk_embed_and_store/` (POST)

- **Description**: Upload a ZIP file containing JSON data to process and store in the vector database.
- **Request**:
  - `uploaded_file`: A ZIP file containing JSON files.
- **Response**:
  - Success: `{"status": "success", "message": "Data embedded and stored in vector DB."}`
  - Error: `{"status": "error", "message": "No valid entries found in ZIP."}`

### 2. `/rag/` (POST)

- **Description**: Perform a RAG query to identify drug interactions.
- **Request**:
  ```json
  {
    "query": "Any interaction between panadol and profinal",
    "top_k": 3
  }
  ```
- **Response**:
  ```json
  {
    "answer": "No interaction",
    "retrieved_documents": ["Document 1 content", "Document 2 content"]
  }
  ```

## Running Tests

1. Install `pytest`:

   ```bash
   pip install pytest pytest-mock
   ```

2. Run tests:
   ```bash
   pytest src/tests
   ```

## Project Structure

```
pharm-bot/
├── src/
│   ├── app.py                # Main FastAPI application
│   ├── services/             # Business logic for embedding and querying
│   ├── utils/                # Utility functions (e.g., ZIP processing)
│   ├── prompts/              # Prompt templates for RAG queries
│   ├── models/               # Pydantic models for request validation
│   └── tests/                # Unit tests
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
└── README.md                 # Project documentation
```
