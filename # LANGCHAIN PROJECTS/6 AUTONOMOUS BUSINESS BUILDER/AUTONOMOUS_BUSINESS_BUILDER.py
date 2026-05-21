"""
UPDATED AUTONOMOUS BUSINESS BUILDER
USING GOOGLE GEMINI + LANGGRAPH

TOPICS COVERED:
✔ LangGraph
✔ Stateful Graphs
✔ Multi-Agent Systems
✔ Tool Calling
✔ Memory
✔ Persistence
✔ Conditional Edges
✔ Streaming
✔ Human-in-the-loop
✔ Supervisor Architecture
✔ Async Execution
✔ Checkpoints
✔ Durable Execution
✔ ReAct Pattern
✔ Cyclic Graphs
✔ LangSmith Observability

INSTALL:
pip install langgraph langchain langsmith google-genai

ENV:
GOOGLE_API_KEY=your_key
LANGCHAIN_API_KEY=your_langsmith_key
"""

# =========================================================
# IMPORTS
# =========================================================

import os
import uuid
import asyncio
import operator

from typing import TypedDict, Annotated, List, Dict, Any
from dotenv import load_dotenv
from google import genai

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
load_dotenv()
# =========================================================
# LANGSMITH CONFIGURATION
# =========================================================

"""
Tracing & Observability
"""

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "AutonomousBusinessBuilder"

# =========================================================
# GEMINI CLIENT
# =========================================================

"""
Gemini LLM Initialization
"""

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================================================
# GEMINI HELPER FUNCTION
# =========================================================

"""
All LLM Calls Go Through Here
"""

def ask_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# =========================================================
# STATE MANAGEMENT
# =========================================================

"""
Stateful Graph
Reducers
Persistent Conversations
"""

class AgentState(TypedDict):

    messages: Annotated[list, add_messages]

    business_idea: str

    market_research: str

    website_code: str

    marketing_strategy: str

    financial_report: str

    approved: bool

    next_agent: str

    errors: Annotated[List[str], operator.add]

    memory: Dict[str, Any]

    thread_id: str

# =========================================================
# TOOLS
# =========================================================

"""
Tool Calling
ReAct Architecture
"""

@tool
def web_search(query: str):

    """
    Web search tool
    """

    print(f"\n🌐 SEARCHING: {query}")

    result = ask_gemini(
        f"""
        Perform market research for:
        {query}

        Give:
        - Market size
        - Competitors
        - Risks
        - Opportunities
        """
    )

    return result

# ---------------------------------------------------------

@tool
def generate_website(prompt: str):

    """
    AI Website Generator Tool
    """

    print("\n💻 GENERATING WEBSITE")

    result = ask_gemini(
        f"""
        Generate modern landing page HTML
        for startup idea:

        {prompt}

        Include:
        - Hero section
        - Features
        - Pricing
        - CTA
        """
    )

    return result

# ---------------------------------------------------------

@tool
def financial_analysis(data: str):

    """
    Finance Analysis Tool
    """

    print("\n💰 ANALYZING FINANCIALS")

    result = ask_gemini(
        f"""
        Create financial analysis for:

        {data}

        Include:
        - Startup cost
        - Monthly expenses
        - Revenue prediction
        - Profitability
        """
    )

    return result

# ---------------------------------------------------------

@tool
def marketing_campaign(data: str):

    """
    Marketing Tool
    """

    print("\n📢 GENERATING MARKETING CAMPAIGN")

    result = ask_gemini(
        f"""
        Create marketing strategy for:

        {data}

        Include:
        - Instagram strategy
        - SEO
        - Ads
        - Influencer marketing
        """
    )

    return result

# =========================================================
# TOOL NODE
# =========================================================

tools = [
    web_search,
    generate_website,
    financial_analysis,
    marketing_campaign
]

tool_node = ToolNode(tools)

# =========================================================
# AGENTS
# =========================================================

"""
Multi-Agent Architecture
Supervisor-Worker Pattern
"""

# =========================================================
# RESEARCH AGENT
# =========================================================

def research_agent(state: AgentState):

    print("\n🔍 RESEARCH AGENT RUNNING")

    idea = state["business_idea"]

    research = web_search.invoke(
        f"AI Startup Idea: {idea}"
    )

    return {
        "market_research": research,
        "messages": [
            AIMessage(
                content="Research completed successfully"
            )
        ]
    }

# =========================================================
# WEBSITE BUILDER AGENT
# =========================================================

def website_builder_agent(state: AgentState):

    print("\n💻 WEBSITE BUILDER AGENT RUNNING")

    website = generate_website.invoke(
        state["business_idea"]
    )

    return {
        "website_code": website,
        "messages": [
            AIMessage(
                content="Website generated successfully"
            )
        ]
    }

# =========================================================
# MARKETING AGENT
# =========================================================

def marketing_agent(state: AgentState):

    print("\n📢 MARKETING AGENT RUNNING")

    strategy = marketing_campaign.invoke(
        state["business_idea"]
    )

    return {
        "marketing_strategy": strategy,
        "messages": [
            AIMessage(
                content="Marketing strategy completed"
            )
        ]
    }

# =========================================================
# FINANCE AGENT
# =========================================================

def finance_agent(state: AgentState):

    print("\n💰 FINANCE AGENT RUNNING")

    report = financial_analysis.invoke(
        state["business_idea"]
    )

    return {
        "financial_report": report,
        "messages": [
            AIMessage(
                content="Financial report completed"
            )
        ]
    }

# =========================================================
# HUMAN APPROVAL NODE
# =========================================================

"""
Human-in-the-loop
Interrupts & Approvals
"""

