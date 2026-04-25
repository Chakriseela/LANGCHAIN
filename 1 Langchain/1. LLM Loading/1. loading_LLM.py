from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
# ***********************************************************
                        # OPENAI #
# ***********************************************************
def LLM_call_OpenAI():
    import os
    os.environ["OPENAI_API_KEY"] = "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"

    prompt = PromptTemplate.from_template("Explain {topic} simply")

    llm = ChatOpenAI(model="gpt-4o-mini")

    chain = prompt | llm

    response = chain.invoke({"topic": "Vector Databases"})
    print(response.content)
# LLM_call_OpenAI()
# ***********************************************************
                        # GEMINI #
# ***********************************************************
def LLM_call_Gemini_AI():
    from google import genai
    client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents="Explain Vector Databases simply"
    )
    print(response.text)
LLM_call_Gemini_AI()

# ***********************************************************