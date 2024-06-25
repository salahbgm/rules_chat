import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI
import os
from scripts.embedding import get_embedding_function

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "../data/VectorStores/chroma"

PROMPT_TEMPLATE = """
You are an assistant helping a user with a question about board games. There will be a context followed by a question.
You need to answer the question based on the context provided.

If the question does not write the name of the board game, ask the user to provide the name of the board game and you
cannot answer the question without the name of the board game, even if context is provided, do not answer the question.

If you don't know the answer, don't make up an answer. Just answer that you don't know the answer.



Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    # model = Ollama(model="llama3")
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = {
        "response": response_text,
        "sources": sources,
    }
    print(formatted_response)
    print(formatted_response['response'].content)
    print(formatted_response['sources'])
    return formatted_response


if __name__ == "__main__":
    query_rag("Comment commence une partie de la Bonne paye ?")
