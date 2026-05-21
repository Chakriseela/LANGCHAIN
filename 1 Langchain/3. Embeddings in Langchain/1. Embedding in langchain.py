# 4. Embedding Example

import os
from dotenv import load_dotenv
load_dotenv()

def embedding_1():
    from google import genai

    client = genai.Client(api_key= os.getenv("GOOGLE_API_KEY"))

    result = client.models.embed_content(
            model="gemini-embedding-001",
            contents= [
                "What is the meaning of life?",
                "What is the purpose of existence?",
                "How do I bake a cake?"
            ]
    )

    for embedding in result.embeddings:
        print(embedding)
# embedding_1()


def embedding_2():
    from google import genai

    client = genai.Client(api_key= os.getenv("GOOGLE_API_KEY"))

    texts = [
        "What is the meaning of life?",
        "What is the purpose of existence?",
        "How do I bake a cake?"
    ]

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts
    )
    print(result.embeddings)
    embeddings = [e.values for e in result.embeddings]
    # print(embeddings)

    for i, emb in enumerate(embeddings):
        print(f"Text: {texts[i]}")
        print(f"Vector length: {len(emb)}\n")

embedding_2()