# !pip install -U langchain-google-genai
# !pip install langchain-tavily
import os
from dotenv import load_dotenv  
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
import requests
from langchain.tools import tool
# from google.colab import userdata
load_dotenv()

google_api_key = os.getenv('GOOGLE_API_KEY')
model = init_chat_model(
    "google_genai:gemini-2.5-flash", 
    api_key=google_api_key
)


tavily_api_key = os.getenv('TAVILY_API_KEY')

skill_demand_tool = TavilySearch(
    max_results=5,
    search_depth="advanced",
    tavily_api_key=tavily_api_key
)


import requests
from langchain.tools import tool

@tool
def search_jobs(skill: str, location: str) -> list:
    """Search for jobs requiring a specific skill using JSearch API from RapidAPI."""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")

    rapidapi_key = os.getenv('RAPIDAPI_KEY')

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    querystring = {
        "query": f"{skill} in {location}",
        "page": "1",
        "country": "in",
        "employment_types": "INTERN,FULLTIME",
        "job_requirements": "no_experience,under_3_years_experience"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    jobs = data.get("data", [])
    print(f"Found {len(jobs)} jobs\n")

    result = []
    for job in jobs:
        result.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "apply_link": job.get("job_apply_link")
        })
    return result


result = skill_demand_tool.invoke({"query": "generative ai skills demand 2025"})
print(result)




agent = create_agent(
  model = model,  #The language model instance
  tools = [skill_demand_tool],  # List of tools
#   system_prompt = system_prompt,
)