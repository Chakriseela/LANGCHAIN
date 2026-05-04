# 4. Embedding Example

def embedding_1():
    from google import genai

    client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

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

    client = genai.Client(api_key="AIzaSyDrcEFK_3KWMwAHb0mq4D3qqxOij4Zje_A")

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