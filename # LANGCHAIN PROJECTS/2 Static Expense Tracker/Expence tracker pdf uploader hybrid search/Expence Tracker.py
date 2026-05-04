import os
import re
import streamlit as st
from datetime import datetime
from google import genai

from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
# from langchain_community.retrievers import EnsembleRetriever
# from langchain.retrievers.ensemble import EnsembleRetriever
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
# from langchain_community import RetrievalQA
# from langchain.llms.base import LLM


# -----------------------------
# 🌐 Page Config
# -----------------------------
st.set_page_config(page_title="AI Expense Tracker", page_icon="💸")

# -----------------------------
# 🎨 UI Styling
# -----------------------------
st.markdown("""
<style>
.main { background-color: #0f172a; }
h1, h2, h3 { color: #22c55e; }
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.card {
    background-color: #1e293b;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🔹 Gemini Setup
# -----------------------------
client = genai.Client(api_key="AIzaSyBkk5y1pOE_UjOiLXzBDNDtZAitYdW1ml0")

# -----------------------------
# 🔹 Custom LLM (for RetrievalQA)
# -----------------------------
# class GeminiLLM(LLM):
#     def _call(self, prompt, stop=None):
#         response = client.models.generate_content(
#             model="gemini-3-flash-preview",
#             contents=prompt
#         )
#         return response.text

#     @property
#     def _llm_type(self):
#         return "gemini"

# -----------------------------
# 🔹 Embeddings
# -----------------------------
class GeminiEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [
            client.models.embed_content(
                model="gemini-embedding-001",
                contents=[text]
            ).embeddings[0].values
            for text in texts
        ]

    def embed_query(self, text):
        return client.models.embed_content(
            model="gemini-embedding-001",
            contents=[text]
        ).embeddings[0].values

embeddings = GeminiEmbeddings()

# -----------------------------
# 📂 DB Path
# -----------------------------
DB_PATH = r"C:\HCLTech\Project Training\# LANGCHAIN PROJECTS\2 Static Expense Tracker\Expence tracker pdf uploader hybrid search\faiss_db"

def load_db():
    if os.path.exists(DB_PATH):
        return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def save_db(vs):
    vs.save_local(DB_PATH)

# -----------------------------
# 🔹 Default URLs
# -----------------------------
default_urls = [
    "https://www.investopedia.com/budgeting-basics-5189752",
    "https://www.nerdwallet.com/article/finance/how-to-save-money"
]

# -----------------------------
# 🔹 Utils
# -----------------------------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)

def rerank(query, docs):
    scored = []
    for doc in docs:
        score = len(set(query.split()) & set(doc.page_content.split()))
        scored.append((score, doc))
    ranked = sorted(scored, key=lambda x: x[0], reverse=True)
    return [doc for score, doc in ranked]
# def rerank(query, docs):
#     return sorted(
#         docs,
#         key=lambda doc: len(set(query.lower().split()) & set(doc.page_content.lower().split())),
#         reverse=True
#     )


# -----------------------------
# 🌐 Web Loader with Fallback
# -----------------------------
def load_web_data(user_url=None):
    urls = []

    if user_url and user_url.strip() != "":
        st.info("Using user URL + default URLs")
        urls.append(user_url)
    else:
        st.info("Using default financial knowledge")

    urls.extend(default_urls)
    urls = list(set(urls))  # remove duplicates

    loader = WebBaseLoader(urls)
    docs = loader.load()

    return docs

# -----------------------------
# 🔹 Session State
# -----------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = load_db()

if "documents" not in st.session_state:
    st.session_state.documents = []

# -----------------------------
# 💸 Title
# -----------------------------
st.title("💸 AI Expense Tracker (Advanced RAG)")

# =========================================================
# 📄 PDF UPLOADER
# =========================================================
import os
import uuid

st.subheader("📄 Upload PDF")

pdf = st.file_uploader("Upload bank statement", type=["pdf"])

# 📁 Base directory
BASE_DIR = r"C:\HCLTech\Project Training\# LANGCHAIN PROJECTS\2 Static Expense Tracker\Expence tracker pdf uploader hybrid search"

PDF_DIR = os.path.join(BASE_DIR, "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

if pdf:
    # ✅ Unique file name (avoid overwrite)
    file_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(PDF_DIR, file_name)

    # ✅ Save PDF to fixed directory
    with open(file_path, "wb") as f:
        f.write(pdf.read())

    # ✅ Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # ✅ Clean text
    docs = [Document(page_content=clean_text(d.page_content)) for d in docs]
    print(docs)

    # ✅ Chunking
    chunks = chunk_docs(docs)
    print(chunks)

    # ✅ Store in session
    st.session_state.documents.extend(chunks)

    # ✅ Vector DB update
    if st.session_state.vectorstore is None:
        st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
    else:
        st.session_state.vectorstore.add_documents(chunks)

    # ✅ Save DB
    save_db(st.session_state.vectorstore)

    st.success(f"✅ PDF data added! Saved as {file_name}")

# =========================================================
# 🌐 WEBSITE LOADER
# =========================================================
st.subheader("🌐 Load Web Knowledge")

user_url = st.text_input("Enter URL (optional)")

if st.button("Load Web Data"):
    try:
        docs = load_web_data(user_url)

        docs = [Document(page_content=clean_text(d.page_content)) for d in docs]
        chunks = chunk_docs(docs)

        st.session_state.documents.extend(chunks)

        if st.session_state.vectorstore is None:
            st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
        else:
            st.session_state.vectorstore.add_documents(chunks)

        save_db(st.session_state.vectorstore)

        st.success("✅ Web data added!")

    except Exception as e:
        st.error(str(e))

# =========================================================
# ➕ ADD EXPENSE
# =========================================================
st.subheader("➕ Add Expense")

expense = st.text_input("Enter expense")

if st.button("Add Expense"):
    if expense:
        text = clean_text(f"{expense} on {datetime.now().date()}")
        doc = Document(page_content=text)

        st.session_state.documents.append(doc)

        chunks = chunk_docs([doc])

        if st.session_state.vectorstore is None:
            st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
        else:
            st.session_state.vectorstore.add_documents(chunks)

        save_db(st.session_state.vectorstore)

        st.success("Expense added!")

# =========================================================
#                   ❓ ASK QUESTION
# =========================================================
st.subheader("❓ Ask Questions")

query = st.text_input("Ask your question")

if st.button("Get Answer"):

    if not st.session_state.vectorstore:
        st.warning("No data available")

    elif query:
        
        # -----------------------------
        # 🔥 MANUAL HYBRID RETRIEVAL
        # -----------------------------

        # 1️⃣ FAISS Results (Semantic Search)
        faiss_ret = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 20})
        faiss_docs = faiss_ret.invoke(query)

        # 2️⃣ BM25 Results (Keyword Search)
        bm25 = BM25Retriever.from_documents(st.session_state.documents)
        bm25.k = 5
        bm25_docs = bm25.invoke(query)

        # 3️⃣ Combine Results
        all_docs = faiss_docs + bm25_docs

        # 4️⃣ Remove Duplicates
        unique_docs = []
        seen = set()

        for doc in all_docs:
            if doc.page_content not in seen:
                unique_docs.append(doc)
                seen.add(doc.page_content)

        # 5️⃣ Re-rank (your custom logic)
        docs = rerank(query, unique_docs)[:15]

        # 6️⃣ Final Context
        context = "\n".join([d.page_content for d in docs])

        # Prompt
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are an expert financial assistant.

Rules:
- Use ONLY context
- Do NOT guess
- If missing → say "No data found"

Context:
{context}

Question:
{question}

Steps:
1. Extract expenses
2. Group them
3. Calculate totals
4. Tell how to manage money related to the expences

Answer:
- Total:
- Breakdown:
- Explanation in detail step by steps:
"""
        )

        final_prompt = prompt.format(context=context, question=query)

        # Gemini Answer
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=final_prompt
        )

        answer = response.text

        # UI Output
        st.subheader("🔍 Retrieved Data")
        for d in docs:
            st.markdown(f'<div class="card">📌 {d.page_content}</div>', unsafe_allow_html=True)

        st.subheader("🤖 Gemini Answer")
        st.success(answer)

        # st.subheader("⚡ RetrievalQA Answer")
        # st.info(answer)