def human_approval(state: AgentState):

    print("\n🛑 HUMAN APPROVAL REQUIRED")

    print("\nBUSINESS IDEA:")
    print(state["business_idea"])

    approval = input(
        "\nApprove Workflow? (yes/no): "
    )

    if approval.lower() == "yes":

        return {
            "approved": True
        }

    return {
        "approved": False,
        "errors": ["Workflow rejected by human"]
    }

# =========================================================
# SUPERVISOR AGENT
# =========================================================

"""
Conditional Routing
Decision Making
"""

def supervisor_agent(state: AgentState):

    print("\n🧠 SUPERVISOR AGENT RUNNING")

    if not state["market_research"]:

        next_agent = "research"

    elif not state["website_code"]:

        next_agent = "website"

    elif not state["marketing_strategy"]:

        next_agent = "marketing"

    elif not state["financial_report"]:

        next_agent = "finance"

    else:

        next_agent = "end"

    return {
        "next_agent": next_agent
    }

# =========================================================
# ROUTER
# =========================================================

"""
Conditional Edges
"""

def router(state: AgentState):

    route = state["next_agent"]

    if route == "research":
        return "research"

    elif route == "website":
        return "website"

    elif route == "marketing":
        return "marketing"

    elif route == "finance":
        return "finance"

    return END

# =========================================================
# MEMORY SAVER
# =========================================================

"""
Persistence
Checkpoints
Time Travel
Durable Execution
"""

memory = MemorySaver()

# =========================================================
# GRAPH BUILDING
# =========================================================

"""
Graph Architecture
Linear + DAG + Cyclic Graphs
"""

builder = StateGraph(AgentState)

# ---------------------------------------------------------
# ADD NODES
# ---------------------------------------------------------

builder.add_node(
    "approval",
    human_approval
)

builder.add_node(
    "supervisor",
    supervisor_agent
)

builder.add_node(
    "research",
    research_agent
)

builder.add_node(
    "website",
    website_builder_agent
)

builder.add_node(
    "marketing",
    marketing_agent
)

builder.add_node(
    "finance",
    finance_agent
)

builder.add_node(
    "tools",
    tool_node
)

# ---------------------------------------------------------
# LINEAR FLOW
# ---------------------------------------------------------

builder.add_edge(
    START,
    "approval"
)

builder.add_edge(
    "approval",
    "supervisor"
)

# ---------------------------------------------------------
# CONDITIONAL DAG
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# CYCLIC GRAPH
# ---------------------------------------------------------

builder.add_edge(
    "research",
    "supervisor"
)

builder.add_edge(
    "website",
    "supervisor"
)

builder.add_edge(
    "marketing",
    "supervisor"
)

builder.add_edge(
    "finance",
    "supervisor"
)

# =========================================================
# COMPILE GRAPH
# =========================================================

graph = builder.compile(
    checkpointer=memory
)

# =========================================================
# THREADS & CONFIG
# =========================================================

"""
Threads
Persistent State
Conversation Continuity
"""

thread_id = str(uuid.uuid4())

config = RunnableConfig(
    configurable={
        "thread_id": thread_id
    }
)

# =========================================================
# STREAMING EXECUTION
# =========================================================

"""
Streaming
Async Graph Execution
"""

async def run_workflow():

    print("\n🚀 STARTING AUTONOMOUS BUSINESS BUILDER\n")

    initial_state = {

        "messages": [
            HumanMessage(
                content="Build AI SaaS startup"
            )
        ],

        "business_idea": "AI Website Builder SaaS",

        "market_research": "",

        "website_code": "",

        "marketing_strategy": "",

        "financial_report": "",

        "approved": False,

        "next_agent": "",

        "errors": [],

        "memory": {},

        "thread_id": thread_id
    }

    try:

        async for event in graph.astream(
            initial_state,
            config=config,
            stream_mode="values"
        ):

            print("\n========================")
            print("📌 STREAM EVENT")
            print("========================")

            for key, value in event.items():

                if key != "messages":

                    print(f"\n{key}:")
                    print(value)

            await asyncio.sleep(1)

    except Exception as e:

        print("\n❌ ERROR")
        print(str(e))

# =========================================================
# REPLAY EXECUTION
# =========================================================

"""
Time Travel & Replay
"""

def replay_execution():

    print("\n⏪ REPLAY EXECUTION")

    state = graph.get_state(config)

    print(state)

# =========================================================
# RECOVER WORKFLOW
# =========================================================

"""
Recover Interrupted Workflow
"""

def recover_workflow():

    print("\n🛠 RECOVERING WORKFLOW")

    state = graph.get_state(config)

    print(state)

# =========================================================
# OBSERVABILITY
# =========================================================

"""
LangSmith Monitoring
"""

def monitor_graph():

    print("""

    LANGSMITH FEATURES:

    ✔ Execution tracing
    ✔ Token monitoring
    ✔ Graph visualization
    ✔ Error tracking
    ✔ Agent debugging
    ✔ Performance analytics

    """)

# =========================================================
# LIMITATIONS
# =========================================================

def limitations():

    print("""

    LANGGRAPH CHALLENGES:

    - Expensive LLM calls
    - Long workflows
    - Multi-agent complexity
    - Hallucinations
    - Memory growth
    - Tool reliability
    - Scaling difficulties

    """)

# =========================================================
# FUTURE OF AGENTIC AI
# =========================================================

def future_of_ai():

    print("""

    FUTURE OF AI AGENTS:

    ✔ Autonomous companies
    ✔ AI employees
    ✔ Self-improving systems
    ✔ AI operating systems
    ✔ Autonomous SaaS builders
    ✔ Distributed AI economies

    """)

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    asyncio.run(
        run_workflow()
    )

    replay_execution()

    recover_workflow()

    monitor_graph()

    limitations()

    future_of_ai()
