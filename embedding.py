from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #   credentials_profile_name="default", region_name="us-east-1"
    # )
    # embeddings = OllamaEmbeddings(model="llama3")
    embeddings = OllamaEmbeddings(model="text-embedding-3-small",
                                  openai_api_key=OPENAI_API_KEY)
    return embeddings
