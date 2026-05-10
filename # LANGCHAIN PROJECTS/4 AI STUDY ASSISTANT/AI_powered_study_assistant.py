import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

personalities = {
  "Friendly":
  "You are a friendly, enthusiastic, and highly encouraging Study Assistant. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding",
  "Academic":
  "You are a strictly academic, highly detailed, and professional university Professor. Use precise, formal terminology, cite key concepts and structure your response. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding"
}

def study_assistant(question, persona):
    system_prompt = personalities[persona]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=1000
        ),
        contents=question
    )
    return response.text

question = "What are LLMs?"
personality = "Friendly"
print(study_assistant(question, personality))