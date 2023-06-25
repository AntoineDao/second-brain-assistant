import os
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


llm_client = OpenAI(
    openai_api_key=OPENAI_API_KEY
)

embedding_client = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY,
)
