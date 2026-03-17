import warnings
warnings.filterwarnings("ignore")

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os


def get_answer(query, index_path):
    """Answer questions strictly from the uploaded PDF."""
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index not found at: {index_path}")

    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    db = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(query, k=4)

    if not docs:
        return "No relevant content found in the document."

    context = "\n".join([doc.page_content for doc in docs])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )

    prompt = f"""You are an academic assistant.
Answer ONLY from the given context.
If the answer is not found in the context, say "Not in document".

Context:
{context}

Question:
{query}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content


def get_general_answer(query):
    """Answer questions without a PDF using general GPT knowledge."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )

    messages = [
        SystemMessage(content="You are a helpful and knowledgeable assistant. Answer the user's questions clearly, concisely and accurately."),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)
    return response.content
