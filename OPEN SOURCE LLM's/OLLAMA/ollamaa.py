import ollama

response = ollama.chat(
    model="llama3.2:1b",   # ✅ use this
    messages=[
        {
            "role": "user", 
            "content": "Explain AI in simple words"
        }
    ]
)

print(response['message']['content'])