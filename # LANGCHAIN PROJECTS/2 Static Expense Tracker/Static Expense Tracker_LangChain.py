from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
# from langchain.chains import RetrievalQA

from google import genai
from datetime import datetime

# -----------------------------
# 1. Gemini Setup
# -----------------------------
client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

# -----------------------------
# 2. Custom Gemini Embeddings
# -----------------------------
class GeminiEmbeddings(Embeddings):
    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=[text]
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings

    def embed_query(self, text):
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=[text]
        )
        return response.embeddings[0].values

embeddings = GeminiEmbeddings()

# -----------------------------
# 3. Fake LLM Wrapper
# -----------------------------
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text

# -----------------------------
# 4. Initialize Vector DB
# -----------------------------
vectorstore = None

# -----------------------------
# 5. Add Expense
# -----------------------------
def add_expense(user_input):
    global vectorstore

    today = datetime.now().strftime("%Y-%m-%d")
    text = f"{user_input} on {today}"

    doc = Document(page_content=text)

    if vectorstore is None:
        vectorstore = FAISS.from_documents([doc], embeddings)
    else:
        vectorstore.add_documents([doc])

    print("✅ Added:", text)

# -----------------------------
# 6. Ask Query
# -----------------------------
def ask_query(query):
    global vectorstore

    if vectorstore is None:
        print("⚠️ No data available")
        return

    retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

    docs = retriever.get_relevant_documents(query)

    context = "\n".join([doc.page_content for doc in docs])

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are an expense assistant.

        Context:
        {context}

        Question:
        {question}

        Calculate totals properly and give a clear answer.
        """
    )

    final_prompt = prompt_template.format(context=context, question=query)

    answer = ask_gemini(final_prompt)

    print("\n🔍 Retrieved Data:")
    for d in docs:
        print("-", d.page_content)

    print("\n🤖 Answer:\n", answer)

# -----------------------------
# 7. MAIN LOOP
# -----------------------------
print("\n💸 LangChain Expense Tracker Started")

while True:
    cmd = input("\nEnter command (add/ask/exit): ").lower()

    if cmd == "add":
        text = input("Enter expense: ")
        add_expense(text)

    elif cmd == "ask":
        query = input("Ask your question: ")
        ask_query(query)

    elif cmd == "exit":
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid command")