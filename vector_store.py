from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os


def create_vector_store(chunks, path):
    if not chunks:
        raise ValueError("No chunks provided to create vector store.")

    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(path)
    print(f"Vector store saved to: {path}")
