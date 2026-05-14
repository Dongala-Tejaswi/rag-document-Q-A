import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="documents")


def store_embeddings(texts):
    ids = [str(i) for i in range(len(texts))]

    collection.add(
        documents=texts,
        ids=ids
    )


def search_embeddings(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return results["documents"][0]