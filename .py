from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.chains import RetrievalQA
from langchain_community.llms import OpenAI

# Load vector DB
vectorstore = FAISS.load_local("db", OpenAIEmbeddings())

# LLM
llm = OpenAI()

# RAG Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

query = "What did I spend last month?"
result = qa.run(query)

print(result)