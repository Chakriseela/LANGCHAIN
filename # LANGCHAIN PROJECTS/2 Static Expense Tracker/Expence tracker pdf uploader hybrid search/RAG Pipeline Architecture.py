'''
                ┌──────────────────────┐
                │   Data Sources       │
                │----------------------│
                │  📄 PDF (expenses)   │
                │  🌐 Website (tips)   │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   Document Loaders   │
                │----------------------│
                │ PyPDFLoader          │
                │ WebBaseLoader        │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   Combine Documents  │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   Text Chunking      │
                │----------------------│
                │ Split into small     │
                │ meaningful chunks    │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   Embeddings         │
                │----------------------│
                │ Text → Vectors       │
                │ (semantic meaning)   │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   Vector Database    │
                │----------------------│
                │ FAISS                │
                │ Stores vectors       │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │     Retriever        │
                │----------------------│
                │ Finds top-k similar  │
                │ chunks using vectors │
                └─────────┬────────────┘
                          ↓
        ┌────────────────────────────────────┐
        │        User Query                  │
        │ "What is my food expense?"        │
        └──────────────┬─────────────────────┘
                       ↓
                ┌──────────────────────┐
                │ Query Embedding      │
                │ (convert to vector)  │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │ Similarity Search    │
                │----------------------│
                │ Compare with all     │
                │ stored vectors       │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │ Relevant Chunks      │
                │----------------------│
                │ "Food - ₹2000"       │
                │ "Food - ₹3000"       │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   LLM (Generator)    │
                │----------------------│
                │ Uses retrieved data  │
                │ + prompt             │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   Final Answer       │
                │----------------------│
                │ "Total = ₹5000"      │
                └──────────────────────┘
'''




'''
PDF + Website + Manual
        ↓
Document Loaders
        ↓
Chunking
        ↓
Embeddings
        ↓
FAISS
        ↓
Hybrid Retrieval
        ↓
Re-ranking
        ↓
Prompt
        ↓
Gemini LLM
        ↓
Final Answer
'''