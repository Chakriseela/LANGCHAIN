'''


# =========================================================
# 📄 PDF UPLOADER (FIXED - NO DUPLICATES)
# =========================================================
import os
import uuid
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_core.documents import Document

st.subheader("📄 Upload PDF")

pdf = st.file_uploader("Upload bank statement", type=["pdf"])

# 📁 Base directory
BASE_DIR = r"C:\HCLTech\Project Training\# LANGCHAIN PROJECTS\2 Static Expense Tracker\Expence tracker pdf uploader hybrid search"
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

# ✅ Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = set()

if pdf:
    # 🔑 Unique identifier for file (based on content)
    file_id = pdf.name + str(pdf.size)

    # ✅ Process only if NOT already uploaded
    if file_id not in st.session_state.uploaded_files:

        # Save with original name (simple)
        file_path = os.path.join(PDF_DIR, pdf.name)

        with open(file_path, "wb") as f:
            f.write(pdf.read())

        # Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Clean text
        docs = [Document(page_content=clean_text(d.page_content)) for d in docs]

        # Chunking
        chunks = chunk_docs(docs)

        # Store in session
        st.session_state.documents.extend(chunks)

        # Vector DB update
        if st.session_state.vectorstore is None:
            st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
        else:
            st.session_state.vectorstore.add_documents(chunks)

        # Save DB
        save_db(st.session_state.vectorstore)

        # ✅ Mark as uploaded
        st.session_state.uploaded_files.add(file_id)

        st.success(f"✅ PDF '{pdf.name}' processed and added!")

    else:
        st.info("📌 This PDF is already processed. Skipping...")


'''