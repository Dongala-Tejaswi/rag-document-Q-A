import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="rag_collection"
)


def store_embeddings(chunks, embeddings):

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        embeddings=embeddings,
        documents=chunks,
        ids=ids
    )


def search(query_embedding):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]