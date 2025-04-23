from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.embeddings.openai import OpenAIEmbedding


def initialize_models(llm_model="gpt-4o-mini"):
    llm = OpenAI(model=llm_model, temperature=0)
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.llm = llm
    Settings.embed_model = embed_model
    return llm, embed_model


def get_answer(query_engine, messages):
    response = query_engine.query(messages)
    return response.response, response.metadata


def structured_rag_model(user_prompt, vector_db, output_structure):
    llm, _ = initialize_models()
    sllm = llm.as_structured_llm(output_cls=output_structure)
    query_engine = vector_db.as_query_engine(llm=sllm)
    user_msg = ChatMessage(role="user", content=user_prompt)
    answer, meta_data = get_answer(query_engine, user_msg)
    answer = answer.to_dict()
    return answer
