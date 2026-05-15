import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(chunks, embeddings):

    for i, chunk in enumerate(chunks):

        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embeddings[i]]
        )


def search(query_embedding):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    documents = results["documents"][0]

    return " ".join(documents)