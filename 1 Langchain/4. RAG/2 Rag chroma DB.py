# pip install -qU  langchain langchain-huggingface sentence_transformers
import os
from dotenv import load_dotenv
load_dotenv()

# !pip install -qU langchain-community pypdf
from langchain_community.document_loaders import PyPDFLoader

# Make sure you have uploaded the PDF to your Colab environment
file_path = r"D:\Downloads\Chakravarthi_Expense_Report.pdf"
loader = PyPDFLoader(file_path)
doc = loader.load()
print(doc)
print(doc[0].metadata)
print(doc[0].page_content)



# !pip install -qU langchain-text-splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1000,      
  chunk_overlap=200,    
)
all_splits = text_splitter.split_documents(doc)
print(all_splits)
print(f"Paper split into {len(all_splits)} sub-documents.")
print(f"Metadata: {all_splits[0].metadata}")


from langchain_huggingface import HuggingFaceEmbeddings

# Initialize free, local embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)


# pip install -qU langchain-chroma

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=r"D:\D drive\HCLTech\Project Training\LANGCHAIN\1 Langchain\4. RAG/chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
document_ids = vector_store.add_documents(documents=all_splits)
sample = vector_store.get(limit=1, include=["embeddings", "documents"])
print(f"Embedding dimensions: {len(sample['embeddings'][0])}")
print(sample)
print(document_ids[:3])



from langchain.chat_models import init_chat_model
# from google.colab import userdata

# !pip install -U langchain-google-genai
api_key = os.getenv('GEMINI_API_KEY')
model = init_chat_model(
   "google_genai:gemini-2.5-flash",
   api_key=api_key,
)

def retrieve_context(query: str, k: int = 2):
  retrieved_docs = vector_store.similarity_search(query, k=k)

  docs_content = ""
  for doc in retrieved_docs:
    docs_content += f"Source: {doc.metadata}\n"
    docs_content += f"Content: {doc.page_content}\n\n"

  return docs_content, retrieved_docs

def docu_chat(user_query):
    context, source_docs = retrieve_context(user_query, k=2)
    system_message = f"""You are a helpful chatbot.
                        Use only the following pieces of context to answer the 
                        question. Don't makeup any new information: {context} """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_query}
    ]
    response = model.invoke(messages)           
    return {
        "answer": response.content,
        "source_documents": source_docs,
        "context_used": context
    }
result = docu_chat( "Explain what is the use of decoders in transformers?")
print(result)
print(result["answer"])