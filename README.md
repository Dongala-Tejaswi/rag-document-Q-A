# 🚀 AI Document Q&A System (RAG)

An AI-powered Document Question Answering System built using Retrieval-Augmented Generation (RAG).  
Users can upload PDF documents and ask questions in natural language.  
The system retrieves relevant document chunks using vector embeddings and generates intelligent answers using an LLM.

---

# 📌 Features

- 📄 Upload PDF documents
- 🔍 Semantic search using vector embeddings
- 🤖 AI-powered question answering
- ⚡ Redis caching for faster responses
- 🐳 Fully Dockerized architecture
- 📡 FastAPI backend
- 🎨 React frontend
- 🧠 Retrieval-Augmented Generation (RAG)
- 📊 Scalable backend architecture
- 🔐 Environment-based configuration
Deployment link https://rag-document-q-a-2.onrender.com/
---

# 🏗️ System Architecture

```text
                +-------------------+
                |     Frontend      |
                |   React / Vite    |
                +---------+---------+
                          |
                          v
                +-------------------+
                |    FastAPI API    |
                +---------+---------+
                          |
        +-----------------+------------------+
        |                                    |
        v                                    v
+---------------+                  +------------------+
| Redis Cache   |                  | Vector Database  |
| Query Cache   |                  | ChromaDB/Faiss   |
+---------------+                  +------------------+
        |                                    |
        +-----------------+------------------+
                          |
                          v
                +-------------------+
                |      OpenAI       |
                |   LLM Response    |
                +-------------------+
