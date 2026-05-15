import chromadb
from chromadb.config import Settings

# Create ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Collection
collection = client.get_or_create_collection(name="documents")


# Store embeddings into vector DB
def store_embeddings(texts, embeddings):
    ids = [str(i) for i in range(len(texts))]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )


# Search similar chunks
def search(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]