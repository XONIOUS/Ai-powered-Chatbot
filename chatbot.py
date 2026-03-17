from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import HumanMessage
import os

def get_answer(query, index_path):
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
        allow_dangerous_deserialization=True  # Required in newer LangChain versions
    )

    docs = db.similarity_search(query, k=4)  # k=4 is explicit and tunable

    if not docs:
        return "No relevant content found in the document."

    context = "\n".join([doc.page_content for doc in docs])

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0  # Keeps answers factual and consistent
    )

    prompt = f"""You are an academic assistant.
Answer ONLY from the given context.
If the answer is not found in the context, say "Not in document".

Context:
{context}

Question:
{query}
"""

    # .predict() is deprecated — use .invoke() instead
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
