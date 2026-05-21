from langgraph.graph import StateGraph
from typing import TypedDict
from google import genai
import os
from dotenv import load_dotenv

# 🔑 Load env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Correct client initialization
client = genai.Client(api_key=GOOGLE_API_KEY)

# 🧠 State
class State(TypedDict):
    input: str
    output: str

# 🤖 Gemini call function
def call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


# 🔵 Node 1: LLM
def llm_node(state: State):
    result = call_gemini(state["input"])
    return {"output": result}


# 🟢 Node 2: Improve response
def improve_node(state: State):
    improved = call_gemini(f"Improve this response:\n{state['output']}")
    return {"output": improved}


# 🧱 Build Graph
graph = StateGraph(State)

graph.add_node("llm", llm_node)
graph.add_node("improve", improve_node)

graph.set_entry_point("llm")
graph.add_edge("llm", "improve")

# 🚀 Compile
app = graph.compile()

# ▶️ Run
result = app.invoke({"input": "Explain AI in simple words"})
print(result["output"])












































##########################################################
########################## NOTE ##########################
##########################################################

# ```markdown
# # 🧠 What This Code Actually Builds
# You’ve created a **2-step AI workflow pipeline** using:
# - LangGraph → controls execution flow
# - Google Gemini → generates responses

# ### 🔥 Flow:
# ```

# User Input
# ↓
# llm_node (generate answer)
# ↓
# improve_node (refine answer)
# ↓
# Final Output

# ````

# # 🔍 Deep Breakdown (Line-by-Line Thinking)

# ## 🔑 1. Client Initialization
# ```python
# client = genai.Client(api_key=GOOGLE_API_KEY)
# ````

# 👉 Connection to Gemini
# Think: `client = "gateway to AI"`
# ✔️ Outside functions
# ✔️ Reused across nodes

# ## 🧠 2. State (VERY IMPORTANT)

# ```python
# class State(TypedDict):
#     input: str
#     output: str
# ```

# 👉 Shared memory

# ```
# state = {
#   "input": "...",
#   "output": "..."
# }
# ```

# ✔️ Passed to every node
# ✔️ Nodes update it

# ## 🤖 3. Gemini Call Function

# ```python
# def call_gemini(prompt: str) -> str:
# ```

# Flow:

# ```
# Prompt → Gemini API → Response → return text
# ```

# ## 🔵 4. First Node (llm_node)

# ```python
# def llm_node(state: State):
# ```

# Input:

# ```
# {"input": "Explain AI..."}
# ```

# Output:

# ```
# {"output": "AI is..."}
# ```

# 👉 Reads `input`, writes `output`

# ## 🟢 5. Second Node (improve_node)

# ```python
# def improve_node(state: State):
# ```

# Input:

# ```
# {"output": "AI is..."}
# ```

# Output:

# ```
# {"output": "Improved version..."}
# ```

# 👉 Overwrites output
# ⚠️ No reducer → previous output lost

# ## 🧱 6. Graph Construction

# ```python
# graph = StateGraph(State)
# ```

# 👉 Execution engine

# ## 🔗 7. Nodes + Edges

# ```python
# graph.add_node("llm", llm_node)
# graph.add_node("improve", improve_node)
# ```

# 👉 Register nodes

# ## 🚦 Flow Definition

# ```python
# graph.set_entry_point("llm")
# graph.add_edge("llm", "improve")
# ```

# Flow:

# ```
# START → llm → improve → END
# ```

# ## 🚀 8. Compile

# ```python
# app = graph.compile()
# ```

# 👉 Graph → runnable

# ## ▶️ 9. Execution

# ```python
# result = app.invoke({"input": "Explain AI in simple words"})
# ```

# Execution:

# ```
# 1. llm_node → adds output
# 2. improve_node → improves it
# 3. return final state
# ```

# # ⚡ Important Observations

# ## 🔥 1. Linear Pipeline

# ```
# llm → improve
# ```

# 👉 No decision-making

# ## 🔥 2. Overwriting State

# ```python
# return {"output": improved}
# ```

# 👉 Previous output lost

# ## 🔥 3. Double LLM Call

# ```
# 1 → generate
# 2 → improve
# ```

# 👉 Better quality
# 👉 Higher cost/latency

# ## 🔥 4. No Error Handling

# 👉 Failure → crash

# # 🧠 System Design Thinking

# Current level:

# ```
# Pipeline System (Level 1)
# ```

# # 🚀 Upgrade Ideas

# ## 🔥 1. Add Routing

# ```
# User → Router → (Math / General / Code)
# ```

# ## 🔥 2. Add Memory

# ```
# Chat history → context → Gemini
# ```

# ## 🔥 3. Add Tools

# * Calculator
# * Expense DB
# * File reader

# ## 🔥 4. Convert to Project

# ```
# "Add ₹500 food"
#    ↓
# Router
#    ↓
# Expense tool
#    ↓
# Save to DB
# ```

# # 💡 Quick Improvement

# ```python
# def llm_node(state: State):
#     print("Running LLM node...")
#     result = call_gemini(state["input"])
#     return {"output": result}
# ```

# # 🧠 Final Understanding

# ✅ Multi-step AI workflow
# ✅ Graph-based execution
# ✅ LLM integration

# # 🚀 Next Step

# 👉 Turn into agent (decision-making + tools)

# ```
# ```
