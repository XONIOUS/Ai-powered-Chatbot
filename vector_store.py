# New import paths (langchain v0.2+)
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_vector_store(chunks, path):
    if not chunks:
        raise ValueError("No chunks provided to create vector store.")
    
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")  # Explicitly pull from env
    )
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(path)
    print(f"Vector store saved to: {path}")
