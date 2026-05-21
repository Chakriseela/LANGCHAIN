# 1. Simulating a simple Chain (Prompt → LLM)

import os
from dotenv import load_dotenv
load_dotenv()

def Simulating_a_chain():
    from google import genai

    client = genai.Client(api_key= os.getenv("GOOGLE_API_KEY"))

    def prompt_template(topic):
        return f"Explain {topic} in simple terms with an example"

    def llm_chain(topic):
        prompt = prompt_template(topic)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        return response.text


    result = llm_chain("Vector Databases")
    print(result)

# Simulating_a_chain()