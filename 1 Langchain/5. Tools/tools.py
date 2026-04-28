# 🔥 ALL-IN-ONE LANGCHAIN DEMO
# Covers: Tools + Tool Calling + Vector DB + RAG

# =========================
# 1. IMPORTS
# =========================
from langchain.tools import tool
from langchain_core.tools import StructuredTool
from langchain.agents import initialize_agent
from langgraph.prebuilt import create_react_agent
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
# from langchain_community.llms import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from pydantic import BaseModel

# =========================
# 2. CUSTOM TOOL (@tool)
# =========================
@tool
def add_expense(amount: float, category: str) -> str:
    """Add an expense to the system"""
    return f"✅ Added ₹{amount} for {category}"

# =========================
# 3. STRUCTURED TOOL (ADVANCED)
# =========================
class ExpenseInput(BaseModel):
    amount: float
    category: str

def structured_add_expense(data: ExpenseInput):
    return f"📊 Structured Entry: ₹{data.amount} for {data.category}"

structured_tool = StructuredTool.from_function(
    func=structured_add_expense,
    name="StructuredExpenseTool",
    description="Add structured expense"
)

# =========================
# 4. VECTOR DATABASE (FAISS)
# =========================
documents = [
    "Spent 500 on food",
    "Spent 1000 on shopping",
    "Spent 200 on travel",
]

embeddings = OpenAIEmbeddings()
vector_db = FAISS.from_texts(documents, embeddings)

# =========================
# 5. RAG SETUP (RetrievalQA)
# =========================
retriever = vector_db.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=retriever
)

# =========================
# 6. TOOL FOR RAG
# =========================
@tool
def query_expenses(question: str) -> str:
    """Query past expenses using RAG"""
    return qa_chain.run(question)

# =========================
# 7. TOOLKIT (COLLECTION)
# =========================
tools = [add_expense, structured_tool, query_expenses]
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# =========================
# 8. AGENT (TOOL CALLING)
# =========================
agent = AgentExecutor(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# =========================
# 9. RUN EXAMPLES
# =========================

# Tool calling example
print(agent.run("Add 300 for groceries"))

# Structured tool usage
print(agent.run("Add structured expense of 700 for travel"))

# RAG example
print(agent.run("What did I spend on food?"))