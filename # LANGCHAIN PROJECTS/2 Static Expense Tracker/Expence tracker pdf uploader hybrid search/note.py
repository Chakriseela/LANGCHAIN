'''
pip install langchain-text-splitters
pip uninstall langchain langchain-community -y
pip install langchain==0.1.16
pip install langchain-community==0.0.32
pip install langchain-openai
pip install langchain-text-splitters
pip install faiss-cpu
pip install rank-bm25
pip install pypdf




# Text Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Loaders
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

# Embeddings
from langchain_openai import OpenAIEmbeddings

# Vector Store
from langchain_community.vectorstores import FAISS

# Retrievers
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever





pip install trulens trulens-apps-langchain trulens-providers-openai openai langchain langchain_community langchain_openai rank_bm25 faiss_cpu






        # Hybrid Retrieval using EnsembleRetriever
        # faiss_ret = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5})
        # bm25 = BM25Retriever.from_documents(st.session_state.documents)

        # hybrid = EnsembleRetriever(
        #     retrievers=[bm25, faiss_ret],
        #     weights=[0.5, 0.5]
        # )

        # docs = hybrid.invoke(query)
        # docs = rerank(query, docs)[:5]

        # context = "\n".join([d.page_content for d in docs])


'''