# 3. Sequential Chain (Multi-step Chain)

def manual_implementation_of_chains():
    from google import genai

    client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

    def summarize(text):
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"Summarize this: {text}"
        )
        return response.text

    def explain(summary):
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"Explain this in simple terms: {summary}"
        )
        return response.text


    topic = "Vector Databases store embeddings and help in semantic search"

    step1 = summarize(topic)
    step2 = explain(step1)

    print("Summary:", step1)
    print("Explanation:", step2)

# manual_implementation_of_chains()

def chains_using_langchain():
    from langchain_core.prompts import PromptTemplate
    from langchain.chains import LLMChain, SequentialChain # type: ignore
    from langchain_core.language_models import LLM
    from google import genai

    # -----------------------------
    # 1. Gemini LLM Wrapper
    # -----------------------------
    class GeminiLLM(LLM):
        def _call(self, prompt, stop=None):
            client = genai.Client(api_key="AIzaSyA34-lLu-xLIthDFwElzgARjoV38tlxBwc")

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            return response.text

        @property
        def _llm_type(self):
            return "gemini"


    llm = GeminiLLM()

    # -----------------------------
    # 2. Prompt Templates
    # -----------------------------
    summary_prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize this: {text}"
    )

    explain_prompt = PromptTemplate(
        input_variables=["summary"],
        template="Explain this in simple terms: {summary}"
    )

    # -----------------------------
    # 3. Chains
    # -----------------------------
    summary_chain = LLMChain(
        llm=llm,
        prompt=summary_prompt,
        output_key="summary"
    )

    explain_chain = LLMChain(
        llm=llm,
        prompt=explain_prompt,
        output_key="explanation"
    )

    # -----------------------------
    # 4. Sequential Chain
    # -----------------------------
    overall_chain = SequentialChain(
        chains=[summary_chain, explain_chain],
        input_variables=["text"],
        output_variables=["summary", "explanation"],
        verbose=True   # 🔥 shows flow step-by-step
    )

    # -----------------------------
    # 5. Run
    # -----------------------------
    topic = "Vector Databases store embeddings and help in semantic search"

    result = overall_chain.invoke({"text": topic})

    print("Summary:", result["summary"])
    print("Explanation:", result["explanation"])

chains_using_langchain()













# Got it — let’s break down exactly what happens in your code when you call:
# Pythonresult = overall_chain.invoke({"text": topic})


# 1. How .invoke() Works Here
# overall_chain is a SequentialChain, which means:

# Takes the input you pass ({"text": topic}).
# Runs the first chain (summary_chain) using that input.
# Stores the output from the first chain in a dictionary under the key "summary".
# Passes that output into the second chain (explain_chain) as its "summary" input.
# Stores the output from the second chain under the key "explanation".
# Returns a dictionary containing:

# All intermediate outputs (summary)
# All final outputs (explanation)




# 2. Step-by-Step Flow in Your Code
# Step 1 — Input
# Python{"text": "Vector Databases store embeddings and help in semantic search"}


# Step 2 — First Chain (summary_chain)

# PromptTemplate: "Summarize this: {text}"
# Fills {text} with your topic:Summarize this: Vector Databases store embeddings and help in semantic search


# GeminiLLM sends this to the Gemini API.
# Gemini returns a short summary, e.g.:"Vector databases store numerical representations of data to enable semantic search."


# Stored in the result dict as:Python{"summary": "Vector databases store numerical representations of data to enable semantic search."}




# Step 3 — Second Chain (explain_chain)

# PromptTemplate: "Explain this in simple terms: {summary}"
# Fills {summary} with the output from step 2:Explain this in simple terms: Vector databases store numerical representations of data to enable semantic search.


# GeminiLLM sends this to the Gemini API.
# Gemini returns a simpler explanation, e.g.:"They are like special libraries that store meanings of words and ideas so computers can find related things more easily."


# Stored in the result dict as:Python{"explanation": "They are like special libraries that store meanings of words and ideas so computers can find related things more easily."}




# Step 4 — Final Output
# The SequentialChain merges everything into one dictionary:
# Python{
#     "summary": "Vector databases store numerical representations of data to enable semantic search.",
#     "explanation": "They are like special libraries that store meanings of words and ideas so computers can find related things more easily."
# }


# 3. How result["summary"] and result["explanation"] Work

# result is just a Python dictionary returned by .invoke().
# result["summary"] → The output from the first chain.
# result["explanation"] → The output from the second chain.


# 4. Visual Flow Diagram
# Input: {"text": topic}
#         │
#         ▼
# [summary_chain]
#   Prompt: "Summarize this: {text}"
#   → Gemini LLM → "Short summary"
#         │
#         ▼
# [explain_chain]
#   Prompt: "Explain this in simple terms: {summary}"
#   → Gemini LLM → "Simplified explanation"
#         │
#         ▼
# Output: {
#     "summary": "...",
#     "explanation": "..."
# }


# ✅ In short:
# .invoke() here runs both chains in sequence, passing the output of the first as input to the second, and returns a dictionary with both results.

# If you want, I can modify your code so that it also returns intermediate debug prints showing exactly what prompt was sent to Gemini at each step.
# Do you want me to add that?
