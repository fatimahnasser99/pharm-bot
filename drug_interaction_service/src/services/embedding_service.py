import time
from typing import List
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os

INDEX_NAME = os.getenv("INDEX_NAME", "default-index-name")

def embed_and_store(chunks: List[Document]):
    embeddings = OpenAIEmbeddings()
    pinecone = Pinecone()

    if INDEX_NAME not in [idx["name"] for idx in pinecone.list_indexes()]:
        pinecone.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        while not pinecone.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(1)

    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        vectorstore.add_documents(chunks[i:i + batch_size])

    return vectorstore
