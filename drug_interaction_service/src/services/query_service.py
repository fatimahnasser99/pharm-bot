from fastapi import HTTPException
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.prompts.rag_prompt import generate_rag_prompt
import os

INDEX_NAME = os.getenv("INDEX_NAME", "default-index-name")

def perform_rag_query(query):
    if not isinstance(query.drugs, list) or not all(isinstance(drug, str) for drug in query.drugs):
        raise HTTPException(status_code=400, detail="Input must be an array of strings.")

    formatted_query = " interaction with ".join(query.drugs)

    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    retrieved_docs = retriever.invoke(formatted_query)

    context = "\n".join([doc.page_content for doc in retrieved_docs])
    prompt = generate_rag_prompt(context, formatted_query)

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    answer = llm.invoke(prompt)

    return {
        "answer": answer,
        "retrieved_documents": [doc.page_content for doc in retrieved_docs]
    }
