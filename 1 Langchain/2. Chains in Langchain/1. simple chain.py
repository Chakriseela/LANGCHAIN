# 1. Simulating a simple Chain (Prompt → LLM)

def Simulating_a_chain():
    from google import genai

    client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

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