import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from google import genai
from datetime import datetime

# -----------------------------
# 🌐 Page Config
# -----------------------------
st.set_page_config(page_title="AI Expense Tracker", page_icon="💸", layout="centered")

# -----------------------------
# 🎨 Custom CSS (UI Upgrade)
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1, h2, h3 {
    color: #22c55e;
}
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
.card {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 1. Gemini Setup
# -----------------------------
client = genai.Client(api_key="AIzaSyA34-lLu-xLIthDFwElzgARjoV38tlxBwc")

# -----------------------------
# 2. Custom Embeddings
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
# 3. LLM Function
# -----------------------------
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text

# -----------------------------
# 4. Session State
# -----------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# -----------------------------
# 5. Title
# -----------------------------
st.title("💸 AI Expense Tracker")
st.caption("Track expenses using AI + LangChain + Gemini")

# -----------------------------
# 6. Add Expense
# -----------------------------
st.subheader("➕ Add Expense")

expense_input = st.text_input("Enter expense", placeholder="Spent 200 on food")

if st.button("Add Expense"):
    if expense_input:
        today = datetime.now().strftime("%Y-%m-%d")
        text = f"{expense_input} on {today}"

        doc = Document(page_content=text)

        if st.session_state.vectorstore is None:
            st.session_state.vectorstore = FAISS.from_documents([doc], embeddings)
        else:
            st.session_state.vectorstore.add_documents([doc])

        st.success(f"✅ Added: {text}")
    else:
        st.warning("⚠️ Please enter expense")

# -----------------------------
# 7. Ask Question
# -----------------------------
st.subheader("❓ Ask Question")

query = st.text_input("Ask your expenses", placeholder="How much did I spend on food?")

if st.button("Get Answer"):
    if st.session_state.vectorstore is None:
        st.warning("⚠️ No expenses added yet")
    elif query:
        try:
            retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5})
            docs = retriever.invoke(query)

            if not docs:
                st.warning("⚠️ No relevant data found")
                st.stop()

            context = "\n".join([doc.page_content for doc in docs])

            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""
                    You are a smart expense assistant.

                    Context:
                    {context}

                    Question:
                    {question}

                    Instructions:
                    - Calculate totals accurately
                    - Group similar expenses
                    - Give a clear final answer
                    """
            )

            final_prompt = prompt_template.format(context=context, question=query)

            answer = ask_gemini(final_prompt)

            # -----------------------------
            # UI Output
            # -----------------------------
            st.subheader("🔍 Retrieved Expenses")

            for d in docs:
                st.markdown(f'<div class="card">📌 {d.page_content}</div>', unsafe_allow_html=True)

            st.subheader("🤖 AI Answer")
            st.success(answer)

        except Exception as e:
            st.error(f"Error: {str(e)}")

    else:
        st.warning("⚠️ Please enter a question")







# class FAISS:
#     @classmethod
#     def from_documents(cls, documents, embedding):
#         texts = [doc.page_content for doc in documents]

#         vectors = embedding.embed_documents(texts)

#         return FAISS(vectors, documents)