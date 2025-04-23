from chromadb import HttpClient
from chromadb.config import Settings as ChromaSettings
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

def get_chroma_index(collection_name) -> VectorStoreIndex:
    chroma_settings = ChromaSettings(
        chroma_api_impl="chromadb.api.fastapi.FastAPI"
    )
    client = HttpClient(
        host="localhost",
        port=8000,
        settings=chroma_settings,
    )
    collection = client.get_or_create_collection(name=collection_name)
    vector_store = ChromaVectorStore(
        chroma_collection=collection
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
    )
    return index
