import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
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
    client = genai.Client(api_key= os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents="Explain Vector Databases simply"
    )
    print(response.text)
LLM_call_Gemini_AI()

# ***********************************************************
                        # LANGCHAIN LLM LOADING #
# ***********************************************************
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

# from google.colab import userdata
api_key=os.getenv('OPENAI_API_KEY')

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("What are Ai Agents?")
messages = [system_msg, human_msg]

model = init_chat_model(
  "openai:gpt-4.1",
  api_key=api_key,
)

# response = model.invoke(messages)
# print(response.content)