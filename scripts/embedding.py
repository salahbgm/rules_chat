from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL = os.getenv("LOCAL")


def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #   credentials_profile_name="default", region_name="us-east-1"
    # )

    if LOCAL is True:
        embeddings = OllamaEmbeddings(model="llama3")
    elif OPENAI_API_KEY is not None:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small",
                                      openai_api_key=OPENAI_API_KEY)
    else:
        raise ValueError("No valid embedding function found.")
    return embeddings
