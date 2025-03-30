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


def structured_model(user_prompt, output_structure):
    llm, _ = initialize_models()
    sllm = llm.as_structured_llm(output_cls=output_structure)

    user_msg = ChatMessage(role="user", content=user_prompt)

    response = sllm.chat([user_msg])
    return response.raw