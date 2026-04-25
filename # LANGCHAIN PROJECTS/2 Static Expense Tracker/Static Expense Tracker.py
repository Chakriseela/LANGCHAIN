from google import genai
import numpy as np
from datetime import datetime

# -----------------------------
# 1. Setup Gemini
# -----------------------------
client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

# -----------------------------
# 2. In-Memory Database
# -----------------------------
expenses = []
doc_vectors = []

# -----------------------------
# 3. Embedding Function
# -----------------------------
def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text]
    )
    return response.embeddings[0].values

# -----------------------------
# 4. Similarity Function
# -----------------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# -----------------------------
# 5. Add Expense
# -----------------------------
def add_expense(user_input):
    today = datetime.now().strftime("%Y-%m-%d")
    
    expense_text = f"{user_input} on {today}"
    
    expenses.append(expense_text)
    doc_vectors.append(get_embedding(expense_text))
    
    print("✅ Expense added:", expense_text)

# -----------------------------
# 6. Retrieve Relevant Data
# -----------------------------
def retrieve(query):
    if not expenses:
        return []
    
    query_vector = get_embedding(query)
    
    scores = [cosine_similarity(query_vector, doc) for doc in doc_vectors]
    
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]
    
    return [expenses[i] for i in top_indices]

# -----------------------------
# 7. Ask LLM
# -----------------------------
def ask_llm(query, context):
    prompt = f"""
    You are an expense assistant.

    Context:
    {context}

    Question:
    {query}

    Give clear and correct answer.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text

# -----------------------------
# 8. MAIN LOOP
# -----------------------------
print("\n💸 AI Expense Tracker Started")
print("Type 'add' to add expense")
print("Type 'ask' to query")
print("Type 'exit' to quit\n")

while True:
    choice = input("\nEnter command (add/ask/exit): ").lower()

    if choice == "add":
        user_input = input("Enter expense (e.g., 'Spent 200 on food'): ")
        add_expense(user_input)

    elif choice == "ask":
        query = input("Ask your question: ")
        
        relevant_data = retrieve(query)
        
        if not relevant_data:
            print("⚠️ No data available")
            continue
        
        print("\n🔍 Retrieved:", relevant_data)
        
        answer = ask_llm(query, relevant_data)
        
        print("\n🤖 Answer:", answer)

    elif choice == "exit":
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid command")