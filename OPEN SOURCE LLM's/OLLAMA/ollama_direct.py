import requests

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.2:3b",   # use 1b if RAM issue
    "prompt": "Explain AI in simple words",
    "stream": False
}

response = requests.post(url, json=data)

print(response.json()["response"])