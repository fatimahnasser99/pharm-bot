from fastapi import FastAPI, UploadFile, File, HTTPException
from src.models.query_model import QueryModel
from src.services.embedding_service import embed_and_store
from src.services.query_service import perform_rag_query
from src.utils.zip_processor import process_zip_of_json

app = FastAPI()

# Endpoint to process and store
@app.post("/chunk_embed_and_store/")
async def embed_and_store_endpoint(uploaded_file: UploadFile = File(...)):
    chunks = process_zip_of_json(uploaded_file)
    if not chunks:
        return {"status": "error", "message": "No valid entries found in ZIP."}

    embed_and_store(chunks)
    return {"status": "success", "message": "Data embedded and stored in vector DB."}

# Stateless RAG query
@app.post("/rag/")
async def rag_query(query: QueryModel):
    return perform_rag_query(query)
