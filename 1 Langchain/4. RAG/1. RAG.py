
from google import genai
client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

# Step 1: Store data
documents = [
    "LangChain is a framework for building LLM applications",
    "Vector databases store embeddings for fast retrieval",
    "Python is widely used in AI development"
]

# Step 2: Convert to embeddings
doc_embeddings = client.models.embed_content(
    model="gemini-embedding-001",
    contents=documents
).embeddings

doc_vectors = [e.values for e in doc_embeddings]

# Step 3: Search (simple similarity)
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query):
    query_embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[query]
    ).embeddings[0].values

    scores = [cosine_similarity(query_embedding, doc) for doc in doc_vectors]

    best_match_index = np.argmax(scores)
    return documents[best_match_index]

# Step 4: Pass to LLM
def rag_chain(query):
    context = retrieve(query)

    prompt = f"""
    Answer the question based on context and explain:

    Context: {context}

    Question: {query}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text

# Step 5: Run
query = "What is LangChain? give me code for it"

answer = rag_chain(query)
print(answer)













#######**** This is a RAG pipeline where:
# Query is converted into embedding
# Compared with stored document embeddings
# Most relevant data is retrieved
# LLM generates answer using that context

#######**** 🔥 Why dot product?
# Because it tells us:
# 👉 How aligned two vectors are
# Similar direction → high value
# Opposite → negative
# Unrelated → small value

######**** What is np.linalg.norm(a)?
# 👉 This is the magnitude (length) of vector
# Formula:
# ||a|| = sqrt(a1² + a2² + a3² + ...)
# a = [3, 4]
# norm = sqrt(3² + 4²) = 5

#####**** Full Formula Meaning
# cosine_similarity = dot(a, b) / (||a|| * ||b||)

#####**** 🔥 Intuition:
# This computes:
# 👉 cos(angle between two vectors)
#####**** Result range:
# |-------------------------------------|
# |   Value	   |     Meaning            |
# |------------|------------------------|    
# |   1	    >>>>>>> exactly same meaning|
# |   0	    >>>>>>>    unrelated        |
# |  -1     >>>>>>>  opposite meaning   |
# |-------------------------------------|

# scores = [0.92, 0.87, 0.12, 0.45, 1, 0.99, 0.1, 0, -1]
# ✅ Angles (in degrees):
# 0.92 → ≈23.07
# 0.87 → ≈29.50
# 0.12 → ≈83.11
# 0.45 → ≈63.26
# 1 → 0
# 0.99 → ≈8.11
# 0.1 → ≈84.26
# 0 → 90
# -1 → 180

# | Score | Angle | Meaning                  |
# | ----- | ----- | ------------------------ |
# | 1     | 0°    | Identical vectors        |
# | 0.99  | 8°    | Almost identical         |
# | 0.92  | 23°   | Very similar             |
# | 0.87  | 29°   | Similar                  |
# | 0.45  | 63°   | Moderate                 |
# | 0.12  | 83°   | Weak                     |
# | 0.1   | 84°   | Very weak                |
# | 0     | 90°   | Orthogonal (no relation) |
# | -1    | 180°  | Opposite direction       |
