import os
import uuid
import asyncio
import operator

from typing import TypedDict, Annotated, List, Dict, Any

from dotenv import load_dotenv
from google import genai

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

load_dotenv()

# =====================================================
# FASTAPI
# =====================================================

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")

from jinja2 import Environment, FileSystemLoader

templates = Jinja2Templates(
    env=Environment(
        loader=FileSystemLoader("templates")
    )
)

# =====================================================
# GEMINI
# =====================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# =====================================================
# STATE
# =====================================================

class AgentState(TypedDict):

    messages: Annotated[list, add_messages]

    business_idea: str

    market_research: str

    website_code: str

    marketing_strategy: str

    financial_report: str

    next_agent: str

    logs: Annotated[List[str], operator.add]

# =====================================================
# AGENTS
# =====================================================

def research_agent(state: AgentState):

    logs = ["🔍 Research Agent Running"]

    result = ask_gemini(
        f"""
        Market research for:
        {state['business_idea']}
        """
    )

    logs.append("✅ Research Completed")

    return {
        "market_research": result,
        "logs": logs
    }

# -----------------------------------------------------

def website_agent(state: AgentState):

    logs = ["💻 Website Agent Running"]

    result = ask_gemini(
        f"""
        Generate landing page HTML for:
        {state['business_idea']}
        """
    )

    logs.append("✅ Website Generated")

    return {
        "website_code": result,
        "logs": logs
    }

# -----------------------------------------------------

def marketing_agent(state: AgentState):

    logs = ["📢 Marketing Agent Running"]

    result = ask_gemini(
        f"""
        Create marketing strategy for:
        {state['business_idea']}
        """
    )

    logs.append("✅ Marketing Strategy Created")

    return {
        "marketing_strategy": result,
        "logs": logs
    }

# -----------------------------------------------------

def finance_agent(state: AgentState):

    logs = ["💰 Finance Agent Running"]

    result = ask_gemini(
        f"""
        Financial report for:
        {state['business_idea']}
        """
    )

    logs.append("✅ Financial Analysis Completed")

    return {
        "financial_report": result,
        "logs": logs
    }

# =====================================================
# SUPERVISOR
# =====================================================

def supervisor(state: AgentState):

    if not state["market_research"]:
        return {"next_agent": "research"}

    elif not state["website_code"]:
        return {"next_agent": "website"}

    elif not state["marketing_strategy"]:
        return {"next_agent": "marketing"}

    elif not state["financial_report"]:
        return {"next_agent": "finance"}

    return {"next_agent": "end"}

# =====================================================
# ROUTER
# =====================================================

def router(state: AgentState):

    if state["next_agent"] == "research":
        return "research"

    elif state["next_agent"] == "website":
        return "website"

    elif state["next_agent"] == "marketing":
        return "marketing"

    elif state["next_agent"] == "finance":
        return "finance"

    return END

# =====================================================
# GRAPH
# =====================================================

memory = MemorySaver()

builder = StateGraph(AgentState)

builder.add_node("supervisor", supervisor)
builder.add_node("research", research_agent)
builder.add_node("website", website_agent)
builder.add_node("marketing", marketing_agent)
builder.add_node("finance", finance_agent)

builder.add_edge(START, "supervisor")

builder.add_conditional_edges(
    "supervisor",
    router,
    {
        "research": "research",
        "website": "website",
        "marketing": "marketing",
        "finance": "finance",
        END: END
    }
)

builder.add_edge("research", "supervisor")
builder.add_edge("website", "supervisor")
builder.add_edge("marketing", "supervisor")
builder.add_edge("finance", "supervisor")

graph = builder.compile(
    checkpointer=memory
)

# =====================================================
# HOME PAGE
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        name="index.html",
        request=request
    )

# =====================================================
# RUN WORKFLOW
# =====================================================

@app.get("/run")

async def run_workflow():

    thread_id = str(uuid.uuid4())

    config = RunnableConfig(
        configurable={
            "thread_id": thread_id
        }
    )

    initial_state = {

        "messages": [
            HumanMessage(content="Start Business")
        ],

        "business_idea": "AI Website Builder SaaS",

        "market_research": "",

        "website_code": "",

        "marketing_strategy": "",

        "financial_report": "",

        "next_agent": "",

        "logs": []
    }

    final_state = None

    async for event in graph.astream(
        initial_state,
        config=config,
        stream_mode="values"
    ):

        final_state = event

    return {
        "research": final_state["market_research"],
        "website": final_state["website_code"],
        "marketing": final_state["marketing_strategy"],
        "finance": final_state["financial_report"],
        "logs": final_state["logs"]
    }